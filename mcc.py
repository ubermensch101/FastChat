from client_class import *
import threading

HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080


def abc(data,con):
    global g
    # print("infunc")
    # x=True
    print(f"{data['sender_name']} => {data['data']}")
    if data["sender_name"]=="SERVER" and (data["data"]=="user exist" or data["data"]=="Wrong Password" or data["data"]=="Username doesn't exist"):
        
        c.SEND("test","exit")
        c.CLOSE()
        return
    else:
        print("here")
        g=True

    con.SEND("test","Hello!")

def client_msg(data):
    print(f"{data['sender_name']} => {data['data']}")

g=False
x=False
i=0
while True:
    # print("i= ",i)
    type=input("type: ")
    usrname=input("u: ")
    pswd=input("pswd: ")

    c=client(usrname)
    c.CLIENT(HOST_ADDR,HOST_PORT)
    c.CREATE_CHANNEL("test")
    msg={
        "type":type,
        "username": usrname,
        "password": pswd,
        "data" : ""
        }
        
    c.SEND("test",msg)
    
    print("hello")
    while not x: x=c.LISTEN( channel = "test", function = abc, args = (c,) )
    time.sleep(0.5)
    print("bye")
    if g: break

print("entered")

def clmsg(z):
    while(True):
        z.LISTEN(channel="DSP_MSG",function=client_msg)

def mymsg(m):
    z=False
    while(not z):
        p=input("msg: ")
        if(p=="exit"):
            m.SEND("test",p)
            m.CLOSE()
            z=True
        else:
            s=p.split(",")
            print("s: ",s)
            m.SEND_TO_CLIENT(target_name=s[0],data=s[1])

t1=threading.Thread(target=clmsg,args=(c,))
t2=threading.Thread(target=mymsg,args=(c,))

t1.setDaemon(True)
t2.setDaemon(True)

t1.start()
t2.start()