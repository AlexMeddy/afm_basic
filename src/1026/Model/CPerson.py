import argparse
from icecream import ic

__padding__ = ''
class CPersonModel:
    h = 0
    deepest_level = -1
    #pg:int = 2
    #pg = 2 
    # ^^^ shared attribute across all object instances
    def __init__(self, name_p:str) -> None:
        self.name = name_p
        self.children_list = []
        self.age = -1

def __print_list_recursive__(parent_p:CPersonModel, temp_p:int, parent_depth_p:int) -> None: 
    global __padding__
    #print('{}-----------------start-----------------'.format(__padding__))
    print(f'{__padding__}---------------start----------------')
    #ic(parent_p.__dict__)
    print(f'{__padding__}--------dealing with children-------')
    for cn in parent_p.children_list:
        ic(parent_p.name, cn.name)
    for cn in parent_p.children_list:
        __padding__ += '     '
        __print_list_recursive__(cn, temp_p) 
    print(f'{__padding__}---------------end------------------')
    # removing padding
    PT = ''
    for cn_i in range(5, len(__padding__)-1): 
        PT += (__padding__[cn_i])
    #__padding__ -= '           '  
    __padding__ = PT  
    
def print_list_recursive_2(parent_p):
    for cn in parent_p.children_list:
        ic(parent_p.name, cn.name)
    for cn in parent_p.children_list:
        print_list_recursive_2(cn)

def print_list_recursive_3(parent_p, parent_depth_p):
    call_depth = parent_depth_p + 1
    print(f'{calc_iden(call_depth)}[start] parent_p = {parent_p.name}')
    ic(parent_depth_p, call_depth)
    for cn in parent_p.children_list:
        ic(parent_p.name, cn.name)
    for cn in parent_p.children_list:
        print_list_recursive_3(cn, call_depth)
    print(f'{calc_iden(call_depth)}[ end ] parent_p = {parent_p.name}')
        
def calc_iden(nested_depth_p):
    return "----" * nested_depth_p
        
def find_height(pl_p, parent_obj_p):
    level = 1 + pl_p
    print(f'{calc_iden(level)}[start] parent_p = {parent_obj_p.name} level = {level} CPersonModel.h = {CPersonModel.h}')
    if len(parent_obj_p.children_list) == 0:
        print(f'{calc_iden(level)}i am a leaf')
    for cn in parent_obj_p.children_list:
        find_height(level, cn)
    if level > CPersonModel.h: #check if needs update
        CPersonModel.h = level
        print(f'{calc_iden(level)}going back update')
    else:
        print(f'{calc_iden(level)}going back NOT update')
    print(f'{calc_iden(level)}[ end ] parent_p = {parent_obj_p.name} level = {level} CPersonModel.h = {CPersonModel.h}')
    return CPersonModel.h

        

if __name__ == "__main__":
    print('bla')
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'structure_testing':
        ic(args['test'])
        root_obj = CPersonModel(name_p = "root")
        gildo_obj = CPersonModel(name_p = "gildo")
        root_obj.children_list.append(gildo_obj)
        ic(gildo_obj.__dict__)
        alex_obj = CPersonModel(name_p = "alex")
        julio_obj = CPersonModel(name_p = "julio")
        gildo_obj.children_list.append(alex_obj)
        ic(gildo_obj.children_list[0].__dict__)
        gildo_obj.children_list.append(julio_obj)
        pablo_obj = CPersonModel(name_p = "pablo")
        alex_obj.children_list.append(pablo_obj)
        print_list_recursive_3(root_obj, -1)
    if args['test'] == 'fh':
        root_obj = CPersonModel(name_p = "root")
        gildo_obj = CPersonModel(name_p = "gildo")
        root_obj.children_list.append(gildo_obj)
        alex_obj = CPersonModel(name_p = "alex")
        julio_obj = CPersonModel(name_p = "julio")
        gildo_obj.children_list.append(alex_obj)
        gildo_obj.children_list.append(julio_obj)
        pablo_obj = CPersonModel(name_p = "pablo")
        julio_obj.children_list.append(pablo_obj)
        pablo_son_obj = CPersonModel(name_p = "pabloijr")
        pablo_obj.children_list.append(pablo_son_obj)
        #print_list_recursive_3(root_obj, -1)
        l = 0
        ic(l)
        ic(CPersonModel.h)
        h = find_height(l, root_obj)
        CPersonModel.h = h
        ic(CPersonModel.h, h)
