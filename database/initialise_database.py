import sqlite3


def create_users_table():
    drop_cmd="DROP TABLE IF EXISTS Users"
    cursor.execute(drop_cmd)

    create_cmd='''CREATE TABLE Users
    (UserID TEXT PRIMARY KEY,
    Password TEXT,
    Online INT
    );'''
    
    cursor.execute(create_cmd)
    conn.commit()
    return

def create_groups_table():
    drop_cmd="DROP TABLE IF EXISTS Groups"
    cursor.execute(drop_cmd)

    create_cmd='''CREATE TABLE Groups
    (GroupID TEXT PRIMARY KEY,
    AdminID TEXT,
    UserIDList TEXT
    );'''
    cursor.execute(create_cmd)
    conn.commit()
    return

def create_undelivered_table():
    drop_cmd="DROP TABLE IF EXISTS Undelivered"
    cursor.execute(drop_cmd)

    create_cmd='''CREATE TABLE Undelivered
    (SenderID TEXT,
    ReceiverID TEXT,
    Receiver_Group TEXT,
    GroupID TEXT,
    Text_Image TEXT,
    Text TEXT,
    Image TEXT,
    UnsentIDList TEXT
    );'''
    cursor.execute(create_cmd)
    conn.commit()
    return

conn=sqlite3.connect("user_data.db",check_same_thread=False)
cursor=conn.cursor()

create_users_table()
create_groups_table()
create_undelivered_table()
