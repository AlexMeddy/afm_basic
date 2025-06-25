import sys
sys.path.append("..\\lib")
from icecream import ic
from camlog import debug_log
class CDescendant:
    @debug_log
    def __init__(self, name_p):
        self.name = name_p
        self.descendant_list = []
        self.age = -1
        
    @debug_log
    def calculate_number_of_descendants(self):
        counter = len(self.descendant_list)
        for cn in self.descendant_list:
            ret = cn.calculate_number_of_descendants()
            counter += ret
        return counter
        
    @debug_log
    def find_descendant_by_name(self, which_name_p):
        rc = -1
        if self.name == which_name_p:
            rc = 1
        else:
            rc = 0
            for cn in self.descendant_list:
                rc = cn.find_descendant_by_name(which_name_p)
                if rc == 1:
                    break
        return rc    
    @debug_log
    def find_descendant_by_namev2(self, which_name_p):
        descendant_ptr_l = None
        ###checking each direct descendant
        for cn_descendant in self.descendant_list:
            if cn_descendant.name == which_name_p:
                descendant_ptr_l = cn_descendant
                return descendant_ptr_l
        ###ask each indirect descendant to find
        for cn_descendant in self.descendant_list:
            temp = cn_descendant.find_descendant_by_namev2(which_name_p)
            if temp != None: #found
                descendant_ptr_l = temp
                return descendant_ptr_l
