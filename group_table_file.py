import sqlite3
import json

conn=sqlite3.connect("user_data.db")
cursor=conn.cursor()

def create_groups_table():
    drop_cmd="DROP TABLE IF EXISTS Groups"
    cursor.execute(drop_cmd)

    create_cmd='''CREATE TABLE Groups
    (GroupID TEXT PRIMARY KEY,
    AdminID TEXT,
    UserIDList TEXT,
    );'''
    cursor.execute(create_cmd)
    conn.commit()
    return

def check_admin(group_ID, admin_ID):
    check_cmd="SELECT GroupID FROM Groups WHERE GroupID = \""+str(group_ID)
    check_cmd+="\" AND AdminID = \""+str(admin_ID)+"\";"
    cursor.execute(check_cmd)
    output_check=cursor.fetchall()

    if len(output_check)>0:
        return True
    else:
        return False

def get_user_list(group_ID):
    user_list_cmd="SELECT UserIDList FROM Groups WHERE GroupID = \""+str(group_ID)+"\";"
    cursor.execute(user_list_cmd)
    output_user_list=cursor.fetchall()

    if len(output_user_list)==0:
        return []
    else:
        user_list_json=output_user_list[0]
        user_list=json.loads(user_list_json)
        return user_list

def create_group(group_ID, admin_ID):
    user_list_json=json.dumps([admin_ID])

    create_cmd="INSERT INTO Groups (GroupID, AdminID, UserIDList) VALUES (\""
    create_cmd+=str(group_ID)
    create_cmd+="\", \""+str(admin_ID)
    create_cmd+="\", \""+str(user_list_json)+"\");"

    cursor.execute(create_cmd)
    conn.commit()
    return

def add_to_group(group_ID, user_ID):
    user_list=get_user_list(group_ID)
    if user_ID not in user_list:
        user_list.append(user_ID)
    user_list_json=json.dumps(user_list)

    user_list_cmd="UPDATE GroupID "
    user_list_cmd+="SET UserIDList = \""+str(user_list_json)
    user_list_cmd+="\" WHERE GroupID = \""+str(group_ID)
    user_list_cmd+="\";"

    cursor.execute(user_list_cmd)
    conn.commit()

    return

def remove_from_group(group_ID, user_ID):

    if(check_admin(user_ID)):
        return
    
    user_list=get_user_list(group_ID)
    if user_ID in user_list:
        user_list.remove(user_ID)
    user_list_json=json.dumps(user_list)

    user_list_cmd="UPDATE GroupID "
    user_list_cmd+="SET UserIDList = \""+str(user_list_json)
    user_list_cmd+="\" WHERE GroupID = \""+str(group_ID)
    user_list_cmd+="\";"

    cursor.execute(user_list_cmd)
    conn.commit()
    return




