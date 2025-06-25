import socket			 
import sys
sys.path.append("C:\\Users\\alexf\\OneDrive\\Desktop\\1014")
from CMessage import CMessage
import time

class socket_serv:   
    def connect(self):
        # first of all import the socket library 

        # next create a socket object 
        self.s = socket.socket()		 
        print ("Socket successfully created")

        # reserve a port on your computer in our 
        # case it is 12345 but it can be anything 
        port = 1002			

        # Next bind to the port 
        # we have not typed any ip in the ip field 
        # instead we have inputted an empty string 
        # this makes the server listen to requests 
        # coming from other computers on the network 
        self.s.bind(('', port))		 
        print ("socket binded to port {:d}".format(port)) 

        # put the socket into listening mode 
        self.s.listen(5)	 
        print ("socket is listening")		 
    
    def send(self, msg_p, c_p):
        msg_obj_l = CMessage() 
        enc_msg_l = msg_obj_l.encrypt_string(msg_p)
        # send a thank you message to the client. encoding to send byte type.
        print("sending message-----------------") 
        c_p.send(enc_msg_l.encode())
        # Close the connection with the client 
    
    def accept(self):
        c_l, addr_l = self.s.accept()	 
        return c_l, addr_l

serv_obj_ptr_l = socket_serv()
serv_obj_ptr_l.connect()
print("waiting to accept connection")		 
c_l, addr_l = serv_obj_ptr_l.accept()	 
file_msg_l = open("msg_file.txt", "r")
lines_l = file_msg_l.readlines()
for line_l in lines_l:
    print("------------------line_l UNENCRYPTED TO BE SENT = {} type = {}-----------------".format(line_l, type(line_l)))
    input("press any key to continue: ")
    serv_obj_ptr_l.send(line_l, c_l)
c_l.close()

