import sys
sys.path.append("C:\\Users\\alexf\\afm_basic\\src\\ai\\CResistor")
import argparse
import socket
from CTreeView import CTreeView
from CFolderModel import CFolderModel
from CResistorModel import CResistorModel
from CResistorModel import CResistorModelListManager
#from CController import CController
from CWindow import CWindow
from CSocket import CSocket
from CBotPlayer import CBotPlayer
import pygame
import socket

class CMainController:
    def __init__(self, mode_p, file_src_p):
        pygame.init()
        self.window = CWindow(width=800, height=600)
        self.my_socket = CSocket()
        self.screen = pygame.display.set_mode((self.window.width, self.window.height))
        pygame.display.set_caption("CMainController Example")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)       
        self.view_root_obj = None
        self.bot_player = None
        self.resistor_manager = CResistorModelListManager()
        #self.resistor_manager.instantiate_from_flat_file("ResistorModelctreetest.txt")
        #self.view_root_obj = self.map_from_resistor_model_to_view_linear(resistor_list_p = self.resistor_manager.resistor_list)
        self.model_root_obj = None
        #self.model_root_obj = CFolderModel.my_instantiate_from_flat_file("CFolderModel.txt") #C:\\Users\\alexf\\afm_basic\\src\\ai\\CFolder\\CFolderModel.txt
        if self.model_root_obj != None:
            self.model_root_obj.print_list()
        #self.view_root_obj = CMainController.map_from_model_to_view_tree(self.model_root_obj, None) #use CMainController.map_from_model_to_view_tree()
        if self.view_root_obj != None:
            self.align_tree_view()

        print('----------------print tree before calculation-----------------')
        self.rect_width = 50
        self.rect_height = 50
        self.rect_x = 10
        self.rect_y = self.window.height - 60
        self.toggle_activate_lines = 0
        print('----------------print tree after calculation-----------------')
        if self.view_root_obj != None:
            self.view_root_obj.print_tree()
        self.buffer_size = 1024
        self.model_src = file_src_p
        self.mode = mode_p
        if self.mode == "server":
            self.my_socket.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_socket.server_conn.bind(("0.0.0.0", 2012))
            self.my_socket.server_conn.listen()
            self.my_socket.server_conn.setblocking(False)            
            print("Server started")
            
        if self.mode == "client":
            server_ip = args.ip
            if not server_ip:
                raise ValueError("Client requires --ip")

            self.my_socket.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_socket.server_conn.connect((server_ip, 2012))
            self.my_socket.server_conn.setblocking(False)

            print("Client connected to server")
    
    @staticmethod
    def map_from_model_to_view(model_p):
        view_obj = None
        view_obj = CTreeView(model_p.guid, x = -1, y = -1, w = 100 * model_p.size, h = 100 * model_p.size, parent = None)
        return view_obj
    
    @staticmethod
    def map_from_model_to_view_tree(model_p, view_root_global_p):
        view_root_global = view_root_global_p
        if view_root_global == None: #if this tree exists
            view_root_global = CMainController.map_from_model_to_view(model_p)
        else:
            view_parent = view_root_global.find_by_guid_tree(model_p.parent.guid)
            new_view_node = CTreeView(model_p.guid, x = -1, y = -1, w = 100 * model_p.size, h = 100 * model_p.size, parent = view_parent)
            view_parent.add_child(new_view_node)
        for child in model_p.children_list:
            view_root_global = CMainController.map_from_model_to_view_tree(child, view_root_global)
        return view_root_global

    def align_tree_view(self):
        if self.view_root_obj != None:
            self.view_root_obj.print_tree()
        self.view_root_obj.CALC_ps_TREE()
        self.view_root_obj.CALC_cousin_TREE()
        self.view_root_obj.CALC_space_x_TREE()
        self.view_root_obj.CALC_space_y_TREE()
        self.view_root_obj.calc_x_tree()
        self.view_root_obj.calc_y_tree()
        longest_x = self.view_root_obj.find_longest_width_x_tree(0)
        available_screen_width = self.view_root_obj.find_available_screen_width(self.window.width)
        longest_y = self.view_root_obj.find_longest_width_y_tree(0)
        available_screen_height = self.view_root_obj.find_available_screen_height(self.window.height)
        scale_x = self.view_root_obj.calc_scale_x(available_screen_width, longest_x)
        scale_y = self.view_root_obj.calc_scale_y(available_screen_height, longest_y)
        self.view_root_obj.CALC_p_w_TREE(scale_x)
        self.view_root_obj.CALC_p_h_TREE(scale_y)
        self.view_root_obj.CALC_p_x_TREE(scale_x)
        self.view_root_obj.CALC_p_y_TREE(scale_y)
        
    def map_from_resistor_model_to_view_linear(self, resistor_list_p): #list to tree
        view_root = None
        view_root = CTreeView.tree_append(view_root, "d_root", "None")
        for child in resistor_list_p: #go through the list
            view_root = CTreeView.tree_append(view_root, child.guid, view_root.guid, w_p = child.current, h_p = child.current)
        return view_root
        
    def handle_network_message(self, msg_p):
        parts = msg_p.split(",")
        if len(parts) < 2:
            return

        guid = parts[0].strip()
        action = parts[1].strip()

        if not self.view_root_obj:
            return

        folder = self.view_root_obj.find_by_guid_tree(guid)
        if not folder:
            return

        if action == "select":
            folder.selected = 1

        elif action == "deselect":
            folder.selected = 0

        elif action == "move" and len(parts) == 4:
            folder.p_x = int(parts[2])
            folder.p_y = int(parts[3])
        elif action == "delete":
            folder.delete()
            self.view_root_obj.calc_i_self_tree(0)
                
    def broadcast(self, msg, sender=None):
        for client in self.my_socket.clients:
            if client != sender:
                try:
                    client.sendall(msg.encode())
                except:
                    client.close()
                    self.my_socket.clients.remove(client)
        
    def handle_event(self, event):
        def handle_collision2():
            if self.view_root_obj:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                folder = self.view_root_obj.find_by_single_point_tree(pointer_x = mouse_x, pointer_y = mouse_y, filter_p = "")
                if folder:
                    print(folder.guid)
                else:
                    print('folder not found')
        def select():
            if self.view_root_obj:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                folder = self.view_root_obj.find_by_single_point_tree(pointer_x=mouse_x, pointer_y=mouse_y, filter_p = "")
                if folder:
                    folder.selected = 0 if folder.selected else 1
                    action = "select" if folder.selected else "deselect"
                    msg = f"{folder.guid},{action}\n"

                    if self.mode == "server":
                        self.broadcast(msg)
                    elif self.mode == "client":
                        self.my_socket.server_conn.sendall(msg.encode())
        def initiate_tree():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_pressed = self.window.find_by_mouse_pos_button(mouse_x, mouse_y, self.rect_x, self.rect_y, self.rect_width, self.rect_height)
            if button_pressed == 1:
                if self.model_src == "v":
                    self.view_root_obj = CTreeView.instantiate_from_flat_file("TreeView.txt")
                elif self.model_src == "r":
                    self.resistor_manager.instantiate_from_flat_file("ResistorModelctreetest.txt")
                    self.view_root_obj = self.map_from_resistor_model_to_view_linear(resistor_list_p = self.resistor_manager.resistor_list)
                elif self.model_src == "m":
                    self.model_root_obj = CFolderModel.my_instantiate_from_flat_file("CFolderModel.txt")
                    self.view_root_obj = CMainController.map_from_model_to_view_tree(self.model_root_obj, None)
                self.view_root_obj.calc_i_self_tree(0)
                self.view_root_obj.print_tree(0)
                self.align_tree_view()
                
        def delete():    
            if self.view_root_obj != None:
                folders_list = []
                folders_list = self.view_root_obj.find_list_by_selection_tree(folders_list)
                for folder in folders_list:
                    print("----------", folder.guid)
                    folder.delete()
                    self.align_tree_view()
                    self.view_root_obj.calc_i_self_tree(0)
                    self.view_root_obj.print_tree(0)                    
                    msg = f"{folder.guid},delete\n"
                    if self.mode == "server":
                        self.broadcast(msg)
                    elif self.mode == "client":
                        self.my_socket.server_conn.sendall(msg.encode())
        
        def add_child():    
            count = 0
            if self.view_root_obj != None:
                folders_list = []
                folders_list = self.view_root_obj.find_list_by_selection_tree(folders_list)
                for folder in folders_list:
                    for child in folder.children_list:
                        if child.guid.startswith(folder.guid):
                            count += 1
                    new_child = CTreeView(f"{folder.guid}{count + 1}", -1, -1, 100, 100)
                    folder.add_child(new_child)
                    self.align_tree_view()
           
        def toggle_lines():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.window.toggle_activate_lines = self.window.find_by_mouse_pos_button(mouse_x, mouse_y, self.rect_x+self.rect_width+10, self.rect_y, self.rect_width, self.rect_height)
            if self.window.toggle_activate_lines == 0:                
                self.window.toggle_activate_lines = 1
            else:
                self.window.toggle_activate_lines = 0
                
        def handle_collision5():    
            if self.view_root_obj != None:
                folders_list = []
                folders_list = self.view_root_obj.find_list_by_selection_tree(folders_list)
                for folder in folders_list:
                    print("----------", folder.guid)
                    if folder.p_x != self.window.height:                   
                        folder.p_x -= 3 #move local
                        msg = f"{folder.guid},move,{int(folder.p_x)},{int(folder.p_y)}\n"
                        if self.mode == "server":
                            self.broadcast(msg)
                        elif self.mode == "client":
                            print(msg)
                            self.my_socket.server_conn.sendall(msg.encode())
                    
        def handle_collision6():    
            if self.view_root_obj != None:
                folders_list = []
                folders_list = self.view_root_obj.find_list_by_selection_tree(folders_list)
                for folder in folders_list:
                    print("----------", folder.guid)
                    if folder.p_x != self.window.height:                   
                        folder.p_x += 3 #move local
                        msg = f"{folder.guid},move,{int(folder.p_x)},{int(folder.p_y)}\n"
                        if self.mode == "server":
                            self.broadcast(msg)
                        elif self.mode == "client":
                            print(msg)
                            self.my_socket.server_conn.sendall(msg.encode())
                    
        def handle_collision7():    
            if self.view_root_obj != None:
                folders_list = []
                folders_list = self.view_root_obj.find_list_by_selection_tree(folders_list)
                for folder in folders_list:
                    print("----------", folder.guid)
                    if folder.p_y != self.window.height:                   
                        folder.p_y += 3 #move local
                        msg = f"{folder.guid},move,{int(folder.p_x)},{int(folder.p_y)}\n"
                        if self.mode == "server":
                            self.broadcast(msg)
                        elif self.mode == "client":
                            print(msg)
                            self.my_socket.server_conn.sendall(msg.encode())
                    
        def handle_collision8():    
            if self.view_root_obj != None:
                folders_list = []
                folders_list = self.view_root_obj.find_list_by_selection_tree(folders_list)
                for folder in folders_list:
                    print("----------", folder.guid)
                    if folder.p_y != self.window.height:                   
                        folder.p_y -= 3 #move local
                        msg = f"{folder.guid},move,{int(folder.p_x)},{int(folder.p_y)}\n"
                        if self.mode == "server":
                            self.broadcast(msg)
                        elif self.mode == "client":
                            print(msg)
                            self.my_socket.server_conn.sendall(msg.encode())
                            
        def move(vertical_direction_p, horizontal_direction_p):    
            if self.view_root_obj != None:
                folders_list = []
                folders_list = self.view_root_obj.find_list_by_selection_tree(folders_list)
                for folder in folders_list:
                    print("----------", folder.guid)
                    if folder.p_y != self.window.height:       
                        folder.p_y = folder.p_y + vertical_direction_p #move local
                    if folder.p_x != self.window.width:                       
                        folder.p_x = folder.p_x + horizontal_direction_p #move local
                    msg = f"{folder.guid},move,{int(folder.p_x)},{int(folder.p_y)}\n"
                    if self.mode == "server":
                        self.broadcast(msg)
                    elif self.mode == "client":
                        print(msg)
                        self.my_socket.server_conn.sendall(msg.encode())
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            select()
            initiate_tree()
            if self.view_root_obj != None:
                ghost = self.view_root_obj.find_by_guid_tree("ghost")
                self.bot_player = CBotPlayer(guid = "bot", ghost_p = ghost)  
            toggle_lines()
        if event.type == pygame.KEYDOWN:
            speed = 5
            if event.key == pygame.K_UP:
                move(vertical_direction_p = speed *(-1), horizontal_direction_p = 0)
            if event.key == pygame.K_DOWN:
                move(vertical_direction_p = speed *(1), horizontal_direction_p = 0)
            if event.key == pygame.K_RIGHT:
                move(vertical_direction_p = 0, horizontal_direction_p = speed *(1))
            if event.key == pygame.K_LEFT:
                move(vertical_direction_p = 0, horizontal_direction_p = speed *(-1))
            if event.key == pygame.K_DELETE:
                delete()
            if event.key == pygame.K_a and (event.mod & pygame.KMOD_CTRL):
                add_child()
                


    def run(self):
        """Main application loop."""
        running = True
        while running:
            try:
                if self.mode == "server":
                    try:
                        conn, addr = self.my_socket.server_conn.accept()
                        conn.setblocking(False)
                        self.my_socket.clients.append(conn)
                        print("Client connected:", addr)
                    except BlockingIOError:
                        pass

                    for conn in self.my_socket.clients[:]:
                        try:
                            data = conn.recv(self.buffer_size)
                            if data:
                                raw_msg = data.decode()
                                message_list = raw_msg.split("\n")
                                for msg in message_list:
                                    if msg:
                                        self.handle_network_message(msg)
                                        self.broadcast(msg + "\n", sender=conn)
                        except BlockingIOError:
                            pass
                        except ConnectionResetError:
                            self.my_socket.clients.remove(conn)
                            conn.close()

                elif self.mode == "client":
                    data = self.my_socket.server_conn.recv(self.buffer_size)
                    if data:
                        raw_msg = data.decode()
                        print(f"start---------raw msg: {raw_msg}--------end")
                        message_list = raw_msg.split("\n")
                        for msg in message_list:
                            print("new msg: ", msg)
                            if msg != "":
                                self.handle_network_message(msg)
            except BlockingIOError:
                pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.screen.fill((0, 0, 0))  # Clear screen
            self.window.draw_mouse_coordinates(pygame)
            self.window.draw_button(self.rect_x, self.rect_y, self.rect_width, self.rect_height, pygame)
            self.window.draw_line_button(self.rect_x+self.rect_width+10, self.rect_y, self.rect_width, self.rect_height, pygame)
            if self.view_root_obj != None:                               
                colliding_node = self.view_root_obj.find_by_single_point_tree(self.bot_player.ghost.p_x+self.bot_player.ghost.p_w/2, self.bot_player.ghost.p_y+self.bot_player.ghost.p_h/2, "ghost")
                if colliding_node != None:
                    print("ghost collision", colliding_node.guid)
                if self.bot_player != None:
                    self.bot_player.play()                  
                self.view_root_obj.draw_tree(self.screen, pygame, self.font)
                if self.window.toggle_activate_lines == 1:
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
    parser.add_argument("--ip", help="Server IP (client mode only)")
    parser.add_argument(
        "--model_src",
        choices=["r", "m", "v"],
        required=True,
        help="Run as socket server or client"
    )
    args = parser.parse_args()
    
    app = CMainController(mode_p=args.mode, file_src_p=args.model_src)
    
        
    app.run()