from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import owner
class Pet:
    db="pets_schema"
    def __init__(self,data):
        self.id= data['id']
        self.name = data['name']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']
        self.owner = None

# create
    @classmethod
    def save(cls, data):
        query = "INSERT INTO pets (name,type,owner_id) VALUES (%(name)s,%(type)s,%(owner_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    # read

    @classmethod
    def get_pets(cls):
        query = "SELECT * FROM pets LEFT JOIN owners ON owner_id = owners.id;"
        results = connectToMySQL(cls.db).query_db(query)
        pets=[]
        for row in results:
            pet = cls(row)

            owner_data={
                'id': row['owners.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['owners.created_at'],
                'updated_at': row['owners.updated_at']
            }
            pet.owner = owner.Owner(owner_data)
            pets.append(pet)
        return pets

    @classmethod
    def get_one_pet(cls,id):
        data = {
            'id':id
        }
        query="SELECT * FROM pets LEFT JOIN owners ON owner_id = owners.id WHERE pets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        pet = cls(results[0])

        owner_data={
            'id': results[0]['owners.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['owners.created_at'],
            'updated_at': results[0]['owners.updated_at']
        }
        pet.owner=owner.Owner(owner_data)
        return pet


# update
    @classmethod
    def update(cls,data):
        query="UPDATE pets SET name=%(name)s, type= %(type)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

# delete
    @classmethod
    def delete_pet(cls, id):
        data={
            'id':id
        }
        query="DELETE FROM pets WHERE id= %(id)s;"
        return  connectToMySQL(cls.db).query_db(query,data)







    @staticmethod
    def vlidate_pet(pet):
        is_valid = True
        if len(pet['name']) <2:
            is_valid=False
            flash('Pet nam emust be at least 2 characters', 'pet')
        if len(pet['type']) <1:
            flash('Pet must have a type', 'pet')
            is_valid=False
        return is_valid