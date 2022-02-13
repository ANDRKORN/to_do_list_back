
from passlib.hash import bcrypt
from sqlalchemy import bindparam
from flask_jwt_extended import create_access_token
from datetime import timedelta

class User():
    
    def __init__(self, first_name, last_name, email, id_user, password):
        self.first_name=first_name, 
        self.last_name=last_name, 
        self.email=email,
        self.id_user=id_user, 
        self.password=bcrypt.hash(password)

    def addUser(self):
        return (["""
        INSERT INTO public.users
        VALUES (:first_name, 
                :last_name , 
                :email, 
                :id_user, 
                :password)
        """,[
            bindparam(key='first_name', value=self.first_name,),
            bindparam(key='last_name', value=self.last_name),
            bindparam(key='email', value=self.email),
            bindparam(key='id_user', value=self.id_user),
            bindparam(key='password', value=self.password)]])

    def getEmailAllUsers():
        return ("""SELECT email FROM users""")   

    def get_token(id_user, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=id_user, expires_delta=expire_delta)
        return token

    def authenticate(email):
        return (["""
        SELECT *
        FROM public.users
        WHERE public.users.email = :email
        LIMIT 1
        """,[           
            bindparam(key='email', value=email)        
           ]])