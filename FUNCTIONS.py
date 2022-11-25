import random
from client_class import client, received_from_server
import json
import time
from cryptography.fernet import Fernet


address="0.0.0.0"
ports=[8080,8081,8082,8083,8084]
port=random.choice(ports)

dummy_client=client("0000000"+str(random.randint(0, 1000)))
dummy_client.CLIENT(address, port)

key=b'4hJZ3LWZeyOsXWWMCn7BUnUXfMPYSSyIj-Z120Pl-54='
F_encrypt=Fernet(key)

user_client=None
print("port:",port)

class FUNCTIONS:

    def check_user_exists(user_ID):

        message={
            "type": "Check User Exists",
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        # print("0")
        dummy_client.SEND(message_json)
        # print("sent")
        counter=0
        while received_from_server["Check User Exists Return"] is None:
            time.sleep(0.1)
            counter+=1
            if counter>100:
                break
        
        # print("recvd")
        is_received=received_from_server["Check User Exists Return"]
        received_from_server["Check User Exists Return"]=None

        if is_received=="True":
            return True
        else:
            return False

    def check_user_password(user_ID, user_password):
        message={
            "type": "Check User Password",
            "user_ID": str(user_ID),
            "password": str(user_password)
        }
        message_json=json.dumps(message)
        dummy_client.SEND(message_json)

        counter=0
        while received_from_server["Check User Password Return"] is None:
            time.sleep(0.1)
            counter+=1
            if counter>100:
                break
        
        is_received=received_from_server["Check User Password Return"]
        received_from_server["Check User Password Return"]=None
        # message={
        #     "type": "Set User Offline",
        #     "user_ID": str(user_ID)
        # }
        # message_json=json.dumps(message)
        # dummy_client.SEND(message_json)
        # dummy_client.CLOSE()

        if is_received=="True":
            return True
        else:
            return False
    

    def check_group_exists(group_ID):
        message={
            "type": "Check Group Exists",
            "group_ID": str(group_ID),
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)

        counter=0
        while received_from_server["Check Group Exists Return"] is None:
            time.sleep(0.1)
            counter+=1
            if counter>100:
                break
        
        is_received=received_from_server["Check Group Exists Return"]
        received_from_server["Check Group Exists Return"]=None

        if is_received=="True":
            return True
        else:
            return False
    

    def check_admin(group_ID, admin_ID):
        message={
            "type": "Check Admin For Group",
            "group_ID": str(group_ID),
            "admin_ID": str(admin_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)

        counter=0
        while received_from_server["Check Admin For Group Return"] is None:
            time.sleep(0.1)
            counter+=1
            if counter>100:
                break
        
        is_received=received_from_server["Check Admin For Group Return"]
        received_from_server["Check Admin For Group Return"]=None

        if is_received=="True":
            return True
        else:
            return False
    

    def check_member(group_ID, user_ID):
        message={
            "type": "Check Member in Group",
            "group_ID": str(group_ID),
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)

        counter=0
        while received_from_server["Check Member in Group Return"] is None:
            time.sleep(0.1)
            counter+=1
            if counter>100:
                break
        
        is_received=received_from_server["Check Member in Group Return"]
        received_from_server["Check Member in Group Return"]=None

        if is_received=="True":
            return True
        else:
            return False
    

    def add_user(user_ID, user_password):
        message={
            "type": "Sign Up",
            "user_ID": str(user_ID),
            "password": str(user_password)
        }
        message_json=json.dumps(message)
        dummy_client.SEND(message_json)
    
    
    def set_user_online(user_ID):
        global user_client
        
        user_client=client(user_ID)
        user_client.CLIENT(address, port)
        message={
            "type": "Set User Online",
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def set_user_offline(user_ID):
        message={
            "type": "Set User Offline",
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
        user_client.CLOSE()
    

    def send_text(sender_ID, receiver_ID, text_message):
        # text_message=text_message.replace("'","")
        token_text=F_encrypt.encrypt(bytes(text_message, "utf-8")).decode("utf-8")
        print("token_text:",token_text)
        # token_text=token_text.replace("'",".")

        message={
            "type": "Send Text",
            "sender_ID": str(sender_ID),
            "receiver_ID": str(receiver_ID),
            "text_message": str(token_text)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def send_image(sender_ID, receiver_ID, image):
        image_byte=open(image,"rb").read()
        token_image=F_encrypt.encrypt(image_byte)
        token_image=token_image.decode("utf-8")
        print("Length of token image:", len(token_image))
        print(token_image[:100])
        message={
            "type": "Send Image",
            "sender_ID": str(sender_ID),
            "receiver_ID": str(receiver_ID),
            "image": str(token_image)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def create_group(group_ID, admin_ID):
        message={
            "type": "Create Group",
            "group_ID": str(group_ID),
            "admin_ID": str(admin_ID),
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)

    
    def add_member(group_ID, user_ID):
        message={
            "type": "Add Member to Group",
            "group_ID": str(group_ID),
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def remove_member(group_ID, user_ID):
        message={
            "type": "Remove Member From Group",
            "group_ID": str(group_ID),
            "user_ID": str(user_ID)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def send_group_text(sender_ID, group_ID, text_message):
        # text_message=text_message.replace("'","")
        token_text=F_encrypt.encrypt(bytes(text_message, "utf-8")).decode("utf-8")
        print("token_text:",token_text)
        message={
            "type": "Send Group Text",
            "group_ID": str(group_ID),
            "sender_ID": str(sender_ID),
            "text_message": str(token_text)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
    

    def send_group_image(sender_ID, group_ID, image):
        image_byte=open(image,"rb").read()
        token_image=F_encrypt.encrypt(image_byte)
        token_image=token_image.decode("utf-8")
        print("Length of token image:", len(token_image))
        print(token_image[:100])
        message={
            "type": "Send Group Image",
            "group_ID": str(group_ID),
            "sender_ID": str(sender_ID),
            "image": str(token_image)
        }
        message_json=json.dumps(message)
        user_client.SEND(message_json)
