from icecream import ic
import argparse

class CPeople:
    def __init__(self, name_p):
        self.name = name_p
        self.length = 0
        self.children_list = []
        self.s = 0
        self.e = 0
        self.unl = []
        self.bnopta = 0
        
def calculate_start_end_layer_for_all_people(current_person_p):
    ic(current_person_p.name, current_person_p.length, current_person_p.s, current_person_p.e)
    for cn in current_person_p.children_list:
        cn.s = current_person_p.e
        cn.e = cn.s + cn.length
        calculate_start_end_layer_for_all_people(cn)
        
def transfer_useful_nodes(root_p, which_task_p): #always root, if the unneccessary nodes are in the lis everything will be upse
    for cn in root_p.children_list:
        temp = calc_vt(cn, which_task_p)
        if temp.s != -1 and temp.e != -1:
            which_task_p.unl.append(cn)
        transfer_useful_nodes(cn, which_task_p)
    return which_task_p.unl

def calc_vt(t1_p, t2_p):
    temp = CPeople("temp")
    temp.s = -1
    temp.e = -1
    if t2_p.s < t1_p.s and t2_p.e < t1_p.s: #1, t1 left and t2 right
        ic()
        temp.s = -1
        temp.e = -1
    elif t2_p.s > t1_p.e and t2_p.e > t1_p.e: #2 t1 right and t2 left
        ic()
        temp.s = -1
        temp.e = -1
    elif t2_p.s < t1_p.s and t2_p.e < t1_p.e and t2_p.e > t1_p.s: #3 t1 starts before t2 start
        ic()
        temp.s = t1_p.s
        temp.e = t2_p.e
    elif t2_p.s > t1_p.s and t2_p.s < t1_p.e and t2_p.e < t1_p.e and t2_p.e > t1_p.s: #4
        ic()
        temp.s = t2_p.s
        temp.e = t2_p.e
    elif t2_p.s > t1_p.s and t2_p.s < t1_p.e and t2_p.e > t1_p.e: #5
        ic()
        temp.s = t2_p.s
        temp.e = t1_p.e
    elif t2_p.s < t1_p.s and t2_p.e > t1_p.e: #6
        ic()
        temp.s = t1_p.s
        temp.e = t1_p.e
    elif t2_p.s == t1_p.s and t2_p.e < t1_p.e: #7
        ic()
        temp.s = t1_p.s
        temp.e = t2_p.e
    elif t2_p.s == t1_p.s and t2_p.e > t1_p.e: #8
        ic()
        temp.s = t1_p.s
        temp.e = t1_p.e
    elif t2_p.s > t1_p.s and t2_p.e == t1_p.e: #9
        ic()
        temp.s = t1_p.s
        temp.e = t2_p.e
    elif t2_p.s < t1_p.s and t2_p.e == t1_p.e: #10
        ic()
        temp.s = t1_p.s
        temp.e = t1_p.e
    elif t2_p.s == t1_p.s and t2_p.e == t1_p.e: #11
        ic()
        temp.s = t1_p.s
        temp.e = t1_p.e
    return temp
    
def calculate_biggest_number_of_pp_of_1_person(person_p):
    vt = person_p
    ic(person_p.name, person_p.s, person_p.e, vt.name)
    for child in person_p.unl:
        ic(person_p.name, child.name)
        vt = calc_vt(child, vt)
        if vt.s != -1 and vt.e != -1:
            person_p.bnopta +=1
    return person_p.bnopta
    
def calc_max_parallel_people_for_all_people(current_node_p, mnopp_p, bnopp_p, root_p):
    ic(current_node_p.name, root_p.name)
    for cn in current_node_p.children_list:
        cn.unl = transfer_useful_nodes(root_p, cn)    #for each task
        bnopp_p = calculate_biggest_number_of_pp_of_1_person(cn)
        ic(bnopp_p)        
        bnopp_p = calc_max_parallel_people_for_all_people(cn, bnopp_p, bnopp_p, root_p) 
        if bnopp_p > mnopp_p:
            mnopp_p = bnopp_p
    return mnopp_p

if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'calc_vt1':
        root = CPeople("root")
        root.length = 0
        a = CPeople("a")
        a.length = 1
        b = CPeople("b")
        b.length = 1
        c = CPeople("c")
        c.length = 1
        d = CPeople("d")
        d.length = 1
        e = CPeople("e")
        e.length = 1
        f = CPeople("f")
        f.length = 1
        g = CPeople("g")
        g.length = 1
        h = CPeople("h")
        h.length = 1
        
        root.children_list.append(a)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(d)
        b.children_list.append(e)
        b.children_list.append(f)
        d.children_list.append(g)
        d.children_list.append(h)
        
        calculate_start_end_layer_for_all_people(root)
        unl = transfer_useful_nodes(root, a)
        for cn in unl:
            ic(cn.name)
        ic('testing calc vt')
        vt = calc_vt(a, b)
        ic(vt.s, vt.e)
            
        #bnopt = calc_max_parallel_people_for_all_people(root, 0, 0, root)
        #ic(bnopt)
        
