from icecream import ic
import argparse
class CDescendantModel:
    def __init__(self, name_p):
        self.name = name_p
        self.descendant_list = []
        self.age = -1
        
    def add_child(self, input_child_name_p):
        child_model_obj = CDescendantModel(input_child_name_p)
        self.descendant_list.append(child_model_obj)
        return child_model_obj
    
    def find_descendant_by_namev2(self, which_name_p):
        descendant_ptr_l = None
        for cn_descendant in self.descendant_list:
            if cn_descendant.name == which_name_p:
                descendant_ptr_l = cn_descendant
                return descendant_ptr_l
        for cn_descendant in self.descendant_list:
            temp = cn_descendant.find_descendant_by_namev2(which_name_p)
            if temp != None:
                descendant_ptr_l = temp
                return descendant_ptr_l
    
    def calculate_number_of_descendants(self):
        counter = len(self.descendant_list)
        for cn in self.descendant_list:
            ret = cn.calculate_number_of_descendants()
            counter += ret
        return counter
        
        
if __name__ == "__main__": 
    ic.configureOutput(includeContext=True)

    #@debug_log
    def print_tree(parent_obj_p:CDescendantModel) -> None:
        for child_obj in parent_obj_p.descendant_list:
            ic(parent_obj_p.name,child_obj.name) 
        for child_obj in parent_obj_p.descendant_list:
            print_tree(child_obj)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'find':
        ic(args['test'])
        ########test_data########
        root_obj = CDescendantModel("root")
        vo_neiva_obj = CDescendantModel("vo neiva")
        vo_neiva_obj = CDescendantModel("vo neiva")
        root_obj.descendant_list.append(vo_neiva_obj)
        gildo_obj = CDescendantModel("gildo")
        vo_neiva_obj.descendant_list.append(gildo_obj)
        anna_obj = CDescendantModel("anna")
        vo_neiva_obj.descendant_list.append(anna_obj)
        descendant_obj = root_obj.find_descendant_by_namev2("anna")
        matt_obj = CDescendantModel("matt")
        descendant_obj.descendant_list.append(matt_obj)
        print_tree(root_obj)
        ic(descendant_obj.name)
        #########################
        ########test_data########
    elif args['test'] == 'calculate':
        ########test_data########
        root_obj = CDescendantModel("root")
        vo_neiva_obj = CDescendantModel("vo neiva")
        root_obj.descendant_list.append(vo_neiva_obj)
        gildo_obj = CDescendantModel("gildo")
        vo_neiva_obj.descendant_list.append(gildo_obj)
        anna_obj = CDescendantModel("anna")
        vo_neiva_obj.descendant_list.append(anna_obj)
        num_of_descendants = root_obj.calculate_number_of_descendants()
        ic(num_of_descendants)
        print_tree(root_obj)
        ########test_data######## 
    elif args['test'] == 'add_child':
        ########test_data########
        root_obj = CDescendantModel("root")
        ic(args['test'])
        input_child_name = "vo neiva"
        vo_neiva_obj = root_obj.add_child(input_child_name)
        input_child_name = "gildo"
        gildo_obj = vo_neiva_obj.add_child(input_child_name)
        input_child_name = "alex"
        alex_obj = gildo_obj.add_child(input_child_name)
        input_child_name = "julio"
        alex_obj.add_child(input_child_name)
        num_of_descendants = root_obj.calculate_number_of_descendants()
        ic(num_of_descendants)
        print_tree(root_obj)