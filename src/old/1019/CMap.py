from CPath import CPath
from CLocation import CLocation
class CMap:
    def __init__(self):
        self.location_list = []
        self.path_list = []
    
    def calculate_shortest_distance(self):
        self.location_list.append(CLocation("house"))
        self.location_list.append(CLocation("robina town centre"))
        self.location_list.append(CLocation("burleigh beach"))
        self.path_list.append(CPath(12, "house", "burleigh"))
        self.path_list.append(CPath(5, "town centre", "school"))
        return self.location_list, self.path_list

map_obj_l = CMap()
location_list_l, path_list_l = map_obj_l.calculate_shortest_distance()
for cn in location_list_l:
    print(cn.name)
for cn in path_list_l:
    print(cn.distance)