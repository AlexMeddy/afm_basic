import socket			 

class socket_serv:
    # first of all import the socket library 

    # next create a socket object 
    s = socket.socket()		 
    print ("Socket successfully created")

    # reserve a port on your computer in our 
    # case it is 12345 but it can be anything 
    port = 1001			

    # Next bind to the port 
    # we have not typed any ip in the ip field 
    # instead we have inputted an empty string 
    # this makes the server listen to requests 
    # coming from other computers on the network 
    s.bind(('', port))		 
    print ("socket binded to %s" %(port)) 

    # put the socket into listening mode 
    s.listen(5)	 
    print ("socket is listening")		 

    # a forever loop until we interrupt it or 
    # an error occurs 
    while True: 

    # Establish connection with client. 
        print("waiting to accept connection")		 
        c, addr = s.accept()	 
        print ('Got connection from', addr )
        while 1:
            msg = input("enter a msg to be sent to client: ")
            # send a thank you message to the client. encoding to send byte type. 
            c.send(msg.encode())             
        
        # Close the connection with the client 
        c.close()

        # Breaking once connection closed
        break
