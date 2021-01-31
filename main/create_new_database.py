import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import MysqlConnector
from Config import *


def run(database_name):

    # initialize parameters from Config.py
    connector = MysqlConnector(host=Config.Host, user=Config.User, password=Config.Password)

    connector.create_new_database(database_name=database_name)
    # database name -> "test_database"
    connector.create_project_tables()


if __name__ == "__main__":
    run(input("enter database name: "))
