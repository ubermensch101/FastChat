import socket
import base64
import pickle
import threading
import multiprocessing
import hashlib
import json
import time

class MAIN():

    def __init__(self,client_name : str = None):

        self.__client_name = client_name

        self.__CUSTOM_CHANNEL = []
        self.__MESSAGE_HANDLER = []
        self.__CALLBACK_LOOP = []
        self.__SENDER_QUEUE = []
        self.done=False
        
        self.__CUSTOM_CHANNEL.append("DSP_MSG")

    def CLIENT(self,address : str = None, port : int = None):

        print("[Connecting To Server]")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address,port))
        
        print("[Connected]")

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

        callback_loop_thread_process = threading.Thread(
            target = self.__callback_loop,
            args = (self.__CALLBACK_LOOP,)
        )

        receiver_thread.start()
        sender_thread.start()
        callback_loop_thread_process.start()


    def __receiver(self):

            x=False
            while not x:
                data_len = int(self.sock.recv(16).decode().strip("|"))
                if not data_len:
                    self.sock.close()
                    raise ConnectionError("[SERVER GOES DOWN - CONNECTION LOST]")

                recv_data = self.sock.recv(data_len)
                recv_data = pickle.loads(base64.b64decode(recv_data))

                if(recv_data["data"]=="exited" and recv_data["sender_name"]=="SERVER"): 
                    x=True
                    print("exited0")

                if type(recv_data) is type({}):
                    if recv_data["channel"] == "DSP_MSG":
                        print("recv_msg: ",recv_data)
                        self.__MESSAGE_HANDLER.append(recv_data)
                    elif recv_data["channel"] in self.__CUSTOM_CHANNEL:
                        self.__MESSAGE_HANDLER.append(recv_data)
            
            print("exited1")
            self.done=True
                    
    def __sender(self,sock,message_queue):

        z=False
        while not z:
            for i,s in enumerate(message_queue):
                
                print("msg2: ",s)
                prepare_for_send = base64.b64encode(pickle.dumps(s))
                # print(prepare_for_send)
                # print(bytes(str(len(prepare_for_send)),"utf-8"))
                sock.send(bytes(str(len(prepare_for_send)),"utf-8"))
                time.sleep(0.5)
                sock.send(prepare_for_send)
                message_queue.pop(i)
                if(s["data"]=="exit"): z=True
                
        
        print("exited2")

    def __callback_loop(self,callback_lst):

        while not self.done:
            for i,func in enumerate(callback_lst):
                callback_lst.pop(i)
                func[0](*func[1])

        print("exited3")

    def CREATE_CHANNEL(self,channels : str = None, multiple : bool = False):

        if channels not in self.__CUSTOM_CHANNEL:
            self.__CUSTOM_CHANNEL.append(channels)


    def LISTEN(self,channel : str = None, function : object = None, ex_counter = None, args = None):
        if not channel:
            raise TypeError("LISTEN() missing 1 required positional argument: 'channel'")
        else:
            found = False
            index = None
            
            if channel in self.__CUSTOM_CHANNEL:
                for i,d in enumerate(self.__MESSAGE_HANDLER):
                    if d["channel"] == channel:
                        found = True
                        index = i
                        break

                if found:
                    print("found")
                    if not args:
                        p_data = self.__MESSAGE_HANDLER.pop(index)
                        self.__CALLBACK_LOOP.append([function,[p_data]])
                    else:
                        p_data = self.__MESSAGE_HANDLER.pop(index)
                        args = list(args)
                        args.insert(0,p_data)
                        self.__CALLBACK_LOOP.append([function,args])
                    
                    return 1
        
        return 0

    def SEND(self,channel : str = None, data = None):

        if not channel:
            raise TypeError("SEND() missing 1 required positional argument: 'channel'")
        if not data:
            raise TypeError("SEND() missing 1 required positional argument: 'data'")

        lst = [ [1,2], {"a":1}, (1,2), {1,2,}, "a", 12, 0.45, b"bytes" ]
        allowed_lst= []
        
        for l in lst:
            allowed_lst.append(type(l))
        # print("data: ", data)
        if type(data) in allowed_lst:
            if channel in self.__CUSTOM_CHANNEL:
                prepare_send_data = {
                    "channel" : channel,
                    "type":"",
                    "sender_name" : self.__client_name,
                    "target_name" : "SERVER",
                    "data" : data
                    }
                
                # if type(data)==dict and "password" in data.keys():
                #     # print("dictionary")
                #     prepare_send_data=data
                
                # print(prepare_send_data)

                self.__SENDER_QUEUE.append(prepare_send_data)


    def SEND_TO_CLIENT(self,target_name : str = None, data = None):
        if not target_name:
            raise TypeError("SEND() missing 1 required positional argument: 'target_name'")
        if not data:
            raise TypeError("SEND() missing 1 required positional argument: 'data'")

        lst = [ [1,2], {"a":1}, (1,2), {1,2,}, "a", 12, 0.45, b"bytes" ]
        allowed_lst= []
        for l in lst:
            allowed_lst.append(type(l))
        if type(data) in allowed_lst:
            prepare_send_data = {
                "channel" : "DSP_MSG",
                "type":"",
                "sender_name" : self.__client_name,
                "target_name" : target_name,
                "data" : data
            }
            print("msg1: ",prepare_send_data)
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
        self.LISTEN = __parent.LISTEN
        self.CREATE_CHANNEL = __parent.CREATE_CHANNEL
        self.SEND = __parent.SEND
        self.SEND_TO_CLIENT = __parent.SEND_TO_CLIENT
        self.CLOSE = __parent.CLOSE
