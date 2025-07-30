import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
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
        self.input_box = TextInput(100, 200, 440, 40)
        self.employee_root_obj = None

    def draw_mouse_coordinates(self):
        x, y = pygame.mouse.get_pos()
        coord_text = FONT.render(f"({x}, {y})", True, BLACK)
        text_width = coord_text.get_width()
        self.screen.blit(coord_text, (WIDTH - text_width - 10, 10))  # Top-right corner

    def run(self):
        while self.running:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.input_box.handle_event(event)

            self.input_box.draw(self.screen)
            if self.employee_root_obj:
                self.employee_root_obj.draw(self.screen)
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
