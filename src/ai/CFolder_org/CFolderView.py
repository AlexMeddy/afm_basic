import uuid
from typing import List, Optional, Tuple


class CFolderView:
    def __init__(self, guid: Optional[str] = None,
                 x: int = 0, y: int = 0, w: int = 100, h: int = 50,
                 parent: "CFolderView" = None):
        self.guid: str = guid if guid else str(uuid.uuid4())
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.parent: Optional[CFolderView] = parent
        self.children_list: List[CFolderView] = []
        self.p_x: int = -1
        self.p_y: int = -1

    # ------------------------
    # methods
    # ------------------------

    def add_child(self, child: "CFolderView") -> None:
        """Adds a child folder view."""
        child.parent = self
        self.children_list.append(child)
        
    def find_by_guid_tree(self, guid: str) -> Optional["CFolderView"]:
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

    def print_tree(self, level: int = 0) -> None:
        """Prints the folder view tree with parent details."""
        indent = "    " * level
        parent_guid = self.parent.guid if self.parent else "None"
        print(f"{indent}- View GUID: {self.guid} "
              f"(Parent: {parent_guid}, Pos: ({self.x},{self.y}), Size: {self.w}x{self.h})")
        for child in self.children_list:
            child.print_tree(level + 1)

    def find_by_mouse_pos_tree(self, pos: Tuple[int, int]) -> Optional["CFolderView"]:
        """
        Recursively searches for the folder view containing the given mouse position.
        """
        mx, my = pos
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            for child in self.children_list:
                found = child.find_by_mouse_pos_tree(pos)
                if found:
                    return found
            return self
        return None

    def draw_tree(self) -> None:
        """
        Mockup draw function for tree rendering.
        In real apps, integrate with a GUI library like pygame or tkinter.
        """
        print(f"Drawing folder view {self.guid} at ({self.x},{self.y},{self.w},{self.h})")
        for child in self.children_list:
            child.draw_tree()

    # ------------------------
    # instantiation
    # ------------------------

    @staticmethod
    def instantiate_from_flat_file(filename: str) -> "CFolderView":
        """
        Instantiates a folder view tree from a flat file.
        Expected format: guid,parent_guid,x,y,w,h
        Root has parent_guid as 'None'.
        """
        folder_dict = {}

        # Step 1: Create all views
        with open(filename, "r") as f:
            lines = f.read().strip().splitlines()
            for line in lines:
                guid, parent_guid, x, y, w, h = line.split(",")
                folder_dict[guid] = {
                    "view": CFolderView(
                        guid=guid,
                        x=int(x),
                        y=int(y),
                        w=int(w),
                        h=int(h),
                    ),
                    "parent_guid": parent_guid if parent_guid != "None" else None,
                }

        # Step 2: Link hierarchy
        root = None
        for guid, entry in folder_dict.items():
            view = entry["view"]
            parent_guid = entry["parent_guid"]
            if parent_guid:
                parent_view = folder_dict[parent_guid]["view"]
                parent_view.add_child(view)
            else:
                root = view

        return root


# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    # Load from file
    root = CFolderView.instantiate_from_flat_file("FolderView.txt")

    print("Folder View Tree:")
    root.print_tree()

    print("\nDrawing Views:")
    root.draw_tree()

    test_pos = (60, 60)
    found = root.find_by_mouse_pos_tree(test_pos)
    print(f"\nMouse at {test_pos} is over: {found.guid if found else 'None'}")
