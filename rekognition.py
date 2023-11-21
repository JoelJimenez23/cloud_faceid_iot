import boto3
import base64


def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
            base64_encoded = base64.b64encode(img_bytes).decode('utf-8')
            return base64_encoded
    except FileNotFoundError:
        print("El archivo de imagen no se encontró.")
        return None



def upload_face_user(path,collection):
    image_base64 = image_to_base64(path)
    client = boto3.client('rekognition',region_name='us-east-1')
    response = client.index_faces(
            CollectionId=collection,
            Image={'Bytes':base64.b64decode(image_base64)},
            )
    return response['FaceRecords'][0]['Face']['FaceId']



def face_comparison(image_path,collection):
    image_base64 = image_to_base64(image_path)
    client = boto3.client('rekognition',region_name='us-east-1')
    response = client.search_faces_by_image(
            CollectionId=collection,
            Image={
                'Bytes':base64.b64decode(image_base64)
                },
            MaxFaces=1
            )
    print(response)
    return response

