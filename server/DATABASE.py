import sqlite3
import json
import threading

global lock

conn=sqlite3.connect("../database/user_data.db",check_same_thread=False)
cursor=conn.cursor()
lock = threading.Lock()


class User_Table:

    # 0 - Offline, 1 - Online
    def create_users_table():
        lock.acquire(True)
        drop_cmd="DROP TABLE IF EXISTS Users"
        cursor.execute(drop_cmd)

        create_cmd='''CREATE TABLE Users
        (UserID TEXT PRIMARY KEY,
        Password TEXT,
        Online INT
        );'''
        
        cursor.execute(create_cmd)
        conn.commit()
        lock.release()
        return

    def check_user_password(user_ID, user_password):
        lock.acquire(True)
        check_cmd="SELECT UserID FROM Users WHERE UserID = \""+str(user_ID)
        check_cmd+="\" AND Password = \""+str(user_password)+"\";"
        cursor.execute(check_cmd)
        output_check=cursor.fetchall()
        lock.release()
        if len(output_check)>0:
            return True
        else:
            return False

    def check_online(user_ID):
        lock.acquire(True)
        online_cmd="SELECT Online FROM Users WHERE UserID = \""+str(user_ID)+"\";"
        cursor.execute(online_cmd)
        output_online=cursor.fetchone()[0]
        lock.release()
        if output_online==1:
            return True
        else:
            return False

    def add_user(user_ID, user_password):
        add_cmd="INSERT INTO Users (UserID, Password, Online) VALUES (\""
        add_cmd+=str(user_ID)
        add_cmd+="\", \""+str(user_password)
        add_cmd+="\", 0);"
        lock.acquire(True)
        cursor.execute(add_cmd)
        conn.commit()
        lock.release()
        return
    
    def set_online(user_ID):
        lock.acquire(True)
        cursor.execute("UPDATE Users SET Online = 1 WHERE UserID = \""+str(user_ID)+"\";")
        conn.commit()
        lock.release()
        return
    
    def set_offline(user_ID):
        lock.acquire(True)
        cursor.execute("UPDATE Users SET Online = 0 WHERE UserID = \""+str(user_ID)+"\";")
        conn.commit()
        lock.release()
        return
    
    def check_user_existence(user_ID):
        lock.acquire(True)
        cursor.execute("SELECT UserID FROM Users WHERE UserID = \""+str(user_ID)+"\";")
        output_check=cursor.fetchall()
        lock.release()
        if len(output_check)>0:
            return True
        else:
            return False

