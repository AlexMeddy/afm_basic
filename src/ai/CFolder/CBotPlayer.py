import uuid
import random

class CBotPlayer:
    def __init__(self, guid, ghost_p):
        self.guid = guid
        self.ghost = ghost_p

    def play(self, root_p):
        direction = random.randint(0, 3)
        if direction == 0: #up
            self.ghost.p_y -=3
        elif direction == 1: #down
            self.ghost.p_y +=3
        elif direction == 2: #left
            self.ghost.p_x -=3
        elif direction == 3: #right
            self.ghost.p_x +=3            
        centre_x = self.ghost.p_x + self.ghost.p_w / 2
        centre_y = self.ghost.p_y + self.ghost.p_h / 2
        colliding_node = self.find_by_single_point_tree(root_p, centre_x, centre_y, self.ghost.guid)
        return colliding_node
            
    def find_by_single_point_tree(self, node_p, pointer_x, pointer_y, filter_p=""):
        result = None
        if pointer_x >= node_p.p_x and pointer_x <= (node_p.p_x + node_p.p_w) and pointer_y >= node_p.p_y and pointer_y <= (node_p.p_y + node_p.p_h) and node_p.guid != filter_p:#found
            result = node_p
        else:  #keep going
            for child in node_p.children_list:
                result = child.find_by_single_point_tree(pointer_x, pointer_y, filter_p)
                if result: #found
                    break
        return result
    
    #delete, new from ctv
            
        


if __name__ == "__main__":
    bot = CBotPlayer()
    bot.play(None)
    