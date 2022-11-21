import sqlite3
import json


conn=sqlite3.connect("user_data.db")
cursor=conn.cursor()

class User_Table:

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
        add_cmd+="\", 0);"
        cursor.execute(add_cmd)
        conn.commit()
        return
    
    def set_online(user_ID):
        cursor.execute("UPDATE Users SET Online = 1 WHERE UserID = \""+str(user_ID)+"\";")
        conn.commit()
        return
    
    def set_offline(user_ID):
        cursor.execute("UPDATE Users SET Online = 0 WHERE UserID = \""+str(user_ID)+"\";")
        conn.commit()
        return
    
    def check_user_existence(user_ID):
        cursor.execute("SELECT UserID FROM Users WHERE UserID = \""+str(user_ID)+"\";")
        output_check=cursor.fetchall()
        if len(output_check)>0:
            return True
        else:
            return False

class Group_Table:

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
        user_list=Group_Table.get_user_list(group_ID)
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

        if(Group_Table.check_admin(user_ID)):
            return
        
        user_list=Group_Table.get_user_list(group_ID)
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

    def check_group_existence(group_ID):
        check_cmd="SELECT GroupID FROM Groups WHERE GroupID = \""+str(group_ID)
        cursor.execute(check_cmd)
        output_check=cursor.fetchall()

        if len(output_check)>0:
            return True
        else:
            return False

    def check_user_existence(group_ID,user_ID):
        check_cmd="SELECT userIDList FROM Groups WHERE GroupID = \""+str(group_ID)+"\";"
        cursor.execute(check_cmd)
        output_check=cursor.fetchall()
        user_list=json.loads(output_check)
        if user_ID in user_list:
            return True
        else:
            return False

class Undelivered_Messages_Table:

    # Figure out a way to get a unique iD for message

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
        );'''
        cursor.execute(create_cmd)
        conn.commit()
        return

    def get_all_undelivered_messages():
        all_cmd="SELECT * FROM Undelivered"
        cursor.execute(all_cmd)
        conn.commit()
        return

    def add_undelivered_pair(sender_ID, receiver_ID, receiver_or_group, group_ID, text_or_image, text, image):
        add_cmd="INSERT INTO Undelivered (SenderID, ReceiverID, Receiver_Group, GroupID, Text_Image, Text, Image) VALUES (\""
        add_cmd+=str(sender_ID)+"\", \""
        add_cmd+=str(receiver_ID)+"\", \""
        add_cmd+=str(receiver_or_group)+"\", \""
        add_cmd+=str(group_ID)+"\", \""
        add_cmd+=str(text_or_image)+"\", \""
        add_cmd+=str(text)+"\", \""
        add_cmd+=str(image)+"\");"

        cursor.execute(add_cmd)
        conn.commit()
        return

    def remove_undelivered_pair(sender_ID, receiver_ID, text, image):
        delete_cmd="DELTE FROM Undelivered WHERE SenderID = \""
        delete_cmd+=str(sender_ID)
        delete_cmd+="\" AND ReceiverID = \""+str(receiver_ID)
        delete_cmd+="\" AND Text = \""+str(text)
        delete_cmd+="\" AND Image = \""+str(image)
        delete_cmd+="\";"

        cursor.execute(delete_cmd)
        conn.commit()
        return

    def retrieve_receiver_messages(receiver_ID):
        retrieve_cmd="SELECT * FROM Undelivered WHERE ReceiverID = \""
        retrieve_cmd+=str(receiver_ID)+"\";"
        cursor.execute(retrieve_cmd)
        output_retrieve=cursor.fetchall()
        return output_retrieve
