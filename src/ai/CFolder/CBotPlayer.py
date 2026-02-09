import uuid
import random

class CBotPlayer:
    def __init__(self, guid, ghost_p):
        self.guid = guid
        self.ghost = ghost_p

    def play(self):
        direction = random.randint(0, 3)
        if direction == 0: #up
            self.ghost.p_y -=2
        elif direction == 1: #down
            self.ghost.p_y +=2
        elif direction == 2: #left
            self.ghost.p_x -=2
        elif direction == 3: #right
            self.ghost.p_x +=2
            
    #check if colliding, move from ctv
    
    #delete, new from ctv
            
        


if __name__ == "__main__":
    bot = CBotPlayer()
    bot.play(None)
    