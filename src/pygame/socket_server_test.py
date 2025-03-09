import socket             
import pygame

screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption('server window')

s = socket.socket()         
print ("Socket successfully created")
port = 12345               
s.bind(('', port))         
print ("socket binded to %s" %(port)) 
s.listen(5)     
print ("socket is listening")            
 
while True: 
    run = True
    while run:
        if pygame.mouse.get_pressed()[0] == True:
            c, addr = s.accept()     
            print ('Got connection from', addr )
            input_msg = input("enter a message to be sent to client: ")
            c.send(input_msg.encode()) 

            c.close()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    break