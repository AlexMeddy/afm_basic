import socket			 
from CCharacter import CCharacter
class CHuffman:
    def __init__(self):
        self.char_list = []
        
    def find_by_name(self, name_p):
        which_node_l = None
        for cn_obj_ptr_l in self.char_list:
            if cn_obj_ptr_l.name == name_p:
                which_node_l = cn_obj_ptr_l
                break 
        return which_node_l    
    
    def calculate_char_frequency_of_an_input_string(self, input_char_p):
        for a in input_char_p:
            chr_name_l = a
            print(chr_name_l)
            which_node_l = self.find_by_name(chr_name_l)
            if which_node_l == None: #not found
                self.char_list.append(CCharacter(chr_name_l))
            else: #found
                which_node_l.frequency +=1
        for cn in self.char_list:
            print("character = {} frequency = {:d}".format(cn.name, cn.frequency))
        # close the connection 
        #self.s.close()	
    