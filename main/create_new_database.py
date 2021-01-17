from util.MysqlConnector import MysqlConnector

connector = MysqlConnector(host="localhost", user="python_user", password="password")

connector.create_new_database(database_name=input("enter database name: "))
# database name -> "test_database"
connector.create_project_tables()
