from icecream import ic
import argparse
import pygame
import sys
import time

pygame.init()


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('Arial', 25)
class CBus:
    def __init__(self, name_p):
        self.children_list = []
        self.name = name_p
        self.x = 0
        self.y = 0
        self.h = 0
        self.l = 0
        self.r_l = 0
class CEmployee:
    def __init__(self, name_p):
        self.name = name_p
        self.length = 0
        self.children_list = []
        self.previous_sibling = None
        self.s = 0
        self.e = 0
        self.x = 0
        self.rx = 0
        self.ry = 0
        self.y = 0
        self.w = 0
        self.aw = 0
        self.rw = 0
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
            if previous_sibling == None:
                if cousin == None: # there is cousin
                    child.x = parent_p.x
                else:
                    child.x = cousin.x + 60
                    ic(cousin.name, cousin.x)
            else:
                child.x = previous_sibling.x + 60
        calc_x_y_children_v2(child, scale_p, previous_sibling)
        previous_sibling = child #e.g child = c, previous_sibling = b
        ic(previous_sibling.name)
 
def calc_x_y_children_v3(parent_p, scale_p, uncle_p): #first sibling gets the same x of the parent and the rest increment by 60 + the last sibling
    #previous sibling of root is None, children are A, previous sibling of C is B, no children, previous sibling of D is C and children is G and H
    ic(parent_p.name)       
    first_sibling_flag = 1
    previous_sibling = None  
    for child in parent_p.children_list:
        if first_sibling_flag == 1:
            first_sibling_flag = 0
            child.x = parent_p.x # e.g parent_p = a, child = b
        else: #rest of the siblings
            child.x = 60 + previous_sibling.x #e.g c, d
        child.y= child.s * scale_p
        #previous sibling of root is None, children are A, previous sibling of C is B, no children, previous sibling of D is C and children is G and H
        if previous_sibling != None:
            nephew = previous_sibling.get_last_child()
            if nephew != None:
                child.x = nephew.x + 60
        calc_x_y_children_v3(child, scale_p, previous_sibling)
        previous_sibling = child #e.g child = c, previous_sibling = b
        
def calc_y_children(parent_p, scale_p):
    for child in parent_p.children_list:
        child.y= child.s * scale_p
        calc_y_children(child, scale_p)
        
def calc_x_children(parent_p, uncle_p):
    first_sibling_flag = 1
    previous_sibling = None  
    for child in parent_p.children_list:
        if first_sibling_flag == 1:
            first_sibling_flag = 0
            child.x = parent_p.x 
        else:
            child.x = 60 + previous_sibling.x       
        if previous_sibling != None:
            nephew = previous_sibling.get_last_child()
            if nephew != None:
                child.x = nephew.x + 60
        calc_x_children(child, previous_sibling)
        previous_sibling = child #e.g child = c, previous_sibling = b

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
        
def calc_biggest_x(parent_p, biggest_x):
    for cn in parent_p.children_list:
        ic(cn.x)
        if cn.x > biggest_x:
            biggest_x = cn.x
        biggest_x = calc_biggest_x(cn, biggest_x)
    return biggest_x
    
def calc_biggest_y(parent_p, biggest_y):
    for cn in parent_p.children_list:
        ic(cn.y)
        if cn.y > biggest_y:
            biggest_y = cn.y
        biggest_y = calc_biggest_y(cn, biggest_y)
    return biggest_y
    
def calc_ps_of_children(parent_p):
    first_sibling_flag = 1
    previous_child = None
    for child in parent_p.children_list:
        if first_sibling_flag == 1:
            first_sibling_flag = 0
            child.previous_sibling = None
        else:
            child.previous_sibling = previous_child    
        previous_child = child            
        calc_ps_of_children(child)
        
