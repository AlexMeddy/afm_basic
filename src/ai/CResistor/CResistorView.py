from CResistorModel import CResistorModelListManager
# ------------------------ core class ------------------------
class CResistorView:
    def __init__(self, guid: str, x: int, y: int, w: int, h: int):
        self.guid: str = guid
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.p_x: int = -1
        self.p_y: int = -1
        #self.model = model_p

    # ------------------------ methods ------------------------
    def calc_p_x(self):
        # Placeholder calculation logic for p_x
        self.p_x = self.x + 5
        return self.p_x
        
    
    def calc_p_y(self):
        # Placeholder calculation logic for p_y
        self.p_y = self.y + 5
        return self.p_y
        

    def __repr__(self):
        return f"CResistorView(guid={self.guid}, x={self.x}, y={self.y}, w={self.w}, h={self.h})"


# ------------------------ list manager class ------------------------
class CResistorViewListManager:
    def __init__(self):
        self.resistor_list: list[CResistorView] = []

    def calc_p_x_list(self):
        # Placeholder calculation logic for p_x
        for child in self.resistor_list:
            child.calc_p_x()

    def calc_p_y_list(self):
        # Placeholder calculation logic for p_x
        for child in self.resistor_list:
            child.calc_p_y()
            
    def add_child(self, child_p):
        self.resistor_list.append(child_p)

    # ------------------------ list manager methods ------------------------
    def print_list(self):
        for r in self.resistor_list:
            print(r)

    def find_by_mouse_pos_list(self, mouse_x: int, mouse_y: int):
        found = None
        for r in self.resistor_list:
            if r.p_x <= mouse_x <= r.p_x + r.w and r.p_y <= mouse_y <= r.p_y + r.h:
                found = r
                break
        return found

    def draw_list(self, surface, pygame_p):
        for r in self.resistor_list:
            pygame_p.draw.rect(surface, (255, 0, 0), (r.p_x, r.p_y, r.w, r.h))

    # ------------------------ instantiation ------------------------
    def instantiate_list_from_flat_file(self, filename: str):
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    guid, x, y, w, h = line.split(",")
                    resistor = CResistorView(guid, int(x), int(y), int(w), int(h))
                    self.resistor_list.append(resistor)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            

if __name__ == "__main__":
    manager = CResistorViewListManager()

    # File path
    file_path = "ResistorView.txt"

    # Load characters from file
    manager.instantiate_list_from_flat_file(file_path)

    # Print loaded characters
    print("\nLoaded Characters:")
    manager.print_list()