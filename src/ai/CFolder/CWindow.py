import pygame
import sys

class CWindow:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 24)
        self.score = 0
        self.score_running = False
        self.last_score_time = pygame.time.get_ticks()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.toggle_activate_lines = 0
        
    def draw_mouse_coordinates(self, pygame_p):
        """Draws mouse coordinates in the top-right corner."""
        mouse_x, mouse_y = pygame_p.mouse.get_pos()
        coord_text = f"({mouse_x}, {mouse_y})"
        text_surface = self.font.render(coord_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text_surface, text_rect)
        
    def draw_button(self, rect_x, rect_y, rect_width, rect_height, pygame_p):
        pygame_p.draw.rect(self.screen, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height), 0)
        
        
    def draw_line_button(self, rect_x, rect_y, rect_width, rect_height, pygame_p):
        pygame_p.draw.rect(self.screen, (0, 255, 0), (rect_x, rect_y, rect_width, rect_height), 0)
        
    def find_by_mouse_pos_button(self, mx, my, bx, by, bw, bh):
        button_pressed = 0
        if mx >= bx and mx <= (bx + bw) and my >= by and my <= (by + bh):#found
            if self.toggle_activate_lines == 1:
                button_pressed = 1
            print("button pressed")
        return button_pressed