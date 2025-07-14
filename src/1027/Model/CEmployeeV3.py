from icecream import ic
import argparse
import pygame
import sys
sys.path.append("..\\..\\lib")
from mylogger_v3_4 import mylogger,mylog_section,myic,DISPLAY_SELF,DISPLAY_PARAM,DISPLAY_STATE,DISPLAY_STD,DISPLAY_FULL
import time

pygame.init()


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('Arial', 15)
class CEmployee:
    def __init__(self, guid_p, name_p, w_p, h_p, parent_p):
        self.guid = guid_p 
        self.name = name_p
        self.parent = parent_p
        self.c_l = []
        self.ps = None #previous sibling
        self.w = w_p
        self.h = h_p
        self.aw = -1 #accumulated width
        self.ah = -1 #accumulated height
        self.rw = -1 #resized width
        self.rh = -1 #resized height
        self.raw = -1 #resized accumulated width
        self.rah = -1 #resized accumulated height
        self.x = -1
        self.y = -1
        self.i_self = -1 #resized width
        self.space_x = 10
        self.r_space_x = -1
        self.space_y = 10
        self.r_space_y = -1
        
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
            
    def calc_ps_tree(self):
        self.ps = self.parent.c_l[self.i_self-1]  if  (self.parent != None and 
                                                                self.parent.c_l != [] and
                                                                self.i_self>0) else None
        for child in self.c_l:           
            child.calc_ps_tree()
            
    def calc_i_self(self, i_self_p):
        self.i_self = i_self_p
        for i_child in range(len(self.c_l)):
            self.c_l[i_child].calc_i_self(i_child)
            
    @mylogger()                               
    def calc_aw_tree(self):
        r1 = 0
        r2 = 0
        r3 = 0
        nephew = self.ps.get_last_child()  if  (self.ps != None) else None
        if nephew != None:
            r3 = 1
        if self.ps != None:
            r2 = 1 
        if self.ps == None:
            r1 = 1
        temp = None
        if r3 == 1:
            temp = nephew.aw + nephew.space_x + self.w
        elif r2 == 1:
            temp = self.w + self.ps.aw + self.ps.space_x
        if r1 == 1:
            temp = self.w
        self.aw = temp
        
        for child in self.c_l:           
            child.calc_aw_tree()  
    
    @mylogger()                               
    def calc_ah_tree(self):
        if self.parent != None:
            self.ah = self.parent.ah + self.h + self.space_y
        else:
            self.ah = self.h
        for child in self.c_l:           
            child.calc_ah_tree()  
    
    @mylogger()                               
    def get_longest_distance_tree_x(self, biggest_distance_p):
        biggest_distance = biggest_distance_p
        if self.aw > biggest_distance:
            biggest_distance = self.aw
        for child in self.c_l:
            biggest_distance = child.get_longest_distance_tree_x(biggest_distance) 
        return biggest_distance
        
    @mylogger()                               
    def get_longest_distance_tree_y(self, biggest_distance_p):
        biggest_distance = biggest_distance_p
        if self.ah > biggest_distance:
            biggest_distance = self.ah
        for child in self.c_l:
            biggest_distance = child.get_longest_distance_tree_y(biggest_distance) 
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
    def calc_rh_tree(self, scale_yd_p):
        self.rh = self.h * scale_yd_p
        for child in self.c_l:
            child.calc_rh_tree(scale_yd_p)        
            
    @mylogger()                               
    def calc_x_tree(self):
        r0 = 0
        r1 = 0
        r2 = 0
        r3 = 0
        if self.parent == None:
            r0 = 1 
        nephew = self.ps.get_last_child()  if  (self.ps != None) else None
        if nephew != None:
            r3 = 1
        if self.ps == None: #no ps
            r1 = 1
        if self.ps != None: #ps
            r2 = 1         
        if r0 == 1:
            temp = 0
        elif r3 == 1:
            temp = nephew.raw + nephew.space_x
        elif r2 == 1:
            temp = self.ps.raw + self.ps.r_space_x
        elif r1 == 1:
            temp = self.parent.x
        self.x = temp
        for child in self.c_l:
            child.calc_x_tree()
        myic(r0,r1,r2,r3, nephew) #for logging purposes
        return r0,r1,r2,r3 #for logging purposes
    
    def calc_y_tree(self):
        r0 = 0
        r1 = 0
        if self.parent == None:
            r0 = 1 
        if self.parent != None:
            r1 = 1
        if r0 == 1:
            temp = 0
        if r1 == 1:
            temp = self.parent.rah + self.parent.r_space_y
        self.y = temp
        for child in self.c_l:
            child.calc_y_tree()
        myic(r0,r1) #for logging purposes
        return r0,r1 #for logging purposes
            
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
    
    def calc_rah_tree(self, scale_yd_p):
        self.rah = self.ah * scale_yd_p
        for child in self.c_l:
            child.calc_rah_tree(scale_yd_p)
    
    def calc_r_space_x(self, scale_xd_p):
        self.r_space_x = self.space_x * scale_xd_p
        for child in self.c_l:
            child.calc_r_space_x(scale_xd_p)
            
    def calc_r_space_y(self, scale_yd_p):
        self.r_space_y = self.space_y * scale_yd_p
        for child in self.c_l:
            child.calc_r_space_y(scale_yd_p)
    
    @mylogger()                               
    def draw_tree(self):
        square_rect = pygame.Rect(self.x, self.y, self.rw, self.rh) 
        myic(self.x, self.y)
        pygame.draw.rect(screen, (self.x % 255, self.y % 255, 100), square_rect)
        text = font.render(self.name, True, (255,255,255))
        screen.blit(text, (self.x+self.rw/2, self.y+self.rh/2))
        text = font.render(str(int(self.aw)), True, (255,255,255))
        screen.blit(text, (self.x+self.rw/2, self.y+self.rh/2+20))
        if self.parent != None:
            myic(self.parent.x,self.parent.rw, self.parent.y,self.parent.rah, self.x,self.rw, self.y,self.rh)
            pygame.draw.line(screen, (255,255,255), (self.parent.x+self.parent.rw/2, self.parent.rah)
            , (self.x+self.rw/2, self.y))
        pygame.display.update() 
        pygame.event.get()        
        input()
        for child in self.c_l:
            child.draw_tree()        


