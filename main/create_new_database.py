import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import MysqlConnector, return_data_from_the_file

host, user, password, _ = return_data_from_the_file("../database_data.txt")
connector = MysqlConnector(host=host, user=user, password=password)

connector.create_new_database(database_name=input("enter database name: "))
# database name -> "test_database"
connector.create_project_tables()