def calc_ps_of_childrenv2(parent_p):
    for i in range(len(parent_p.children_list)):
        ic(i)
        if i == 0:
            parent_p.children_list[i].previous_sibling = None
        else:
            parent_p.children_list[i].previous_sibling = parent_p.children_list[i-1]
        calc_ps_of_childrenv2(parent_p.children_list[i])
        
def calc_x_children_v2(parent_p):
    for cn in parent_p.children_list:
        r3 = 0
        r2 = 0 
        r1 = 0
        ic('testing--------------------------------------')
        ic(cn.name)
        if cn.previous_sibling != None:
            nephew = cn.previous_sibling.get_last_child()
            ic(nephew)
            if nephew != None:
                #child.x = nephew.x + 60
                r3 = 1
                ic(r3)
            else:
                ic("nephew is none")           
        if cn.previous_sibling != None:
            r2 = 1
        if cn.previous_sibling == None:
            r1 = 1   
        ###
        if r3 == 1:
            ic(cn.name, r3)
            cn.x = nephew.x + 20
        elif r2 == 1:
            ic(cn.name, r2)
            cn.x = cn.previous_sibling.x + 20
        if r1 == 1:
            ic(cn.name, r1)
            cn.x = parent_p.x
        calc_x_children_v2(cn)
        
def calc_accumalated_distance_children(parent_p):
    for cn in parent_p.children_list:
        r1 = 0
        r2 = 0
        print("-----------------------calculating rules start-------------------------")
        if cn.previous_sibling != None:
            r2 = 1 
        if cn.previous_sibling == None:
            r1 = 1
        ic(cn.name, r1, r2)
        print("-----------------------calculating rules end-------------------------")
        print("-----------------------selecting rules start-------------------------")
        if r1 == 1:
            ic(cn.name, r1)
            cn.aw = cn.w
            ic(cn.aw)
        elif r2 == 1:
            ic(cn.name, r2)
            cn.aw = cn.w + cn.previous_sibling.aw
            ic(cn.aw)
        print("-----------------------selecting rules end-------------------------")
        calc_accumalated_distance_children(cn)
            
def calc_rx_children(parent_p, scale_p): #x coordinate
    for cn in parent_p.children_list:
        cn.rx = cn.x * scale_p
        calc_rx_children(cn, scale_p)
        
def calc_ry_children(parent_p, scale_p):
    for cn in parent_p.children_list:
        cn.ry = cn.y * scale_p
        calc_ry_children(cn, scale_p)
        

def print_ps(parent_p):
    msg = ('print_ps------------------------------- start---------------')
    ic(msg)
    for cn in parent_p.children_list:        
        msg = ('cn.name = ' + cn.name + ' ps = ' + cn.previous_sibling.name if cn.previous_sibling != None else 'no ps')
        ic(msg)
        print_ps(cn)
    msg = ('print_ps------------------------------- end---------------')
    ic(msg)
    
def print_rx_ry_children(parent_p):
    for cn in parent_p.children_list:
        ic(cn.name)
        ic(cn.rx, cn.ry)
        print_rx_ry_children(cn)
        
def draw_childrenv2(cn_p):#first sibling gets the same x of the parent and the rest increment by 60 + the last sibling
    for child in cn_p.children_list:
        square_rect = pygame.Rect(child.rx, child.y, child.rw, child.h)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 
        time.sleep(1)
        pygame.display.update()  
        text = font.render(child.name, True, (0,0,0))
        screen.blit(text, (child.x+child.w/2, child.y+child.h/2))
        draw_childrenv2(child)    
    
def calc_rw_children(parent_p, scale_p):
    for cn in parent_p.children_list:
        cn.rw = cn.w * scale_p
        ic(cn.rw)
        calc_rw_children(cn, scale_p)
    
