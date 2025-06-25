import sys
import argparse
sys.path.append("..\\Model")
sys.path.append("..\\..\\lib")
from CDescendantModel import CDescendantModel
from icecream import ic
from camlog import debug_log


class CMainController:
    root_obj: CDescendantModel
    
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
        controller_obj = CMainController()
        root_obj.descendant_list.append(CDescendantModel("vo neiva"))
        root_obj.descendant_list[0].descendant_list.append(CDescendantModel("gildo"))
        root_obj.descendant_list[0].descendant_list.append(CDescendantModel("anna"))
        descendant_obj = root_obj.find_descendant_by_namev2("anna")
        descendant_obj.descendant_list.append(CDescendantModel("matt"))
        print_tree(root_obj)
        ic(descendant_obj.name)
        #########################
    elif args['test'] == 'add_child':
        ########test_data########
        controller_obj = CMainController()
        root_obj = CDescendantModel("root")
        ic(args['test'])
        input_parent_name = "root"
        input_child_name = "vo neiva"
        controller_obj.add_child(root_obj, input_parent_name, input_child_name)
        input_parent_name = "vo neiva"
        input_child_name = "gildo"
        controller_obj.add_child(root_obj, input_parent_name, input_child_name)
        input_parent_name = "gildo"
        input_child_name = "alex"
        controller_obj.add_child(root_obj, input_parent_name, input_child_name)
        input_parent_name = "gildo"
        input_child_name = "julio"
        controller_obj.add_child(root_obj, input_parent_name, input_child_name)
        num_of_descendants = root_obj.calculate_number_of_descendants()
        ic(num_of_descendants)
        print_tree(root_obj)
        ########test_data########
    elif args['test'] == 'calculate':
        ########test_data########
        root_obj = CDescendantModel("root")
        controller_obj = CMainController()
        root_obj.descendant_list.append(CDescendantModel("vo neiva"))
        root_obj.descendant_list[0].descendant_list.append(CDescendantModel("gildo"))
        root_obj.descendant_list[0].descendant_list.append(CDescendantModel("anna"))
        num_of_descendants = root_obj.calculate_number_of_descendants()
        ic(num_of_descendants)
        print_tree(root_obj)
        ########test_data########