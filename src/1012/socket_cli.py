from CCharacter import CCharacter
from CHuffman import CHuffman
import socket			 

class socket_cli:
    def connect(self):
        # Import socket module 

        # Create a socket object 
        self.s = socket.socket()		 

        # Define the port on which you want to connect 
        port = 1001			

        # connect to the server on local computer 
        self.s.connect(('192.168.0.149', port)) 
        
        self.huffman_obj = CHuffman()
        self.huffman_obj.char_list = []
          
        
    def process_msg(self):       
        # receive data from the server and decoding to get the string.
        while True:
            print("before recv")
            msg_l = self.s.recv(1024).decode()
            print ("waiting for msg")		 
            print (msg_l)
            self.huffman_obj.calculate_char_frequency_of_a_string(msg_l)
            if msg_l == "quit":
                break
        
cli_obj_ptr_l = socket_cli()
cli_obj_ptr_l.connect()
cli_obj_ptr_l.process_msg()