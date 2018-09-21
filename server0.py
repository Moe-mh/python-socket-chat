import socket
import threading
import sqlite3
import datetime
from queue import Queue
q1=Queue()
q2=Queue()

lock=threading.Lock()


def send_handling(c, addr, socks):
    while True:
        try:
            raw_msg=input()
            if raw_msg:
                msg="server : "+raw_msg
                
                for x in (socks):
                    if not x._closed :
                        x.send(msg.encode('utf-8'))
                    else:
                        print(addr[1],": disconnected")
                        socks.remove(x)

        except(ConnectionError, BrokenPipeError):
            print('sending exception happened!!')
            break
            

def broadcast( socks):

    while True:
        try:
            #locking the thread
            with lock:
                
                #messege that needs to be broadcast
                msg=q1.get()     
                
                #the client that had sent the messege
                c=q2.get()
                
                if msg:
                    for x in(socks):
                        if x!=c and not x._closed:
                            x.send(msg.encode('utf-8'))
                else:
                    if c._closed:
                        print(addr[1], " disconnected")
        except:


            c.close()
            break


def recieve(sock, addr, socks):

    while True:
        try:
    
            if not sock._closed :

                    msg=sock.recv(BUFSIZ)
                    if msg and msg!='q':
                        msg=msg.decode('utf-8')
                        print(addr, ":", msg)
                        msg=str(addr[1])+":"+msg
                        
            #Queue for broadcasting messege to all clients
                        q1.put(msg)       
                        
            #Queue for the client
                        q2.put(sock)
                    else:
                        print(addr[1],"disconnected")
                        sock.close()

                        break

            else:
                sock.close()
                socks.remove(sock)
    
    #                       break
        except:
            print('recieving exception occured')
            sock.close()
            break

    
#threading function for sending , recieving and broadcasting
 
def thread(c, addr,socks): 
    
    send_thread=threading.Thread(target=send_handling, args=[ c, addr, socks], daemon=True)

    
    recv_thread=threading.Thread(target=recieve, args=[c, addr, socks], daemon=True)

    broadcastin=threading.Thread(target=broadcast, args=[socks], daemon=True)
    send_thread.start()
    recv_thread.start()
    broadcastin.start()
    
    



if __name__ == '__main__':
    HOST ='127.0.0.1'
    PORT =1234
    PORT=int(PORT)
    BUFSIZ=4096
    ADDR =(HOST, PORT)
    
    #using Tcp protocol in sockets connection
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    date=datetime.datetime.now()
    #bind the address to the socket
    s.bind(ADDR)
    
    #DATABASE
    conndb=sqlite3.connect('/home/moe/Documents/chatdb')
    db=conndb.cursor()

    
    #listening for new connectoins
    s.listen(5)
    socks=[]
    
    print("waiting for connections")

    while True:  #accepting as many as it can
        try:
            c, addr=s.accept()

	    #connecting to database

            db.execute("INSERT INTO CLIENT (port, datestamp) VALUES (?,?)" , (addr[1], str(date)))
            db.execute("INSERT INTO CONNECTIONS (S_port,C_port, datestamp) VALUES (?,?,?)" , (HOST, addr[1], str(date)))
            conndb.commit()
		##################
            print("now connected to :", addr)
            socks.append(c)
            if c._closed:
                print(addr[1], " disconnected")
            
            thread(c, addr, socks)
            

            

        except(ConnectionError, BrokenPipeError):
            print('connection broke')
            conndb.close()
            db.close()
            c.close()
            s.close()
            break
     
    conndb.close()
    db.close()
    s.close()





