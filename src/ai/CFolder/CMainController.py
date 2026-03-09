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
        self.window = CWindow(width=900, height=800)
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
        
        self.pending_tree_data = []
        self.waiting_for_tree = False

        print('----------------print tree before calculation-----------------')
        self.rect_width = 50
        self.rect_height = 50
        self.rect_x = 10
        self.rect_y = self.window.height - 60
        self.toggle_activate_lines = 0
        print('----------------print tree after calculation-----------------')
        #if self.view_root_obj != None:
            #self.view_root_obj.print_tree()
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
    
    def is_game_finished(self):
        if self.view_root_obj is None:
            return False
        nodes = []
        nodes = self.view_root_obj.collect_all_nodes_tree(nodes)
        for node in nodes:
            guid_value = node.guid
            if guid_value != "root":
                if guid_value != "ghost":
                    return False
        return True
    
    @staticmethod
    def map_from_model_to_view(model_p):
        view_obj = None
        view_obj = CTreeView(model_p.guid, x = -1, y = -1, w = 100, h = 100, parent = None)
        view_obj.model_size = model_p.size
        return view_obj
    
    @staticmethod
    def map_from_model_to_view_tree(model_p, view_root_global_p):
        view_root_global = view_root_global_p
        if view_root_global == None: #if this tree exists
            view_root_global = CMainController.map_from_model_to_view(model_p)
        else:
            view_parent = view_root_global.find_by_guid_tree(model_p.parent.guid)
            new_view_node = CTreeView(model_p.guid, x = -1, y = -1, w = 100, h = 100, parent = view_parent)
            new_view_node.model_size = model_p.size
            view_parent.add_child(new_view_node)
        for child in model_p.children_list:
            view_root_global = CMainController.map_from_model_to_view_tree(child, view_root_global)
        return view_root_global

    def align_tree_view(self):
        if self.view_root_obj != None:
            #self.view_root_obj.print_tree()
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
            self.view_root_obj.CALC_p_w_TREE(scale_x) #when game scale is 1
            self.view_root_obj.CALC_p_h_TREE(scale_y) #when game scale is 1
            self.view_root_obj.CALC_p_x_TREE(scale_x)
            self.view_root_obj.CALC_p_y_TREE(scale_y)
        
    def map_from_resistor_model_to_view_linear(self, resistor_list_p): #list to tree
        view_root = None
        view_root = CTreeView.tree_append(view_root, "d_root", "None")
        for child in resistor_list_p: #go through the list
            view_root = CTreeView.tree_append(view_root, child.guid, view_root.guid, w_p = child.current, h_p = child.current)
        return view_root
        
    def handle_network_message(self, msg_p):
        if msg_p.startswith("tree_blob|"):
            print("new msg: ", msg_p)
            if self.mode == "client":
                raw = msg_p[len("tree_blob|"):].replace("\\n", "\n")
                lines = raw.split("\n")

                node_map = {}
                parent_map = {}

                for line in lines:
                    if line.strip() == "":
                        continue

                    parts = line.split(",")

                    if len(parts) >= 2:
                        guid = parts[0]
                        parent = parts[1]

                        node_map[guid] = CTreeView(guid=guid, x=-1, y=-1, w=50, h=50)
                        parent_map[guid] = parent

                root = None

                for guid, node in node_map.items():
                    parent_guid = parent_map[guid]

                    if parent_guid == "None":
                        root = node
                    else:
                        parent_node = node_map.get(parent_guid)
                        if parent_node:
                            parent_node.add_child(node)

                self.view_root_obj = root

                if self.view_root_obj:
                    self.view_root_obj.calc_i_self_tree(0)
                    self.align_tree_view()
                    print("Tree received and built")

            return
        """
        if msg_p.startswith("tree_data_end"):
            if self.mode == "client" and self.waiting_for_tree:
                print("Finished receiving tree")
                node_map = {}
                parent_map = {}
                for line in self.pending_tree_data:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        guid = parts[0]
                        parent = parts[1]
                        node_map[guid] = CTreeView(guid=guid, x=-1, y=-1, w=50, h=50)
                        parent_map[guid] = parent
                root = None
                for guid, node in node_map.items():
                    parent_guid = parent_map[guid]
                    if parent_guid == "None":
                        root = node
                    else:
                        parent_node = node_map.get(parent_guid)
                        if parent_node:
                            parent_node.add_child(node)
                self.view_root_obj = root
                if self.view_root_obj:
                    self.view_root_obj.calc_i_self_tree(0)
                    self.align_tree_view()
                    print("Tree received and built successfully")
                self.waiting_for_tree = False
                self.pending_tree_data = []
            return

        if msg_p.startswith("tree_data"):
            print("FROM SERVER:", msg_p)
            if self.mode == "client":
                content = msg_p.replace("tree_data,", "").strip()
                self.pending_tree_data.append(content)
            return
        """
        if msg_p.strip() == "request_tree":
            if self.mode == "server":
                print("FROM CLIENT: request_tree")

                if not self.view_root_obj:
                    return

                nodes = self.view_root_obj.collect_all_nodes_tree()

                lines = []
                for node in nodes:
                    parent_guid = "None"
                    if node.parent:
                        parent_guid = node.parent.guid

                    lines.append(f"{node.guid},{parent_guid}")

                tree_blob = "\\n".join(lines)
                send_msg = f"tree_blob|{tree_blob}\n"

                self.my_socket.broadcast(send_msg)

            return



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
                
        
    def handle_event(self, event):
        messages_to_send = []  # collect all messages to send at once

        def handle_collision2():
            if self.view_root_obj:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                folder = self.view_root_obj.find_by_single_point_tree(pointer_x=mouse_x, pointer_y=mouse_y, filter_p="")
                if folder:
                    print(folder.guid)
                else:
                    print('folder not found')

        def select():
            if self.view_root_obj:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                folder = self.view_root_obj.find_by_single_point_tree(pointer_x=mouse_x, pointer_y=mouse_y, filter_p="")
                if folder:
                    folder.selected = 0 if folder.selected else 1
                    action = "select" if folder.selected else "deselect"
                    msg = f"{folder.guid},{action}\n"
                    messages_to_send.append(msg)

        def initiate_tree():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_pressed = self.window.find_by_mouse_pos_button(mouse_x, mouse_y, self.rect_x, self.rect_y, self.rect_width, self.rect_height)
            if button_pressed == 1:
                if self.model_src == "v":
                    self.view_root_obj = CTreeView.instantiate_from_flat_file("TreeView.txt")
                elif self.model_src == "r":
                    self.resistor_manager.instantiate_from_flat_file("ResistorModelctreetest.txt")
                    self.view_root_obj = self.map_from_resistor_model_to_view_linear(resistor_list_p=self.resistor_manager.resistor_list)
                elif self.model_src == "m":
                    self.view_root_obj = None
                    self.model_root_obj = CFolderModel.my_instantiate_from_flat_file("CFolderModel.txt")
                    if self.model_root_obj:
                        self.model_root_obj.size = 10
                        self.view_root_obj = CMainController.map_from_model_to_view_tree(self.model_root_obj, None)
                        biggest_node = self.view_root_obj.find_by_biggest_size_tree(self.view_root_obj)
                        biggest_node.is_biggest = 1
                elif self.model_src == "g":
                    if self.mode == "client":
                        self.view_root_obj = None
                        self.pending_tree_data = []
                        self.waiting_for_tree = True
                        messages_to_send.append("request_tree\n")
                    elif self.mode == "server":
                        self.view_root_obj = CTreeView.instantiate_from_flat_file("TreeView.txt")

                if self.view_root_obj:
                    self.view_root_obj.calc_i_self_tree(0)
                self.align_tree_view()
                self.window.score = 0
                self.window.score_running = True
                self.window.last_score_time = pygame.time.get_ticks()

        def delete():
            if self.view_root_obj:
                folders_list = self.view_root_obj.find_list_by_selection_tree([])
                for folder in folders_list:
                    folder.delete()
                    self.view_root_obj.calc_i_self_tree(0)
                    msg = f"{folder.guid},delete\n"
                    messages_to_send.append(msg)
            self.align_tree_view()

        def add_child():
            count = 0
            if self.view_root_obj:
                folders_list = self.view_root_obj.find_list_by_selection_tree([])
                for folder in folders_list:
                    for child in folder.children_list:
                        if child.guid.startswith(folder.guid):
                            count += 1
                    new_child = CTreeView(f"{folder.guid}{count + 1}", -1, -1, 100, 100)
                    folder.add_child(new_child)
                self.align_tree_view()

        def toggle_lines():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.window.toggle_activate_lines = self.window.find_by_mouse_pos_button(
                mouse_x, mouse_y, self.rect_x+self.rect_width+10, self.rect_y, self.rect_width, self.rect_height
            )
            self.window.toggle_activate_lines = 1 if self.window.toggle_activate_lines == 0 else 0

        def move(vertical_direction_p, horizontal_direction_p):
            if self.view_root_obj:
                folders_list = self.view_root_obj.find_list_by_selection_tree([])
                for folder in folders_list:
                    folder.p_y += vertical_direction_p
                    folder.p_x += horizontal_direction_p
                    msg = f"{folder.guid},move,{int(folder.p_x)},{int(folder.p_y)}\n"
                    messages_to_send.append(msg)

        if event.type == pygame.MOUSEBUTTONDOWN:
            select()
            initiate_tree()
            if self.mode == "server" and self.view_root_obj:
                ghost = self.view_root_obj.find_by_guid_tree("ghost")
                self.bot_player = CBotPlayer(guid="bot", ghost_p=ghost, window_width=self.window.width, window_height=self.window.height)
            toggle_lines()

        if event.type == pygame.KEYDOWN:
            speed = 9
            if event.key == pygame.K_UP:
                move(-speed, 0)
            if event.key == pygame.K_DOWN:
                move(speed, 0)
            if event.key == pygame.K_LEFT:
                move(0, -speed)
            if event.key == pygame.K_RIGHT:
                move(0, speed)
            if event.key == pygame.K_DELETE:
                delete()
            if event.key == pygame.K_a and (event.mod & pygame.KMOD_CTRL):
                add_child()

        for msg in messages_to_send:
            if self.mode == "server":
                self.my_socket.broadcast(msg)
            elif self.mode == "client":
                self.my_socket.send_to_server(msg)

                


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

                                    if msg.strip() != "request_tree":
                                        self.my_socket.broadcast(msg + "\n", sender=conn)
                                        #print_log("socket-------", 1)

                        except BlockingIOError:
                            pass
                        except ConnectionResetError:
                            self.my_socket.clients.remove(conn)
                            conn.close()

                elif self.mode == "client":
                    data = self.my_socket.server_conn.recv(self.buffer_size)
                    if data:
                        raw_msg = data.decode()
                        #print(f"start---------raw msg: {raw_msg}--------end")
                        message_list = raw_msg.split("\n")
                        for msg in message_list:
                            #print("new msg: ", msg)
                            if msg != "":
                                self.handle_network_message(msg)
            except BlockingIOError:
                pass
            if self.window.score_running:
                if self.view_root_obj:
                    only_root_and_ghost_left = self.view_root_obj.is_only_root_and_ghost_left_tree()
                    if only_root_and_ghost_left == True:
                        self.window.score_running = False
                    else:
                        current_time = pygame.time.get_ticks()
                        if current_time - self.window.last_score_time >= 1000:
                            self.window.score += 5
                            self.window.last_score_time = current_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.screen.fill((0, 0, 0))  # Clear screen
            #self.window.draw_mouse_coordinates(pygame)
            self.window.draw_button(self.rect_x, self.rect_y, self.rect_width, self.rect_height, pygame)
            if self.model_src != "g":
                self.window.draw_line_button(self.rect_x+self.rect_width+10, self.rect_y, self.rect_width, self.rect_height, pygame)
            if self.view_root_obj != None:
                if self.mode == "server" and self.model_src == "g" and self.bot_player.ghost != None:
                    if self.mode == "server" and self.bot_player != None:
                        colliding_node = self.bot_player.play(self.view_root_obj)
                        ghost = self.bot_player.ghost
                        msg = f"{ghost.guid},move,{int(ghost.p_x)},{int(ghost.p_y)}\n"
                        self.my_socket.broadcast(msg)
                        if colliding_node:
                            #print("ghost collision", colliding_node.guid)
                            colliding_node.delete()
                            self.view_root_obj.calc_i_self_tree(0)
                            self.align_tree_view()
                            msg = f"{colliding_node.guid},delete\n"
                            self.my_socket.broadcast(msg)
                self.view_root_obj.draw_tree(self.screen, pygame, self.font)
                if self.window.toggle_activate_lines == 1 and self.model_src != "g":
                    self.view_root_obj.draw_line_tree(self.screen, pygame)
                self.view_root_obj.draw_guid_tree(self.screen, self.font)
            score_text = self.font.render(f"score: {self.window.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(topright=(self.window.width - 10, 10))
            self.screen.blit(score_text, score_rect)
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
        choices=["r", "m", "v", "g"],
        required=True,
        help="Run as socket server or client"
    )
    args = parser.parse_args()
    
    app = CMainController(mode_p=args.mode, file_src_p=args.model_src)
    
        
    app.run()