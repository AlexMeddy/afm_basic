import uuid
import random

class CBotPlayer:
    def __init__(self, guid: str = None):
        self.guid: str = guid if guid else str(uuid.uuid4())

    def play(self, root_p):
        direction = random.randint(0, 3)
        if direction == 0: #up
            root_p.p_y -=2
        elif direction == 1: #down
            root_p.p_y +=2
        elif direction == 2: #left
            root_p.p_x -=2
        elif direction == 3: #right
            root_p.p_x +=2


if __name__ == "__main__":
    bot = CBotPlayer()
    bot.play(None)
    