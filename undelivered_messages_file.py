import sqlite3

conn=sqlite3.connect("user_data.db")
cursor=conn.cursor()

# Figure out a way to get a unique iD for message

def create_undelivered_table():
    drop_cmd="DROP TABLE IF EXISTS Undelivered"
    cursor.execute(drop_cmd)

    create_cmd='''CREATE TABLE Undelivered
    (SenderID TEXT,
    ReceiverID TEXT,
    Sender/Group TEXT,
    GroupID TEXT,
    Text/Image TEXT,
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

def add_undelivered_pair(sender_ID, receiver_ID, sender_or_group, group_ID, text_or_image, text, image):
    add_cmd="INSERT INTO Undelivered (SenderID, ReceiverID, Sender/Group, GroupID, Text/Image, Text, Image) VALUES (\""
    add_cmd+=str(sender_ID)+"\", \""
    add_cmd+=str(receiver_ID)+"\", \""
    add_cmd+=str(sender_or_group)+"\", \""
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

