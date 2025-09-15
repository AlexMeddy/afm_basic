import pygame
import sys
from CResistorView import CResistorViewListManager
from CResistorModel import CResistorModelListManager
from CController import CController

class CMainView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CMainView - ResistorView Demo")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 20)
        
        self.resistor_view_manager = None    
        self.resistor_manager_model = CResistorModelListManager()
        if self.resistor_manager_model:
            self.resistor_manager_model.instantiate_from_flat_file("ResistorModel.txt")
            self.resistor_manager_model.print_list()        
            self.resistor_view_manager = CController.instantiate_resistor_view_lm_from_model(self.resistor_manager_model)
        
        if self.resistor_view_manager.resistor_list:
            self.resistor_view_manager.print_list()


    def handle_event(self, event):
        def handle_collision2():
            if self.resistor_view_manager:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                chosen_resistor = self.resistor_view_manager.find_by_mouse_pos_list(mouse_x = mouse_x, mouse_y = mouse_y)
                if chosen_resistor:
                    print(chosen_resistor.guid)
                    #print(chosen_resistor.model.voltage)
                else:
                    print('chosen_resistor not found')

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            handle_collision2()

    def draw_mouse_coords(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = self.font.render(f"({mouse_x}, {mouse_y})", True, (0, 0, 0))
        text_rect = text.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text, text_rect)

    def draw_blue_rectangle_middle(self):
        rect_w, rect_h = 100, 50
        rect_x = (self.width - rect_w) // 2
        rect_y = (self.height - rect_h) // 2
        pygame.draw.rect(self.screen, (0, 0, 255), (rect_x, rect_y, rect_w, rect_h))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)

            self.screen.fill((255, 255, 255))

            if self.resistor_view_manager:
                self.resistor_view_manager.calc_p_x_list()
                self.resistor_view_manager.calc_p_y_list()
                # Draw all resistor views
                self.resistor_view_manager.draw_list(self.screen, pygame)

            # Draw mouse coordinates
            self.draw_mouse_coords()

            # Draw blue rectangle in the middle
            self.draw_blue_rectangle_middle()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


# ------------------------ sample ResistorView.txt ------------------------
"""
Sample file contents (ResistorView.txt):

R1,100,100,80,40
R2,300,200,100,50
R3,500,400,120,60
"""

# ------------------------ entry point ------------------------
if __name__ == "__main__":
    app = CMainView()
    app.run()