import uuid


class CFolderView:
    def __init__(self, guid: str = None, x: int = -1, y: int = -1, w: int = -1, h: int = -1, parent=None):
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
        self.p_w: int = -1
        self.p_h: int = -1
        self.space_x: int = 0
        self.space_y: int = 0
        self.ps = None

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
        print(" " * indent + f"GUID: {self.guid}, Parent: {parent_guid}, \
        self.x:{self.x}, self.y:{self.y}, self.w:{self.w}, self.h:{self.h}, \
        self.p_x:{self.p_x}, self.p_y:{self.p_y},\
        self.p_w:{self.p_w}, self.p_h:{self.p_h}, ps:({self.ps.guid if (self.ps != None)  else "None"})")
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
        
    def find_by_mouse_pos_tree(self, mx: int, my: int):
        result = None
        if mx >= self.p_x and mx <= (self.p_x + self.p_w) and my >= self.p_y and my <= (self.p_y + self.p_h):#found
            result = self
        else:  #keep going
            for child in self.children_list:
                result = child.find_by_mouse_pos_tree(mx, my)
                if result: #found
                    break
        return result

    def CALC_p_w(self, scale_p):
        self.p_w = self.w * scale_p

    def CALC_p_w_TREE(self, scale_p):
        self.CALC_p_w(scale_p)
        for child in self.children_list:
            child.CALC_p_w_TREE(scale_p)
            
    def CALC_p_h(self, scale_p):
        self.p_h = self.h * scale_p

    def CALC_p_h_TREE(self, scale_p):
        self.CALC_p_h(scale_p)
        for child in self.children_list:
            child.CALC_p_h_TREE(scale_p)
    
    def calc_x(self):
        print(self.guid)
        r1 = 0
        r2 = 0
        if self.parent == None:
            r1 = 1
        if self.ps == None:
            r2 = 1
        if r1 == 1:
            self.x = 0
        elif r2 == 1:
            self.x = self.parent.x

    def calc_x_tree(self):
        self.calc_x()
        for child in self.children_list:
            child.calc_x_tree()

    def calc_y(self):
        print(self.guid)
        r1 = 0
        r2 = 0
        if self.parent == None:
            r1 = 1
        if self.parent != None:
            r2 = 1
        if r1 == 1:
            self.y = 0
        if r2 == 1:
            self.y = self.parent.h + self.parent.y + self.space_y

    def calc_y_tree(self):
        self.calc_y()
        for child in self.children_list:
            child.calc_y_tree()

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
        
    def CALC_ps_TREE(self):
        if self.parent == None:
            self.ps = None
        ps_for_next_node = None
        for child in self.children_list:
            child.ps = ps_for_next_node
            ps_for_next_node = child
            child.CALC_ps_TREE()

    def CALC_ps2(self, prior_node_p):
        self.ps = prior_node_p

    def CALC_ps_TREE2(self, prior_node_p):
        prior_node = prior_node_p
        self.CALC_ps2(prior_node) 
        #care about siblings
        sibling_prior_node = None 
        for child in self.children_list:   
            child.CALC_ps_TREE2(sibling_prior_node) #1
            sibling_prior_node = child  #save for next node #2  

    def CALC_space_x(self):
        self.space_x = 10

    def CALC_space_x_TREE(self):
        self.CALC_space_x()
        for child in self.children_list:
            child.CALC_space_x_TREE()
            
    def CALC_space_y(self):
        self.space_y = 10

    def CALC_space_y_TREE(self):
        self.CALC_space_y()
        for child in self.children_list:
            child.CALC_space_y_TREE()

    # -------------------------------------------------------------------------
    # Draw recursive structure (simulation)
    # -------------------------------------------------------------------------
    def draw(self, surface, pygame_p):
        #print(self.guid, self.p_x, self.p_y)
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
    
    print("------------------------------------------")
    root_folder.CALC_ps_TREE2(None)
    root_folder.print_tree(0)