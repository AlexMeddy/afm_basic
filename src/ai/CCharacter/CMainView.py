import pygame
import sys
from CCharacterView import CCharacterViewListManager


class CMainView:
    def __init__(self, width=800, height=600):
        """Initialize the Pygame window and setup attributes."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("CMainView Pygame App")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)  # Default font
        self.char_lm = CCharacterViewListManager()
        file_path = "chars.txt"
        self.char_lm.instantiate_chars_from_flat_file(file_path)
        self.char_lm.print_list()
    
    def handle_event(self, event):
        def handle_collision2():
            if self.char_lm:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                chosen_char = self.char_lm.find_by_mouse_pos_list(mouse_x_p = mouse_x, mouse_y_p = mouse_y)
                if chosen_char:
                    print(chosen_char.guid)
                else:
                    print('chosen_char not found')

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            handle_collision2()

    def draw_mouse_coordinates(self):
        """Draw the mouse coordinates in the top-right corner."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coord_text = f"({mouse_x}, {mouse_y})"
        text_surface = self.font.render(coord_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        """Main application loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            
            self.screen.fill((0, 0, 0))  # Clear screen with black
            self.draw_mouse_coordinates()
            self.char_lm.draw_list(screen_p = self.screen, pygame_p = pygame)

            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = CMainView()   
    app.run()
