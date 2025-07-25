from icecream import ic
import argparse
import pygame
import sys
sys.path.append("..\\..\\lib")
from mylogger_v3_2 import mylogger,mylog_section,myic,DISPLAY_SELF,DISPLAY_PARAM,DISPLAY_STATE,DISPLAY_STD,DISPLAY_FULL
import time

pygame.init()


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('Arial', 25)
class CEmployee:
    def __init__(self, guid_p, name_p, w_p, parent_p):
        self.guid = guid_p 
        self.name = name_p
        self.parent = parent_p
        self.c_l = []
        self.ps = None #previous sibling
        self.w = w_p
        self.aw = 0 #accumulated width
        self.rw = 0 #resized width
        self.raw = 0 #resized accumulated width
        self.x = 0
        self.rh = 0
        self.y = 0
        self.i_self = -1 #resized width
        self.space = 10 #resized width
        
    def get_last_child(self):
        last_node = None
        if len(self.c_l) > 0:
            last_node = self.c_l[len(self.c_l) -1]
            #ic(last_node.name)
        return last_node
        
    @mylogger()    
    def print_tree(self):
        for child in self.c_l:
            child.print_tree()
    #@mylogger()    
    def add_child(self, child_p):#child_name_p only to help logger
        self.c_l.append(child_p) 
            
    @mylogger()                               
    def calc_ps_treev2(self, ps_p):
        self.ps = ps_p
        
        first_sibling_flag = 1
        previous_child = None
        for child in self.c_l:
            temp = None
            if first_sibling_flag == 1:
                first_sibling_flag = 0
                temp = None
            else:
                temp = previous_child
            previous_child = child #save last child
            
            child.calc_ps_treev2(temp)
            
    @mylogger()                               
    def calc_ps_tree(self):
        self.ps = self.parent.c_l[self.i_self-1]  if  (self.parent != None and 
                                                                self.parent.c_l != [] and
                                                                self.i_self>0) else None
        for child in self.c_l:           
            child.calc_ps_tree()
            
    @mylogger()                               
    def calc_i_self(self, i_self_p):
        self.i_self = i_self_p
        for i_child in range(len(self.c_l)):
            self.c_l[i_child].calc_i_self(i_child)
            
    @mylogger()                               
    def calc_aw_tree(self):
        r1 = 0
        r2 = 0
        if self.ps != None:
            r2 = 1 
        if self.ps == None:
            r1 = 1
        temp = None
        if r2 == 1:
            temp = self.w + self.ps.aw + self.ps.space
        elif r1 == 1:
            temp = self.w
        self.aw = temp
        
        for child in self.c_l:           
            child.calc_aw_tree()  
    
    @mylogger()                               
    def get_longest_distance_tree(self, biggest_distance_p):
        biggest_distance = biggest_distance_p
        if self.aw > biggest_distance:
            biggest_distance = self.aw
        for child in self.c_l:
            biggest_distance = child.get_longest_distance_tree(biggest_distance) 
        return biggest_distance
    
    #not needed, just for learning, get pattern
    def get_all_the_names_concatenated(self, all_the_names_concatenated_p):
        all_the_names_concatenated = all_the_names_concatenated_p
        all_the_names_concatenated = self.name + ', ' + all_the_names_concatenated
        for child in self.c_l:
            all_the_names_concatenated = child.get_all_the_names_concatenated(all_the_names_concatenated)         
        return all_the_names_concatenated
        
    #not needed, just for learning, get pattern
    def get_bla(self, bla_p):
        bla = bla_p
        bla += 1
        bla *= self.w
        for child in self.c_l:
            bla = child.get_bla(bla)   
        return bla
        
    @mylogger()                               
    def calc_rw_tree(self, scale_xd_p):
        self.rw = self.w * scale_xd_p
        for child in self.c_l:
            child.calc_rw_tree(scale_xd_p)
            
            
    @mylogger()                               
    def calc_x_tree(self, lm_p):
        r0 = 0
        r1 = 0
        r2 = 0
        if self.parent == None:
            r0 = 1 
        if self.ps == None: #no ps
            r1 = 1
        if self.ps != None: #ps
            r2 = 1 
        if r0 == 1:
            temp = 0 + lm_p
        elif r2 == 1:
            temp = self.ps.raw + lm_p
        elif r1 == 1:
            temp = self.parent.x
        self.x = temp
        for child in self.c_l:
            child.calc_x_tree(lm_p)
        myic(r0,r1,r2) #for logging purposes
        return r0,r1,r2 #for logging purposes
            
    @mylogger()                               
    def calc_raw_tree(self, scale_xd_p):
        #rules already applied in calc_aw
        '''
        r1 = 0
        r2 = 0
        if self.ps != None:
            r2 = 1 
        if self.ps == None:
            r1 = 1
        temp = None
        if r2 == 1:
            temp = self.rw + self.ps.rw
        if r1 == 1:
            temp = self.rw
        self.raw = temp
        '''
        self.raw = self.aw * scale_xd_p
        for child in self.c_l:
            child.calc_raw_tree(scale_xd_p)
    
    
    def draw_tree(self):
        square_rect = pygame.Rect(self.x, self.y, self.rw, self.rh)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect)
        for child in self.c_l:
            child.draw_tree()

