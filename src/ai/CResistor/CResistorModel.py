# ------------------------ core class ------------------------
class CResistorModel:
    def __init__(self, guid: str, resistance: int = -1, current: int = -1, voltage: int = -1):
        self.guid = guid
        self.resistance = resistance
        self.current = current
        self.voltage = voltage

    # ------------------------ methods ------------------------
    def calc_voltage(self):
        self.voltage = self.current * self.resistance


# ------------------------ list manager class ------------------------
class CResistorModelListManager:
    def __init__(self):
        self.resistor_list: list[CResistorModel] = []

    # ------------------------ list manager methods ------------------------
    def print_list(self):
        if not self.resistor_list:
            print("Resistor list is empty.")
            return
        for resistor in self.resistor_list:
            print(f"GUID: {resistor.guid}, R: {resistor.resistance}, I: {resistor.current}, V: {resistor.voltage}")

    def find_by_name_list(self, guid: str):
        return [r for r in self.resistor_list if r.guid == guid]

    # ------------------------ instantiation ------------------------
    def instantiate_from_flat_file(self, filename: str = "ResistorModel.txt"):
        self.resistor_list = []
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # skip comments or empty lines
                guid, resistance, current = line.split(",")
                resistor = CResistorModel(
                    guid.strip(),
                    int(resistance.strip()),
                    int(current.strip()),
                )
                resistor.calc_voltage()
                self.resistor_list.append(resistor)
        except FileNotFoundError:
            print(f"File {filename} not found.")


# ------------------------ sample file ------------------------
"""
Sample content of ResistorModel.txt
-----------------------------------
# guid,resistance,current,voltage
R1,100,2,200
R2,220,1,220
R3,330,3,990
"""


# ------------------------ main ------------------------
if __name__ == "__main__":
    manager = CResistorModelListManager()
    manager.instantiate_from_flat_file("ResistorModel.txt")

    print("Printing all resistors in the list:")
    manager.print_list()

    search_guid = "R2"
    print(f"\nSearching for resistor with GUID = {search_guid}")
    found = manager.find_by_name_list(search_guid)
    for r in found:
        print(f"Found -> GUID: {r.guid}, R: {r.resistance}, I: {r.current}, V: {r.voltage}")
