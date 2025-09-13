from CResistorView import CResistorViewListManager
from CResistorView import CResistorView

class CController:
        
    def print_list(view_manager_list_p):
        for child in view_manager_list_p:
            print(child.guid)
            
            
    @staticmethod        
    def instantiate_list_from_model(filename: str):
        resistor_view_list = []
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    guid, w, h = line.split(",")
                    resistor = CResistorView(guid, -1, -1, int(w), int(h))
                    resistor_view_list.append(resistor) #view_lm_p.add_child()
        except FileNotFoundError:
            print(f"File {filename} not found.")
        return resistor_view_list
        
if __name__ == "__main__":
    # File path
    file_path = "ResistorModel.txt"

    # Load characters from file
    view_list = CController.instantiate_list_from_model(file_path)
    
    if view_list:
        CController.print_list(view_list)