import select
import socket
import base64
import pickle
import threading
import time
import json
from DATABASE import User_Table, Group_Table, Undelivered_Messages_Table

class MAIN():

    def __init__(self):

        # self.__READABLE = []
        self.__WRITABLE = []
        self.__INPUTS = []
        self.__OUTPUTS = []
        self.__MESSAGE_QUEUES = {}
        # self.__CUSTOM_CHANNEL = []
        # self.__CALLBACK_LOOP = []
        self.__RECEIVING_MSG = []
        # self.__MESSAGE_HANDLER = []
        # self.__BYPASS_MSG  = []
        self.__SENDER_QUEUE = []
        self.conClients = []
        
    def SERVER(self, address : str = None, port : int = None, listeners : int = None):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)

        self.sock.bind((address, port))
        self.sock.listen(listeners)

        print("[SERVER IS ACTIVATED | LISTENING]")


        self.__INPUTS.append(self.sock)

        server_thread = threading.Thread(
            target = self.__server,
            args = ()
        )

        receiver_thread = threading.Thread(
            target=self.__handler,
            args = (
                self.__RECEIVING_MSG,
                # self.__BYPASS_MSG,
                # # self.__CUSTOM_CHANNEL,
                # self.__MESSAGE_HANDLER
            )
        )

        sender_thread = threading.Thread(
            target=self.__sender,
            args = (
                self.__WRITABLE,
                self.__SENDER_QUEUE
            )
        )

        # callback_loop_thread = threading.Thread(
        #     target=self.__callback_loop,
        #     args = (
        #         self.__CALLBACK_LOOP,
        #     )
        # )

        sending_undeliverd_msg_thread = threading.Thread(
            target=self.__undelivered_msg,
            args=()
        )

        # server_thread.daemon = True
        # receiver_thread.daemon = True
        # sender_thread.daemon = True
        # # callback_loop_thread.daemon = True
        # sending_undeliverd_msg_thread.daemon = True

        server_thread.start()
        receiver_thread.start()
        sender_thread.start()
        # callback_loop_thread.start()
        sending_undeliverd_msg_thread.start()


    def __undelivered_msg(self):
        while True:
            undeliverd_msg_list=Undelivered_Messages_Table.get_all_undelivered_messages()
            for m in undeliverd_msg_list:
                # print("u_m_l: ",m)
                if m[4]=="Text":
                    text_message=json.loads(m[5].replace("'","\""))
                    if m[2]=="Group":
                        user_list=Group_Table.get_user_list(m[3])
                        for u in user_list:
                            if u in self.conClients:  # Improve this by storing server in User Table, and checking if u is connected to server. Although this may be the best solution.
                                self.__SENDER_QUEUE.append(u, text_message)
                                Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
                    elif m[2]=="Receiver":
                        if m[1] in self.conClients:
                            self.__SENDER_QUEUE.append([m[1], text_message])
                            Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
                elif m[4]=="Image":
                    image=json.loads(m[6])
                    if m[2]=="Group":
                        user_list=Group_Table.get_user_list(m[3])
                        for u in user_list:
                            if u in self.conClients:
                                self.__SENDER_QUEUE.append([u, image])
                                Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
                    elif m[2]=="Receiver":
                        if m[1] in self.conClients:
                            self.__SENDER_QUEUE.append(m[1], image)
                            Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
            

    def __server(self):
        data_recv_len = []

        while True:
            readable, writable, exception = select.select(self.__INPUTS, self.__OUTPUTS, self.__INPUTS)

            for r in readable:
                #print("hi1")
                if r is self.sock:
                    con,addr = r.accept()
                    con.setblocking(False)
                    self.__INPUTS.append(con)
                    self.__MESSAGE_QUEUES[con] = "no_data"

                else:
                    #print("client socket")
                    ini = list(zip(*data_recv_len))
                    if len(ini) == 0 or r not in ini[0]:
                        data_len=0
                        try:
                            #print("recving length")
                            if r in self.__INPUTS:
                                data_len = int(r.recv(32).decode())
                            #print("data_len: ",data_len)
                        except ConnectionResetError:
                            print("User Disconnected1")
                            if r in self.__OUTPUTS:
                                self.__OUTPUTS.remove(r)
                            if r in self.__WRITABLE:
                                self.__WRITABLE.remove(r)
                            self.__INPUTS.remove(r)
                            r.close()
                            del self.__MESSAGE_QUEUES[r]
                            continue
                        except Exception as exc:
                            print(exc)

                        if data_len:
                            data_recv_len.append([r,data_len])
                        else:
                            print("User Disconnected2")
                            if r in self.__OUTPUTS:
                                self.__OUTPUTS.remove(r)
                            if r in self.__INPUTS:
                                self.__INPUTS.remove(r)
                            if r in self.__WRITABLE:
                                self.__WRITABLE.remove(r)
                            r.close()
                            del self.__MESSAGE_QUEUES[r]
                            continue
                    else:
                        INDEX = ini[0].index(r)
                        try:
                            recv_len = data_recv_len.pop(INDEX)[1]
                            if r in self.__INPUTS:
                                data = r.recv(recv_len)
                            data = pickle.loads(base64.b64decode(data))
                            
                            if self.__MESSAGE_QUEUES[r] == "no_data":
                                #print("first_msg: ",data)
                                self.__MESSAGE_QUEUES[r] = data["sender_name"]
                                self.conClients.append(data["sender_name"])
                            # else:
                            #     #print("recv_msg: ",data)

                            self.__RECEIVING_MSG.append(data)
                            if r not in self.__OUTPUTS:
                                self.__OUTPUTS.append(r)
                            
                        except ConnectionResetError:
                            print("User Disconnected3")
                            if r in self.__OUTPUTS:
                                self.__OUTPUTS.remove(r)
                            self.__INPUTS.remove(r)
                            if r in self.__WRITABLE:
                                self.__WRITABLE.remove(r)
                            r.close()
                            del self.__MESSAGE_QUEUES[r]
                            continue
                        except EOFError:
                            pass

            for w in writable:
                if w not in self.__WRITABLE:
                    self.__WRITABLE.append(w)

            for e in exception:
                self.__INPUTS.remove(e)
                if e in self.__OUTPUTS:
                    self.__OUTPUTS.remove(e)
                e.close()
                del self.__MESSAGE_QUEUES[e]

    def __handler(self,__receivingMsg):
        while True:
            for i, _data_ in enumerate(__receivingMsg):
                
                # channel=_data_["channel"]
                #print("_data_: ",_data_)
                message_data_json=_data_["data"]
                message_data=json.loads(message_data_json)
                #print("md: ",message_data)
                #print(type(message_data))
                if message_data["type"]=="Sign Up":
                    user_ID=message_data["user_ID"]
                    user_password=message_data["password"]
                    User_Table.add_user(user_ID, user_password)

                elif message_data["type"]=="Set User Online":
                    user_ID=message_data["user_ID"]
                    #print("u_i: ",user_ID)
                    User_Table.set_online(user_ID)
                
                elif message_data["type"]=="Set User Offline":
                    user_ID=message_data["user_ID"]
                    User_Table.set_offline(user_ID)

                    server_message={
                        "type": "Set User Offline Return",
                        "user_ID": str(user_ID)
                    }

                    server_message_json=json.dumps(server_message)

                    prepare_send = {
                        "sender_name" : "SERVER",
                        "target_name" : user_ID,
                        "data" : server_message_json
                    }
                    #print(prepare_send)
                    self.__SENDER_QUEUE.append([_data_["sender_name"], prepare_send])
                
                elif message_data["type"]=="Send Text":
                    sender_ID=message_data["sender_ID"]
                    receiver_ID=message_data["receiver_ID"]
                    text_message=message_data["text_message"]
                    #print(type(_data_))
                    #print(json.dumps(_data_))
                    Undelivered_Messages_Table.add_undelivered_pair(sender_ID, receiver_ID, "Receiver", "NULL", "Text", json.dumps(_data_), "NULL")
                
                elif message_data["type"]=="Send Image":
                    sender_ID=message_data["sender_ID"]
                    receiver_ID=message_data["receiver_ID"]
                    image=message_data["image"]
                    Undelivered_Messages_Table.add_undelivered_pair(sender_ID, receiver_ID, "Receiver", "NULL", "Image", "NULL", json.dumps(_data_))
                
                elif message_data["type"]=="Create Group":
                    group_ID=message_data["group_ID"]
                    admin_ID=message_data["admin_ID"]
                    Group_Table.create_group(group_ID, admin_ID)
                
                elif message_data["type"]=="Add Member to Group":
                    group_ID=message_data["group_ID"]
                    user_ID=message_data["user_ID"]
                    Group_Table.add_to_group(group_ID, user_ID)

                elif message_data["type"]=="Remove Member From Group":
                    group_ID=message_data["group_ID"]
                    user_ID=message_data["user_ID"]
                    Group_Table.remove_from_group(group_ID, user_ID)
                
                elif message_data["type"]=="Send Group Text":
                    group_ID=message_data["group_ID"]
                    sender_ID=message_data["sender_ID"]
                    text_message=message_data["text_message"]
                    Undelivered_Messages_Table.add_undelivered_pair(sender_ID, "NULL", "Group", group_ID, "Text", json.dumps(text_message), "NULL")
                
                elif message_data["type"]=="Send Group Image":
                    group_ID=message_data["group_ID"]
                    sender_ID=message_data["sender_ID"]
                    image=message_data["image"]
                    Undelivered_Messages_Table.add_undelivered_pair(sender_ID, "NULL", "Group", group_ID, "Image", "NULL", json.dumps(image))
                
                elif message_data["type"]=="Check User Exists":
                    user_ID=message_data["user_ID"]
                    user_exists=User_Table.check_user_existence(user_ID)
                    #print("u_e: ",user_exists)
                    server_message={
                        "type": "Check User Exists Return",
                        "user_exists": str(user_exists)
                    }

                    server_message_json=json.dumps(server_message)

                    prepare_send = {
                        "sender_name" : "SERVER",
                        "target_name" : user_ID,
                        "data" : server_message_json
                    }

                    self.__SENDER_QUEUE.append([_data_["sender_name"], prepare_send])
                   
                elif message_data["type"]=="Check User Password":
                    user_ID=message_data["user_ID"]
                    user_password=message_data["password"]
                    check_password=User_Table.check_user_password(user_ID,user_password)
                    #print("c_p: ",check_password)
                    
                    server_message={
                        "type": "Check User Password Return",
                        "password_correct": str(check_password)
                    }

                    server_message_json=json.dumps(server_message)

                    prepare_send = {
                        "sender_name" : "SERVER",
                        "target_name" : user_ID,
                        "data" : server_message_json
                    }
                    
                    self.__SENDER_QUEUE.append([_data_["sender_name"], prepare_send])

                elif message_data["type"]=="Check Group Exists":
                    group_ID=message_data["group_ID"]
                    group_exists=Group_Table.check_group_existence(group_ID)
                    
                    server_message={
                        "type": "Check Group Exists Return",
                        "group_exists": str(group_exists)
                    }

                    server_message_json=json.dumps(server_message)

                    prepare_send = {
                        "sender_name" : "SERVER",
                        "target_name" : user_ID,
                        "data" : server_message_json
                    }
                    
                    self.__SENDER_QUEUE.append([_data_["sender_name"], prepare_send])
                    
                elif message_data["type"]=="Check Admin For Group":
                    group_ID=message_data["group_ID"]
                    admin_ID=message_data["admin_ID"]
                    check_admin=Group_Table.check_admin(group_ID,admin_ID)
                    
                    server_message={
                        "type": "Check Admin For Group Return",
                        "admin_correct": str(check_admin)
                    }

                    server_message_json=json.dumps(server_message)

                    prepare_send = {
                        "sender_name" : "SERVER",
                        "target_name" : user_ID,
                        "data" : server_message_json
                    }
                    
                    self.__SENDER_QUEUE.append([_data_["sender_name"], prepare_send])

                elif message_data["type"]=="check Member In Group":
                    group_ID=message_data["group_ID"]
                    user_ID=message_data["user_ID"]
                    member_exists=Group_Table.check_user_existence(group_ID,user_ID)
                    
                    server_message={
                        "type": "Check Member In Group Return",
                        "member_exists": str(member_exists)
                    }

                    server_message_json=json.dumps(server_message)

                    prepare_send = {
                        "sender_name" : "SERVER",
                        "target_name" : user_ID,
                        "data" : server_message_json
                    }
                    
                    self.__SENDER_QUEUE.append([_data_["sender_name"], prepare_send])

                __receivingMsg.pop(i)

                # if _data_["channel"] == "DSP_MSG":
                #     print("data: " ,_data_)
                #     __bypassMsg.append([_data_["target_name"],_data_])
                #     __receivingMsg.pop(i)
                # elif _data_["channel"] in __customChannel:
                #     __messageHandler.append(_data_)
                #     __receivingMsg.pop(i)

    def __sender(self,__writable, __senderQueue ):
        while True:

            for s in __writable:
                if s._closed and s.fileno() == -1:
                    __writable.remove(s)
                try:
                    username = self.__MESSAGE_QUEUES[s]
                except KeyError:
                    pass
                # bypassMsg = list(zip(*__bypassMsg))
                sender_q = list(zip(*__senderQueue))

                # if len(bypassMsg) > 0:
                #     if username in bypassMsg[0]:
                #         INDEX = bypassMsg[0].index(username)
                #         prepare_send = base64.b64encode(pickle.dumps(bypassMsg[1][INDEX]))
                #         s.send(str(len(prepare_send)).center(16,"|").encode("utf-8"))
                #         s.send(prepare_send)
                #         __bypassMsg.pop(INDEX)
                #         print("Message bypasses")
                
                if len(sender_q) > 0:
                    #print("usr: ",username)
                    if username in sender_q[0]:
                        # print("user exist")
                        INDEX = sender_q[0].index(username)
                        prepare_send = base64.b64encode(pickle.dumps(sender_q[1][INDEX]))
                        s.send(str(len(prepare_send)).center(16,"|").encode("utf-8"))
                        time.sleep(0.5)
                        s.send(prepare_send)
                        #print("msg_sent: ",sender_q[1][INDEX])

                        message_data=json.loads(sender_q[1][INDEX]["data"])
                        if message_data["type"]=="Set User Offline Return":
                            del self.__MESSAGE_QUEUES[s]
                            if message_data["user_ID"] in self.conClients:
                                self.conClients.remove(message_data["user_ID"])
                            if s in self.__OUTPUTS:
                                self.__OUTPUTS.remove(s)
                            if s in self.__INPUTS:
                                self.__INPUTS.remove(s)
                            if s in self.__WRITABLE:
                                self.__WRITABLE.remove(s)
                            
                            s.close()

                        __senderQueue.pop(INDEX)
                        print("User exited")


    # def __callback_loop(self,__callbackLst):
    #     while True:
    #         for i,func in enumerate(__callbackLst):
    #             __callbackLst.pop(i)
    #             func[0](*func[1])

    # def CREATE_CHANNEL(self,channels : str = None, multiple : bool = False):
    #     if multiple:
    #         if type(channels) is type([]):
    #             for channel in channels:
    #                 if channel not in self.__CUSTOM_CHANNEL:
    #                     self.__CUSTOM_CHANNEL.append(channel)
    #     else:
    #         if channels not in self.__CUSTOM_CHANNEL:
    #             self.__CUSTOM_CHANNEL.append(channels)
    #     pass

    # def SEND(self,target_name, channel : str = None, data = None):
    #     if not channel:
    #         raise TypeError("SEND() missing 1 required positional argument: 'channel'")
    #     if not data:
    #         raise TypeError("SEND() missing 1 required positional argument: 'data'")

    #     lst = [ [1,2], {"a":1}, (1,2), {1,2,}, "a", 12, 0.45, b"bytes" ]
    #     allowed_lst= []
    #     for l in lst:
    #         allowed_lst.append(type(l))
    #     if type(data) in allowed_lst:
    #         if channel in self.__CUSTOM_CHANNEL:
    #             prepare_send = {
    #                 "channel" : channel,
    #                 "sender_name" : "SERVER",
    #                 "target_name" : target_name,
    #                 "data" : data
    #             }
    #             # print(prepare_send)
    #             self.__SENDER_QUEUE.append([prepare_send["target_name"],prepare_send])

    #     else:
    #         raise TypeError(f"{type(data)} is not allowed as a sendable data type for 'data'")

    # def LISTEN(self,channel : str = None, function : object = None, ex_counter = None, args = None):
    #     if not channel:
    #         raise TypeError("LISTEN() missing 1 required positional argument: 'channel'")
    #     else:
    #         found = False
    #         index = None
            
    #         if channel in self.__CUSTOM_CHANNEL:
    #             for i,d in enumerate(self.__MESSAGE_HANDLER):
    #                 if d["channel"] == channel:
    #                     found = True
    #                     index = i
    #                     break
    #             if found:
    #                 if not args:
    #                     p_data = self.__MESSAGE_HANDLER.pop(index)
    #                     self.__CALLBACK_LOOP.append([function,[p_data]])
    #                 else:
    #                     p_data = self.__MESSAGE_HANDLER.pop(index)
    #                     args = list(args)
    #                     args.insert(0,p_data)
    #                     self.__CALLBACK_LOOP.append([function,[args]])


class server():
    def __init__(self):
        __parent = MAIN()
        self.SERVER = __parent.SERVER
        # self.CREATE_CHANNEL = __parent.CREATE_CHANNEL
        # self.LISTEN = __parent.LISTEN
        # self.SEND = __parent.SEND
        self.conClients = __parent.conClients