from email.header import make_header
from passlib.hash import bcrypt
from user import User
from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_jwt_extended import JWTManager, jwt_required
import uuid
import json


def execute_command(sql):
    """Выполнить команду SQL."""
    return db.engine.execute(collect2_sql(*sql))


def get_list(body, params: list = None, none_result=None):
    """Получение всех записей в виде списка по SQL запросу."""
    if none_result is None:
        none_result = []
    sql = (body, params) if type(body) == str else body  # noqa: C0123 pylint: disable=C0123
    res = [{col[0]: col[1] for col in row.items()}
           for row in execute_command(sql)]
    return none_result if not res else res


def exec_command(body, params=None):
    """Выполнить одну команду SQL."""
    sql = (body, params) if type(body) == str else body
    return db.engine.execute(collect2_sql(*sql))


def get_dict(body, params=None, none_result=None):
    """Получение одной записи в виде словаря по SQL запросу."""
    if none_result is None:
        none_result = {}
    sql = (body, params) if type(body) == str else body
    row = execute_first(sql)
    return none_result if row is None else {col[0]: col[1] for col in row.items()}


def execute_first(sql):
    """Выполнить команду SQL возвращающую одну запись."""
    return db.engine.execute(collect2_sql(*sql)).first()


def collect2_sql(sql_text: str, sql_bindparam: list):
    """Собрать SQL запрос для выполнения.

    :param sql_text: Текст запроса
    :param sql_bindparam: Параметры запроса
    """
    sql = text(sql_text)
    if sql_bindparam is not None:
        sql = sql.bindparams(
            *sql_bindparam,
        )
    return sql


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/to_do_list"
app.config['SECRET_KEY'] = "3139bbad-378f-4037-bf22-b395d8b5e3f6"
db = SQLAlchemy(app)
jwt = JWTManager(app)


@app.route('/api/')
@jwt_required()
def hello():
    row = get_dict("""SELECT * FROM users""")
    return row


@app.route('/api/registration', methods=['POST'])
def registration():
    emailUser = request.json.get('email')
    password = request.json.get('password')
    allUsersEmail = get_list(User.getEmailAllUsers())
    res = None
    for email in allUsersEmail:
        if emailUser == email.get('email'):
            res = make_response(
                {"message": "Пользователь с такой почтой уже есть"}, 0)
            break
    if res is None:
        id_user = str(uuid.uuid4())
        user = User('liza', 'konovalova', emailUser, id_user, password)
        exec_command(user.addUser())
        res = make_response({"message": "Вы успешно зарегистированы"}, 200)
        #res.set_cookie = {'session_id': str(User.get_token(id_user))}   
        res.set_cookie('session_id', str(User.get_token(id_user)))  
    else:
        res
    return res


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    emailUser = request.json.get('email')
    password = request.json.get('password')
    user_info = get_dict(User.authenticate(emailUser))
    if not user_info:
        return make_response({"message": "Не верный email или пароль"}, 0)
    if bcrypt.verify(password, user_info['password']):
        
        userid = str(user_info['id_user'])
        res = make_response({"message": "Вы успешно авторизировались",
                             "body": {'first_name': user_info['first_name'],
                                      'last_name': user_info['last_name'],
                                      }}, 200)
        res.headers['access_token'] = User.get_token(userid)  
        res.set_cookie = {'session_id': str(User.get_token(userid))}   
        res.set_cookie('somecookiename', 'I am cookie')   
        return res
    else:
        return make_response({"message": "Не верный email или пароль"}, 0)


if __name__ == '__main__':
    app.run(debug=True)
