from CResistorView import CResistorViewListManager
from CResistorModel import CResistorModelListManager
from CResistorModel import CResistorModel
from CResistorView import CResistorView

class CController:
        
    def print_list(view_list_p):
        for child in view_list_p:
            print(child.guid)        
            
    @staticmethod        
    def instantiate_list_from_modelv2(filename: str):
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
        
    @staticmethod        
    def instantiate_resistor_view_lm_from_model(resistor_model_lm_p):
        resistor_view_lm = CResistorViewListManager()
        for resistor_model_child in resistor_model_lm_p.resistor_list:
            resistor_view_child = CResistorView(resistor_model_child.guid + "v", resistor_model_child.resistance,
                resistor_model_child.current, 100, 100)
            resistor_view_lm.add_child(resistor_view_child)
        return resistor_view_lm
        
if __name__ == "__main__":
    # File path
    file_path = "ResistorModel.txt"
    resistor_model_lm = CResistorModelListManager()
    resistor_model_lm.instantiate_from_flat_file(file_path)   
    resistor_view_lm = CController.instantiate_resistor_view_lm_from_model(resistor_model_lm)
    if resistor_view_lm:
        CController.print_list(resistor_view_lm.resistor_list)   
        
    resistor_list_view = []
    resistor_list_model = []
    resistor_list_model.append(CResistorModel('a', 10, 10))
    resistor_list_model.append(CResistorModel('b', 10, 10))
    for child in resistor_list_model:
        print(child.guid)
        
    for child in resistor_list_model:
        view_obj = CResistorView(child.guid + 'v', 10, 10, 100, 100)
        resistor_list_view.append(view_obj)
    for child in resistor_list_view:
        print(child.guid)
    