from PIL import Image
import cv2
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import FaceDetector, recognize_users, draw_bounding_box, convert_to_cv
from util import MysqlConnector, encode
from Config import *




def run(image_path, font, font_size, distance):
    detector = FaceDetector()
    tested_image = Image.open(image_path)
    #  tested image path -> ../images/multi/3.jpg
    #  invalid picture path ->  ../images/invalid/1.jpg

    mtcnn = detector.mtcnn(tested_image)

    if mtcnn is not None:
        tested_image_embedding = detector.resnet(mtcnn)

        # initialize parameters from config.txt
        mysql = MysqlConnector(host=Config.Host, user=Config.User, password=Config.Password,
                               database=Config.Database_name)

        database_users = mysql.select_all_users()

        users = encode(database_users=database_users)

        recognized_users = recognize_users(face_embedding=tested_image_embedding, users=users, distance=distance)

        boxes, _ = detector.mtcnn.detect(tested_image)

        tested_image = draw_bounding_box(boxes=boxes, recognized_users=recognized_users, pil_image=tested_image,
                                         font_path=font,
                                         font_size=font_size)
    else:
        print("no face was detected")

    cv2.imshow("recognized Image", convert_to_cv(pil_image=tested_image))
    cv2.waitKey(0)


if __name__ == '__main__':
    run(image_path=input("Enter image path: "), font='arial.ttf', font_size=17, distance=0.9)
