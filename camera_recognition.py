import cv2
from PIL import Image
import face_recognition
import subprocess
from entrance_login_verification import get_shadow_collection, send_user_access
import rekognition

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
        pil_image.save("temp.png")
        contador+=1
        collection = get_shadow_collection()
        value = rekognition.face_comparison('temp.png',collection)
        if len(value['FaceMatches']) == 1:
            face_id =  value['FaceMatches'][0]['Face']['FaceId']
            send_user_access(face_id,collection)
            break
        else:
            contador = 0
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
