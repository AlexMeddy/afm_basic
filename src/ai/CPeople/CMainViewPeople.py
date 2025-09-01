import pygame
import sys
from CPersonView import CPersonView


class CMainView:
    def __init__(self, width=800, height=600):
        """Initialize the Pygame window."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CMainView Pygame App")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)  # Default font, size 30
        file_path = "people.txt"
        self.char_lm.instantiate_people_from_flat_file(file_path)
        self.char_lm.print_list()

    def draw_mouse_coordinates(self):
        """Draw the mouse coordinates in the top-right corner."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coord_text = f"X: {mouse_x}, Y: {mouse_y}"
        text_surface = self.font.render(coord_text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text_surface, text_rect)

    def draw_center_blue_rectangle(self):
        """Draw a blue rectangle in the center of the window."""
        rect_width, rect_height = 100, 80
        rect_x = (self.width - rect_width) // 2
        rect_y = (self.height - rect_height) // 2
        pygame.draw.rect(self.screen, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height))

    def run(self):
        """Main game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))  # Clear screen with black

            # Draw UI elements
            self.draw_mouse_coordinates()
            self.draw_center_blue_rectangle()

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Cap the frame rate at 60 FPS


if __name__ == "__main__":
    app = CMainView()
    app.run()
