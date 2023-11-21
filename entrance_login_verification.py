
from awscrt import http,mqtt
from awsiot import mqtt_connection_builder
from datetime import datetime
import json
import sys
import threading
import time
import boto3


endpoint = "a3rb7btf73xuz0-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "AmazonRootCA1.pem"
certificatePath = "136a250ec67fce30bc8151cca747fb5d0a592d9d06f45760490b24f7d24c4dd7-certificate.pem.crt"
privateKeyPath = "136a250ec67fce30bc8151cca747fb5d0a592d9d06f45760490b24f7d24c4dd7-private.pem.key"
clientId = "basicPubSub"
topic_pub = "$aws/things/faceid_iot/shadow/name/login_access/get"
topic_sub = "$aws/things/faceid_iot/shadow/name/login_access/get/accepted"
topic_default_shadow = "$aws/things/faceid_iot/shadow/name/login_access/update"
topic_sub_shadow = "$aws/things/faceid_iot/shadow/name/login_access/update/accepted"
topic_access = 'iot/sensortest'
topic_register_user = 'iot/user_register'
topic_admin_login = 'iot/admin_login'
value = ""


def on_message_received(topic,payload,qos,retain, **kwargs):
    global value
    if payload:
        value = json.loads(payload)
    else:
        value = ""
    return value


def set_default_values():
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=certificatePath,
        pri_key_filepath=privateKeyPath,
        ca_filepath=rootCAPath,
        client_id=clientId,
    )

    message = {
        "state":{
            "desired":{
                "welcome":"aws-iot",
                "access":False,
                "colecction":"",
                "session_id":""
            }
        }
    }
    message_json = json.dumps(message)

    connect_future = mqtt_connection.connect()
    connect_future.result()
    mqtt_connection.publish(topic=topic_default_shadow,payload=message_json,qos=mqtt.QoS.AT_LEAST_ONCE)
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()


def get_shadow_collection():

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=certificatePath,
        pri_key_filepath=privateKeyPath,
        ca_filepath=rootCAPath,
        client_id=clientId,
    )
    connect_future = mqtt_connection.connect()
    connect_future.result()
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=topic_sub,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )

    subscribe_result = subscribe_future.result()

    while len(value) == 0:
        mqtt_connection.publish(topic=topic_pub,payload="",qos=mqtt.QoS.AT_LEAST_ONCE)

    collecction = value['state']['desired']['collection']

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

    return collecction


def register_user(email,codigo,collection,face_id):

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=certificatePath,
        pri_key_filepath=privateKeyPath,
        ca_filepath=rootCAPath,
        client_id=clientId,
    )
    connect_future = mqtt_connection.connect()
    connect_future.result()

    message = {"email":email,"codigo":codigo,"collection":collection,"face_id":face_id}#collection es el tennant
    message_json = json.dumps(message)

    response = mqtt_connection.publish(
        topic=topic_register_user,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()


def login_admin(email,password,token,uuid):

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=certificatePath,
        pri_key_filepath=privateKeyPath,
        ca_filepath=rootCAPath,
        client_id=clientId,
    )

    connect_future = mqtt_connection.connect()
    connect_future.result()

    message = {"email":email,"password":password,"token":token,"session_id":uuid}#mandar codigo mqtt al shadow
    message_json = json.dumps(message)

    response = mqtt_connection.publish(
        topic=topic_admin_login,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()


def send2bucket(code,collection,path2file):
    s3 = boto3.client('s3')
    response = s3.upload_file(path2file,'faceidcloud',str(collection+'/'+code+'.png'))
    

def update_accepted_wait_entrance(uuid):
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=certificatePath,
        pri_key_filepath=privateKeyPath,
        ca_filepath=rootCAPath,
        client_id=clientId,
    )
    connect_future = mqtt_connection.connect()
    connect_future.result()
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=topic_sub_shadow,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )
    subscribe_result = subscribe_future.result()

    while True:
        if len(value) != 0 and value['state']['desired']['session_id'] == uuid:
            break
        time.sleep(1)

    access = value['state']['desired']['access']
    collection = value['state']['desired']['collection']
    array = [access,collection]

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    return array


def send_user_access(face_id,collection):
    date = datetime.now()
    date_iso = date.isoformat()

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=certificatePath,
        pri_key_filepath=privateKeyPath,
        ca_filepath=rootCAPath,
        client_id=clientId,
    )

    connect_future = mqtt_connection.connect()
    connect_future.result()

    message = {"face_id":face_id,"collection":collection,"date":date_iso}#registrar entrada
    message_json = json.dumps(message)

    response = mqtt_connection.publish(
        topic=topic_access,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()


send_user_access("joel","UTEC")