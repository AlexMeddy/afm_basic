class CPersonView:
    def __init__(self, guid: str, x: int, y: int, w: int, h: int, parent: str):
        """Initialize a person with position, size, and optional parent."""
        self.guid = guid
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent
        self.p_x = -1
        self.p_y = -1
        self.children_list = []  # List of child CPersonView objects

    def __repr__(self):
        """Readable string representation of the object."""
        return (f"CPersonView(guid='{self.guid}', x={self.x}, y={self.y}, "
                f"w={self.w}, h={self.h}, parent='{self.parent}')")

    def print_recursive(self, level=0):
        """Recursively print this node and its children."""
        indent = "  " * level
        print(f"{indent}{self}")
        for child in self.children_list:
            child.print_recursive(level + 1)

    def find_by_mouse_pos_recursive(self, mouse_x: int, mouse_y: int):
        """
        Recursively search for a person under the mouse position.
        Returns the CPersonView if found, else None.
        """
        if (self.x <= mouse_x <= self.x + self.w) and (self.y <= mouse_y <= self.y + self.h):
            return self
        for child in self.children_list:
            found = child.find_by_mouse_pos_recursive(mouse_x, mouse_y)
            if found:
                return found
        return None

    def draw_recursive(self, screen, color=(255, 0, 0)):
        """
        Recursively draw rectangles for this person and its children.
        Requires a pygame screen surface.
        """
        import pygame
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), 2)
        for child in self.children_list:
            child.draw_recursive(screen, color)

    @staticmethod
    def instantiate_people_from_flat_file(file_path: str):
        """
        Instantiate a tree of CPersonView objects from a comma-delimited file.
        Each line format: guid, x, y, w, h, parent
        """
        nodes = {}
        parents = []

        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = [p.strip() for p in line.strip().split(",")]
                    if len(parts) != 6:
                        print(f"Invalid line format: {line.strip()}")
                        continue

                    guid, x_str, y_str, w_str, h_str, parent = parts
                    try:
                        x = int(x_str)
                        y = int(y_str)
                        w = int(w_str)
                        h = int(h_str)
                    except ValueError:
                        print(f"Invalid numeric values: {line.strip()}")
                        continue

                    node = CPersonView(guid, x, y, w, h, parent)
                    nodes[guid] = node

            # Link parents and children
            for node in nodes.values():
                if node.parent.lower() != "none":
                    parent_node = nodes.get(node.parent)
                    if parent_node:
                        parent_node.children_list.append(node)
                    else:
                        print(f"Warning: Parent '{node.parent}' not found for {node.guid}")
                else:
                    parents.append(node)

            return parents

        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return []


if __name__ == "__main__":
    # Sample usage
    root_obj = CPersonView.instantiate_people_from_flat_file("people.txt")

    print("People Tree:")
    root_obj.print_recursive()

