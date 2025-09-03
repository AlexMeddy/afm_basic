import sys
from typing import List, Optional


class CPersonView:
    def __init__(self, guid: str, x: int, y: int, w: int, h: int, parent: 'CPersonView' = None):
        self.guid = guid
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent
        self.children_list: List[CPersonView] = []
        self.p_x = -1
        self.p_y = -1

    # ---------------- Mockup Calculation Methods ----------------
    def calc_p_x(self):
        # Placeholder calculation logic for p_x
        self.p_x = self.x + 5
        return self.p_x

    def calc_p_y(self):
        # Placeholder calculation logic for p_y
        self.p_y = self.y + 5
        return self.p_y

    # ---------------- Recursive Methods ----------------
    def print_tree(self, indent: int = 0):
        parent_id = self.parent.guid if self.parent else "None"
        print(" " * indent + f"GUID: {self.guid}, Parent: {parent_id}, Pos: ({self.x},{self.y}), Size: ({self.w}x{self.h})")
        for child in self.children_list:
            child.print_tree(indent + 4)

    def find_by_mouse_pos_tree(self, mouse_x: int, mouse_y: int) -> Optional['CPersonView']:
        # Check if mouse is inside this node's rect
        if self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h:
            return self
        for child in self.children_list:
            found = child.find_by_mouse_pos_tree(mouse_x, mouse_y)
            if found:
                return found
        return None

    def draw_tree(self, surface):
        import pygame
        # Draw rectangle for this node
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surface, (255, 0, 0), rect, 2)
        for child in self.children_list:
            child.draw_tree(surface)

    # ---------------- Instantiation from Flat File ----------------
    @staticmethod
    def instantiate_from_flat_file(filename: str) -> 'CPersonView':
        nodes = {}
        parent_map = {}

        with open(filename, "r") as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                guid, x, y, w, h, parent_guid = line.strip().split(",")
                x, y, w, h = int(x), int(y), int(w), int(h)
                node = CPersonView(guid, x, y, w, h)
                nodes[guid] = node
                parent_map[guid] = parent_guid if parent_guid != "None" else None

        root = None
        for guid, node in nodes.items():
            parent_guid = parent_map[guid]
            if parent_guid:
                node.parent = nodes[parent_guid]
                nodes[parent_guid].children_list.append(node)
            else:
                root = node

        return root
if __name__ == "__main__":
    # Sample usage
    root_obj = CPersonView.instantiate_from_flat_file("PersonView.txt")

    print("People Tree:")
    root_obj.print_tree()

