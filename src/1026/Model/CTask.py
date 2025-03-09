from icecream import ic
import argparse

#test
class CTask:
    #lp = 0
    def __init__(self, name_p, dur_p):
        self.name = name_p
        self.duration = dur_p
        self.children_list = []
        self.ad = 0
        self.st = 0
        self.et = 0
        self.at = []
        self.ap = []
        self.lp_tl = []
        self.unl = []
        self.bnopta = 1
        self.w = 0
        self.h = 0

def print_list_recursive(current_node_p):
    for child in current_node_p.children_list:
        ic(current_node_p.name, child.name)
    for child in current_node_p.children_list:
        print_list_recursive(child)

def print_list_recursive_test(current_node_p, root_p):
    ic(root_p.name)
    for child in current_node_p.children_list:
        ic(current_node_p.name, child.name)
    for child in current_node_p.children_list:
        print_list_recursive(child, root_p)
        
def print_list_recursive_2(current_node_p, parent_depth_p):
    call_depth = parent_depth_p + 1
    print(f'{calc_iden(call_depth)}[start] current_node_p = {current_node_p.name}')
    for child in current_node_p.children_list:
        print_list_recursive_2(child, call_depth)
    print(f'{calc_iden(call_depth)}[ end ] current_node_p = {current_node_p.name}')
        
def calc_iden(nested_depth_p):
    return "----" * nested_depth_p
        
def calculate_longest_duration(current_node_p, pl_p, pad_p):
    ad = current_node_p.duration + pad_p
    if ad > CTask.lp:
        CTask.lp = pad_p + current_node_p.duration
    level = 1 + pl_p
    print(f'{calc_iden(level)}[start] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} ad = {ad} lp = {CTask.lp}')
    for child in current_node_p.children_list:
        calculate_longest_duration(current_node_p = child, pl_p = level, pad_p = ad)
    print(f'{calc_iden(level)}[ end ] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} ad = {ad} lp = {CTask.lp}')

def calculate_longest_duration2(current_node_p, pl_p, pad_p):  #pad is parent
    ad = current_node_p.duration + pad_p
    lp = ad 
    level = 1 + pl_p
    print(f'{calc_iden(level)}[start] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} lp = {lp}')
    for child in current_node_p.children_list:
        child_lp = calculate_longest_duration2(child, level, ad)
        if child_lp > lp:
            lp = child_lp
    print(f'{calc_iden(level)}[ end ] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} lp = {lp}')
    return lp

def calc_which_tasks_old(current_node_p, pl_p, pad_p, pat_p):
    level = 1 + pl_p
    ad = current_node_p.duration + pad_p
    lp = ad 
    pat = pat_p.copy()
    pat.append(current_node_p)    
    at = pat
    lp_tl = at
    print(f'{calc_iden(level)}[start] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} lp = {lp}')
    msg = f'{calc_iden(level)}pat = '
    for cn in pat:
        msg += f'{cn.name}, '
    print(msg)
    msg = f'{calc_iden(level)}at = '
    for cn in at:
        msg += f'{cn.name}, '
    print(msg)
    for child in current_node_p.children_list:
        child_lp, child_lp_tl = calc_which_tasks(child, level, ad, at)
        if child_lp > lp:
            lp = child_lp
            lp_tl = child_lp_tl
    print(f'{calc_iden(level)}[ end ] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} lp = {lp}')
    return lp, lp_tl
    
