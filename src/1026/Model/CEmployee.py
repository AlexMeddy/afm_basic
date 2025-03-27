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
        self.w = 0
        self.h = 0
        self.unl = []
        self.bnopta = 0

def draw_block_tree(root_p, x_p, y_p, w_p, h_p):
    y = y_p+60
    x = x_p-60
    for cn in root_p.children_list:
        x+=60
        ic(cn.name, x, y)
        square_rect = pygame.Rect(x, y, w_p, h_p)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 
        text = font.render(cn.name, True, (0,0,0))
        screen.blit(text, (x+w_p/2, y+h_p/2))
        draw_block_tree(cn, x, y, w_p, h_p)    
        
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
        a.w = 60
        a.h = 60
        b = CEmployee("b")
        b.length = 1
        b.w = 60
        b.h = 60
        c = CEmployee("c")
        c.length = 1
        c.w = 60
        c.h = 60
        d = CEmployee("d")
        d.length = 1
        d.w = 60
        d.h = 60
        e = CEmployee("e")
        e.length = 1
        e.w = 60
        e.h = 60
        f = CEmployee("f")
        f.length = 1
        f.w = 60
        f.h = 60
        g = CEmployee("g")
        g.length = 1
        g.w = 60
        g.h = 60
        h = CEmployee("h")
        h.length = 1
        h.w = 60
        h.h = 60
        
        root.children_list.append(a)
        a.children_list.append(b)
        a.children_list.append(c)
        a.children_list.append(d)
        b.children_list.append(e)
        b.children_list.append(f)
        d.children_list.append(g)
        d.children_list.append(h)
        
        calculate_start_end_layer_for_all_people(root)
        ic('testing calc vt')
        vt = calc_vt(b, c)
        ic(vt.s, vt.e)
            
        bnopt = calc_max_parallel_people_for_all_people(root, 0, 0, root)
        ic(bnopt)
        
        #run = True
        #while run:
        
        y_p=60
        x_p=60
        draw_block_tree(root, x_p, y_p, 50, 50)     
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
        sys.exit()     
        #pygame.quit()
