class CState:
    def __init__(self, name_p):
        self.name = name_p
        self.city_list = []
    
    def find_city_by_name(self, which_name_p):
        rc = -1
        for cn in self.city_list:
            if cn.name == which_name_p:
                rc = 1
                return rc
            else:
                rc = 0
        return rc
        
    def find_city_by_namev2(self, which_name_p):
        city_ptr_l = None
        for cn in self.city_list:
            if cn.name == which_name_p:
                city_ptr_l = cn
                return city_ptr_l
            else:
                return 
        return city_ptr_l 