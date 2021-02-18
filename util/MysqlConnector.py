import pickle
import sys

import mysql.connector
import re
from .User import User
from tqdm import tqdm


# encodes to bytes and deserialize and return database users table in format
# [[name, users embedding, access(True or False)], ...]
def encode(database_users):
    return [User(num[0], pickle.loads(num[1].encode('ISO-8859-1')), num[2]) for num in database_users]


# list format -> [name, embedding]
# serializes tensor object to bytes and decode to String
def decode(users_embedding):
    return pickle.dumps(users_embedding).decode('ISO-8859-1')


class MysqlConnector:

    # initialize database and makes cursor
    def __init__(self, host, user, password, database=None):
        if database is None:
            self.database = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
            )
            self.cursor = self.database.cursor()

        else:
            self.database = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.database.cursor()

    # Uploads users list to database.
    # List format -> [User(name, embedding, access)]
    def upload_dataset(self, users):
        for x in tqdm(users, desc="Uploading dataset", position=0):
            if self.find_duplicates(x.get_embedding()):
                pass
            else:
                sql = "INSERT INTO users (name_surname, embedding, access) VALUES (%s, %s, %s)"
                val = x.get_name(), decode(users_embedding=x.get_embedding()), x.get_access()

                self.cursor.execute(sql, val)

        self.database.commit()
        print("import complete")

    # selects all columns from table "users" and return them in format
    # [name, String representation of bytes object, access(1 == True; 2 == False)]
    def select_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    # looks for duplicates
    def find_duplicates(self, inserted_embedding):
        flag = False
        for y in tqdm(encode(self.select_all_users()), desc="checking for duplicates", position=0):
            if (inserted_embedding - y.get_embedding()).norm().item() == 0:
                flag = True

        return flag

    def create_new_database(self, database_name):

        if not re.match("^[0-9a-zA-Z_]+$", database_name):
            print("ERROR - allowed characters are only a-z, A-Z, 0-9, \'_\'")
            sys.exit(1)

        try:
            query = "CREATE DATABASE " + database_name
            self.cursor.execute(query)

            self.database.database = database_name
            print(database_name + " was created")

        except mysql.connector.errors.DatabaseError:
            print("Database is already exists.")

    def create_project_tables(self):
        try:
            self.cursor.execute(
                "CREATE TABLE users (name_surname varchar(150) not null,embedding text not null,access varchar (25) "
                "null) "
                "")
            print("the tables has been created")

        except mysql.connector.errors.ProgrammingError:
            pass

    def change_access(self, name, new_status):

        query = "SELECT name_surname FROM users WHERE name_surname LIKE %s"
        self.cursor.execute(query, (name,))

        if len(self.cursor.fetchall()) != 0:
            query = "UPDATE users SET access = %s WHERE name_surname LIKE %s"

            if new_status:
                val = "Allowed"
            else:
                val = "Denied"

            self.cursor.execute(query, (val, name))
            self.database.commit()
            print("Status updated")
        else:
            print("The subject is not in the database.")