class Group_Table:

    def create_groups_table():
        lock.acquire()
        drop_cmd="DROP TABLE IF EXISTS Groups"
        cursor.execute(drop_cmd)

        create_cmd='''CREATE TABLE Groups
        (GroupID TEXT PRIMARY KEY,
        AdminID TEXT,
        UserIDList TEXT
        );'''
        cursor.execute(create_cmd)
        conn.commit()
        lock.release()
        return

    def check_admin(group_ID, admin_ID):
        lock.acquire(True)
        check_cmd="SELECT GroupID FROM Groups WHERE GroupID = \""+str(group_ID)
        check_cmd+="\" AND AdminID = \""+str(admin_ID)+"\";"
        cursor.execute(check_cmd)
        output_check=cursor.fetchall()
        lock.release()
        if len(output_check)>0:
            return True
        else:
            return False

    def get_user_list(group_ID):
        lock.acquire(True)
        user_list_cmd="SELECT UserIDList FROM Groups WHERE GroupID = \""+str(group_ID)+"\";"
        cursor.execute(user_list_cmd)
        output_user_list=cursor.fetchall()
        lock.release()
        if len(output_user_list)==0:
            return []
        else:
            user_list_json=output_user_list[0][0]
            user_list_json=user_list_json.replace("'", "\"")
            user_list=json.loads(user_list_json)
            return user_list
    
    def get_user_list_database(group_ID):
        user_list_cmd="SELECT UserIDList FROM Groups WHERE GroupID = \""+str(group_ID)+"\";"
        cursor.execute(user_list_cmd)
        output_user_list=cursor.fetchall()
        if len(output_user_list)==0:
            return []
        else:
            user_list_json=output_user_list[0][0]
            user_list_json=user_list_json.replace("'", "\"")
            user_list=json.loads(user_list_json)
            return user_list

    def create_group(group_ID, admin_ID):
        lock.acquire(True)
        user_list_json=json.dumps([admin_ID])
        user_list_json=user_list_json.replace("\"","'")
        create_cmd="INSERT INTO Groups (GroupID, AdminID, UserIDList) VALUES (\""
        create_cmd+=str(group_ID)
        create_cmd+="\", \""+str(admin_ID)
        create_cmd+="\", \""+str(user_list_json)+"\");"

        cursor.execute(create_cmd)
        conn.commit()
        lock.release()
        return

    def add_to_group(group_ID, user_ID):
        lock.acquire(True)
        user_list=Group_Table.get_user_list_database(group_ID)
        
        if user_ID not in user_list:
            user_list.append(user_ID)
        user_list_json=json.dumps(user_list)
        user_list_json=user_list_json.replace("\"","'")
        user_list_cmd="UPDATE Groups "
        user_list_cmd+="SET UserIDList = \""+str(user_list_json)
        user_list_cmd+="\" WHERE GroupID = \""+str(group_ID)
        user_list_cmd+="\";"

        cursor.execute(user_list_cmd)
        conn.commit()
        lock.release()

        return

    def remove_from_group(group_ID, user_ID):
        lock.acquire(True)

        check_cmd="SELECT GroupID FROM Groups WHERE GroupID = \""+str(group_ID)
        check_cmd+="\" AND AdminID = \""+str(user_ID)+"\";"
        cursor.execute(check_cmd)
        output_check=cursor.fetchall()

        if len(output_check)>0:
            lock.release()
            return
        
        user_list=Group_Table.get_user_list_database(group_ID)
        if user_ID in user_list:
            user_list.remove(user_ID)
        user_list_json=json.dumps(user_list)
        user_list_json=user_list_json.replace("\"","'")
        user_list_cmd="UPDATE Groups "
        user_list_cmd+="SET UserIDList = \""+str(user_list_json)
        user_list_cmd+="\" WHERE GroupID = \""+str(group_ID)
        user_list_cmd+="\";"

        cursor.execute(user_list_cmd)
        conn.commit()
        lock.release()
        return

    def check_group_existence(group_ID):
        lock.acquire(True)
        check_cmd="SELECT GroupID FROM Groups WHERE GroupID = \""+str(group_ID)+"\";"
        cursor.execute(check_cmd)
        output_check=cursor.fetchall()
        lock.release()
        if len(output_check)>0:
            return True
        else:
            return False

    def check_user_existence(group_ID,user_ID):
        lock.acquire(True)
        check_cmd="SELECT UserIDList FROM Groups WHERE GroupID = \""+str(group_ID)+"\";"
        cursor.execute(check_cmd)
        output_check=cursor.fetchall()
        lock.release()
        if len(output_check) > 0:
            output_check=output_check[0][0]
            output_check=output_check.replace("'", "\"")
            user_list=json.loads(output_check)
        else:
            user_list=[]

        if user_ID in user_list:
            return True
        else:
            return False

