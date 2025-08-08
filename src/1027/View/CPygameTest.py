import pygame
import sys
from CEmployeeView import CEmployeeView
class CPygameTest:
    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Text Input Example")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)

        # Input box settings
        self.input_box = pygame.Rect(0, 0, 200, 40)
        self.input_text = 'r,r,100,100,10,100,n'
        self.active = False
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.root_obj = None
        self.flag_first_employee = 1
    
        self.top_margin = 50
    

    def handle_event(self, event):
        def handle_collision():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.root_obj:
                scale_x, scale_y = self.root_obj.get_scale_xy(available_screen_width_p=self.width, available_screen_height_p=self.height-self.top_margin)
                if( (mouse_x > self.root_obj.x*scale_x and mouse_x < self.root_obj.aw*scale_x) 
                and (mouse_y > self.root_obj.y*scale_y+self.top_margin and mouse_y < self.root_obj.ah*scale_y+self.top_margin)):
                    print(self.root_obj.guid)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
            handle_collision()
                
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:        
                if self.flag_first_employee == 1:  #if first employee instantiate root
                    self.flag_first_employee = 0
                    parts = self.input_text.split(',', 6)
                    if len(parts) == 7:
                        guid, name, w, h, space_x, space_y, parent_name = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[6].strip() 
                        self.root_obj = CEmployeeView(guid, name, int(w), int(h), int(space_x), int(space_y), None)
                        print('root created')
                else:
                    parts = self.input_text.split(',', 6)
                    if len(parts) == 7:
                        guid, name, w, h, space_x, space_y, parent_name = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[6].strip() 
                        parent = self.root_obj.get_employee_by_name(parent_name)
                        employee = CEmployeeView(guid, name, int(w), int(h), int(space_x), int(space_y), parent)
                        if parent:
                            parent.add_child(child_p = employee)
                        else:
                            myic('parent not found')
                    
                self.input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode                

    def draw_input(self):
        # Render the current input text
        text_surface = self.font.render(self.input_text, True, pygame.Color('white'))
        width = max(200, text_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)
            
            self.screen.fill((0, 0, 0))  # Clear screen
            self.draw_input()  # Draw text input box
            if self.root_obj:
                scale_x, scale_y = self.root_obj.align(available_screen_width_p=self.width, available_screen_height_p=self.height-self.top_margin)
                self.root_obj.draw_tree(scale_xd_p=scale_x, scale_yd_p=scale_y, pygame_p=pygame, screen_p=self.screen, font_p=self.font, top_margin_p=self.top_margin)
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    app = CPygameTest()
    app.run()
