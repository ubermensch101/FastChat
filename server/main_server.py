from server_class import *
from DATABASE import User_Table, Group_Table, Undelivered_Messages_Table
import sqlite3,sys

import threading

global lock
lock=threading.Lock()

HOST_ADDR = "0.0.0.0"

if len(sys.argv)!=2:
    print("Give one argument for port number")
    exit()

s = server()
s.SERVER(HOST_ADDR, int(sys.argv[1]),100)