def calc_which_tasksv2(current_node_p, pl_p, pad_p, pat_p, pst, pet):
    level = 1 + pl_p
    current_node_p.ad = current_node_p.duration + pad_p
    current_node_p.st = pet
    current_node_p.et = pst + current_node_p.duration
    lp = current_node_p.ad 
    pat = pat_p.copy()
    pat.append(current_node_p)    
    current_node_p.at = pat
    current_node_p.lp_tl = current_node_p.at
    print(f'{calc_iden(level)}[start] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} lp = {lp} st = {current_node_p.st} et = {current_node_p.et}')
    msg = f'{calc_iden(level)}pat = '
    for cn in pat:
        msg += f'{cn.name}, '
    print(msg)
    msg = f'{calc_iden(level)}current_node_p.at = '
    for cn in current_node_p.at:
        msg += f'{cn.name}, '
    print(msg)
    msg = f'{calc_iden(level)}current_node_p.ad = {current_node_p.ad}'
    print(msg)
    for child in current_node_p.children_list:
        child_lp, child_lp_tl = calc_which_tasksv2(child, level, current_node_p.ad, current_node_p.at, current_node_p.et, current_node_p.et)
        if child_lp > lp:
            lp = child_lp
            current_node_p.lp_tl = child_lp_tl
    print(f'{calc_iden(level)}[ end ] current_node_p = {current_node_p.name} current_node_p.duration = {current_node_p.duration} level = {level} lp = {lp} st = {current_node_p.st} et = {current_node_p.et}')
    return lp, current_node_p.lp_tl

def calc_how_many_tasks_by_name(num_of_tasks_with_same_name, which_name_p, current_node_p):
    for cn in current_node_p.children_list:
        if cn.name == which_name_p:
            num_of_tasks_with_same_name += 1
        print(num_of_tasks_with_same_name)
        pcl = calc_how_many_tasks_by_name(num_of_tasks_with_same_name, which_name_p, cn)
        num_of_tasks_with_same_name = pcl
    return num_of_tasks_with_same_name

def calc_duplicate_tasks_by_node_name(num_of_tasks_with_same_name, which_node_p, current_node_p):
    for cn in current_node_p.children_list:
        if cn.name == which_node_p.name:
            num_of_tasks_with_same_name += 1
        print(num_of_tasks_with_same_name)
        pcl = calc_how_many_tasks_by_name(num_of_tasks_with_same_name, which_node_p, cn)
        num_of_tasks_with_same_name = pcl
    return num_of_tasks_with_same_name

def find_task_by_name(pl_p, which_name_p, current_node_p):
    cl = 1 + pl_p
    task_ptr_l = None
    print(f'{calc_iden(cl)}[start] current_node_p = {current_node_p.name} cl = {cl} task_ptr_l = {task_ptr_l}')
    if current_node_p.name == which_name_p:
        task_ptr_l = current_node_p
    else: #not found
        for cn in current_node_p.children_list:
            temp = find_task_by_name(cl, which_name_p, cn)
            if temp != None:
                task_ptr_l = temp
                break
    print(f'{calc_iden(cl)}[ end ] current_node_p = {current_node_p.name} cl = {cl} task_ptr_l = {task_ptr_l}')
    return task_ptr_l
    
def check_overlapping(t1, t2):
    overlapping_status = 0
    if t2.st > t1.st and t2.st < t1.et or t2.et > t1.st and t2.et < t1.et or t2.st < t1.st and t2.et > t1.et:
        overlapping_status = 1
    return overlapping_status
        
def calc_intersection(t1_p, t2_p):
    intersection_point = (-1, -1) #intersection_point[0/1]
    if t2_p.st < t1_p.st and t2_p.et < t1_p.st: #1
        intersection_point = (-1, -1)
    elif t2_p.st > t1_p.et and t2_p.et > t1_p.et: #2
        intersection_point = (-1, -1)
    elif t2_p.st < t1_p.st and t2_p.et < t1_p.et and t2_p.et > t1_p.st: #3
        intersection_point = (t1_p.st, t2_p.et)
    elif t2_p.st > t1_p.st and t2_p.st < t1_p.et and t2_p.et < t1_p.et and t2_p.et > t1_p.st: #4
        intersection_point = (t2_p.st, t2_p.et)
    elif t2_p.st > t1_p.st and t2_p.st < t1_p.et and t2_p.et > t1_p.et: #5
        intersection_point = (t2_p.st, t1_p.et)
    elif t2_p.st < t1_p.st and t2_p.et > t1_p.et: #6
        intersection_point = (t1_p.st, t1_p.et)
    return intersection_point
    
