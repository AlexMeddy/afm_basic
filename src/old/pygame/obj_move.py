import pygame
pygame.init()

screen = pygame.display.set_mode((500,500)) 
pygame.display.set_caption('moving object') 
x = 100
y = 100 
speed = 3  
width = 50
height = 50
while True:
    pygame.time.delay(10)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill('black')
    key  = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and x>0:
        x -= speed
    if key[pygame.K_RIGHT] and x<500-width:
        x += speed
    if key[pygame.K_UP] and y>0:
        y -= speed
    if key[pygame.K_DOWN] and y<500-height:
        y += speed
    pygame.draw.rect(screen, 'dark green',(x,y,width, height))
    pygame.display.update()
