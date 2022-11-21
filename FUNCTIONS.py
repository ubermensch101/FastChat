import random
from client_class import client
import json


dummy_client=client("0000000"+str(random.randint(0, 1000)))



class FUNCTIONS:


    def check_user_exists(user_ID):
        pass
    def add_user(user_ID, user_password):
        user_client=client(user_ID)
        message={
            "message_type": "Sign Up",
            "user_ID": str(user_ID),
            "password": str(user_password)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
        user_client.SEND("exit")
        user_client.CLOSE()
    
    def check_user_password(user_ID, user_password):
        message={
            "message_type": "Check User Password",
            "user_ID": str(user_ID),
            "password": str(user_password)
        }
        message_json=json.dumps(message_json)
        dummy_client.SEND(message_json)
    
    def set_user_online(user_ID):
        pass
    






def check_user_exists(user_ID):
    return random.randint(0, 1)
def check_user_password(user_ID, user_password):
    return True
def add_user(user_ID, user_password):
    return
def set_user_online(user_ID):
    return
def set_user_offline(user_ID):
    return
def send_text(sender_ID, receiver_ID, text_message):
    return
def send_image(sender_ID, receiver_ID, image):
    return
def create_group(group_ID, admin_ID):
    return
def check_group_exists(group_ID):
    return random.randint(0, 1)
def check_admin(group_Id, admin_ID):
    return random.randint(0, 1)
def add_member(group_ID, user_ID):
    return
def remove_member(group_ID, user_ID):
    return
def check_member(group_ID, user_ID):
    return True
def send_group_text(sender_ID, group_ID, text_message):
    return
def send_group_image(sender_ID, group_ID, image):
    return
