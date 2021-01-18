from PIL import Image
import cv2

from util.FaceDetector import FaceDetector, recognize_users, draw_bounding_box, convert_to_cv
from util.MysqlConnector import MysqlConnector, encode, return_data_from_the_file

detector = FaceDetector()

tested_image = Image.open(input("Enter image path: "))
#  tested image path -> ../images/multi/3.jpg
#  invalid picture path ->  ../images/invalid/1.jpg

mtcnn = detector.mtcnn(tested_image)

if mtcnn is not None:
    tested_image_embedding = detector.resnet(mtcnn)

    host, user, password, database = return_data_from_the_file("../database_data.txt")
    mysql = MysqlConnector(host=host, user=user, password=password, database=database)

    database_users = mysql.select_all_users()

    users = encode(database_users=database_users)

    recognized_users = recognize_users(face_embedding=tested_image_embedding, users=users, distance=0.9)

    boxes, _ = detector.mtcnn.detect(tested_image)

    tested_image = draw_bounding_box(boxes=boxes, recognized_users=recognized_users, pil_image=tested_image,
                                     font_path='arial.ttf',
                                     font_size=17)
else:
    print("no face was detected")

cv2.imshow("Recognized Image", convert_to_cv(pil_image=tested_image))
cv2.waitKey(0)
