from server_class import *
from DATABASE import User_Table, Group_Table, Undelivered_Messages_Table
import sqlite3,sys

HOST_ADDR = "0.0.0.0"
HOST_PORT1 = 8080
HOST_PORT2 = 8081
HOST_PORT3 = 8082
HOST_PORT4 = 8083
HOST_PORT5 = 8084

conn=sqlite3.connect("user_data.db",check_same_thread=False)
cursor=conn.cursor()

User_Table.create_users_table()
Group_Table.create_groups_table()
Undelivered_Messages_Table.create_undelivered_table()

s1 = server()
s1.SERVER(HOST_ADDR,HOST_PORT1,100)

s2 = server()
s2.SERVER(HOST_ADDR,HOST_PORT2,100)

s3 = server()
s3.SERVER(HOST_ADDR,HOST_PORT3,100)

s4 = server()
s4.SERVER(HOST_ADDR,HOST_PORT4,100)

s5 = server()
s5.SERVER(HOST_ADDR,HOST_PORT5,100)

