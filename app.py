
from user import User
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import uuid , json

def exec_command(body, params= None):
    """Выполнить одну команду SQL."""
    sql = (body, params) if type(body) == str else body  
    return db.engine.execute(collect2_sql(*sql))

def get_dict(body, params = None, none_result = None):
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
db = SQLAlchemy(app)

@app.route('/')
def hello():    
    row = get_dict("""SELECT last_name FROM users""") 
    return row

@app.route('/registration')
def registration():    
    emailUser=request.json.get('email')
    allUsersEmail=get_dict(User.getAllUsers())  
    for email in allUsersEmail.values():
        if emailUser == email:
            return "Пользователь с такой почтой уже есть", 0
    exec_command(User('liza','konovalova','@',uuid.uuid4(),'poshol_naxuy').addUser())    
    return {"message":"Добро пожаловать"} , 1

if __name__ == '__main__':
    app.run(debug=True)