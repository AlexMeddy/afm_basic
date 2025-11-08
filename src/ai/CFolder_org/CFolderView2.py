from __future__ import annotations
from typing import List, Optional
import uuid


class CFolderView:
    def __init__(
        self,
        guid: Optional[str] = None,
        x: int = 0,
        y: int = 0,
        w: int = 0,
        h: int = 0,
        parent: Optional[CFolderView] = None
    ):
        self.guid: str = guid if guid else str(uuid.uuid4())
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.parent: Optional[CFolderView] = parent
        self.children_list: List[CFolderView] = []
        self.p_x: int = -1
        self.p_y: int = -1

    # -------------------- Recursive Tree Methods --------------------

    def print_tree(self, level: int = 0):
        """Recursively print this folder and its children, including parent details."""
        indent = "  " * level
        parent_guid = self.parent.guid if self.parent else "None"
        print(f"{indent}Folder GUID: {self.guid} (Parent: {parent_guid})  Pos=({self.x},{self.y}) Size=({self.w},{self.h})")

        for child in self.children_list:
            child.print_tree(level + 1)

    def find_by_mouse_pos_tree(self, mx: int, my: int) -> Optional[CFolderView]:
        """Recursively find the first folder under the given mouse position."""
        # Check if mouse is within this folder’s bounds
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            # Check children recursively (deepest match)
            for child in self.children_list:
                found = child.find_by_mouse_pos_tree(mx, my)
                if found:
                    return found
            return self
        return None

    def draw_tree(self, level: int = 0):
        """Simulate drawing this folder and its children."""
        indent = "  " * level
        print(f"{indent}Drawing folder {self.guid} at ({self.x},{self.y}) size ({self.w},{self.h})")
        for child in self.children_list:
            child.draw_tree(level + 1)

    def add_child(self, child: CFolderView):
        """Add a child folder to this folder."""
        child.parent = self
        self.children_list.append(child)

    def find_by_guid_tree(self, search_guid: str) -> Optional[CFolderView]:
        """Recursively search for a folder by GUID."""
        if self.guid == search_guid:
            return self
        for child in self.children_list:
            found = child.find_by_guid_tree(search_guid)
            if found:
                return found
        return None

    # -------------------- File-Based Instantiation --------------------

    @classmethod
    def instantiate_from_flat_file(cls, filename: str) -> CFolderView:
        """
        Instantiate a tree of CFolderView objects from a flat comma-delimited file.

        Expected columns:
        guid,parent_guid,x,y,w,h
        """
        nodes = {}

        with open(filename, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

        # First pass: create all nodes
        for line in lines:
            parts = line.split(",")
            if len(parts) != 6:
                raise ValueError(f"Invalid line: {line}")

            guid, parent_guid, x, y, w, h = parts
            node = cls(guid, int(x), int(y), int(w), int(h))
            nodes[guid] = (node, parent_guid)

        # Second pass: link parent-child relationships
        root = None
        for guid, (node, parent_guid) in nodes.items():
            if parent_guid == "None" or parent_guid == "":
                root = node
            else:
                parent_node = nodes[parent_guid][0]
                parent_node.add_child(node)

        if root is None:
            raise ValueError("No root node found in the file (missing parent=None entry).")

        return root


# -------------------- Sample File: CFolderView2.txt --------------------
"""
# Sample CFolderView2.txt
# guid,parent_guid,x,y,w,h
root_guid,None,0,0,200,150
child1_guid,root_guid,10,10,80,60
child2_guid,root_guid,100,20,60,50
subchild1_guid,child1_guid,15,15,40,30
"""

# -------------------- Main Program --------------------
if __name__ == "__main__":
    # Create a sample file for demonstration
    sample_content = """\
root_guid,None,0,0,200,150
child1_guid,root_guid,10,10,80,60
child2_guid,root_guid,100,20,60,50
subchild1_guid,child1_guid,15,15,40,30
"""
    with open("CFolderView2.txt", "w") as f:
        f.write(sample_content)

    # Instantiate from file
    root = CFolderView.instantiate_from_flat_file("CFolderView2.txt")

    print("=== Folder Tree ===")
    root.print_tree()

    print("\n=== Draw Tree ===")
    root.draw_tree()

    print("\n=== Find by GUID ===")
    node = root.find_by_guid_tree("child2_guid")
    print(f"Found: {node.guid if node else 'None'}")

    print("\n=== Find by Mouse Pos ===")
    mx, my = 18, 18
    found = root.find_by_mouse_pos_tree(mx, my)
    print(f"Mouse ({mx},{my}) is over: {found.guid if found else 'None'}")
