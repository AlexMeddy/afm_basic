import pygame
import sys
from CFolderView import CFolderView
from CFolderModel import CFolderModel
from CController import CController

class CMainView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CMainView Example")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        #self.model_root_obj = CFolderModel.my_instantiate_from_flat_file("CFolderModel.txt")
        #self.view_root_obj = CController.map_from_model_to_view_tree(self.model_root_obj, None) #use CController.map_from_model_to_view_tree()
        self.view_root_obj = CFolderView.instantiate_from_flat_file("FolderView.txt")
        self.view_root_obj.calc_x_tree()
        self.view_root_obj.calc_y_tree()
        self.view_root_obj.CALC_p_x_TREE(1)
        self.view_root_obj.CALC_p_y_TREE(1)

        if self.view_root_obj != None:
            self.view_root_obj.print_tree()

    def handle_event(self, event):
        def handle_collision2():
            if self.view_root_obj:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                folder = self.view_root_obj.find_by_mouse_pos_tree(mx = mouse_x, my = mouse_y)
                if folder:
                    print(folder.guid)
                else:
                    print('folder not found')

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            handle_collision2()

    def draw_mouse_coordinates(self):
        """Draws mouse coordinates in the top-right corner."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coord_text = f"({mouse_x}, {mouse_y})"
        text_surface = self.font.render(coord_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text_surface, text_rect)

    def draw_center_rectangle(self):
        """Draws a blue rectangle in the middle of the screen."""
        rect_width, rect_height = 200, 100
        rect_x = (self.width - rect_width) // 2
        rect_y = (self.height - rect_height) // 2
        pygame.draw.rect(self.screen, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height))

    def run(self):
        """Main application loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.screen.fill((0, 0, 0))  # Clear screen
            self.draw_mouse_coordinates()
            self.view_root_obj.draw_tree(self.screen, pygame)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = CMainView()
    app.run()
