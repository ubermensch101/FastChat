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

        self.__WRITABLE = []
        self.__INPUTS = []
        self.__OUTPUTS = []
        self.__MESSAGE_QUEUES = {}
        self.__RECEIVING_MSG = []
        self.__SENDER_QUEUE = []
        self.conClients = []
        
    def SERVER(self, address : str = None, port : int = None, listeners : int = None):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.settimeout(150)

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
            )
        )

        sender_thread = threading.Thread(
            target=self.__sender,
            args = (
                self.__WRITABLE,
                self.__SENDER_QUEUE
            )
        )

        sending_undeliverd_msg_thread = threading.Thread(
            target=self.__undelivered_msg,
            args=()
        )

        server_thread.start()
        receiver_thread.start()
        sender_thread.start()
        sending_undeliverd_msg_thread.start()


    def __undelivered_msg(self):
        while True:
            time.sleep(3)
            undeliverd_msg_list=Undelivered_Messages_Table.get_all_undelivered_messages()
            for m in undeliverd_msg_list:
                print("u_m_l: ",m)
                if m[4]=="Text":
                    text_message=json.loads(m[5].replace("'","\""))
                    if m[2]=="Group":
                        user_list=Group_Table.get_user_list(m[3])
                        for u in user_list:
                            if u in self.conClients:  # Improve this by storing server in User Table, and checking if u is connected to server. Although this may be the best solution.
                                self.__SENDER_QUEUE.append([u, text_message])
                                Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
                    elif m[2]=="Receiver":
                        if m[1] in self.conClients:
                            self.__SENDER_QUEUE.append([m[1], text_message])
                            Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
                elif m[4]=="Image":
                    image=m[6].replace("'","\"")
                    image=json.loads(image)
                    if m[2]=="Group":
                        user_list=Group_Table.get_user_list(m[3])
                        for u in user_list:
                            if u in self.conClients:
                                self.__SENDER_QUEUE.append([u, image])
                                Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
                    elif m[2]=="Receiver":
                        if m[1] in self.conClients:
                            self.__SENDER_QUEUE.append([m[1], image])
                            Undelivered_Messages_Table.remove_undelivered_pair(m[0],m[1],m[5],m[6])
            

    def __server(self):
        data_recv_len = []

        while True:
            readable, writable, exception = select.select(self.__INPUTS, self.__OUTPUTS, self.__INPUTS)

            for r in readable:
                print("hi1")
                if r is self.sock:
                    con,addr = r.accept()
                    con.setblocking(False)
                    self.__INPUTS.append(con)
                    self.__MESSAGE_QUEUES[con] = "no_data"

                else:
                    print("client socket")
                    ini = list(zip(*data_recv_len))
                    if len(ini) == 0 or r not in ini[0]:
                        data_len=0
                        try:
                            print("recving length")
                            if r in self.__INPUTS:
                                data_len = int(r.recv(16).decode())
                            else: 
                                continue
                            print("data_len: ",data_len)
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
                            try:
                                r.close()
                            except:
                                pass
                            if r in self.__MESSAGE_QUEUES:
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
                                print("first_msg: ",data)
                                self.__MESSAGE_QUEUES[r] = data["sender_name"]
                                self.conClients.append(data["sender_name"])
                            else:
                                print("recv_msg: ",data)

                            print("before appending")
                            self.__RECEIVING_MSG.append(data)
                            print("after appending",data)
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
                
                print("_data_: ",_data_)
                message_data_json=_data_["data"]
                message_data=json.loads(message_data_json)
                print("md: ",message_data)
                print(type(message_data))
                if message_data["type"]=="Sign Up":
                    user_ID=message_data["user_ID"]
                    user_password=message_data["password"]
                    User_Table.add_user(user_ID, user_password)

                elif message_data["type"]=="Set User Online":
                    user_ID=message_data["user_ID"]
                    print("u_i: ",user_ID)
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
                    print(prepare_send)
                    self.__SENDER_QUEUE.append([_data_["sender_name"], prepare_send])
                
                elif message_data["type"]=="Send Text":
                    sender_ID=message_data["sender_ID"]
                    receiver_ID=message_data["receiver_ID"]
                    text_message=message_data["text_message"]
                    print(type(_data_))
                    print(json.dumps(_data_))
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
                    Undelivered_Messages_Table.add_undelivered_pair(sender_ID, "NULL", "Group", group_ID, "Text", json.dumps(_data_), "NULL")
                
                elif message_data["type"]=="Send Group Image":
                    group_ID=message_data["group_ID"]
                    sender_ID=message_data["sender_ID"]
                    image=message_data["image"]
                    Undelivered_Messages_Table.add_undelivered_pair(sender_ID, "NULL", "Group", group_ID, "Image", "NULL", json.dumps(_data_))
                
                elif message_data["type"]=="Check User Exists":
                    user_ID=message_data["user_ID"]
                    user_exists=User_Table.check_user_existence(user_ID)
                    print("u_e: ",user_exists)
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
                    print("c_p: ",check_password)
                    
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

                elif message_data["type"]=="Check Member in Group":
                    group_ID=message_data["group_ID"]
                    user_ID=message_data["user_ID"]
                    member_exists=Group_Table.check_user_existence(group_ID,user_ID)
                    
                    server_message={
                        "type": "Check Member in Group Return",
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


    def __sender(self,__writable, __senderQueue ):
        while True:

            for s in __writable:
                if s._closed and s.fileno() == -1:
                    __writable.remove(s)
                try:
                    username = self.__MESSAGE_QUEUES[s]
                except KeyError:
                    pass
                sender_q = list(zip(*__senderQueue))

                
                if len(sender_q) > 0:
                    print("usr: ",username)
                    if username in sender_q[0]:
                        INDEX = sender_q[0].index(username)
                        prepare_send = base64.b64encode(pickle.dumps(sender_q[1][INDEX]))
                        s.send(str(len(prepare_send)).center(16,"|").encode("utf-8"))
                        time.sleep(0.5)
                        s.send(prepare_send)
                        print("msg_sent: ",sender_q[1][INDEX])

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
                            print("user exited")

                        __senderQueue.pop(INDEX)
                        

class server():
    def __init__(self):
        __parent = MAIN()
        self.SERVER = __parent.SERVER
        self.conClients = __parent.conClients