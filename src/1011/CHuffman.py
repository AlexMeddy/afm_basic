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
    
    def find_by_ascii(self, ascii_p):
        which_node_l = None
        for cn_obj_ptr_l in self.char_list:
            if cn_obj_ptr_l.ascii_a == ascii_p:
                which_node_l = cn_obj_ptr_l
                break 
        return which_node_l
        
    def calculate_input_string(self):
        input_char = input("please enter a string: ")
        for a in input_char:
            chr_name_l = a 
            print(chr_name_l)
            which_node_l = self.find_by_name(chr_name_l)
            if which_node_l == None:
                self.char_list.append(CCharacter(chr_name_l))
            else:
                which_node_l.frequency +=1
        for cn in self.char_list:
            print("name = {} frequency = {:d}".format(cn.name, cn.frequency))
    
    def calculate_v2(self):
        file = open("char_test_file.txt", "r")
        while True:
            c = file.read(1) #c is single character
            chr_name_l = c
            if not c:   #if c == False end of file EOF
                break
            print("type of chr_name_l = {} contents of chr_name_l = {}".format(type(chr_name_l), chr_name_l))
            which_node_l = self.find_by_name(chr_name_l)
            if which_node_l == None: #not found
                self.char_list.append(CCharacter(chr_name_l))
            else: #found
                which_node_l.frequency +=1
        
    def calculate_v3(self):
        file = open("char_test_file.txt", "r")
        while True:
            c = file.read(1) #c is single character
            if not c:   #if c == False end of file EOF
                break
            ascii_l = ord(c)
            print("type of ascii_l = {} contents of ascii_l = {}".format(type(ascii_l), ascii_l))
            which_node_l = self.find_by_ascii(ascii_l)
            if which_node_l == None: #not found
                self.char_list.append(CCharacter(ascii_l))
            else: #found
                which_node_l.frequency +=1    