def calc_vt(t1_p, t2_p):
    temp = CTask("temp", 0)
    temp.st = -1
    temp.et = -1
    if t2_p.st < t1_p.st and t2_p.et < t1_p.st: #1, t1 left and t2 right
        temp.st = -1
        temp.et = -1
    elif t2_p.st > t1_p.et and t2_p.et > t1_p.et: #2 t1 right and t2 left
        temp.st = -1
        temp.et = -1
    elif t2_p.st < t1_p.st and t2_p.et < t1_p.et and t2_p.et > t1_p.st: #3 t1 starts before t2 start
        temp.st = t1_p.st
        temp.et = t2_p.et
    elif t2_p.st > t1_p.st and t2_p.st < t1_p.et and t2_p.et < t1_p.et and t2_p.et > t1_p.st: #4
        temp.st = t2_p.st
        temp.et = t2_p.et
    elif t2_p.st > t1_p.st and t2_p.st < t1_p.et and t2_p.et > t1_p.et: #5
        temp.st = t2_p.st
        temp.et = t1_p.et
    elif t2_p.st < t1_p.st and t2_p.et > t1_p.et: #6
        temp.st = t1_p.st
        temp.et = t1_p.et
    elif t2_p.st == t1_p.st and t2_p.et < t1_p.et: #7
        temp.st = t1_p.st
        temp.et = t2_p.et
    elif t2_p.st == t1_p.st and t2_p.et > t1_p.et: #8
        temp.st = t1_p.st
        temp.et = t1_p.et
    elif t2_p.st > t1_p.st and t2_p.et == t1_p.et: #9
        temp.st = t1_p.st
        temp.et = t2_p.et
    elif t2_p.st < t1_p.st and t2_p.et == t1_p.et: #10
        temp.st = t1_p.st
        temp.et = t1_p.et
    return temp
    
def calc_intersection_total_delete(current_node, pip):
    ip = (-1, -1)
    for child in current_node.children_list:
        ip = calc_intersection(current_node, child)
        ic(ip, current_node.name, child.name)
    return ip
    
def calc_total_vt(current_node, pr):
    ic(type(current_node), current_node.name, current_node.st, current_node.et)
    ic(type(pr), pr.name, pr.st, pr.et)   
    temp = calc_vt(current_node, pr)
    if temp.st != -1 and temp.et != -1:
        vt = temp
    else:
        vt = pr
    for child in current_node.children_list:
        vt = calc_total_vt(child, vt)
        ic(vt.name, current_node.name, child.name)
        ic(type(vt))
        ic(vt.st, vt.et)
    return vt 

def calc_total_vt_linear(task_p):
    ic(task_p.name)
    vt = task_p
    for child in task_p.unl:
        vtr = calc_vt(child, vt)
        if vtr.st != -1 and vtr.et != -1:
            vt = vtr
        ic(vt.st, vt.et)
    return vt    
    
def convert_list_into_flat(parent_p, l_list_p):
    for cn in parent_p.children_list:
        l_list_p.append(cn)
        convert_list_into_flat(cn, l_list_p)
    return l_list_p
    
def calc_total_duration_linear(l_list_p):
    ad = 0
    for cn in l_list_p:
        ad = ad + cn.duration      
    return ad
        
def bla(o1, o2):
    res = o1 + o2
    return res
    
def calculate_total_bla(current_node_p, pad_p):
    ad = bla(current_node_p.duration, pad_p) 
    for child in current_node_p.children_list:
        ad = calculate_total_duration(current_node_p = child, pad_p = ad)
    return ad
    
def calculate_total_duration(current_node_p, pad_p):
    ad = current_node_p.duration + pad_p
    for child in current_node_p.children_list:
        ad = calculate_total_duration(current_node_p = child, pad_p = ad)
    return ad


#REVIEWED 3 methods    

def calculate_biggest_number_of_pt_of_1_task(task_p):
    vt = task_p
    ic(task_p.name, task_p.st, task_p.et, vt.name)
    for child in task_p.unl:
        ic(task_p.name, child.name)
        vt = calc_vt(child, vt)
        if vt.st != -1 and vt.et != -1:
            task_p.bnopta +=1
    return task_p.bnopta
    
