import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import FaceDetector
from util import Loader
from util import MysqlConnector
from Config import *


def run(dataset_path):
    detector = FaceDetector()

    # initialize parameters from config.txt
    mysql = MysqlConnector(host=Config.Host, user=Config.User, password=Config.Password, database=Config.Database_name)

    loader = Loader(dataset_path=dataset_path)
    # my dataset path -> D:/dataset
    users = []

    users = loader.load(mtcnn=detector.mtcnn, resnet=detector.resnet, users=users)

    mysql.upload_dataset(users)


if __name__ == '__main__':
    run(input("Enter dataset path: "))
