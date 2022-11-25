FastChat is an easy-to-use terminal-based message service that allows you to exchange text messages between fellow users, create groups, add and remove members from groups as an admin, and share images with friends. Messages you type up are end-to-end encrypted, and hence your communication is always secure.

The features included are:

- Sending a text to a friend
- Sending an image to a friend
- Creating a group
- Logging in to a group as an admin
- Adding members to a group as an admin
- Removing members of a group as an admin
- Send a text to a group
- Sending an image to a group

To test-run the code, follow these steps:

1. From the "fastchat" directory, locate to the database directory using "cd database" and initialise the database by running the command "python3 initialise_database.py".
2. Go back to the "fastchat" directory, and run the commands "cd server", "chmod u+x run_servers.sh" and "./run_servers.sh" to boot up the servers (5 in total).
3. Now go to the "clients" folder using "cd clients" from the "fastchat" directory, and type in the commands "chmod u+x run_clients.sh" and "./run_clients.sh" to test run the clients. To see the output on the terminal, run instead "./run_clients_terminal.sh". Alternatively, you can run as many clients as needed by typing in "python3 main_clients.py" into as many different terminals from the "clients" directory.
4. If you use the bash file for testing, look at clients/test_clients/test_output.txt (relative to the "fastchat" folder) for the redirected output from running main_client.py. Otherwise, follow the instructions displayed on the terminal to sign up/log in and send/receive messages from other clients.
5. To look at the images sent, check out the clients/images directory. The images are formatted as "senderID_receiverID_randint.png".
6. Finally, to shut everything down, run "chmod u+x kill_servers.sh" followed by "./kill_servers.sh" to kill the servers, and then close the bash/client terminals.

The process flow:

- Created a database shared by all servers, composed of the tables User, Group and Undelivered Messages.
- Abstracted each table as an object, with member functions to obtain data in specific formats.
- Created a server class that serves an interface between the client and the database.
- Used multi-threading to run loops for sending, receiving and database handling, using class attributes to interface between the threads via lists and queues.
- Acquired and released locks for server interactions with database, to ensure two separate threads don't try to access the database at the same time.
- Added functionality for signing up, logging in, sending texts, sending text-like images, creating groups, adding members to groups, removing members from group, sending texts to groups and sending text-like images to groups.
- Formatted messages into dictionaries, handling these messages further dependent on message types, and transferring them after converting them to JSON format and encoding them via pickle.
- Encrypted the text message/image bytes using the library cryptograpy with a pre-generated key, decrypting it upon arrival to intended client
- Added randomised load-balancing to prevent too much stress on any one server
- Created a list of online users on server side, devoting a thread to loop through undelivered messages and send them to users when they come online.
- Created a terminal-based front end that interfaces between the user and the client class. It's got red dashed lines.

Schema of Database:

        TABLE NAME: Users
        FIELD NAME   FIELD TYPE
        UserID          TEXT (PRIMARY KEY)
        Password        TEXT
        Online          INT
        
        TABLE NAME: Groups
        FIELD NAME   FIELD TYPE 
        GroupID         TEXT (PRIMARY KEY)
        AdminID         TEXT (FOREIGN KEY from Users.UserID)
        UserIDList      TEXT

        TABLE NAME: Undelivered
        FIELD NAME    FIELD TYPE
        SenderID        TEXT (FOREIGN KEY from Users.UserID)
        ReceiverID      TEXT (FOREIGN KEY from Users.UserID)
        Receiver_Group  TEXT 
        GroupID         TEXT (FOREIGN KEY from Groups.GroupID)
        Text_Image      TEXT
        Text            TEXT
        Image           TEXT
        UnsentIDList    TEXT
        
        
        
        
        
        
  
