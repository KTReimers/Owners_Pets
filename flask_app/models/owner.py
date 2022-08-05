from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Owner:
    db= 'pets_schema'
    def __init__(self,data):
        self.id= data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# Create
    @classmethod
    def save(cls, data):
        query="""INSERT INTO owners (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query,data)

# Read
    @classmethod
    def getById(cls,id):
        data= {
            'id':id
        }
        query = "SELECT * FROM owners WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def getByEmail(cls,data):
        query = "SELECT * FROM owners WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

# update

# delete

# validate
    @staticmethod
    def validate_register(owner):
        is_valid = True
        query = "SELECT * FROM owners WHERE email = %(email)s;"
        results = connectToMySQL(Owner.db).query_db(query,owner)
        if len(results) >=1:
            flash("Email already taken...find another", "register")
            is_valid = False
        if len(owner['first_name']) < 3:
            flash("First name must be at at least 3 characters", "register")
            is_valid = False
        if not EMAIL_REGEX.match(owner['email']):
            flash('Invalid email format!!!!', "register")
        if len(owner['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(owner['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if owner['password'] != owner['confirm']:
            flash("Passwords don't match","register")
            is_valid= False
        return is_valid

    @staticmethod
    def validate_login(owner):
        query = "SELECT * FROM owners WHERE email = %(email)s;"
        results = connectToMySQL(Owner.db).query_db(query,owner)
        is_valid= True
        if not results:
            flash('invalid email or password', 'login')
            is_valid= False
        elif not bcrypt.check_password_hash(Owner(results[0]).password, owner['password']):
            flash('invalid email or password', 'login')
            is_valid=False
        return is_valid