if __name__ == "__main__":
    def create_tree_for_testing_0():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100, parent_p = None)
        return root_obj
    def create_tree_for_testing_1():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        a.y = 100
        a.rh = 100
        return root_obj
    def create_tree_for_testing_2():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        a.y = 100
        a.rh = 100
        b.y = 100
        b.rh = 100
        return root_obj
    def create_tree_for_testing_3():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100, parent_p = root_obj)        
        b = CEmployee(guid_p = 'b',name_p='b',w_p=100, parent_p = root_obj)        
        c = CEmployee(guid_p = 'c',name_p='c',w_p=100, parent_p = a)        
        c2 = CEmployee(guid_p = 'c2',name_p='c2',w_p=100, parent_p = a)        
        d = CEmployee(guid_p = 'd',name_p='d',w_p=100, parent_p = root_obj)       
        e = CEmployee(guid_p = 'e',name_p='e',w_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        root_obj.add_child(child_p = d)
        root_obj.add_child(child_p = e)
        a.add_child(child_p = c)
        a.add_child(child_p = c2)
        a.y = 100
        a.rh = 100
        b.y = 100
        b.rh = 100
        c.y = 200
        c.rh = 200
        c2.y = 200
        c2.rh = 200
        d.y = 100
        d.rh = 100
        return root_obj
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    parser.add_argument('-s','--scenario', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'rxd':
        mylog_section('intialising tree')
        if args['scenario'] == '0':
            root_obj = create_tree_for_testing_0()
        if args['scenario'] == '1':
            root_obj = create_tree_for_testing_1()
        mylog_section('printing tree')
        root_obj.print_tree()
        mylog_section('calculating ps')
        root_obj.calc_i_self(0)
        root_obj.calc_ps_tree()
        root_obj.calc_aw_tree()
        longest_length = root_obj.get_longest_distance_tree(0)
        myic(longest_length)
        scale_xd = SCREEN_WIDTH / longest_length
        myic(scale_xd)

        root_obj.calc_rw_tree(scale_xd_p = scale_xd)
        root_obj.calc_raw_tree(scale_xd_p = scale_xd)
        root_obj.calc_x_tree(lm_p = 10)
        
        square_rect = pygame.Rect(root_obj.x, 0, root_obj.rw, root_obj.rw)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect) 
        square_rect = pygame.Rect(a.x, 100, a.rw, a.rw)         
        pygame.draw.rect(screen, (25, 100, 0), square_rect)
        square_rect = pygame.Rect(b.x, 100, b.rw, b.rw)         
        pygame.draw.rect(screen, (250, 0, 100), square_rect)
        square_rect = pygame.Rect(c.x, 210, c.rw, c.rw)         
        pygame.draw.rect(screen, (250, 0, 0), square_rect)
        square_rect = pygame.Rect(c2.x, 210, c2.rw, c2.rw)         
        pygame.draw.rect(screen, (0, 250, 0), square_rect)
        square_rect = pygame.Rect(d.x, 100, d.rw, d.rw)         
        pygame.draw.rect(screen, (200, 0, 0), square_rect)
        
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False