if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'calc_vt1_resize':
        root = CEmployee("root")
        root.length = 0
        a = CEmployee("a")
        a.length = 1
        a.w = 10
        a.h = 10
        b = CEmployee("b")
        b.length = 1
        b.w = 10
        b.h = 10
        c = CEmployee("c")
        c.length = 1
        c.w = 10
        c.h = 10
        d = CEmployee("d")
        d.length = 1
        d.w = 10
        d.h = 10
        e = CEmployee("e")
        e.length = 1
        e.w = 10
        e.h = 10
        f = CEmployee("f")
        f.length = 1
        f.w = 10
        f.h = 10
        g = CEmployee("g")
        g.length = 1
        g.w = 10
        g.h = 10
        h = CEmployee("h")
        h.length = 1
        h.w = 10
        h.h = 10
        i = CEmployee("i")
        i.length = 1
        i.w = 10
        i.h = 10
        i2 = CEmployee("i2")
        i2.length = 1
        i2.w = 10
        i2.h = 10
        j = CEmployee("j")
        j.length = 1
        j.w = 10
        j.h = 10
        k = CEmployee("k")
        k.length = 1
        k.w = 10
        k.h = 10
        l = CEmployee("l")
        l.length = 1
        l.w = 10
        l.h = 10
        m = CEmployee("m")
        m.length = 1
        m.w = 10
        m.h = 10
        n = CEmployee("n")
        n.length = 1
        n.w = 10
        n.h = 10
        o = CEmployee("o")
        o.length = 1
        o.w = 10
        o.h = 10
        p = CEmployee("p")
        p.length = 1
        p.w = 10
        p.h = 10
        q = CEmployee("q")
        q.length = 1
        q.w = 10
        q.h = 10
        s = CEmployee("s")
        s.length = 1
        s.w = 10
        s.h = 10
        t = CEmployee("t")
        t.length = 1
        t.w = 10
        t.h = 10
        
        root.children_list.append(a)
        a.children_list.append(b) 
        a.children_list.append(c)
        a.children_list.append(d)
        b.children_list.append(e)
        b.children_list.append(f)
        d.children_list.append(g)
        d.children_list.append(h)
        b.children_list.append(i)
        b.children_list.append(i2)
        b.children_list.append(j)
        b.children_list.append(k)
        b.children_list.append(l)
        b.children_list.append(m)
        b.children_list.append(n)
        b.children_list.append(o)
        b.children_list.append(p)
        b.children_list.append(q)
        b.children_list.append(s)
        b.children_list.append(t)
        
        
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
        #calc_x_y_children_v3(root, 100, None)   
        calc_y_children(root, 20)
        #calc_x_children(root, None)        
        calc_ps_of_children(root)
        print_ps(root)
        calc_x_children_v2(root)
        biggest_x = calc_biggest_x(root, 0)
        ic(biggest_x)
        scale_x = SCREEN_WIDTH / biggest_x
        ic(scale_x)
        #biggest_y = calc_biggest_y(root, 0)
        #ic(biggest_y)
        #scale_y = SCREEN_HEIGHT / biggest_y
        #ic(scale_y)
        calc_rx_children(root, scale_x)
        #calc_ry_children(root, scale_y)
        print_rx_ry_children(root)
        #draw_children(root, 100)
        draw_childrenv2(root)
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
        sys.exit()     
        #pygame.quit()
        
    if args['test'] == 'calc_vt2':
        root = CEmployee("root")
        root.length = 0
        a = CEmployee("a")
        a.length = 1
        a.w = 10
        a.h = 10
        b = CEmployee("b")
        b.length = 1
        b.w = 10
        b.h = 10
        c = CEmployee("c")
        c.length = 1
        c.w = 10
        c.h = 10
        d = CEmployee("d")
        d.length = 1
        d.w = 10
        d.h = 10
        e = CEmployee("e")
        e.length = 1
        e.w = 10
        e.h = 10
        f = CEmployee("f")
        f.length = 1
        f.w = 10
        f.h = 10
        g = CEmployee("g")
        g.length = 1
        g.w = 10
        g.h = 10
        h = CEmployee("h")
        h.length = 1
        h.w = 10
        h.h = 10
        i = CEmployee("i")
        i.length = 1
        i.w = 10
        i.h = 10
        i2 = CEmployee("i2")
        i2.length = 1
        i2.w = 10
        i2.h = 10 
        root.children_list.append(a)
        a.children_list.append(b) 
        a.children_list.append(c)
        a.children_list.append(d)
        b.children_list.append(e)
        b.children_list.append(f)
        d.children_list.append(g)
        d.children_list.append(h)
        b.children_list.append(i)
        b.children_list.append(i2)              
        calculate_start_end_layer_for_all_people(root)
        ic('testing calc vt')
        vt = calc_vt(b, c)
        ic(vt.s, vt.e)            
        bnopt = calc_max_parallel_people_for_all_people(root, 0, 0, root)
        ic(bnopt)
        y_p=0
        x_p=0
        #previous sibling of root is None, children are A, previous sibling of C is B, no children, previous sibling of D is C and children is G and H
        #calc_x_y_children_v3(root, 100, None)   
        calc_y_children(root, 20)
        #calc_x_children(root, None)        
        calc_ps_of_children(root)
        print_ps(root)
        calc_x_children_v2(root)
        biggest_x = calc_biggest_x(root, 0)
        ic(biggest_x)
        scale_x = SCREEN_WIDTH / biggest_x
        ic(scale_x)
        calc_rx_children(root, scale_x)
        calc_rw_children(root, scale_x)
        #draw_children(root, 100)
        draw_childrenv2(root)
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
        sys.exit()     
        #pygame.quit()
        
    if args['test'] == 'calc_vt3':
        root = CBus("root")
        b1 = CBus("b1")
        b1.l = 1000
        b1.y = 201
        b2 = CBus("b2")
        b2.l = 2000
        b2.y = 201
        b3 = CBus("b3")
        b3.l = 3000
        b3.y = 201
        
        #1. plot
        square_rect = pygame.Rect(b1.x, 1, b1.l, 100)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 
        ic(b1.l)
        ic(b2.l)
        ic(b3.l)
        
        square_rect = pygame.Rect(b2.x, 1, b2.l, 100)         
        pygame.draw.rect(screen, (0, 250, 0), square_rect) 

        square_rect = pygame.Rect(b3.x, 1, b3.l, 100)         
        pygame.draw.rect(screen, (0, 0, 250), square_rect) 
        
        pygame.display.update() 
        #2. resize
        all_bus_length = b3.l + b2.l + b1.l
        ic(all_bus_length)
        l_scale = SCREEN_WIDTH / all_bus_length
        b1.r_l = b1.l * l_scale
        ic(b1.r_l)
        b1.x = 0

        square_rect = pygame.Rect(b1.x, b1.y, b1.r_l, 100)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 

        l_scale = SCREEN_WIDTH / all_bus_length
        b2.r_l = b2.l * l_scale
        ic(b2.r_l)
        b2.x = b1.x + b1.r_l
        square_rect = pygame.Rect(b2.x, b2.y, b2.r_l, 100)         
        pygame.draw.rect(screen, (0, 250, 0), square_rect) 

        l_scale = SCREEN_WIDTH / all_bus_length
        b3.r_l = b3.l * l_scale
        ic(b3.r_l)
        b3.x = b2.x + b2.r_l
        square_rect = pygame.Rect(b3.x, b3.y, b3.r_l, 100)         
        pygame.draw.rect(screen, (0, 0, 250), square_rect) 
        pygame.display.update()        
        #3, 4
        
        b1.l = 10
        b1.y += 200
        b2.l = 20
        b2.y += 200
        b3.l = 30
        b3.y += 200
        #5
        square_rect = pygame.Rect(b1.x, b1.y, b1.l, 100)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 

        square_rect = pygame.Rect(b1.l, b2.y, b2.l, 100)         
        pygame.draw.rect(screen, (0, 250, 0), square_rect) 

        square_rect = pygame.Rect(b2.l, b3.y, b3.l, 100)         
        pygame.draw.rect(screen, (0, 0, 250), square_rect) 
        pygame.display.update()    
        
        #6
        b1.l = 1000
        b1.y += 200
        b2.l = 2000
        b2.y += 200
        b3.l = 3000
        b3.y += 200
        all_bus_length = b3.l + b2.l + b1.l
        ic(all_bus_length)
        l_scale = SCREEN_WIDTH / all_bus_length
        b1.r_l = b1.l * l_scale
        ic(b1.r_l)
        b1.x = 0

        square_rect = pygame.Rect(b1.x, b1.y, b1.r_l, 100)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 

        l_scale = SCREEN_WIDTH / all_bus_length
        b2.r_l = b2.l * l_scale
        ic(b2.r_l)
        b2.x = b1.x + b1.r_l
        square_rect = pygame.Rect(b2.x, b2.y, b2.r_l, 100)         
        pygame.draw.rect(screen, (0, 250, 0), square_rect) 

        l_scale = SCREEN_WIDTH / all_bus_length
        b3.r_l = b3.l * l_scale
        ic(b3.r_l)
        b3.x = b2.x + b2.r_l
        square_rect = pygame.Rect(b3.x, b3.y, b3.r_l, 100)         
        pygame.draw.rect(screen, (0, 0, 250), square_rect) 
        pygame.display.update()       
        
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
        sys.exit()     
    if args['test'] == 'calc_vt4':
        root = CEmployee("root")
        root.length = 0
        a = CEmployee("a")
        a.length = 1
        a.w = 100
        a.h = 10
        b = CEmployee("b")
        b.length = 1
        b.w = 150
        b.h = 10
        c = CEmployee("c")
        c.length = 1
        c.w = 200
        c.h = 10
        d = CEmployee("d")
        d.length = 1
        d.w = 50
        d.h = 10
        e = CEmployee("e")
        e.length = 1
        e.w = 10
        e.h = 10
        '''
        f = CEmployee("f")
        f.length = 1
        f.w = 10
        f.h = 10
        g = CEmployee("g")
        g.length = 1
        g.w = 10
        g.h = 10
        h = CEmployee("h")
        h.length = 1
        h.w = 10
        h.h = 10
        i = CEmployee("i")
        i.length = 1
        i.w = 10
        i.h = 10
        i2 = CEmployee("i2")
        i2.length = 1
        i2.w = 10
        i2.h = 10 
        '''
        root.children_list.append(a)
        root.children_list.append(b)
        root.children_list.append(c)
        root.children_list.append(e)
        e.children_list.append(d)
        '''        
        a.children_list.append(c)
        a.children_list.append(d)
        b.children_list.append(e)
        b.children_list.append(f)
        d.children_list.append(g)
        d.children_list.append(h)
        b.children_list.append(i)
        b.children_list.append(i2)        
        '''
        bnopt = calc_max_parallel_people_for_all_people(root, 0, 0, root)
        ic(bnopt)
        y_p=0
        x_p=0
        #previous sibling of root is None, children are A, previous sibling of C is B, no children, previous sibling of D is C and children is G and H
        #calc_x_y_children_v3(root, 100, None)   
        calc_y_children(root, 20)
        #calc_x_children(root, None)        
        calc_ps_of_children(root)
        print_ps(root)
        calc_accumalated_distance_children(root)
        '''
        calc_x_children_v2(root)
        biggest_x = calc_biggest_x(root, 0)
        ic(biggest_x)
        scale_x = SCREEN_WIDTH / biggest_x
        ic(scale_x)
        calc_rx_children(root, scale_x)
        calc_rw_children(root, scale_x)
        #draw_children(root, 100)
        draw_childrenv2(root)
        '''
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
        sys.exit()     
        #pygame.quit()