import sqlite3

conn=sqlite3.connect("user_data.db")
cursor=conn.cursor()

# For speed, reduce commits and use lock

# 0 - Offline, 1 - Online
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

def check_user_password(user_ID, user_password):
    check_cmd="SELECT UserID FROM Users WHERE UserID = \""+str(user_ID)
    check_cmd+="\" AND Password = \""+str(user_password)+"\";"
    cursor.execute(check_cmd)
    output_check=cursor.fetchall()

    if len(output_check)>0:
        return True
    else:
        return False


def check_online(user_ID):
    online_cmd="SELECT Online FROM Users WHERE UserID = \""+str(user_ID)+"\";"
    cursor.execute(online_cmd)
    output_online=cursor.fetchone()[0]
    
    if output_online==1:
        return True
    else:
        return False

def add_user(user_ID, user_password):
    add_cmd="INSERT INTO Users (UserID, Password, Online) VALUES (\""
    add_cmd+=str(user_ID)
    add_cmd+="\", \""+str(user_password)
    add_cmd+="\", 1);"
    cursor.execute(add_cmd)
    conn.commit()
    return


