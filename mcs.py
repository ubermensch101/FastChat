import sqlite3
from server_class import *
from user_table_file import *
from undelivered_messages_file import *

HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
conn=sqlite3.connect("user_data.db",check_same_thread=False)
cursor=conn.cursor()
create_users_table(conn,cursor)
create_undelivered_table(conn,cursor)

s = server()
s.SERVER(HOST_ADDR,HOST_PORT,100)
s.CREATE_CHANNEL("test")

def client_msg(data):
    print(f"{data['sender_name']} => {data['data']}")


while(True):

    for d in s.conClients:
        
        if d["type"]=="SignUp" and not check_online(d["username"],cursor) :
            if not check_user_existence(d["username"],cursor):
                add_user(d["username"],d["password"],conn,cursor)
                # print("finished signup")
                s.SEND(d["username"],"test","Hello From Server")
            else:
                s.SEND(d["username"],"test","username already exist")
        elif d["type"]=="Login" and not check_online(d["username"],cursor):
            if check_user_existence(d["username"],cursor):
                print("user exist")
                if not check_user_password(d["username"],d["password"],cursor):
                    s.SEND(d["username"],"test","Wrong Password")
                else:
                    change_status(d["username"],cursor)
            else:
                s.SEND(d["username"],"test","Username doesn't exist")
        

    s.LISTEN("test",client_msg)