def calc_max_parallel_tasks_for_all_tasks(current_node_p, mnopt_p, bnopt_p, root_p):
    ic(current_node_p.name, root_p.name)
    for cn in current_node_p.children_list:
        cn.unl = transfer_useful_nodes(root_p, cn)    #for each task
        bnopt_p = calculate_biggest_number_of_pt_of_1_task(cn)
        ic(bnopt_p)        
        bnopt_p = calc_max_parallel_tasks_for_all_tasks(cn, bnopt_p, bnopt_p, root_p) 
        if bnopt_p > mnopt_p:
            mnopt_p = bnopt_p
    return mnopt_p

def transfer_useful_nodes(root_p, which_task_p): #always root, if the unneccessary nodes are in the list everything will be upset
    for cn in root_p.children_list:
        temp = calc_vt(cn, which_task_p)
        if temp.st != -1 and temp.et != -1:
            which_task_p.unl.append(cn)
        transfer_useful_nodes(cn, which_task_p)
        #ic(temp.st, temp.et)
    return which_task_p.unl
    
def calculate_start_end_time_for_all_tasks(root, lp):
    ic(root.name, root.st, root.et)
    for cn in root.children_list:
        cn.st = root.et
        cn.et = cn.st + cn.duration
        ic(cn.name, cn.st, cn.et)
        if cn.duration > lp:
            lp = cn.duration
            ic(lp)
        calculate_start_end_time_for_all_tasks(cn, lp)
    
#REVIEWED 2, 2.1    
def calc_ad_for_all_tasks(nn_p, pad):
    nn_p.ad = nn_p.duration + pad
    ic(nn_p.ad, nn_p.name)
    for cn in nn_p.children_list:
        calc_ad_for_all_tasks(cn, nn_p.ad)

def calc_longest_ad(nn_p, lad):
    for cn in nn_p.children_list:       
        lad = calc_longest_ad(cn, lad)
        if cn.ad > lad:
            lad = cn.ad
    return lad
    
def calc_longest_ad_and_ap(nn_p, lad, dn):
    for cn in nn_p.children_list:
        lad, dn = calc_longest_ad_and_ap(cn, lad, dn)
        if cn.ad > lad:
            lad = cn.ad
            dn = cn
    return lad, dn

def find_critical_path(nn_p, lad, cp_list_p):
    for cn in nn_p.children_list:       
        if cn.ad > lad:
            lad = cn.ad
            cp_list_p.append(cn)
        lad, cp_list_p = find_critical_path(cn, lad, cp_list_p)       
    return lad, cp_list_p
    
def calc_a_path_for_1_task(ct_p, parent_ap_p):
    print("---------------calc_a_path_for_1_task----------------")
    ct_p.ap = parent_ap_p.copy()
    ct_p.ap.append(ct_p)
    for cn_ap in ct_p.ap:
        ic(ct_p.name, cn_ap.name)
    print("---------------calc_a_path_for_1_task----------------")
    return ct_p.ap
    
def calc_a_path_for_all_tasks(pt_p, parent_ap_p):
    for cn in pt_p.children_list:
        cn.ap = calc_a_path_for_1_task(cn, parent_ap_p)
        calc_a_path_for_all_tasks(cn, cn.ap)

def calc_longest_abw(nn_p, labw_p): #abw is accumalated box width
    for cn in nn_p.children_list:       
        labw_p = calc_longest_abw(cn, labw_p)
        if cn.w > labw_p:
            labw_p = cn.w
    return labw_p

