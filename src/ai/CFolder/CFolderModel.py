import uuid
from typing import List, Optional


class CFolderModel:
    def __init__(self, guid: Optional[str] = None, parent: "CFolderModel" = None):
        self.guid: str = guid if guid else str(uuid.uuid4())
        self.parent: Optional[CFolderModel] = parent
        self.children_list: List[CFolderModel] = []

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

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    # Example: instantiate from sample file
    root = CFolderModel.instantiate_from_flat_file("CFolderModel.txt")

    print("Folder Tree:")
    root.print_tree()

    print(f"\nTotal number of folders: {root.calc_number_of_folders()}")

    # Test lookup
    search_guid = "child1_guid"
    found = root.find_by_guid_tree(search_guid)
    print(f"\nLookup: Folder with GUID '{search_guid}' was {'found' if found else 'not found'}.")
