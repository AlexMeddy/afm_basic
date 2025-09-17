import uuid


class CFolderModel:
    def __init__(self, guid: str = None, parent=None):
        self.guid: str = guid if guid else str(uuid.uuid4())
        self.parent: "CFolderModel" = parent
        self.children_list: list["CFolderModel"] = []

    # ----------------- mockup methods -----------------
    def calc_number_of_folders(self) -> int:
        """
        Mockup only: count the number of folders in the tree (including self).
        """
        count = 1  # count self
        for child in self.children_list:
            count += child.calc_number_of_folders()
        return count

    # ----------------- child management -----------------
    def add_child(self, child: "CFolderModel"):
        """
        Adds a child folder to this folder.
        """
        child.parent = self
        self.children_list.append(child)

    # ----------------- search -----------------
    def find_by_guid_tree(self, guid: str) -> "CFolderModel":
        """
        Recursively search for a folder by GUID.
        """
        if self.guid == guid:
            return self
        for child in self.children_list:
            result = child.find_by_guid_tree(guid)
            if result:
                return result
        return None

    # ----------------- file instantiation -----------------
    @staticmethod
    def instantiate_from_flat_file(file_path: str) -> "CFolderModel":
        """
        Instantiates CFolderModel tree from a flat comma-delimited file.
        Format: child_guid,parent_guid
        parent_guid can be empty string for the root.
        """
        nodes = {}
        parent_map = {}

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                child_guid = parts[0].strip()
                parent_guid = parts[1].strip() if len(parts) > 1 else ""

                # Create node if not exists
                if child_guid not in nodes:
                    nodes[child_guid] = CFolderModel(guid=child_guid)

                # Track parent relationship
                if parent_guid:
                    parent_map[child_guid] = parent_guid

        # Link parent-child relationships
        root = None
        for child_guid, parent_guid in parent_map.items():
            parent_node = nodes.get(parent_guid)
            child_node = nodes.get(child_guid)
            if parent_node and child_node:
                parent_node.add_child(child_node)

        # Root = node without parent
        for guid, node in nodes.items():
            if guid not in parent_map.values():
                root = node
                break

        return root

    # ----------------- helper print -----------------
    def print_tree(self, indent=0):
        print(" " * indent + f"Folder({self.guid})")
        for child in self.children_list:
            child.print_tree(indent + 2)


# ----------------- usage -----------------
if __name__ == "__main__":
    # Sample instantiation from file
    root = CFolderModel.instantiate_from_flat_file("FolderModel.txt")
    print("Tree structure:")
    root.print_tree()

    print(f"\nTotal folders in tree: {root.calc_number_of_folders()}")

    # Example search
    some_guid = root.children_list[0].guid if root.children_list else root.guid
    found = root.find_by_guid_tree(some_guid)
    print(f"\nSearch for {some_guid}: {'Found' if found else 'Not Found'}")
