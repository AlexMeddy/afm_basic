class CCharacterView:
    def __init__(self, guid: str, x: int, y: int, w: int, h: int):
        """Initialize a character with position, size, and default previous coordinates (-1, -1)."""
        self.guid = guid
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.p_x = -1  # Previous x position
        self.p_y = -1  # Previous y position
        self.color = ''

    def __repr__(self):
        """Return a string representation of the character."""
        return (f"CCharacterView(guid='{self.guid}', x={self.x}, y={self.y}, "
                f"w={self.w}, h={self.h}, p_x={self.p_x}, p_y={self.p_y})")
                
    def calc_p_x(self):
        self.p_x = self.x
        
    def calc_p_y(self):
        self.p_y = self.y

    def calc_bla(self):
        self.bla =+1

    def calc_color(self):
        self.colour = (0, 0, 255*self.x)

    def draw(self, screen_p, pygame_p):
        rect_width, rect_height = self.w, self.h
        pygame_p.draw.rect(screen_p, self.colour, (self.p_x, self.p_y, rect_width, rect_height))

class CCharacterViewListManager:
    def __init__(self):
        """Initialize an empty list of characters."""
        self.characters = []
        
    def calc_bla_list(self):
        for child in self.characters:
            child.calc_bla()
            
    def calc_colour_list(self):
        for child in self.characters:
            child.calc_color()
            
    def calc_bla_list(self):
        for child in self.characters:
            child.calc_bla()
            
    def calc_p_x_list(self):
        for child in self.characters:
            child.calc_p_x()
            
    def calc_p_y_list(self):
        for child in self.characters:
            child.calc_p_y()

    def find_by_mouse_pos_list(self, mouse_x_p, mouse_y_p):      
        found=None
        for cn in self.characters:
            if( (mouse_x_p > cn.p_x and mouse_x_p < (cn.p_x+cn.w)) 
                and (mouse_y_p > cn.p_y and mouse_y_p < (cn.p_y+cn.h))):
                    found = cn
                    break
        return found

    def print_list(self):
        """Print all characters in the list."""
        if not self.characters:
            print("No characters available.")
        else:
            for idx, char in enumerate(self.characters):
                print(f"{idx}: {char}")     

    def draw_list(self, screen_p, pygame_p):
        for child in self.characters:
            child.draw(screen_p, pygame_p)

    def instantiate_chars_from_flat_file(self, file_path: str):
        """
        Instantiate characters from a comma-delimited flat file.
        Each line should be: guid,x,y,w,h
        """
        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = [p.strip() for p in line.strip().split(",")]
                    if len(parts) != 5:
                        print(f"Invalid line format: {line.strip()}")
                        continue
                    guid, x_str, y_str, w_str, h_str = parts
                    try:
                        x = int(x_str)
                        y = int(y_str)
                        w = int(w_str)
                        h = int(h_str)
                        self.characters.append(CCharacterView(guid, x, y, w, h))
                    except ValueError:
                        print(f"Invalid numbers in line: {line.strip()}")
            print(f"Characters successfully loaded from '{file_path}'.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")


if __name__ == "__main__":
    manager = CCharacterViewListManager()

    # File path
    file_path = "chars.txt"

    # Load characters from file
    manager.instantiate_chars_from_flat_file(file_path)
    manager.calc_p_x_list()
    manager.calc_p_y_list()
    manager.calc_colour_list()
    manager.draw_list()

    # Print loaded characters
    print("\nLoaded Characters:")
    manager.print_list()
