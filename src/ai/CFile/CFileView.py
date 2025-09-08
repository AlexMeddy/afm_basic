import pygame
import sys
from typing import List, Optional

# ------------------------ core class ------------------------
class CFileView:
    def __init__(self, guid: str, x: int, y: int, w: int, h: int, parent: Optional['CFileView'] = None):
        self.guid: str = guid
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.parent: Optional['CFileView'] = parent
        self.file_list: List['CFileView'] = []
        self.p_x: int = -1
        self.p_y: int = -1

    # ------------------------ methods ------------------------
    def print_tree(self, indent: int = 0):
        parent_id = self.parent.guid if self.parent else "None"
        print("  " * indent + f"GUID: {self.guid}, Parent: {parent_id}, Pos:({self.x},{self.y}), Size:({self.w},{self.h}))")
        for child in self.file_list:
            child.print_tree(indent + 1)

    def find_by_mouse_pos_tree(self, mx: int, my: int) -> Optional['CFileView']:
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            return self
        for child in self.file_list:
            found = child.find_by_mouse_pos_tree(mx, my)
            if found:
                return found
        return None

    def draw_tree(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.w, self.h), 2)
        font = pygame.font.SysFont(None, 20)
        text = font.render(self.guid, True, (255, 255, 255))
        surface.blit(text, (self.x + 5, self.y + 5))
        for child in self.file_list:
            child.draw_tree(surface)

    # ------------------------ instantiation ------------------------
    @classmethod
    def instantiate_from_flat_file(cls, filename: str) -> List['CFileView']:
        objects = {}
        root = None
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 6:
                    continue
                guid, parent_guid, x, y, w, h = parts
                x, y, w, h = int(x), int(y), int(w), int(h)

                obj = cls(guid, x, y, w, h)
                objects[guid] = obj

                if parent_guid != "None" and parent_guid in objects:
                    obj.parent = objects[parent_guid]
                    objects[parent_guid].file_list.append(obj)
                elif parent_guid == "None":
                    root = obj
        return root

if __name__ == "__main__":
    # File path
    file_path = "FileView.txt"

    root_obj = CFileView.instantiate_from_flat_file(file_path)

    if root_obj:
        # Print loaded characters
        print("\nLoaded Characters:")
        root_obj.print_tree()
