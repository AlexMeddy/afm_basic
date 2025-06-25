import argparse
from icecream import ic

class CPersonModel:
    def __init__(self, name_p:str) -> None:
        self.name = name_p
        self.children_list = []
        self.age = -1

def __print_list_recursive__(parent_p:CPersonModel) -> None:
    for cn in parent_p.children_list:
        ic(parent_p.name, cn.name)
    for cn in parent_p.children_list:
        __print_list_recursive__(cn)   
        
if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'structure_testing':
        ic(args['test'])
        root_obj = CPersonModel(name_p = "root")
        gildo_obj = CPersonModel(name_p = "gildo")
        root_obj.children_list.append(gildo_obj)
        alex_obj = CPersonModel(name_p = "alex")
        julio_obj = CPersonModel(name_p = "julio")
        gildo_obj.children_list.append(alex_obj)
        gildo_obj.children_list.append(julio_obj)
        alex_obj.children_list.append(CPersonModel("pablo"))
        __print_list_recursive__(parent_p = root_obj)