if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'calc_intersection':
        ic(args['test'])
        root = CTask("root", 0)
        t1 = CTask("t1", 1)
        t1.st = 5
        t1.et = 8
        t2 = CTask("t2", 2)
        t2.st = 6
        t2.et = 7
        t6 = CTask("t6", 3)
        root.children_list.append(t1)
        root.children_list.append(t6)
        root.children_list.append(t2)
        t3 = CTask("t3", 4)
        t4 = CTask("t4", 5)
        t5 = CTask("t5", 6)
        t7 = CTask("t7", 7)
        t2.children_list.append(t3)
        t2.children_list.append(t4)
        t1.children_list.append(t5)
        t3.children_list.append(t7)
        t61 = CTask("t61", 8)
        t62 = CTask("t62", 9)     
        
        t61.children_list.append(t62)
        t6.children_list.append(t61)
     
        #print_list_recursive_2(t1, -1)
        '''
        pat = []
        lp, lp_tl = calc_which_tasksv2(root, 0, 0, pat.copy(), pst = 0, pet = 0)
        ic(lp)
        print("print lp_tl starts here")
        for cn in lp_tl:
            ic(cn.name)
        print("print lp_tl ends here")        
        '''
        test = CTask("test", 0)
        test.st = -1
        test.et = -1
        root = CTask("root", 0)
        root.st = -1
        root.et = -1
        a = CTask("a", 0)
        a.st = 1
        a.et = 7
        b = CTask("b", 0)
        b.st = 0
        b.et = 12
        c = CTask("c", 0)
        c.st = 8
        c.et = 11
        d = CTask("d", 0)
        d.st = 2
        d.et = 5
        e = CTask("e", 0)
        e.st = 6
        e.et = 10
        f = CTask("f", 0)
        f.st = 2
        f.et = 3
        g = CTask("g", 0)
        g.st = 3
        g.et = 4
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(e)
        a.children_list.append(f)
        
        op = calc_intersection(t1_p = root, t2_p = a)
        op = calc_intersection(t1_p = c, t2_p = e)
        op_t = e
        op_t.st = op[0]
        op_t.et = op[1]
        #op = calc_intersection(t1_p = a, t2_p = b)
        #op = calc_intersection(t1_p = b, t2_p = f)
        ic(op_t.st, op_t.et)
 
    if args['test'] == 'calc_vt1':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = -1
        root.et = -1
        a = CTask("a", 2)
        a.st = 0
        a.et = 12
        b = CTask("b", 4)
        b.st = 1
        b.et = 11
        c = CTask("c", 5)
        c.st = 2
        c.et = 10
        d = CTask("d", 3)
        d.st = 3
        d.et = 9
        e = CTask("e", 1)
        e.st = 4
        e.et = 8
        f = CTask("f", 4)
        f.st = 5
        f.et = 7
        root.children_list.append(a)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(d)
        a.children_list.append(e)
        a.children_list.append(f)
        l_list = []
        calc_ad_for_all_tasks(root)
        lad = calc_longest_ad(root, 0)
        ic(lad)
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
 
    if args['test'] == 'calc_vt2':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = -1
        root.et = -1
        a = CTask("a", 2)
        a.st = 0
        a.et = 12
        b = CTask("b", 4)
        b.st = 1
        b.et = 2
        c = CTask("c", 5)
        c.st = 3
        c.et = 4
        d = CTask("d", 3)
        d.st = 5
        d.et = 6
        e = CTask("e", 1)
        e.st = 7
        e.et = 9
        f = CTask("f", 4)
        f.st = 10
        f.et = 11
        ic(a.name, a.st, a.et)
        ic(b.name, b.st, b.et)
        root.children_list.append(a)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(d)
        a.children_list.append(e)
        a.children_list.append(f)
        l_list = []
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
        #print_list_recursive_test(root)
          
    if args['test'] == 'calc_vt3':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = -1
        root.et = -1
        a = CTask("a", 2)
        a.st = 1
        a.et = 12
        b = CTask("b", 1)
        b.st = 0
        b.et = 13
        c = CTask("c", 3)
        c.st = 3
        c.et = 4
        d = CTask("d", 1)
        d.st = 5
        d.et = 6
        root.children_list.append(a)
        a.children_list.append(c)
        c.children_list.append(b)
        b.children_list.append(d)
        l_list = []
        calc_ad_for_all_tasks(root)
        lad = calc_longest_ad(root, 0)
        ic(lad)
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
    
    if args['test'] == 'calc_vt4':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = -1
        root.et = -1
        a = CTask("a", 2)
        a.st = 1
        a.et = 14
        b = CTask("b", 4)
        b.st = 0
        b.et = 6
        c = CTask("c", 5)
        c.st = 7
        c.et = 15
        d = CTask("d", 3)
        d.st = 8
        d.et = 13
        e = CTask("e", 1)
        e.st = 9
        e.et = 12
        f = CTask("f", 4)
        f.st = 10
        f.et = 11
        root.children_list.append(a)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(d)
        a.children_list.append(e)
        a.children_list.append(f)
        l_list = []
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
    
    if args['test'] == 'calc_vt5':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = -1
        root.et = -1
        a = CTask("a", 2)
        a.st = 0
        a.et = 12
        b = CTask("b", 4)
        b.st = 10
        b.et = 14
        c = CTask("c", 5)
        c.st = 4
        c.et = 10
        d = CTask("d", 3)
        d.st = 5
        d.et = 8
        e = CTask("e", 1)
        e.st = 11
        e.et = 13
        f = CTask("f", 4)
        f.st = 6
        f.et = 9
        root.children_list.append(a)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(d)
        a.children_list.append(e)
        a.children_list.append(f)
        l_list = []
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
    
    if args['test'] == 'calc_vt6':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = -1
        root.et = -1
        a = CTask("a", 6)
        a.st = 4
        a.et = 15
        b = CTask("b", 8)
        b.st = 2
        b.et = 13
        c = CTask("c", 4)
        c.st = 14
        c.et = 18
        d = CTask("d", 2)
        d.st = 6
        d.et = 15
        bu = CTask("bu", 7)
        bu.st = 0
        bu.et = 3
        du = CTask("du", 1)
        du.st = 14
        du.et = 21
        cu = CTask("cu", 3)
        cu.st = 16
        cu.et = 17
        a.children_list.append(du)
        root.children_list.append(a)
        a.children_list.append(cu)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(bu)
        a.children_list.append(d)
        l_list = []
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
    
    if args['test'] == 'calc_vt7':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = 0
        root.et = 0
        a = CTask("a", 2)
        a.st = 6
        a.et = 17
        b = CTask("b", 4)
        b.st = 0
        b.et = 13
        c = CTask("c", 5)
        c.st = 14
        c.et = 16
        d = CTask("d", 3)
        d.st = 4
        d.et = 18
        e = CTask("e", 1)
        e.st = 2
        e.et = 3
        f = CTask("f", 7)
        f.st = 15
        f.et = 19
        g = CTask("g", 2)
        g.st = 16
        g.et = 21
        root.children_list.append(a)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(d)
        a.children_list.append(e)
        a.children_list.append(f)
        a.children_list.append(g)
        l_list = []
        calculate_start_end_time_for_all_tasks(root, 0)
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
        #calculate_longest_duration2(root, 0, 0)
    
    if args['test'] == 'calc_vt8':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = 0
        root.et = 0
        a = CTask("t1", 2)
        a.st = 2
        a.et = 4
        b = CTask("t2", 1)
        b.st = 0
        b.et = 2
        c = CTask("t3", 6)
        c.st = 4
        c.et = 7
        d = CTask("t4", 4)
        d.st = 4
        d.et = 8
        root.children_list.append(a)
        a.children_list.append(b)
        b.children_list.append(c)
        a.children_list.append(d)
        l_list = []
        l_list2 = []
        calc_ad_for_all_tasks(root, 0)
        lad, cp_l_list = find_critical_path(root, 0, l_list2)
        ic(lad)
        print("---------------calc_a_path_for_all_tasks----------------")
        calc_a_path_for_all_tasks(root, l_list)

        for cn in a.ap:
            ic(a.name, " a_path: ", cn.name)
        for cn in b.ap:
            ic(b.name, " a_path: ", cn.name)
        for cn in c.ap:
            ic(c.name, " a_path: ", cn.name)
        for cn in d.ap:
            ic(d.name, " a_path: ", cn.name)
        print("---------------calc_a_path_for_all_tasks----------------")
        print("---------------calc_longest_ad_and_ap----------------")
        lad, apn = calc_longest_ad_and_ap(root, 0, root)
        ic(apn.name)
        ic("the tasks in the critical path are:")
        for cn in apn.ap:
            ic(cn.name)
        print("---------------calc_longest_ad_and_ap----------------")
        l_list = transfer_useful_nodes(root, root)
        for cn in l_list:
            ic(cn.name)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
        calculate_longest_duration2(root, 0, 0)
        
    if args['test'] == 'calc_vt9':
        ic(args['test'])     
        root = CTask("root", 0)
        root.st = 0
        root.et = 0
        a = CTask("t1", 2)
        a.st = 2
        a.et = 4
        b = CTask("t2", 1)
        b.st = 0
        b.et = 2
        c = CTask("t3", 6)
        c.st = 4
        c.et = 7
        d = CTask("t4", 4)
        d.st = 4
        d.et = 8
        root.children_list.append(a)
        a.children_list.append(b)
        b.children_list.append(c)
        a.children_list.append(d)
        calculate_start_end_time_for_all_tasks(root, 0)
        bnopt = calc_max_parallel_tasks_for_all_tasks(root, 0, 1, root)
        ic(bnopt)
    
    if args['test'] == 'calc_vt10':
        ic(args['test'])  
        gate = CTask("gate", 0)
        gate.st = 0
        gate.et = 0
        root = CTask("root", 0)
        root.st = 0
        root.et = 0
        b1 = CTask("b1", 2)
        b1.w = 2
        b1.h = 2
        b2 = CTask("b2", 1)
        b2.w = 3
        b2.h = 2
        b3 = CTask("b3", 6)
        b3.w = 4
        b3.h = 2
        b4 = CTask("b4", 4)
        b4.w = 1
        b4.h = 2
        root.children_list.append(b1)
        b1.children_list.append(b2)
        b1.children_list.append(b3)
        abw = calc_longest_abw(root, 0)
        ic(abw)
        
    if args['test'] == 'calc_vt11':
        ic(args['test'])  
        gate = CTask("gate", 0)
        gate.st = 0
        gate.et = 0
        root = CTask("root", 0)
        root.st = 0
        root.et = 0
        b1 = CTask("b1", 2)
        b1.st = 2
        b1.et = 2
        b2 = CTask("b2", 1)
        b2.w = 3
        b2.h = 2
        b3 = CTask("b3", 6)
        b3.w = 4
        b3.h = 2
        b4 = CTask("b4", 4)
        b4.w = 1
        b4.h = 2
        root.children_list.append(b1)
        b1.children_list.append(b2)
        b1.children_list.append(b3)
        ic("---------calculate_start_end_time_for_all_tasks--------")
        calculate_start_end_time_for_all_tasks(root, 0)
        ic("---------calculate_start_end_time_for_all_tasks--------")
        ic("---------transfer_useful_nodes--------")
        unl = transfer_useful_nodes(root, b2)
        for cn in unl:
            ic(cn.name)
        ic("---------transfer_useful_nodes--------")
        ic("---------calculate_biggest_number_of_pt_of_1_task--------")
        bnopt = calculate_biggest_number_of_pt_of_1_task(root)
        ic("---------calculate_biggest_number_of_pt_of_1_task--------")
        
    if args['test'] == 'find':
        root = CTask("root", 0)
        t1 = CTask("t1", 1)
        t2 = CTask("t2", 20)
        t6 = CTask("t6", 15)
        root.children_list.append(t1)
        root.children_list.append(t6)
        root.children_list.append(t2)
        t3 = CTask("t3", 3)
        t4 = CTask("t4", 8)
        t5 = CTask("t5", 8)
        t7 = CTask("t7", 10)
        t2.children_list.append(t3)
        t2.children_list.append(t4)
        t1.children_list.append(t5)
        t3.children_list.append(t7)
        t61 = CTask("t61", 10)
        t62 = CTask("t62", 40)     
        
        t61.children_list.append(t62)
        t6.children_list.append(t61)
        
        t = find_task_by_name(pl_p = 0, which_name_p = "t1", current_node_p = root)
        ic(t.name if t != None else None )