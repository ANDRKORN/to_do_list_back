from sqlalchemy import bindparam

class User():
    #__slots__ = ('first_name', 'last_name','email','id_user','password')    
    def __init__(self,first_name,last_name,email,id_user,password):
        self.first_name=first_name, 
        self.last_name=last_name, 
        self.email=email,
        self.id_user=id_user, 
        self.password=password

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

    def getAllUsers():
        return ("""SELECT email FROM users""")    
