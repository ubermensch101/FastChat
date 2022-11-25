import socket
import base64
import pickle
import threading
import json
import time
from cryptography.fernet import Fernet
from PIL import Image
import io
import random

key=b'4hJZ3LWZeyOsXWWMCn7BUnUXfMPYSSyIj-Z120Pl-54='
F_encrypt=Fernet(key)

received_from_server={
    "Check User Exists Return": None,
    "Check User Password Return": None,
    "Check Group Exists Return": None,
    "Check Admin For Group Return": None,
    "Check Member in Group Return": None
}

DASHED_LINE="\033[91m"+"--------------------"+"\033[0m"

class MAIN():

    def __init__(self,client_name : str = None):

        self.__client_name = client_name
        self.__SENDER_QUEUE = []
        self.done=False
        
    def CLIENT(self,address : str = None, port : int = None):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address,port))
        
        receiver_thread = threading.Thread(
            target = self.__receiver,
            args = ()
            )

        sender_thread = threading.Thread(
            target = self.__sender,
            args = (
                self.sock,
                self.__SENDER_QUEUE
            )
        )


        receiver_thread.start()
        sender_thread.start()


    def __receiver(self):

            x=False
            while not x:
                data_len = int(self.sock.recv(16).decode().strip("|"))
                if not data_len:
                    self.sock.close()
                    raise ConnectionError("[SERVER GOES DOWN - CONNECTION LOST]")

                # recv_data = self.sock.recv(data_len)
                bytes_received=0
                packet_list=[]
                while bytes_received<data_len:
                    if data_len-bytes_received>65536:
                        packet=self.sock.recv(65536)
                        bytes_received+=65536
                    else:
                        packet=self.sock.recv(data_len-bytes_received)
                        bytes_received=data_len
                    packet_list.append(packet)

                recv_data=b"".join(packet_list)
                recv_data = pickle.loads(base64.b64decode(recv_data))
                received_message=json.loads(recv_data["data"])
                if received_message["type"]=="Set User Offline Return":
                    x=True
                elif received_message["type"]=="Check User Exists Return":
                    received_from_server["Check User Exists Return"]=received_message["user_exists"]
                
                elif received_message["type"]=="Check User Password Return":
                    received_from_server["Check User Password Return"]=received_message["password_correct"]
                
                elif received_message["type"]=="Check Group Exists Return":
                    received_from_server["Check Group Exists Return"]=received_message["group_exists"]
                
                elif received_message["type"]=="Check Admin For Group Return":
                    received_from_server["Check Admin For Group Return"]=received_message["admin_correct"]
                
                elif received_message["type"]=="Check Member in Group Return":
                    received_from_server["Check Member in Group Return"]=received_message["member_exists"]
                
                elif received_message["type"]=="Send Text":
                    print("\nMessage Received!")
                    print(DASHED_LINE)

                    text_message_bytes=bytes(received_message["text_message"], "utf-8")
                    text_message=F_encrypt.decrypt(text_message_bytes).decode("utf-8")

                    print(text_message)
                    print("\033[91mReceived from:\033[0m "+received_message["sender_ID"])
                    print(DASHED_LINE)
                    print("")
                
                elif received_message["type"]=="Send Image":
                    print("\nMessage Received!")
                    print(DASHED_LINE)

                    image_bytes=bytes(received_message["image"], "utf-8")
                    image_bytes=F_encrypt.decrypt(image_bytes)
                    image=Image.open(io.BytesIO(image_bytes))
                    with open("images/"+received_message["sender_ID"]+"_"+self.__client_name+"_"+str(random.randint(0, 1000))+".png", "wb+") as f:
                        image.save(f)
                    #image.save("images/"+received_message["sender_ID"]+".png")

                    print("\033[91mReceived from:\033[0m "+received_message["sender_ID"])
                    print(DASHED_LINE)
                    print("")
                
                elif received_message["type"]=="Send Group Text":
                    print("\nMessage Received From Group!")
                    print(DASHED_LINE)

                    text_message_bytes=bytes(received_message["text_message"], "utf-8")
                    text_message=F_encrypt.decrypt(text_message_bytes).decode("utf-8")

                    print(text_message)
                    print("\033[91mReceived from:\033[0m "+received_message["sender_ID"])
                    print("\033[91mGroup ID:\033[0m "+received_message["group_ID"])
                    print(DASHED_LINE)
                    print("")
                
                elif received_message["type"]=="Send Group Image":
                    print("\nMessage Received From Group!")
                    print(DASHED_LINE)

                    image_bytes=bytes(received_message["image"], "utf-8")
                    image_bytes=F_encrypt.decrypt(image_bytes)
                    image=Image.open(io.BytesIO(image_bytes))
                    with open("images/"+received_message["sender_ID"]+"_"+self.__client_name+"_"+str(random.randint(0,1000))+".png", "wb+") as f:
                        image.save(f)

                    print("\033[91mReceived from:\033[0m "+received_message["sender_ID"])
                    print("\033[91mGroup ID:\033[0m "+received_message["group_ID"])
                    print(DASHED_LINE)
                    print("")

            
            self.done=True
                    
    def __sender(self,sock,sender_queue):

        z=False
        while not z:
            for i,s in enumerate(sender_queue):
                
                prepare_for_send = base64.b64encode(pickle.dumps(s))

                send_length=str(len(prepare_for_send))
                for kappa in range(8-len(send_length)):
                    send_length="0"+send_length
                
                sock.send(bytes(send_length,"utf-8"))
                sock.send(prepare_for_send)


                sender_queue.pop(i)

                
                if json.loads(s["data"])["type"]=="Set User Offline":
                    z=True
                
        

    def SEND(self,data = None):

        if not data:
            raise TypeError("SEND() missing 1 required positional argument: 'data'")

        lst = [ [1,2], {"a":1}, (1,2), {1,2,}, "a", 12, 0.45, b"bytes" ]
        allowed_lst= []
        
        for l in lst:
            allowed_lst.append(type(l))
        if type(data) in allowed_lst:
            prepare_send_data = {
                'sender_name' : self.__client_name,
                'target_name' : 'SERVER',
                'data' : data
            }

            self.__SENDER_QUEUE.append(prepare_send_data)

    
    def CLOSE(self):
        
        while(True):
            if self.done:
                self.sock.close()
                break
        

class client():
    def __init__(self,client_name : str = None):
        __parent = MAIN(client_name)
        self.CLIENT = __parent.CLIENT
        self.SEND = __parent.SEND
        self.CLOSE = __parent.CLOSE
