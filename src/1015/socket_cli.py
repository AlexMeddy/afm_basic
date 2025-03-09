import socket			 
import sys
sys.path.append("C:\\Users\\alexf\\OneDrive\\Desktop\\1014")
from security import decrypt_string			 

class socket_cli:
    def connect(self):
        # Import socket module 

        # Create a socket object 
        self.s = socket.socket()		 

        # Define the port on which you want to connect 
        port = 1001			

        # connect to the server on local computer 
        self.s.connect(('192.168.0.149', port)) 
        
          
        
    def process_msg(self):       
        # receive data from the server and decoding to get the string.
        while True:
            msg_l = self.s.recv(1024).decode()
            print ("receiving msg------------")		 
            un_enc_msg_l = decrypt_string(msg_l)
            print("un_enc_msg_l = {} type = {}".format(un_enc_msg_l, type(un_enc_msg_l)))
            if un_enc_msg_l == "quit":
                break
        
print("before socket_cli")
cli_obj_ptr_l = socket_cli()
print("after socket_cli")
cli_obj_ptr_l.connect()
cli_obj_ptr_l.process_msg()