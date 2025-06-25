from CCar import CCar
class CDealership:
    def __init__(self):
        self.car_list = []
    
    def find_model(self, model_p):
        which_node_l = None
        for cn_obj_ptr_l in self.car_list:
            if cn_obj_ptr_l.model == model_p:
                which_node_l = cn_obj_ptr_l
                break       
        return which_node_l
    
    def find_model_index(self, model_p):
        which_node_index_l = -1
        for car_index_l in range(0, len(self.car_list)):            
            if self.car_list[car_index_l].model == model_p:
                which_node_index_l = car_index_l
                break       
        return which_node_index_l
        
    def calculate_per_model_v1(self):
        self.car_list = []
        file = open('car_model.txt', 'r') 
        lines = file.readlines()           
        for line_l in lines:  
            model_l = line_l #extracting model from line
            print("TESTING 001 model = {} size = {:d}".format(model_l, len(model_l)))
            which_node_l = self.find_model(model_l)
            if which_node_l == None: #not found
                car_obj_l = CCar(model_l)
                print("TESTING 002 model = {}".format(model_l))
                self.car_list.append(car_obj_l) 
            else:
                which_node_l.number_of_sold_cars +=1
        for cn in self.car_list:    #the whole list
            print("car model: {} how many were sold: {:d}".format(cn.model, cn.number_of_sold_cars))
    
    def calculate_per_model_v2(self):
        self.car_list = []
        file = open('car_model.txt', 'r') 
        lines = file.readlines()           
        for line_l in lines:  
            model_l = line_l #extracting model from line
            print("TESTING 001 model = {} size = {:d}".format(model_l, len(model_l)))
            which_node_l = self.find_model_index(model_l)
            if which_node_l == -1: #not found
                car_obj_l = CCar(model_l)
                print("TESTING 002 model = {}".format(model_l))
                self.car_list.append(car_obj_l) 
            else:
                self.car_list[which_node_l].number_of_sold_cars +=1
        for cn in self.car_list:    #the whole list
            print("car model: {} how many were sold: {:d}".format(cn.model, cn.number_of_sold_cars))
