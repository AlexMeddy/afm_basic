from icecream import ic
import argparse

class CBox:
    def __init__(self, name_p):
        self.name = name_p
        self.children_list = []
        self.w = 0
        self.h = 0
        self.aw = 0
        self.ah = 0
        
def calc_longest_ad(nn_p, lad):
    for cn in nn_p.children_list:       
        lad = calc_longest_ad(cn, lad)
        if cn.ad > lad:
            lad = cn.ad
    return lad
    
def calc_abw(nn_p, abw_p): #abh is accumalated box width
    nn_p.aw = nn_p.w + abw_p
    ic(nn_p.name, nn_p.w, nn_p.aw, abw_p)
    for cn in nn_p.children_list:       
        nn_p.aw = calc_abw(cn, nn_p.aw)
    return nn_p.aw
    
def calc_abh(nn_p, abh_p): #abh is accumalated box height
    nn_p.ah = nn_p.h + abh_p
    ic(nn_p.name, nn_p.h, nn_p.ah, abh_p)
    for cn in nn_p.children_list:       
        nn_p.ah = calc_abh(cn, nn_p.ah)
    return nn_p.ah
    
def calc_longest_aw(nn_p, law):
    ic("calc_longest_aw: START")
    ic(nn_p.name, nn_p.aw, law)
    for cn in nn_p.children_list:       
        law = calc_longest_aw(cn, law)
        if cn.aw > law:
            law = cn.aw
    ic("calc_longest_aw: END")
    return law
    
def calc_longest_ah(nn_p, lah):
    for cn in nn_p.children_list:       
        lah = calc_longest_ah(cn, lah)
        if cn.ah > lah:
            lah = cn.ah  
    return lah
    
if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'calc_gd1':
        ic(args['test'])  
        gate = CBox("gate")
        gate.st = 0
        gate.et = 0
        root = CBox("root")
        root.st = 0
        root.et = 0
        b1 = CBox("b1")
        b1.w = 2
        b1.h = 2
        b2 = CBox("b2")
        b2.w = 3
        b2.h = 2
        b3 = CBox("b3")
        b3.w = 4
        b3.h = 2
        b4 = CBox("b4")
        b4.w = 1
        b4.h = 2
        root.children_list.append(b1)
        b1.children_list.append(b2)
        b1.children_list.append(b3)
        w = calc_abw(root, 0)
        h = calc_abh(root, 0)
        ic("the dimensions of the gate are: ", w, h)
        
    if args['test'] == 'calc_gd2':
        ic(args['test'])  
        gate = CBox("gate")
        root = CBox("root")
        b1 = CBox("b1")
        b1.w = 2
        b1.h = 3
        b2 = CBox("b2")
        b2.w = 1
        b2.h = 1
        b3 = CBox("b3")
        b3.w = 2
        b3.h = 2
        b4 = CBox("b4")
        b4.w = 2
        b4.h = 4
        b5 = CBox("b5")
        b5.w = 1
        b5.h = 1
        b6 = CBox("b6")
        b6.w = 2
        b6.h = 6
        root.children_list.append(b1)
        root.children_list.append(b2)
        root.children_list.append(b3)
        root.children_list.append(b5)
        root.children_list.append(b6)
        b3.children_list.append(b4)
        
        w = calc_abw(root, 0)
        h = calc_abh(root, 0)
        ic("the dimensions of the gate are: ", w, h)
    
    if args['test'] == 'calc_gd3':
        ic(args['test'])  
        gate = CBox("gate")
        root = CBox("root")
        b1 = CBox("b1")
        b1.w = 2
        b1.h = 2
        b2 = CBox("b2")
        b2.w = 2
        b2.h = 3
        b3 = CBox("b3")
        b3.w = 1
        b3.h = 1
        b4 = CBox("b4")
        b4.w = 1
        b4.h = 6
        root.children_list.append(b1)
        root.children_list.append(b3)
        root.children_list.append(b4)
        b1.children_list.append(b2)
        
        w = calc_abw(root, 0)
        h = calc_abh(root, 0)
        ic("the dimensions of the gate are: ", w, h)
        
    if args['test'] == 'calc_gd4':
        ic(args['test'])  
        gate = CBox("gate")
        root = CBox("root")
        b1 = CBox("b1")
        b1.w = 6
        b1.h = 2
        b2 = CBox("b2")
        b2.w = 4
        b2.h = 2
        b3 = CBox("b3")
        b3.w = 2
        b3.h = 2
        b4 = CBox("b4")
        b4.w = 2
        b4.h = 4
        root.children_list.append(b1)
        b1.children_list.append(b2)
        b1.children_list.append(b4)
        b2.children_list.append(b3)
        
        w = calc_abw(root, 0)
        lw = calc_longest_aw(root, 0)
        h = calc_abh(root, 0)
        lh = calc_longest_ah(root, 0)
        ic("calc_longest_aw: ", lw, "calc_longest_ah: ", lh)