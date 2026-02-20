import uuid
import random

class CBotPlayer:
    def __init__(self, guid, ghost_p, window_width, window_height):
        self.guid = guid
        self.ghost = ghost_p
        self.frame_counter = 0
        self.direction = random.randint(0, 3)
        self.window_width = window_width
        self.window_height = window_height

    def play(self, root_p):
        self.frame_counter += 1
        if self.frame_counter % 30 == 0:
            self.direction = random.randint(0, 3)  # pick new direction
        if self.direction == 0:  # up
            self.ghost.p_y -= 3
        elif self.direction == 1:  # down
            self.ghost.p_y += 3
        elif self.direction == 2:  # left
            self.ghost.p_x -= 3
        elif self.direction == 3:  # right
            self.ghost.p_x += 3
        self.ghost.p_x = max(0, min(self.ghost.p_x, self.window_width - self.ghost.p_w))
        self.ghost.p_y = max(0, min(self.ghost.p_y, self.window_height - self.ghost.p_h))
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
    