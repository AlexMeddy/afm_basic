import pygame
import sys

class CMainView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CMainView - Pygame Example")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def draw_mouse_coordinates(self):
        """Draw mouse coordinates in the top-right corner."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coord_text = f"({mouse_x}, {mouse_y})"
        text_surface = self.font.render(coord_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text_surface, text_rect)

    def draw_center_rectangle(self):
        """Draw a blue rectangle in the center of the screen."""
        rect_width, rect_height = 200, 150
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

            self.screen.fill((30, 30, 30))  # dark background
            self.draw_tree
            self.draw_center_rectangle()
            self.draw_mouse_coordinates()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = CMainView()
    app.run()
