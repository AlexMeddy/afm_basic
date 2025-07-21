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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('Comic Sans', 15)
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
        self.ah = -1 #accumulated heightt
        self.x = -1
        self.y = -1
        self.i_self = -1 #resized width
        self.space_x = 100
        self.space_y = 10
        
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
            
    def add_child(self, child_p):#child_name_p only to help logger
        self.c_l.append(child_p) 
            
            
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
            
    def calc_aw_tree(self):
        r0 = 0
        r1 = 0
        r2 = 0
        if self.ps != None:
            biggest_aw = self.ps.get_longest_distance_tree_x(0)
            r2 = 1 
        if self.parent == None:
            r0 = 1 
        if self.ps == None:
            r1 = 1
        temp = None
        if r0 == 1:
            temp = self.w
        elif r2 == 1:
            temp = self.w + biggest_aw + self.ps.space_x
        elif r1 == 1:
            temp = self.w
        else:
            assert false, "cannot apply rule"
        self.aw = temp
        
        for child in self.c_l:           
            child.calc_aw_tree()  
        return r0,r1,r2 #for logging purposes
    
    def calc_ah_tree(self):
        if self.parent != None:
            self.ah = self.parent.ah + self.h + self.space_y
        else:
            self.ah = self.h
        for child in self.c_l:           
            child.calc_ah_tree()  
    
    def get_longest_distance_tree_x(self, biggest_distance_p):
        biggest_distance = biggest_distance_p
        if self.aw > biggest_distance:
            biggest_distance = self.aw
        for child in self.c_l:
            biggest_distance = child.get_longest_distance_tree_x(biggest_distance) 
        return biggest_distance
        
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
        
            
    def calc_x_tree(self):
        r0 = 0
        r1 = 0
        r2 = 0
        if self.ps != None:
            biggest_aw = self.ps.get_longest_distance_tree_x(0)
        if self.parent == None:
            r0 = 1 
        if self.ps == None: #no ps
            r1 = 1
        if self.ps != None: #ps
            r2 = 1         
        if r0 == 1:
            temp = 0
        elif r2 == 1:
            temp = biggest_aw + self.ps.space_x
        elif r1 == 1:
            temp = self.parent.x
        else:
            assert false, "cannot apply rule"
        self.x = temp
        for child in self.c_l:
            child.calc_x_tree()
        return r0,r1,r2 #for logging purposes
    
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
            temp = self.parent.ah + self.parent.space_y
        self.y = temp
        for child in self.c_l:
            child.calc_y_tree()
        return r0,r1 #for logging purposes
            
    
    def draw_tree(self, scale_xd_p, scale_yd_p):
        sqaure_xy = self.x*scale_xd_p, self.y*scale_yd_p
        sqaure_wh = self.w*scale_xd_p, self.h*scale_yd_p
        square_rect = pygame.Rect(sqaure_xy, sqaure_wh) 
        pygame.draw.rect(screen, (self.x*scale_xd_p % 255, self.y*scale_yd_p % 255, 100), square_rect)
        text = font.render(self.name, True, (255,255,255))
        text_xy = (self.x*scale_xd_p+self.w*scale_xd_p/2, self.y*scale_yd_p+self.h*scale_yd_p/2)
        screen.blit(text, text_xy)
        text = font.render(f'r-aw = {int(self.aw*scale_xd_p)}', True, (255,255,255))
        screen.blit(text, (self.x*scale_xd_p, self.y*scale_yd_p+self.h*scale_yd_p/2+20))
        if self.parent != None:
            line_xy = (self.parent.x*scale_xd_p+self.parent.w*scale_xd_p/2, self.parent.ah*scale_yd_p)
            line_wh = (self.x*scale_xd_p+self.w*scale_xd_p/2, self.y*scale_yd_p)
            pygame.draw.line(screen, (255,255,255), line_xy, line_wh)
        #input()
        for child in self.c_l:
            child.draw_tree(scale_xd_p, scale_yd_p)        

    def align(self):        
        #y starts here
        self.calc_ah_tree()
        longest_length_y = self.get_longest_distance_tree_y(0)
        scale_yd = SCREEN_HEIGHT / longest_length_y
        self.calc_y_tree()
        #x starts here
        self.calc_i_self(0)
        self.calc_ps_tree()
        self.calc_aw_tree()
        longest_length_x = self.get_longest_distance_tree_x(0)
        scale_xd = SCREEN_WIDTH / longest_length_x
        self.calc_x_tree()
        return scale_xd, scale_yd
    
    def search_by_name(self, employee_name_p, found_employee_p):
        found_employee = found_employee_p
        if self.name == employee_name_p: #self is always first
            found_employee = self
        else:
            found_employee = None
        myic(found_employee)
        myic(self.name)
        for child in self.c_l:
            found_employee = child.search_by_name(employee_name_p, found_employee)
        return found_employee
        
    def get_bla2(self):
        bla2 = 0
        bla2 = self.w
        return bla2
    
