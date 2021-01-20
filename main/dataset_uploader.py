import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import FaceDetector
from util import Loader
from util import MysqlConnector, return_data_from_the_file

detector = FaceDetector()

# initialize parameters from config.txt
host, user, password, database = return_data_from_the_file("../config.txt")
mysql = MysqlConnector(host=host, user=user, password=password, database=database)

loader = Loader(dataset_path=input("Enter dataset path: "))
# my dataset path -> D:/dataset
users = []

users = loader.load(mtcnn=detector.mtcnn, resnet=detector.resnet, users=users)

mysql.upload_dataset(users)
