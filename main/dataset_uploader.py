from util.FaceDetector import FaceDetector
from util.Loader import Loader
from util.MysqlConnector import MysqlConnector

detector = FaceDetector()

mysql = MysqlConnector(host="localhost", user="python_user", password="password", database="python_project")

loader = Loader(dataset_path=input("Enter dataset path: "))
# my dataset path -> 'D:/dataset'
users = []

users = loader.load(mtcnn=detector.mtcnn, resnet=detector.resnet, users=users)

mysql.upload_dataset(users)
