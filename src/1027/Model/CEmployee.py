from icecream import ic
import argparse
import pygame
import sys
sys.path.append("C:\\Users\\alexf\\afm_basic\\src\\lib")
from mylogger_v3_1 import mylogger,mylog_section,myic,DISPLAY_SELF,DISPLAY_PARAM,DISPLAY_STATE,DISPLAY_STD,DISPLAY_FULL
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
        self.i_self = -1 #resized width
        
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
    def calc_ps_tree(self, ps_p):
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
            
            child.calc_ps_tree(temp)
            
    @mylogger()                               
    def calc_ps_treev3(self):
        self.ps = self.parent.c_l[self.i_self-1]  if  (self.parent != None and 
                                                                self.parent.c_l != [] and
                                                                self.i_self>0) else None
        for child in self.c_l:           
            child.calc_ps_treev3()
            
    @mylogger()                               
    def calc_i_self(self, i_self_p):
        self.i_self = i_self_p
        for i_child in range(len(self.c_l)):
            self.c_l[i_child].calc_i_self(i_child)
            
    @mylogger()                               
    def calc_aw_v3(self):
        r1 = 0
        r2 = 0
        r3 = 0
        if self.ps != None:
            nephew = self.ps.get_last_child()
            if nephew != None:
                r3 = 1
        if self.ps != None:
            r2 = 1 
        if self.ps == None:
            r1 = 1
        temp = None
        if r3 == 1:
            temp = self.w + nephew.aw
        elif r2 == 1:
            temp = self.w + self.ps.aw
        if r1 == 1:
            temp = self.w
        self.aw = temp
        
        for child in self.c_l:           
            child.calc_aw_v3()  
    
    @mylogger()                               
    def get_longest_distance_children(self, biggest_distance_p):
        biggest_distance = biggest_distance_p
        if self.aw > biggest_distance:
            biggest_distance = self.aw
        for child in self.c_l:
            biggest_distance = child.get_longest_distance_children(biggest_distance) 
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
    def calc_rw(self, scale_xd_p):
        self.rw = self.w * scale_xd_p
        for child in self.c_l:
            child.calc_rw(scale_xd_p)
            
    @mylogger()                               
    def calc_rawv2(self):
        r1 = 0
        r2 = 0
        r3 = 0
        if self.ps != None:
            nephew = self.ps.get_last_child()
            if nephew != None:
                r3 = 1
        if self.ps != None:
            r2 = 1 
        if self.ps == None:
            r1 = 1
        temp = None
        if r3 == 1:
            temp = self.rw + nephew.rw
        elif r2 == 1:
            temp = self.rw + self.ps.rw
        if r1 == 1:
            temp = self.rw
        self.raw = temp        
        for child in self.c_l:           
            child.calc_raw()  

    def calc_raw(self, scale_xd_p):
        #already done in calc_aw_v3
        '''
        r1 = 0
        r2 = 0
        r3 = 0
        if self.ps != None:
            nephew = self.ps.get_last_child()
            if nephew != None:
                r3 = 1
        if self.ps != None:
            r2 = 1 
        if self.ps == None:
            r1 = 1
        temp = None
        if r3 == 1:
            temp = self.rw + nephew.rw
        elif r2 == 1:
            temp = self.rw + self.ps.rw
        if r1 == 1:
            temp = self.rw
        self.raw = temp
        '''
        self.raw = self.aw * scale_xd_p
        for child in self.c_l:
            child.calc_raw(scale_xd_p)

if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'tree':
        mylog_section('intialising tree')
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=120, parent_p = root_obj)
        c = CEmployee(guid_p = 'c',name_p='c',w_p=100, parent_p = a)
        c2 = CEmployee(guid_p = 'c2',name_p='c2',w_p=101, parent_p = a)
        d = CEmployee(guid_p = 'd',name_p='d',w_p=200, parent_p = root_obj)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        root_obj.add_child(child_p = d)
        a.add_child(child_p = c)
        a.add_child(child_p = c2)
        mylog_section('printing tree')
        root_obj.print_tree()
        mylog_section('calculating ps')
        root_obj.calc_i_self(0)
        root_obj.calc_ps_treev3()
        root_obj.calc_aw_v3()
        longest_length = root_obj.get_longest_distance_children(0)
        myic(longest_length)
        scale_xd = SCREEN_WIDTH / longest_length
        myic(scale_xd)
        '''
        all_names = root_obj.get_all_the_names_concatenated('')
        myic(all_names)
        bla = root_obj.get_bla(0)
        myic(bla)
        '''
        root_obj.calc_rw(scale_xd)
        root_obj.calc_raw()