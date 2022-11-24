from server_class import *
from DATABASE import User_Table, Group_Table, Undelivered_Messages_Table
import sqlite3,sys

import threading

global lock
lock=threading.Lock()

HOST_ADDR = "0.0.0.0"

if len(sys.argv)!=2:
    print("Give just one argument for port number")

conn=sqlite3.connect("user_data.db",check_same_thread=False)
cursor=conn.cursor()

User_Table.create_users_table()
Group_Table.create_groups_table()
Undelivered_Messages_Table.create_undelivered_table()


s1 = server()
s1.SERVER(HOST_ADDR, int(sys.argv[1]),100)
