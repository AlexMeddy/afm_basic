import uuid


class CFolderView:
    def __init__(self, guid: str = None, x: int = 0, y: int = 0, w: int = 0, h: int = 0, parent=None):
        self.guid: str = guid if guid else str(uuid.uuid4())
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.parent: 'CFolderView' = parent
        self.children_list: list['CFolderView'] = []

        # Additional positional placeholders
        self.p_x: int = -1
        self.p_y: int = -1

    # -------------------------------------------------------------------------
    # Add child to current folder
    # -------------------------------------------------------------------------
    def add_child(self, child: 'CFolderView'):
        """Adds a child folder to this folder."""
        child.parent = self
        self.children_list.append(child)

    # -------------------------------------------------------------------------
    # Print recursive tree structure
    # -------------------------------------------------------------------------
    def print_tree(self, indent: int = 0):
        """Recursively prints the folder tree with parent details."""
        parent_guid = self.parent.guid if self.parent else "None"
        print(" " * indent + f"GUID: {self.guid}, Parent: {parent_guid}, Pos:({self.x},{self.y}), Size:({self.w},{self.h})")
        for child in self.children_list:
            child.print_tree(indent + 4)

    # -------------------------------------------------------------------------
    # Find a folder by GUID recursively
    # -------------------------------------------------------------------------
    def find_by_guid_tree(self, search_guid: str) -> 'CFolderView | None':
        """Recursively search for a folder by its GUID."""
        if self.guid == search_guid:
            return self
        for child in self.children_list:
            result = child.find_by_guid_tree(search_guid)
            if result:
                return result
        return None

    # -------------------------------------------------------------------------
    # Find folder by mouse coordinates (recursive)
    # -------------------------------------------------------------------------
    def find_by_mouse_pos_tree(self, mx: int, my: int) -> 'CFolderView | None':
        """Recursively find the folder containing the mouse position."""
        # Check if mouse is inside this folder’s bounding box
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            # Check deeper children first (front-most)
            for child in self.children_list:
                result = child.find_by_mouse_pos_tree(mx, my)
                if result:
                    return result
            return self
        return None
        
    def calc_x(self):
        r1 = 0
        if self.parent == None:
            r1 = 1
        if r1 == 1:
            self.x = 0
            
    def calc_x_tree(self):
        self.calc_x()
        for child in self.children_list:
            child.calc_x()
            
    def calc_y(self):
        r1 = 0
        if self.parent == None:
            r1 = 1
        if r1 == 1:
            self.y = 0
            
    def calc_y_tree(self):
        self.calc_y()
        for child in self.children_list:
            child.calc_y()
            
    def CALC_p_x(self, scale_p):
        self.p_x = self.x * scale_p

    def CALC_p_x_TREE(self, scale_p):
        self.CALC_p_x(scale_p)
        for child in self.children_list:
            child.CALC_p_x_TREE(scale_p)

    def CALC_p_y(self, scale_p):
        self.p_y = self.y * scale_p

    def CALC_p_y_TREE(self, scale_p):
        self.CALC_p_y(scale_p)
        for child in self.children_list:
            child.CALC_p_y_TREE(scale_p)


    # -------------------------------------------------------------------------
    # Draw recursive structure (simulation)
    # -------------------------------------------------------------------------
    def draw(self, surface, pygame_p):
        print(self.guid, self.p_x, self.p_y)
        if self.p_x != -1 and self.p_y != -1:
            rect = pygame_p.Rect(self.p_x, self.p_y, self.w, self.h)
            pygame_p.draw.rect(surface, (255, 255, 255), rect, 1)
        
    def draw_tree(self, surface, pygame_p):
        # Draw rectangle for this node
        self.draw(surface, pygame_p)
        for child in self.children_list:
            child.draw_tree(surface, pygame_p)

    # -------------------------------------------------------------------------
    # Instantiate from flat file
    # -------------------------------------------------------------------------
    @classmethod
    def instantiate_from_flat_file(cls, filename: str) -> 'CFolderView':
        """
        Instantiate the folder tree from a flat CSV-like text file.
        Expected format per line:
        guid,parent_guid,x,y,w,h
        """
        import csv

        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            nodes = {}

            # First pass: create all nodes
            for row in reader:
                guid, parent_guid, x, y, w, h = row
                node = cls(guid=guid, x=int(x), y=int(y), w=int(w), h=int(h))
                nodes[guid] = (node, parent_guid)

            # Second pass: connect hierarchy
            root = None
            for guid, (node, parent_guid) in nodes.items():
                if parent_guid and parent_guid in nodes:
                    parent_node, _ = nodes[parent_guid]
                    parent_node.add_child(node)
                else:
                    root = node  # root has no parent
            return root


# -------------------------------------------------------------------------
# Example usage and sample flat file content
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample file for demonstration
    sample_data = """guid,parent_guid,x,y,w,h
root_guid,,0,0,400,400
child_1,root_guid,10,10,100,100
child_2,root_guid,150,50,120,120
subchild_1,child_1,20,20,60,60
"""
    with open("FolderView.txt", "w") as f:
        f.write(sample_data)

    # Instantiate from flat file
    root_folder = CFolderView.instantiate_from_flat_file("FolderView.txt")

    print("=== Folder Structure ===")
    root_folder.print_tree()

    print("\n=== Search Tests ===")
    guid_to_find = "subchild_1"
    found = root_folder.find_by_guid_tree(guid_to_find)
    print(f"Found GUID {guid_to_find}: {found.guid if found else 'Not Found'}")

    print("\n=== Mouse Position Test ===")
    mx, my = 25, 25
    hit = root_folder.find_by_mouse_pos_tree(mx, my)
    print(f"Mouse ({mx},{my}) inside folder: {hit.guid if hit else 'None'}")
