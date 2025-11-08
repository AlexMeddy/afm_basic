import pygame
import sys


class CMainView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("CMainView Example")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def draw_mouse_coordinates(self):
        """Draw the current mouse coordinates at the top-right corner."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coord_text = f"({mouse_x}, {mouse_y})"
        text_surface = self.font.render(coord_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text_surface, text_rect)

    def draw_center_rectangle(self):
        """Draw a blue rectangle in the middle of the screen."""
        rect_width, rect_height = 150, 100
        rect_x = (self.width - rect_width) // 2
        rect_y = (self.height - rect_height) // 2
        pygame.draw.rect(self.screen, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height))

    def run(self):
        """Main loop of the app."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))  # Clear screen with black
            self.draw_center_rectangle()
            self.draw_mouse_coordinates()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    app = CMainView()
    app.run()