def initialise_employee_tree():
    def create_tree_for_testing_14():
        root_obj = CEmployee(guid_p = 'root',name_p='root',w_p=100,h_p=100, parent_p = None)
        a = CEmployee(guid_p = 'a',name_p='a',w_p=100,h_p=100/2, parent_p = root_obj)
        b = CEmployee(guid_p = 'b',name_p='b',w_p=200,h_p=100, parent_p = root_obj)
        c = CEmployee(guid_p = 'c',name_p='c',w_p=100,h_p=100, parent_p = root_obj)
        d = CEmployee(guid_p = 'd',name_p='d',w_p=200,h_p=100, parent_p = a)
        e = CEmployee(guid_p = 'e',name_p='e',w_p=100,h_p=100/2, parent_p = a)
        f = CEmployee(guid_p = 'f',name_p='f',w_p=400,h_p=100, parent_p = a)
        g = CEmployee(guid_p = 'g',name_p='g',w_p=51,h_p=100, parent_p = a)
        root_obj.add_child(child_p = a)
        root_obj.add_child(child_p = b)
        root_obj.add_child(child_p = c)
        a.add_child(child_p = d)
        a.add_child(child_p = e)
        a.add_child(child_p = f)
        a.add_child(child_p = g)
        return root_obj, a
    def create_tree_from_input(employee_p):
        while True:
            result = input("please enter guid,name,w,h,parent or enter q to quit: ")
            if result != "q":
                parts = result.split(",", 4)
                if len(parts) == 5:
                    guid, name, w, h, parent_name = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip()
                    employee_p.search_by_name(parent_name, None)
                    employee = CEmployee(guid, name, w, h, parent)
                    print("Employee Created:", employee)
            else:
                break
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    parser.add_argument('-s','--scenario', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'rxyd':
        mylog_section('intialising tree')       
        if args['scenario'] == '4':
            root_obj, a = create_tree_for_testing_14()
        
        scale_xd, scale_yd = root_obj.align()
        root_obj.print_tree()
    return root_obj, scale_xd, scale_yd

def draw_mouse_coordinates(screen):
    x, y = pygame.mouse.get_pos()
    coord_text = font.render(f"({x}, {y})", True, WHITE)
    
    # Position the text near the top-right corner
    text_width = coord_text.get_width()
    screen.blit(coord_text, (SCREEN_WIDTH - text_width - 10, 10))  # 10px padding
    
def main(): 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Text Input with __name__")

    #input_box = TextInputBox(100, 200, 440, 40)
    clock = pygame.time.Clock()
    root_obj, scale_xd, scale_yd = initialise_employee_tree()
    parent = root_obj.search_by_name("a", None)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #input_box.handle_event(event)

        screen.fill(BLACK)
        #input_box.draw(screen)
        root_obj.draw_tree(scale_xd, scale_yd)
        myic(parent.name)
        draw_mouse_coordinates(screen)
        pygame.display.flip()
        clock.tick(30)

# Standard Python entry point
if __name__ == "__main__":
    main()