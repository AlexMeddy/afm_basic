import socket			 
import sys
sys.path.append("C:\\Users\\alexf\\OneDrive\\Desktop\\1014")
from security import encrypt_string

class socket_serv:
    def connect(self):
        # first of all import the socket library 

        # next create a socket object 
        self.s = socket.socket()		 
        print ("Socket successfully created")

        # reserve a port on your computer in our 
        # case it is 12345 but it can be anything 
        port = 1001			

        # Next bind to the port 
        # we have not typed any ip in the ip field 
        # instead we have inputted an empty string 
        # this makes the server listen to requests 
        # coming from other computers on the network 
        self.s.bind(('', port))		 
        print ("socket binded to %s" %(port)) 

        # put the socket into listening mode 
        self.s.listen(5)	 
        print ("socket is listening")		 
    
    def send(self):
        # a forever loop until we interrupt it or 
        # an error occurs 
        while True: 

        # Establish connection with client. 
            print("waiting to accept connection")		 
            c, addr = self.s.accept()	 
            print ('Got connection from', addr )
            while 1:
                msg_l = input("enter a msg to be sent to client: ")
                enc_msg_l = encrypt_string(msg_l)
                # send a thank you message to the client. encoding to send byte type.
                print("sending message-----------------")            
                c.send(enc_msg_l.encode())             
            
            # Close the connection with the client 
            c.close()

            # Breaking once connection closed
            break

print("before socket_serv")    
serv_obj_ptr_l = socket_serv()
print("after socket_serv")    
serv_obj_ptr_l.connect()
serv_obj_ptr_l.send()
