import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from PIL import Image
import cv2

from util import FaceDetector, recognize_users, draw_bounding_box, convert_to_cv
from util import MysqlConnector, encode, return_data_from_the_file

detector = FaceDetector()

# initialize parameters from config.txt
host, user, password, database = return_data_from_the_file("../config.txt")
mysql = MysqlConnector(host=host, user=user, password=password, database=database)

database_users = mysql.select_all_users()

users = encode(database_users=database_users)

v_cap = cv2.VideoCapture(0)

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
            recognized_users = recognize_users(face_embedding=img_embedding, users=users, distance=0.9)

    image = draw_bounding_box(boxes=boxes, recognized_users=recognized_users, pil_image=img,
                              font_path='arial.ttf',
                              font_size=17)

    counter += 1

    if counter == 45:
        counter = 0

    # display and close window
    cv2.imshow("test", convert_to_cv(image))
    if cv2.waitKey(1) & 0xFF == ord('g'):
        print("Program has been closed")
        sys.exit()
