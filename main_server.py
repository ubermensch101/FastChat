from server_class import *
from DATABASE import User_Table, Group_Table, Undelivered_Messages_Table
import sqlite3

HOST_ADDR = "0.0.0.0"
HOST_PORT = 8081
conn=sqlite3.connect("user_data.db",check_same_thread=False)
cursor=conn.cursor()

User_Table.create_users_table()
Group_Table.create_groups_table()
Undelivered_Messages_Table.create_undelivered_table()

s = server()
s.SERVER(HOST_ADDR,HOST_PORT,100)

