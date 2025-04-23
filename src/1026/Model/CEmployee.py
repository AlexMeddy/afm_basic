from icecream import ic
import argparse
import pygame
import sys
import time

pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('Arial', 25)

class CEmployee:
    def __init__(self, name_p):
        self.name = name_p
        self.length = 0
        self.children_list = []
        self.s = 0
        self.e = 0
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.unl = []
        self.bnopta = 0
    
    def get_last_child(self):
        last_node = None
        if len(self.children_list) > 0:
            last_node = self.children_list[len(self.children_list) -1]
            #ic(last_node.name)
        return last_node
        
def draw_block_tree(cn_p, x_p, y_p, w_p, h_p, scale_p):#first sibling gets the same x of the parent and the rest increment by 60 + the last sibling
    x= x_p # x is for the children
    for child in cn_p.children_list: #drawing children of cn_p
        y= child.s * scale_p
        ic(child.name, x, y, child.s, child.e)
        square_rect = pygame.Rect(x, y, w_p, h_p)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 
        time.sleep(1)
        pygame.display.update()  
        text = font.render(child.name, True, (0,0,0))
        screen.blit(text, (x+w_p/2, y+h_p/2))
        draw_block_tree(child, x, y, w_p, h_p, scale_p)    
        x += 60
        
def calc_x_y_children(cn_p, scale_p): #first sibling gets the same x of the parent and the rest increment by 60 + the last sibling
    first_sibling_flag = 1
    previous_sibling = None
    for child in cn_p.children_list:
        if first_sibling_flag == 1:
            ic(first_sibling_flag)
            first_sibling_flag = 0
            child.x = cn_p.x # e.g cn_p = a, child = b
        else: #rest of the siblings
            child.x = 60 + previous_sibling.x #e.g c, d
        child.y= child.s * scale_p
        ic(child.name, child.x, child.y)
        previous_sibling = child #e.g child = c, previous_sibling = b
        ic(previous_sibling.name)
        calc_x_y_children(child, scale_p) 

def calc_x_y_children_v2(parent_p, scale_p, uncle_p): #first sibling gets the same x of the parent and the rest increment by 60 + the last sibling
    #previous sibling of root is None, children are A, previous sibling of C is B, no children, previous sibling of D is C and children is G and H
    ic(parent_p.name)       
    first_sibling_flag = 1
    previous_sibling = None
    if uncle_p == None:
        ic('uncle_p == None')
    else:
        ic(uncle_p.name)    
    for child in parent_p.children_list:
        if first_sibling_flag == 1:
            ic(first_sibling_flag)
            first_sibling_flag = 0
            child.x = parent_p.x # e.g parent_p = a, child = b
        else: #rest of the siblings
            child.x = 60 + previous_sibling.x #e.g c, d
        child.y= child.s * scale_p
        ic(child.name, child.x, child.y)
        #previous sibling of root is None, children are A, previous sibling of C is B, no children, previous sibling of D is C and children is G and H
        if uncle_p == None: # no uncle = no cousin
            ic('NC')
        else: #there is uncle
            cousin = uncle_p.get_last_child()
            if cousin != None: # there is cousin
                ic(cousin.name, cousin.x)
            #else:
                #ic('NC')
        calc_x_y_children_v2(child, scale_p, previous_sibling)
        previous_sibling = child #e.g child = c, previous_sibling = b
        ic(previous_sibling.name)
        
def draw_children(cn_p, scale_p):#first sibling gets the same x of the parent and the rest increment by 60 + the last sibling
    for child in cn_p.children_list:
        square_rect = pygame.Rect(child.x, child.y, child.w, child.h)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 
        time.sleep(1)
        pygame.display.update()  
        text = font.render(child.name, True, (0,0,0))
        screen.blit(text, (child.x+child.w/2, child.y+child.h/2))
        draw_children(child, scale_p)    
        
def calculate_start_end_layer_for_all_people(current_person_p):
    ic(current_person_p.name, current_person_p.length, current_person_p.s, current_person_p.e)
    for cn in current_person_p.children_list:
        cn.s = current_person_p.e + 1
        cn.e = cn.length + cn.s
        calculate_start_end_layer_for_all_people(cn)
        
def transfer_useful_nodes(root_p, which_task_p): #always root, if the unneccessary nodes are in the lis everything will be upse
    for cn in root_p.children_list:
        temp = calc_vt(cn, which_task_p)
        if temp.s != -1 and temp.e != -1:
            which_task_p.unl.append(cn)
        transfer_useful_nodes(cn, which_task_p)
    return which_task_p.unl

def calc_vt(t1_p, t2_p):
    temp = CEmployee("temp")
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
    for cn in current_node_p.unl:
        ic(current_node_p.name, cn.name)
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
        root = CEmployee("root")
        root.length = 0
        a = CEmployee("a")
        a.length = 1
        a.w = 50
        a.h = 50
        b = CEmployee("b")
        b.length = 1
        b.w = 50
        b.h = 50
        c = CEmployee("c")
        c.length = 1
        c.w = 50
        c.h = 50
        d = CEmployee("d")
        d.length = 1
        d.w = 50
        d.h = 50
        e = CEmployee("e")
        e.length = 1
        e.w = 50
        e.h = 50
        f = CEmployee("f")
        f.length = 1
        f.w = 50
        f.h = 50
        g = CEmployee("g")
        g.length = 1
        g.w = 50
        g.h = 50
        h = CEmployee("h")
        h.length = 1
        h.w = 50
        h.h = 50
        i = CEmployee("i")
        i.length = 1
        i.w = 50
        i.h = 50
        
        root.children_list.append(a)
        a.children_list.append(b) 
        a.children_list.append(c)
        a.children_list.append(d)
        b.children_list.append(e)
        b.children_list.append(f)
        d.children_list.append(g)
        d.children_list.append(h)
        c.children_list.append(i)
        
        
        calculate_start_end_layer_for_all_people(root)
        ic('testing calc vt')
        vt = calc_vt(b, c)
        ic(vt.s, vt.e)
            
        bnopt = calc_max_parallel_people_for_all_people(root, 0, 0, root)
        ic(bnopt)
        
        #run = True
        #while run:
        
        y_p=0
        x_p=0
        #previous sibling of root is None, children are A, previous sibling of C is B, no children, previous sibling of D is C and children is G and H
        calc_x_y_children_v2(root, 100, None)     
        draw_children(root, 100)
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
        sys.exit()     
        #pygame.quit()
