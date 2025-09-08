import pygame
import sys
from CFileView import CFileView
# ------------------------ pygame app ------------------------
class CMainView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CFileView Tree Viewer")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load file view tree
        self.root = CFileView.instantiate_from_flat_file("FileView.txt")
        if self.root:
            self.root.print_tree()


    def handle_event(self, event):
        def handle_collision2():
            if self.root:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                chosen_obj = self.root.find_by_mouse_pos_tree(mx = mouse_x, my = mouse_y)
                if chosen_obj:
                    print(chosen_obj.guid)
                    #print(chosen_obj.model.voltage)
                else:
                    print('chosen_obj not found')

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            handle_collision2()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)

            self.screen.fill((0, 0, 0))


            self.root.draw_tree(self.screen)


            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


# ------------------------ entry point ------------------------
if __name__ == "__main__":
    app = CMainView()
    app.run()
