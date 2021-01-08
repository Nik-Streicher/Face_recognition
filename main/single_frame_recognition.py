from PIL import Image
import cv2

from util.FaceDetector import FaceDetector, recognize_users, draw_bounding_box, convert_to_cv
from util.MysqlConnector import MysqlConnector, encode

detector = FaceDetector()

tested_image = Image.open("../images/multi/3.jpg")

tested_image_embedding = detector.resnet(detector.mtcnn(tested_image))

mysql = MysqlConnector(host="localhost", user="python_user", password="password", database="python_project")

database_users = mysql.select_all_users()

users = encode(database_users=database_users)

recognized_users = recognize_users(face_embedding=tested_image_embedding, users=users, distance=0.9)

boxes, _ = detector.mtcnn.detect(tested_image)

image = draw_bounding_box(boxes=boxes, recognized_users=recognized_users, pil_image=tested_image,
                          font_path='arial.ttf',
                          font_size=17)

cv2.imshow("Recognized Image", convert_to_cv(pil_image=image))
cv2.waitKey(0)
