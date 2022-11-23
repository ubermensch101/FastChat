The Technology and The Functionality:

-Created a database shared with all servers, composed of User, Group and Undelivered Messages tables.
-Abstracted each table as an object, with many member functions to obtain data in specified formats.
-Created a server class that serves an interface between the client and the database.
-Used multi-threading to run loops for sending, receiving and database handling, using class attributes to interface between the threads via lists and queues.
-Acquired and released locks for server interactions with database, to ensure two separate threads don't try to access the database at the same time.
-Added functionality for signing up, logging in, sending texts, sending text-like images, creating groups, adding members to groups, removing members from group, sending texts to groups and sending text-like images to groups.
-Formatted messages into dictionaries, handling these messages further dependent on message types, and transferring them after converting them to JSON format and encoding them via pickle.
-Created a list of online users on server side, devoting a thread to loop through undelivered messages and send them to users when they come online.
-Created a terminal-based front end that interacts with the client class appropriately.

How to run it:

-Run main_server.py to boot up the server
-Create clients by running main.py from as many terminals as we need clients.
-Follow front-end as a client to sign up, log in, send texts, create groups and so on.

Yet to be done:
-Encryption
-Handling images
-Load balancing techniques

Team member's contributions:
Aaryan- Database, Client class, Debugging
Hruday- Server class, Multi-threading, Debugging
Kesava- Front-end, Encryption, Debugging
