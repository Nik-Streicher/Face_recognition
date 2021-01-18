from util.FaceDetector import FaceDetector
from util.Loader import Loader
from util.MysqlConnector import MysqlConnector, return_data_from_the_file

detector = FaceDetector()

host, user, password, database = return_data_from_the_file("../database_data.txt")
mysql = MysqlConnector(host=host, user=user, password=password, database=database)

loader = Loader(dataset_path=input("Enter dataset path: "))
# my dataset path -> D:/dataset
users = []

users = loader.load(mtcnn=detector.mtcnn, resnet=detector.resnet, users=users)

mysql.upload_dataset(users)
