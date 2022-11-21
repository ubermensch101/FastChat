import random
from client_class import client
import json


address="0.0.0.0"
port=8080

dummy_client=client("0000000"+str(random.randint(0, 1000)))
dummy_client.CLIENT(address, port)

user_client=None


class FUNCTIONS:

    def check_user_exists(user_ID):
        message={
            "type": "Check User Exists",
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        dummy_client.SEND(message_json)

    def check_user_password(user_ID, user_password):
        message={
            "type": "Check User Password",
            "user_ID": str(user_ID),
            "password": str(user_password)
        }
        message_json=json.dumps(message)
        dummy_client.SEND(message_json)
    

    def check_group_exists(group_ID):
        message={
            "type": "Check Group Exists",
            "group_ID": str(group_ID),
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def check_admin(group_ID, admin_ID):
        message={
            "type": "Check Admin For Group",
            "group_ID": str(group_ID),
            "admin_ID": str(admin_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def check_member(group_ID, user_ID):
        message={
            "type": "Remove Member from Group",
            "group_ID": str(group_ID),
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def add_user(user_ID, user_password):
        message={
            "type": "Sign Up",
            "user_ID": str(user_ID),
            "password": str(user_password)
        }
        message_json=json.dumps(message)
        dummy_client.SEND_TO_DATABASE(message_json)
    
    
    def set_user_online(user_ID):
        user_client=client(user_ID)
        user_client.CLIENT(address, port)
        message={
            "type": "Set User Online",
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)
    

    def set_user_offline(user_ID):
        message={
            "type": "Set User Offline",
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)
        user_client.CLOSE()
    

    def send_text(sender_ID, receiver_ID, text_message):
        message={
            "type": "Send Text",
            "sender_ID": str(sender_ID),
            "receiver_ID": str(receiver_ID),
            "text_message": str(text_message)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)
    

    def send_image(sender_ID, receiver_ID, image):
        message={
            "type": "Send Image",
            "sender_ID": str(sender_ID),
            "receiver_ID": str(receiver_ID),
            "image": str(image)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)
    

    def create_group(group_ID, admin_ID):
        message={
            "type": "Create Group",
            "group_ID": str(group_ID),
            "admin_ID": str(admin_ID),
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)

    
    def add_member(group_ID, user_ID):
        message={
            "type": "Add Member to Group",
            "group_ID": str(group_ID),
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)
    

    def remove_member(group_ID, user_ID):
        message={
            "type": "Remove Member from Group",
            "group_ID": str(group_ID),
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)
    

    def send_group_text(sender_ID, group_ID, text_message):
        message={
            "type": "Send Group Text",
            "group_ID": str(group_ID),
            "sender_ID": str(sender_ID),
            "text_message": str(text_message)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)
    

    def send_group_image(sender_ID, group_ID, image):
        message={
            "type": "Send Group Image",
            "group_ID": str(group_ID),
            "sender_ID": str(sender_ID),
            "image": str(image)
        }
        message_json=json.dumps(message)
        user_client.SEND_TO_DATABASE(message_json)

    
        

    






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
