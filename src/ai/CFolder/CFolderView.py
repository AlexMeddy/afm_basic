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
        self.left_margain: int = 10
        self.top_margain: int = 20
        self.ps = None
        self.cousin = None
        self.selected = 0

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

    def find_by_selection_tree(self):
        found_folder = None
        if self.selected == 1:
            found_folder = self
        else:
            for child in self.children_list:
                found_folder = child.find_by_selection_tree()
                if found_folder:
                    break
        return found_folder
        
    def find_list_by_selection_tree(self, found_folders_p):
        found_folders = found_folders_p
        if self.selected == 1:
            found_folders.append(self)
        for child in self.children_list:
            found_folders = child.find_list_by_selection_tree(found_folders)
        return found_folders

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
            
    def calc_cousin(self):
        if self.parent != None and self.parent.ps != None and self.parent.ps.children_list != []:
            self.cousin = self.parent.ps.children_list[len(self.parent.ps.children_list)-1]
            
    def CALC_cousin_TREE(self):
        self.calc_cousin()
        for child in self.children_list:
            child.CALC_cousin_TREE()
            
    def calc_scale_x(self, available_screen_width_p, longest_x_p):
        scale_x = available_screen_width_p / longest_x_p
        return scale_x
    
    def find_longest_width_x(self, longest_x_so_far_p):
        longest_x = longest_x_so_far_p
        if self.x + self.w + self.space_x > longest_x:
            longest_x = self.x + self.w + self.space_x
        return longest_x
    
    def find_longest_width_x_tree(self, longest_x_so_far_p):
        longest_x = longest_x_so_far_p
        longest_x = self.find_longest_width_x(longest_x)
        for child in self.children_list:
            longest_x = child.find_longest_width_x_tree(longest_x) 
        return longest_x
        
    def find_available_screen_width(self, screen_width_p):
        available_screen_width = screen_width_p - self.left_margain
        return available_screen_width
        
    def calc_scale_y(self, available_screen_height_p, longest_y_p):
        scale_y = available_screen_height_p / longest_y_p
        return scale_y
        
    def find_longest_width_y(self, longest_y_so_far_p):
        longest_y = longest_y_so_far_p
        if self.y + self.h + self.space_y > longest_y:
            longest_y = self.y + self.h + self.space_y
        return longest_y
    
    def find_longest_width_y_tree(self, longest_y_so_far_p):
        longest_y = longest_y_so_far_p
        longest_y = self.find_longest_width_y(longest_y)
        for child in self.children_list:
            longest_y = child.find_longest_width_y_tree(longest_y) 
        return longest_y
        
    def find_available_screen_height(self, screen_height_p):
        available_screen_height = screen_height_p - self.top_margain
        return available_screen_height
    
    def calc_x(self):
        print(self.guid)
        r1 = 0
        r2 = 0
        r3 = 0
        r4 = 0
        if self.parent == None:
            r1 = 1
        if self.ps == None:
            r2 = 1
        if self.ps != None:
            r3 = 1
        #if self.parent != None and self.parent.ps != None and self.parent.ps.children_list != []:
        if self.cousin != None:
            r4 = 1
        print("----------printing rules-------------",r1,r2,r3,r4,self.guid)
        #applying rules
        if r1 == 1: #if root
            self.x = 0 + self.left_margain #root anchor to 0, should be anchored to left margain
        elif r2 == 1: #if no ps
            print("----------------------------entering r2--------------------------" + self.guid)
            self.x = self.parent.x #a left corner anchor to parent left corner
        elif r3 == 1: #if ps
            #self.x = self.ps.x + self.ps.w + self.space_x #b left corner anchor to ps right corner
            longest_x = self.ps.find_longest_width_x_tree(0)
            self.x = longest_x #b left corner anchor to longest x ps subtree
        """
        elif r4 == 1: #if last cousin
            print("----------------last cousin of ", self.guid, " is ", self.cousin.guid)
            self.x = self.cousin.x + self.cousin.w + self.space_x
        """
        

        
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
            self.y = 0 + self.top_margain #root anchor to 0, should be anchored to top margain
        if r2 == 1:
            self.y = self.parent.h + self.parent.y + self.space_y #self left top corner anchor to parent left bottom corner

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
    def draw(self, surface, pygame_p, font_p):
        #print(self.guid, self.p_x, self.p_y)
        line_thickness = 1
        if self.p_x != -1 and self.p_y != -1: 
            rect = pygame_p.Rect(self.p_x, self.p_y, self.p_w, self.p_h)
            if self.selected == 0:
                line_thickness = 1
            else: 
                line_thickness = 3
            pygame_p.draw.rect(surface, (255, 255, 255), rect, line_thickness)

    def draw_tree(self, surface, pygame_p, font_p):
        # Draw rectangle for this node
        self.draw(surface, pygame_p, font_p)
        for child in self.children_list:
            child.draw_tree(surface, pygame_p, font_p)
            
    def draw_line(self, surface, pygame_p):
        if self.parent != None:
            line_xy_start = (self.parent.p_x+self.parent.p_w/2, self.parent.p_y+self.parent.p_h)
            line_xy_end = (self.p_x+self.p_w/2, self.p_y)
            pygame_p.draw.line(surface, (255,255,255), line_xy_start, line_xy_end)
    
    def draw_line_tree(self, surface, pygame_p):
        # Draw rectangle for this node
        self.draw_line(surface, pygame_p)
        for child in self.children_list:
            child.draw_line_tree(surface, pygame_p)
            
    def draw_guid(self, surface, font_p):
        text = font_p.render(self.guid, True, (255,255,255))
        text_xy = (self.p_x, self.p_y)
        surface.blit(text, text_xy)
    
    def draw_guid_tree(self, surface, font_p):
        # Draw rectangle for this node
        self.draw_guid(surface, font_p)
        for child in self.children_list:
            child.draw_guid_tree(surface, font_p)

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