import pygame
import sys
import argparse
import socket
from CFolderView import CFolderView
from CFolderModel import CFolderModel
from CController import CController

class CMainView:
    def __init__(self, mode_p, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CMainView Example")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        #self.model_root_obj = CFolderModel.my_instantiate_from_flat_file("CFolderModel.txt")
        #self.view_root_obj = CFolderView.instantiate_from_flat_file("FolderView.txt")
        #self.view_root_obj = CController.map_from_model_to_view_tree(self.model_root_obj, None) #use CController.map_from_model_to_view_tree()
        print('----------------print tree before calculation-----------------')
        self.view_root_obj = None
        '''
        if self.view_root_obj != None:
            self.view_root_obj.print_tree()
        self.view_root_obj.CALC_ps_TREE()
        self.view_root_obj.CALC_cousin_TREE()
        self.view_root_obj.CALC_space_x_TREE()
        self.view_root_obj.CALC_space_y_TREE()
        self.view_root_obj.calc_x_tree()
        self.view_root_obj.calc_y_tree()
        longest_x = self.view_root_obj.find_longest_width_x_tree(0)
        available_screen_width = self.view_root_obj.find_available_screen_width(self.width)
        longest_y = self.view_root_obj.find_longest_width_y_tree(0)
        available_screen_height = self.view_root_obj.find_available_screen_height(self.height)
        scale_x = self.view_root_obj.calc_scale_x(available_screen_width, longest_x)
        scale_y = self.view_root_obj.calc_scale_y(available_screen_height, longest_y)
        self.view_root_obj.CALC_p_w_TREE(scale_x)
        self.view_root_obj.CALC_p_h_TREE(scale_y)
        self.view_root_obj.CALC_p_x_TREE(scale_x)
        self.view_root_obj.CALC_p_y_TREE(scale_y)
        '''
        self.rect_width = 50
        self.rect_height = 50
        self.rect_x = 10
        self.rect_y = self.height - 60
        print('----------------print tree after calculation-----------------')
        if self.view_root_obj != None:
            self.view_root_obj.print_tree()
        self.sock = None
        self.conn = None   
        self.buffer_size = 1024

        self.mode = mode_p
        if self.mode == "server":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("0.0.0.0", 5000))
            self.sock.listen(1)
            self.sock.setblocking(False)            
            print("Server started")
            
        if self.mode == "client":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("127.0.0.1", 5000))
            self.sock.setblocking(False)

            print("Client connected to server")

    def build_tree(self):
        if self.view_root_obj != None:
            self.view_root_obj.print_tree()
        self.view_root_obj.CALC_ps_TREE()
        self.view_root_obj.CALC_cousin_TREE()
        self.view_root_obj.CALC_space_x_TREE()
        self.view_root_obj.CALC_space_y_TREE()
        self.view_root_obj.calc_x_tree()
        self.view_root_obj.calc_y_tree()
        longest_x = self.view_root_obj.find_longest_width_x_tree(0)
        available_screen_width = self.view_root_obj.find_available_screen_width(self.width)
        longest_y = self.view_root_obj.find_longest_width_y_tree(0)
        available_screen_height = self.view_root_obj.find_available_screen_height(self.height)
        scale_x = self.view_root_obj.calc_scale_x(available_screen_width, longest_x)
        scale_y = self.view_root_obj.calc_scale_y(available_screen_height, longest_y)
        self.view_root_obj.CALC_p_w_TREE(scale_x)
        self.view_root_obj.CALC_p_h_TREE(scale_y)
        self.view_root_obj.CALC_p_x_TREE(scale_x)
        self.view_root_obj.CALC_p_y_TREE(scale_y)
        
    def handle_network_message(self, msg_p):
        parts = msg_p.split(",")
        if len(parts) < 2:
            print("Invalid message:", msg_p)
            
        guid = parts[0].strip()
        action = parts[1].strip()
        print(f"Received: guid: {guid}, action: {action}")
        if self.view_root_obj:
            folder = self.view_root_obj.find_by_guid_tree(guid)
            if folder and action == "select":
                folder.selected = 1
        
    def handle_event(self, event):
        def handle_collision2():
            if self.view_root_obj:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                folder = self.view_root_obj.find_by_mouse_pos_tree(mx = mouse_x, my = mouse_y)
                if folder:
                    print(folder.guid)
                else:
                    print('folder not found')
        def handle_collision3():
            if self.view_root_obj:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                folder = self.view_root_obj.find_by_mouse_pos_tree(mx = mouse_x, my = mouse_y)
                if folder:
                    print(folder.guid)
                    if folder.selected == 0:
                        folder.selected = 1
                        msg = f"{folder.guid},select"
                        if self.mode == "server" and self.conn:
                            self.conn.sendall(msg.encode())
                        elif self.mode == "client":
                            self.sock.sendall(msg.encode())
                    else:
                        folder.selected = 0
                else:
                    print('folder not found')
        def handle_collision4():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_pressed = self.find_by_mouse_pos_button(mouse_x, mouse_y, self.rect_x, self.rect_y, self.rect_width, self.rect_height)
            if button_pressed == 1:
                self.view_root_obj = CFolderView.instantiate_from_flat_file("FolderView.txt")
                self.build_tree()
                
        def handle_collision5():    
            if self.view_root_obj != None:
                folder = self.view_root_obj.find_by_selection_tree()
                if folder != None:
                    print("---------", folder.guid)
                if folder.p_x != 0:                   
                    folder.p_x -= 3
                    
        def handle_collision6():    
            if self.view_root_obj != None:
                folder = self.view_root_obj.find_by_selection_tree()
                if folder != None:
                    print("---------", folder.guid)
                if folder.p_x != self.width:                   
                    folder.p_x += 3
                    
        def handle_collision7():    
            if self.view_root_obj != None:
                folder = self.view_root_obj.find_by_selection_tree()
                if folder != None:
                    print("---------", folder.guid)
                if folder.p_y != self.height:                   
                    folder.p_y += 3
                    
        def handle_collision8():    
            if self.view_root_obj != None:
                folder = self.view_root_obj.find_by_selection_tree()
                if folder != None:
                    print("---------", folder.guid)
                if folder.p_y != self.height:                   
                    folder.p_y -= 3
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            handle_collision3()
            handle_collision4()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                handle_collision8()
            if event.key == pygame.K_DOWN:
                handle_collision7()
            if event.key == pygame.K_RIGHT:
                handle_collision6()
            if event.key == pygame.K_LEFT:
                handle_collision5()

    def draw_mouse_coordinates(self):
        """Draws mouse coordinates in the top-right corner."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coord_text = f"({mouse_x}, {mouse_y})"
        text_surface = self.font.render(coord_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, rect_x, rect_y, rect_width, rect_height):
        pygame.draw.rect(self.screen, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height), 0)
        
    def find_by_mouse_pos_button(self, mx, my, bx, by, bw, bh):
        button_pressed = 0
        if mx >= bx and mx <= (bx + bw) and my >= by and my <= (by + bh):#found
            button_pressed = 1
            print("button pressed")
        return button_pressed

    def run(self):
        """Main application loop."""
        running = True
        while running:
            try:
                if self.mode == "server":
                    if self.conn is None:
                        self.conn, addr = self.sock.accept()
                        self.conn.setblocking(False)
                        print("Client connected:", addr)
                    else:
                        data = self.conn.recv(self.buffer_size)
                        if data:
                            msg = data.decode()
                            self.handle_network_message(msg)

                elif self.mode == "client":
                    data = self.sock.recv(self.buffer_size)
                    if data:
                        msg = data.decode()
                        self.handle_network_message(msg)
            except BlockingIOError:
                pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.screen.fill((0, 0, 0))  # Clear screen
            self.draw_mouse_coordinates()
            self.draw_button(self.rect_x, self.rect_y, self.rect_width, self.rect_height)
            if self.view_root_obj != None:
                self.view_root_obj.draw_tree(self.screen, pygame, self.font)
                self.view_root_obj.draw_line_tree(self.screen, pygame)
                self.view_root_obj.draw_guid_tree(self.screen, self.font)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["server", "client"],
        required=True,
        help="Run as socket server or client"
    )
    
    args = parser.parse_args()
    
    app = CMainView(mode_p=args.mode)
    
        
    app.run()
