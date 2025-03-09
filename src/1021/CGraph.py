class CGraph:
    def __init__(self, name_p):
        self.name = name_p
        self.vertex_list = []
        
    def print_all_edges(self):
        print("----------------start print_all_edges-----------------")
        for vertex_cn in self.vertex_list:
            print("vertex_cn.name = {}".format(vertex_cn.name))
            for edge_cn in vertex_cn.edge_list:
                print("edge_cn.name = {}".format(edge_cn.name))
            
                '''
                for coordinate_cn in edge_cn.coordinate_list:
                    print("coordinate_cn.value = {}".format(coordinate_cn.value))
                    for point_cn in coordinate_cn.point_list:
                        print("point_cn.value = {}".format(point_cn.value))
                
            for value_cn in vertex_cn.value_list:
                print("value_cn.value = {}".format(value_cn.value))  
                '''                
        print("----------------end print_all_edges-----------------")
        
            
        