class Undelivered_Messages_Table:

    # Figure out a way to get a unique iD for message

    def create_undelivered_table():
        lock.acquire()
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
        lock.release()
        return

    def get_all_undelivered_messages():
        lock.acquire()
        all_cmd="SELECT * FROM Undelivered"
        cursor=conn.cursor()
        msg_list=cursor.execute(all_cmd)
        conn.commit()
        lock.release()
        return msg_list

    def add_undelivered_pair(sender_ID, receiver_ID, receiver_or_group, group_ID, text_or_image, text, image,unsent_id_list):
        lock.acquire(True)
        text=text.replace("\"","'")
        image=image.replace("\"", "'")
        unsent_id_list=unsent_id_list.replace("\"","'")
        add_cmd="INSERT INTO Undelivered (SenderID, ReceiverID, Receiver_Group, GroupID, Text_Image, Text, Image, UnsentIDList) VALUES (\""
        add_cmd+=str(sender_ID)+"\", \""
        add_cmd+=str(receiver_ID)+"\", \""
        add_cmd+=str(receiver_or_group)+"\", \""
        add_cmd+=str(group_ID)+"\", \""
        add_cmd+=str(text_or_image)+"\", \""
        add_cmd+=text+"\", \""
        add_cmd+=str(image)+"\", \""
        add_cmd+=str(unsent_id_list)+"\");"


        cursor.execute(add_cmd)
        conn.commit()
        lock.release()
        return

    def remove_undelivered_pair(sender_ID, receiver_ID, text, image):
        lock.acquire(True)
        delete_cmd="DELETE FROM Undelivered WHERE SenderID = \""
        delete_cmd+=str(sender_ID)
        delete_cmd+="\" AND ReceiverID = \""+str(receiver_ID)
        delete_cmd+="\" AND Text = \""+str(text)
        delete_cmd+="\" AND Image = \""+str(image)
        delete_cmd+="\";"

        cursor.execute(delete_cmd)
        conn.commit()
        lock.release()
        return
    
    def remove_undelivered_pair_from_database(sender_ID, receiver_ID, text, image):
        delete_cmd="DELETE FROM Undelivered WHERE SenderID = \""
        delete_cmd+=str(sender_ID)
        delete_cmd+="\" AND ReceiverID = \""+str(receiver_ID)
        delete_cmd+="\" AND Text = \""+str(text)
        delete_cmd+="\" AND Image = \""+str(image)
        delete_cmd+="\";"

        cursor.execute(delete_cmd)
        conn.commit()
        return

    def retrieve_receiver_messages(receiver_ID):
        lock.acquire(True)
        retrieve_cmd="SELECT * FROM Undelivered WHERE ReceiverID = \""
        retrieve_cmd+=str(receiver_ID)+"\";"
        cursor.execute(retrieve_cmd)
        output_retrieve=cursor.fetchall()
        lock.release()
        return output_retrieve
    
    def get_unsent_id_list(group_ID, sender_ID, text, image):
        lock.acquire(True)
        text=text.replace("\"","'")
        image=image.replace("\"", "'")
        
        user_list_cmd="SELECT UnsentIDList FROM Undelivered WHERE GroupID = \""+str(group_ID)+"\" AND "
        user_list_cmd+="Text = \""+str(text)+"\" AND "
        user_list_cmd+="Image = \""+str(image)+"\" AND "
        user_list_cmd+="SenderID = \""+str(sender_ID)+"\" ;"

        cursor.execute(user_list_cmd)

        k=cursor.fetchall()
        if len(k)>0:
            output_user_list_json=k[0][0]
            output_user_list_json=output_user_list_json.replace("'", "\"")
            output_user_list=json.loads(output_user_list_json)
        else:
            output_user_list=[]

        lock.release()

        return output_user_list

    def remove_unsent_id(group_ID,sender_ID,receiver_ID,removing_ID,text,image):
        lock.acquire(True)
        text=text.replace("\"","'")
        image=image.replace("\"", "'")
        
        user_list_cmd="SELECT UnsentIDList FROM Undelivered WHERE GroupID = \""+str(group_ID)+"\" AND "
        user_list_cmd+="Text = \""+str(text)+"\" AND "
        user_list_cmd+="Image = \""+str(image)+"\" AND "
        user_list_cmd+="SenderID = \""+str(sender_ID)+"\" ;"
        cursor.execute(user_list_cmd)
        output_user_list=cursor.fetchall()[0][0]

        output_user_list=output_user_list.replace("'","\"")
        output_user_list=json.loads(output_user_list)

        if removing_ID in output_user_list:
            output_user_list.remove(removing_ID)

        if len(output_user_list) > 0 :
            user_list_json=json.dumps(output_user_list)
            user_list_json=user_list_json.replace("\"","'")
            new_user_list_json_cmd="UPDATE Undelivered SET UnsentIDList = \""+str(user_list_json)+"\" "
            new_user_list_json_cmd+="WHERE GroupID = \""+str(group_ID)+"\" AND "
            new_user_list_json_cmd+="SenderID = \""+str(sender_ID)+"\" AND "
            new_user_list_json_cmd+="Text = \""+str(text)+"\" ;"
            cursor.execute(new_user_list_json_cmd)
            conn.commit()
        else:
            Undelivered_Messages_Table.remove_undelivered_pair_from_database(sender_ID,receiver_ID,text,image)
        lock.release()
        return
