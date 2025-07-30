import pygame
import sys
from CEmployeeView import CEmployeeView

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 500
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)
FONT = pygame.font.Font(None, 36)


class TextInput:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = GRAY
        self.color_active = BLUE
        self.color = self.color_inactive
        self.text = ''
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print("Submitted:", self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        text_surface = FONT.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class CMainView:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CMainView: Text Input + Mouse Coordinates")
        self.clock = pygame.time.Clock()
        self.running = True
        self.input_box = TextInput(0, 0, 200, 40)
        
        self.employee_root_obj = self.get_tree_from_flat_file()


    def draw_mouse_coordinates(self):
        x, y = pygame.mouse.get_pos()
        coord_text = FONT.render(f"({x}, {y})", True, BLACK)
        text_width = coord_text.get_width()
        self.screen.blit(coord_text, (WIDTH - text_width - 10, 10))  # Top-right corner

    def get_tree_from_flat_file(self):
        root_obj = None
        flag_first_employee = 1
        with open('employee_tree.txt', 'r') as file:
            lines = file.readlines()
        for line in lines:
            if flag_first_employee == 1:  #if first employee instantiate root
                flag_first_employee = 0
                #parse line
                print(line.strip())
                parts = line.split(',', 6)
                if len(parts) == 7:
                    guid, name, w, h, space_x, space_y, parent_name = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[6].strip() 
                    root_obj = CEmployeeView(guid, name, int(w), int(h), int(space_x), int(space_y), None) 
            else:
                #parse line
                print(line.strip())
                parts = line.split(',', 6)
                if len(parts) == 7:
                    guid, name, w, h, space_x, space_y, parent_name = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[6].strip() 
                    parent = root_obj.get_employee_by_name(parent_name)
                    employee = CEmployeeView(guid, name, int(w), int(h), int(space_x), int(space_y), parent) 
                    if parent:
                        parent.add_child(child_p = employee)
                    else:
                        print('parent not found')
        return root_obj

    def run(self):
        while self.running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.input_box.handle_event(event)
            
            self.input_box.draw(self.screen)
            if self.employee_root_obj:
                top_margin = 50
                scale_x, scale_y = self.employee_root_obj.align(available_screen_width_p = WIDTH, available_screen_height_p = HEIGHT-top_margin)
                self.employee_root_obj.draw_tree(scale_x, scale_y, pygame, self.screen, FONT, top_margin)


            else:
                print("no employee_root_obj")
            self.draw_mouse_coordinates()  # ← Call mouse coordinate drawing

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


# Run the app
if __name__ == "__main__":
    app = CMainView()
    app.run()