if __name__ == "__main__":
    left_margin = 50
    right_margin = 50
    availible_width = SCREEN_WIDTH - left_margin - right_margin
    top_margin = 50
    bottom_margin = 50
    availible_height = SCREEN_HEIGHT - top_margin - bottom_margin
    def create_tree_for_testing_0():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100, h_p=100, parent_p = None)
        root_obj.rh = 100
        root_obj.y = 0
        return root_obj
    def create_tree_for_testing_1():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        root_obj.y = 0
        root_obj.rh = 100
        a.y = 100
        a.rh = 100
        return root_obj
    def create_tree_for_testing_2():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=300,h_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        root_obj.y = 0
        root_obj.rh = 100
        a.y = 100
        a.rh = 100
        b.y = 100
        b.rh = 100
        return root_obj
    def create_tree_for_testing_3():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=300,h_p=100, parent_p = root_obj)
        c = CEmployee(guid_p = 'c',name_p='c',w_p=100,h_p=100, parent_p = a)
        d = CEmployee(guid_p = 'd',name_p='d',w_p=100,h_p=100, parent_p = a)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        a.add_child(child_p = c)
        a.add_child(child_p = d)
        root_obj.y = 0
        root_obj.rh = 100
        a.y = 100
        a.rh = 100
        b.y = 100
        b.rh = 100
        c.y = 200
        c.rh = 100
        d.y = 200
        d.rh = 100
        return root_obj
    def create_tree_for_testing_10():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100, h_p=100, parent_p = None)
        return root_obj
    def create_tree_for_testing_11():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        return root_obj
    def create_tree_for_testing_12():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=300,h_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        return root_obj
    def create_tree_for_testing_13():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=300,h_p=100, parent_p = root_obj)
        c = CEmployee(guid_p = 'c',name_p='c',w_p=100,h_p=100, parent_p = a)
        d = CEmployee(guid_p = 'd',name_p='d',w_p=100,h_p=100, parent_p = a)
        e = CEmployee(guid_p = 'e',name_p='e',w_p=100,h_p=100, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        root_obj.add_child(child_p = e)
        a.add_child(child_p = c)
        a.add_child(child_p = d)
        return root_obj
    def create_tree_for_testing_14():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=300,h_p=100, parent_p = root_obj)
        c = CEmployee(guid_p = 'c',name_p='c',w_p=100,h_p=100, parent_p = root_obj)
        d = CEmployee(guid_p = 'd',name_p='d',w_p=100,h_p=100, parent_p = a)
        e = CEmployee(guid_p = 'e',name_p='e',w_p=100,h_p=100, parent_p = b)
        f = CEmployee(guid_p = 'f',name_p='f',w_p=100,h_p=100, parent_p = c)
        g = CEmployee(guid_p = 'g',name_p='g',w_p=100,h_p=100, parent_p = c)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        root_obj.add_child(child_p = c)
        a.add_child(child_p = d)
        b.add_child(child_p = e)
        c.add_child(child_p = f)
        c.add_child(child_p = g)
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
        if args['scenario'] == '2':
            root_obj = create_tree_for_testing_2()
        if args['scenario'] == '3':
            root_obj = create_tree_for_testing_3()    
        root_obj.print_tree()
        root_obj.calc_i_self(0)
        root_obj.calc_ps_tree()
        root_obj.calc_aw_tree()
        longest_length_x = root_obj.get_longest_distance_tree_x(0)
        scale_xd = SCREEN_WIDTH / longest_length_x
        root_obj.calc_rw_tree(scale_xd_p = scale_xd)
        root_obj.calc_raw_tree(scale_xd_p = scale_xd)
        root_obj.calc_r_space_x(scale_xd_p = scale_xd)
        root_obj.calc_x_tree()
        root_obj.draw_tree()
        
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    if args['test'] == 'ryd':
        mylog_section('intialising tree')       
        if args['scenario'] == '0':
            root_obj = create_tree_for_testing_10()
        if args['scenario'] == '1':
            root_obj = create_tree_for_testing_11()
        if args['scenario'] == '2':
            root_obj = create_tree_for_testing_12()
        if args['scenario'] == '3':
            root_obj = create_tree_for_testing_13()            
        root_obj.print_tree()
        #y starts here
        root_obj.calc_ah_tree()
        longest_length_y = root_obj.get_longest_distance_tree_y(0)
        scale_yd = SCREEN_HEIGHT / longest_length_y
        myic(scale_yd, SCREEN_HEIGHT, longest_length_y)
        root_obj.calc_rh_tree(scale_yd_p = scale_yd)        
        root_obj.calc_rah_tree(scale_yd_p = scale_yd)
        root_obj.calc_r_space_y(scale_yd_p = scale_yd)
        root_obj.calc_y_tree()
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
    if args['test'] == 'rxyd':
        mylog_section('intialising tree')       
        if args['scenario'] == '0':
            root_obj = create_tree_for_testing_10()
        if args['scenario'] == '1':
            root_obj = create_tree_for_testing_11()
        if args['scenario'] == '2':
            root_obj = create_tree_for_testing_12()
        if args['scenario'] == '3':
            root_obj = create_tree_for_testing_13() 
        if args['scenario'] == '4':
            root_obj = create_tree_for_testing_14()
        root_obj.print_tree()
        #y starts here
        root_obj.calc_ah_tree()
        longest_length_y = root_obj.get_longest_distance_tree_y(0)
        scale_yd = SCREEN_HEIGHT / longest_length_y
        myic(scale_yd, availible_height, longest_length_y)
        root_obj.calc_rh_tree(scale_yd_p = scale_yd)        
        root_obj.calc_rah_tree(scale_yd_p = scale_yd)
        root_obj.calc_r_space_y(scale_yd_p = scale_yd)
        root_obj.calc_y_tree()
        #x starts here
        root_obj.calc_i_self(0)
        root_obj.calc_ps_tree()
        root_obj.calc_aw_tree()
        longest_length_x = root_obj.get_longest_distance_tree_x(0)
        scale_xd = SCREEN_WIDTH / longest_length_x
        root_obj.calc_rw_tree(scale_xd_p = scale_xd)
        root_obj.calc_raw_tree(scale_xd_p = scale_xd)
        root_obj.calc_r_space_x(scale_xd_p = scale_xd)
        root_obj.calc_x_tree()
        root_obj.draw_tree()
        pygame.display.update()  
        run = True        
        while run:                                   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False