import uuid


class CFolderView:
    def __init__(self, guid=None, x=0, y=0, w=0, h=0, parent=None):
        self.guid: str = guid if guid else str(uuid.uuid4())
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.parent: "CFolderView" = parent
        self.children_list: list["CFolderView"] = []
        self.p_x: int = -1
        self.p_y: int = -1

    # ------------------------ methods ------------------------

    def add_child(self, child: "CFolderView"):
        """Add a child folder to this folder."""
        child.parent = self
        self.children_list.append(child)

    def print_tree(self, level=0):
        """Recursively print tree including parent details."""
        indent = "  " * level
        parent_guid = self.parent.guid if self.parent else "None"
        print(f"{indent}Folder {self.guid} (Parent: {parent_guid}) "
              f"Coords: ({self.x},{self.y},{self.w},{self.h})")

        for child in self.children_list:
            child.print_tree(level + 1)

    def find_by_mouse_pos_tree(self, mx, my):
        """Recursively find folder by mouse position."""
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            return self
        for child in self.children_list:
            result = child.find_by_mouse_pos_tree(mx, my)
            if result:
                return result
        return None

    def draw_tree(self, depth=0):
        """Mockup draw method for displaying folder tree."""
        indent = "  " * depth
        print(f"{indent}[DRAW] Folder {self.guid} at ({self.x},{self.y},{self.w},{self.h})")
        for child in self.children_list:
            child.draw_tree(depth + 1)

    # ------------------------ instantiation ------------------------

    @staticmethod
    def instantiate_from_flat_file(filename="FolderView.txt"):
        """Instantiate CFolderView tree from flat file."""
        nodes = {}
        root = None

        with open(filename, "r") as f:
            for line in f:
                if not line.strip() or line.startswith("#"):
                    continue
                parts = line.strip().split(",")
                if len(parts) < 6:
                    continue
                guid, parent_guid, x, y, w, h = parts
                node = CFolderView(
                    guid=guid.strip(),
                    x=int(x),
                    y=int(y),
                    w=int(w),
                    h=int(h),
                )
                nodes[guid.strip()] = (node, parent_guid.strip())

        # Build hierarchy
        for guid, (node, parent_guid) in nodes.items():
            if parent_guid and parent_guid in nodes:
                parent_node, _ = nodes[parent_guid]
                parent_node.add_child(node)
            else:
                root = node  # root node has no parent

        return root


# ------------------------ usage example ------------------------
if __name__ == "__main__":
    # Sample instantiation from file
    root = CFolderView.instantiate_from_flat_file("FolderView.txt")

    print("\n--- Tree Structure ---")
    root.print_tree()

    print("\n--- Drawing Tree ---")
    root.draw_tree()

    print("\n--- Finding by Mouse Position (25,25) ---")
    found = root.find_by_mouse_pos_tree(25, 25)
    if found:
        print(f"Found folder GUID: {found.guid}")
    else:
        print("No folder found at that position.")
