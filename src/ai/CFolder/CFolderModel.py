import uuid
from typing import List, Optional
import random

class CFolderModel:
    def __init__(self, guid: Optional[str] = None, parent: "CFolderModel" = None):
        self.guid: str = guid if guid else str(uuid.uuid4())
        self.parent: Optional[CFolderModel] = parent
        self.children_list: List[CFolderModel] = []
        self.size = random.randint(1, 10)

    # ------------------------
    # methods
    # ------------------------

    def calc_number_of_folders(self) -> int:
        """
        Mockup: counts total folders including self and children recursively.
        """
        count = 1  # count self
        for child in self.children_list:
            count += child.calc_number_of_folders()
        return count

    def add_child(self, child: "CFolderModel") -> None:
        """Adds a child folder to this folder."""
        child.parent = self
        self.children_list.append(child)

    def print_tree(self, level: int = 0) -> None:
        """
        Prints the folder tree, including parent details.
        """
        indent = "    " * level
        parent_guid = self.parent.guid if self.parent else "None"
        print(f"{indent}- Folder GUID: {self.guid} (Parent: {parent_guid})")
        for child in self.children_list:
            child.print_tree(level + 1)

    def find_by_guid_tree(self, guid: str) -> Optional["CFolderModel"]:
        """
        Recursively searches the tree for a folder with the given guid.
        """
        if self.guid == guid:
            return self
        for child in self.children_list:
            found = child.find_by_guid_tree(guid)
            if found:
                return found
        return None

    # ------------------------
    # instantiation
    # ------------------------

    @staticmethod
    def instantiate_from_flat_file(filename: str) -> "CFolderModel":
        """
        Instantiates a folder tree from a flat file.
        Expected format: guid,parent_guid
        The root has parent_guid as 'None'.
        """
        folder_dict = {}

        # Step 1: Read file and create all folder objects
        with open(filename, "r") as f:
            lines = f.read().strip().splitlines()
            for line in lines:
                guid, parent_guid = line.split(",")
                folder_dict[guid] = {
                    "folder": CFolderModel(guid=guid),
                    "parent_guid": parent_guid if parent_guid != "None" else None,
                }

        # Step 2: Link parent-child relationships
        root = None
        for guid, entry in folder_dict.items():
            folder = entry["folder"]
            parent_guid = entry["parent_guid"]
            if parent_guid:
                parent_folder = folder_dict[parent_guid]["folder"]
                parent_folder.add_child(folder)
            else:
                root = folder

        return root
        
    def write_to_flat_file(self, filename_p):
        file_name = filename_p
        line = ""
        with open(file_name, "a") as file:
            if self.parent == None:
                line = self.guid + "," + "None"
            else:    
                line = self.guid + "," + self.parent.guid
            file.write(line + "\n")
            
    def write_to_flat_file_tree(self, filename_p):
        self.write_to_flat_file(filename_p)
        for child in self.children_list:
            child.write_to_flat_file_tree(filename_p)
    
    #1 contract
    #2 test contract
    #3 add dummy
    #4 test dummy
    #5 go through linear list and print each
    #6 test step 5
    #7 add check if tree doesnt exist
    #8 test step 7
    #9 add check if tree does exist
    #10 test step 9
    #11 dont copy the whole line
    #12 put the paramater names
    # summary:go through the tree and check if the tree doesnt exist and if it doesnt then create root... 
    @staticmethod
    def my_instantiate_from_flat_file(filename):
        root = None
        with open(filename, "r") as f:
            lines = f.read().strip().splitlines()
            for line in lines:
                guid, parent_guid = line.split(",")
                print(guid, parent_guid)
                
                '''
                if root == None:
                    root = CFolderModel(guid = guid, parent=None)
                else:
                    parent = root.find_by_guid_tree(parent_guid)
                    new_child = CFolderModel(guid = guid, parent=parent)
                    parent.add_child(new_child)
                '''
                root = CFolderModel.tree_append(root_p=root, guid_p=guid, guid_parent_p=parent_guid)
        return root
        
    @staticmethod   
    def list_append(linear_list_p, guid_p, guid_parent_p):
        linear_list = linear_list_p
        if linear_list == None:
            root = CFolderModel(guid_p, "None")
            linear_list = []
            linear_list.append(root)
        else:
            new_child = CFolderModel(guid_p, guid_parent_p)
            linear_list.append(new_child)
        return linear_list
        
    @staticmethod   
    def swap(obj1_p, obj2_p):
        obj1 = obj1_p
        obj2 = obj2_p
        obj1 = obj2
        return obj1
        
    @staticmethod   
    def tree_append(root_p, guid_p, guid_parent_p):
        root = root_p
        if root == None:
            root = CFolderModel(guid = guid_p, parent=None)
        else:
            parent = root.find_by_guid_tree(guid_parent_p)
            new_child = CFolderModel(guid = guid_p, parent=parent)
            parent.add_child(new_child)
        return root
        
        
    def event_handler_bla(root_p):
        ...
        ...
        root = root_p
        input_text = "r,none"
        guid = "r"
        parent_guid = "none"
        root = CFolderModel.tree_append(root_p=root, guid_p=guid, guid_parent_p=parent_guid)

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    # Example: instantiate from sample file
    #root = CFolderModel.instantiate_from_flat_file("CFolderModel.txt")
    root = CFolderModel.my_instantiate_from_flat_file("CFolderModel.txt")
    a = CFolderModel(guid = "a", parent=root)
    swapped_obj = CFolderModel.swap(root, a)
    print(swapped_obj.guid)
    #print("Folder Tree:")
    if root != None:
        root.print_tree()
    else:
        print("no root")