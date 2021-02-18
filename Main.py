from util import FaceDetector, recognize_users, draw_bounding_box, convert_to_cv
from util import Loader
from util import MysqlConnector, encode
from Config import *
from Settings import *
from fire import Fire
from PIL import Image
import cv2
import sys


class Main:

    def create(self):
        # initialize parameters from Config.py
        connector = MysqlConnector(host=Config.host, user=Config.user, password=Config.password)

        connector.create_new_database(database_name=Config.database_name)
        connector.create_project_tables()

    def upload(self, dataset_path):
        detector = FaceDetector()

        # initialize parameters from config.txt
        mysql = MysqlConnector(host=Config.host, user=Config.user, password=Config.password,
                               database=Config.database_name)

        loader = Loader(dataset_path=dataset_path)
        # my dataset path -> D:/dataset
        users = []

        users = loader.load(mtcnn=detector.mtcnn, resnet=detector.resnet, users=users)

        mysql.upload_dataset(users)

    def recognize_image(self, image_path, font=Settings.font, accuracy=Settings.accuracy, font_size=Settings.font_size):

        try:
            tested_image = Image.open(image_path)
            detector = FaceDetector()
            #  tested image path -> sample-images/multi/3.jpg
            #  invalid picture path ->  sample-images/invalid/1.jpg

            mtcnn = detector.mtcnn(tested_image)

            if mtcnn is not None:
                tested_image_embedding = detector.resnet(mtcnn)

                # initialize parameters from config.txt
                mysql = MysqlConnector(host=Config.host, user=Config.user, password=Config.password,
                                       database=Config.database_name)

                database_users = mysql.select_all_users()

                users = encode(database_users=database_users)

                recognized_users = recognize_users(face_embedding=tested_image_embedding, users=users,
                                                   accuracy=accuracy)

                boxes, _ = detector.mtcnn.detect(tested_image)

                tested_image = draw_bounding_box(boxes=boxes, recognized_users=recognized_users, pil_image=tested_image,
                                                 font_path=font,
                                                 font_size=font_size)
            else:
                print("no face was detected")

            cv2.imshow("recognized Image", convert_to_cv(pil_image=tested_image))
            cv2.waitKey(0)
        except FileNotFoundError:
            print(" No such file or directory: ", end=image_path)

    def recognize_stream(self, font=Settings.font, accuracy=Settings.accuracy, detection_delay=Settings.detection_delay,
                         font_size=Settings.font_size, path_to_video=Settings.path_to_video):
        detector = FaceDetector()

        # initialize parameters from Config.py
        mysql = MysqlConnector(host=Config.host, user=Config.user, password=Config.password,
                               database=Config.database_name)

        database_users = mysql.select_all_users()

        users = encode(database_users=database_users)

        v_cap = cv2.VideoCapture(path_to_video)

        boxes = None
        img_embedding = []
        recognized_users = []
        counter = 0
        while True:
            success, img = v_cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            boxes, _ = detector.mtcnn.detect(img)

            detect = detector.mtcnn(img)
            if counter == 0:
                if detect is not None:
                    img_embedding = detector.resnet(detect)
                    recognized_users = recognize_users(face_embedding=img_embedding, users=users, accuracy=accuracy)

            image = draw_bounding_box(boxes=boxes, recognized_users=recognized_users, pil_image=img,
                                      font_path=font,
                                      font_size=font_size)

            counter += 1

            if counter == detection_delay:
                counter = 0

            # display and close window
            cv2.imshow("Video", convert_to_cv(image))
            if cv2.waitKey(1) & 0xFF == ord('f'):
                print("Program has been closed")
                sys.exit(1)

    def update_access(self, name, new_status):

        # initialize parameters from config.txt
        connector = MysqlConnector(host=Config.host, user=Config.user, password=Config.password,
                                   database=Config.database_name)

        # update the object's access status
        connector.change_access(name=name, new_status=new_status)


if __name__ == "__main__":
    Fire(Main)
