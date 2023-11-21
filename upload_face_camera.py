import cv2
from PIL import Image
import face_recognition
import subprocess
from entrance_login_verification import  register_user, send2bucket
import rekognition
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--email')
parser.add_argument('--code')
parser.add_argument('--collection')

args = parser.parse_args()

cap = cv2.VideoCapture(0)
window_name = 'Webcam Feed'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

contador = 0
while True:
    ret, frame = cap.read()
    cv2.imshow(window_name,  frame)

    rgb_frame = frame[:,:,::-1]
    image = face_recognition.face_locations(rgb_frame)
    if contador < 2 and len(image) != 0:
        top, right,bottom,left = image[0]
        face_image = rgb_frame[top:bottom,left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save("upload.png")
        contador+=1
        face_id = rekognition.upload_face_user("upload.png",args.collection)
        print(face_id)
        register_user(args.email,args.code,args.collection,face_id)
        send2bucket(args.code,args.collection,'upload.png')

        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
