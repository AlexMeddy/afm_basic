# ------------------------ controller ------------------------
from CFolderModel import CFolderModel
from CFolderView import CFolderView

class CController:
    # ------------------------ methods ------------------------
    def print_tree_model(model_p):
        if model_p != None:
            if not isinstance(model_p, CFolderModel):
                raise TypeError(f"Expected CFolderModel, got {type(model_p).__name__}")
            print(model_p.guid)
            for child in model_p.children_list:
                CController.print_tree_model(child)
        else:
            print("empty tree")
        
    def print_tree_view(view_p):
        print(view_p.guid, view_p.x, view_p.y)
        for child in view_p.children_list:
            CController.print_tree_view(child)
        
    @staticmethod
    def map_from_model_to_view(view_p):
        view_obj = None
        view_obj = CFolderView(view_p.guid, -1, -1, -1, -1, view_p.parent)
        return view_obj
       
        
    @staticmethod
    def map_from_model_to_view_treev2(model_p, view_root_global_p):
        view_root_global = view_root_global_p
        if model_p.parent == None: #r1- if this node is root
            view_root_global = CController.map_from_model_to_view(model_p)
        else:
            view_parent = view_root_global.find_by_guid_tree(model_p.parent.guid)
            new_view_node = CFolderView(model_p.guid, -1, -1, -1, -1, view_parent)
            view_parent.add_child(new_view_node)
        for child in model_p.children_list:
            view_root_global = CController.map_from_model_to_view_treev2(child, view_root_global)
        return view_root_global

    @staticmethod
    def map_from_model_to_view_tree(model_p, view_root_global_p):
        view_root_global = view_root_global_p
        if view_root_global == None: #if this tree exists
            view_root_global = CController.map_from_model_to_view(model_p)
        else:
            view_parent = view_root_global.find_by_guid_tree(model_p.parent.guid)
            new_view_node = CFolderView(model_p.guid, -1, -1, -1, -1, view_parent)
            view_parent.add_child(new_view_node)
        for child in model_p.children_list:
            view_root_global = CController.map_from_model_to_view_tree(child, view_root_global)
        return view_root_global
        
    @staticmethod
    def map_from_model_to_viewv3(model_p, view_root_global_p):
        view_root_global = view_root_global_p
        if view_root_global == None: #if this tree exists
            view_root_global = CFolderView(model_p.guid, -1, -1, -1, -1, model_p.parent)
        else:
            view_parent = view_root_global.find_by_guid_tree(model_p.parent.guid)
            new_view_node = CFolderView(model_p.guid, -1, -1, -1, -1, view_parent)
            view_parent.add_child(new_view_node)
        return view_root_global
        
    @staticmethod
    def map_from_model_to_view_treev3(model_p, view_root_global_p):
        view_root_global = CController.map_from_model_to_viewv3(model_p, view_root_global_p)
        for child in model_p.children_list:
            view_root_global = CController.map_from_model_to_view_treev3(child, view_root_global)
        return view_root_global
        
    @staticmethod
    def map_from_model_tree_to_view(view_list_global_p, model_p):
        view_obj = None
        view_obj = CFolderView(model_p.guid, -1, -1, -1, -1, model_p.parent)
        view_list_global_p.append(view_obj)
        return view_list_global_p
        
    @staticmethod
    def map_from_model_tree_to_view_tree(model_p, view_list_global_p):
        view_list_global = view_list_global_p
        view_list_global = CController.map_from_model_tree_to_view(view_list_global, model_p)
        for child in model_p.children_list:
            CController.map_from_model_tree_to_view_tree(child, view_list_global)
        return view_list_global
        
        
    @staticmethod
    def calc_level(level_p):
        level = level_p
        level +=1
        return level
        
    @staticmethod
    def calc_level_tree(model_p, level_p):
        level = level_p
        level = CController.calc_level(level)
        for child in model_p.children_list:
            level = CController.calc_level_tree(child, level)
        return level

    @staticmethod
    def map_from_view_to_model(model_obj_p):
        model_obj = model_obj_p
        if model_obj == None:
            model_obj = CFolderModel("root", None)
        else:
            model_parent = model_obj.find_by_guid_tree(model_obj.parent.guid)
            new_model_node = CFolderModel(model_obj.guid, model_parent)
            model_parent.add_child(new_model_node)
        return model_obj
        
    @staticmethod
    def map_from_view_to_model_linear_backup(view_list_p):
        for child in view_list_p:
            model_root = CController.map_from_view_to_model(child)
            print(model_root.guid)
        return model_root
    
    #1 contract
    #2 test contract
    #3 add dummy
    #4 test dummy
    #5 go through linear list and print each
    #6 test step 5
    #7 add check if tree doesnt exist
    #8 test step 7
    #9 add check if tree does exist
    #10 test step 9
    #11 dont copy the whole line
    #12 put the paramater names
    # summary:go through the tree and check if the tree doesnt exist and if it doesnt then create root... 
    @staticmethod
    def map_from_view_to_model_linear(linear_list_p):
        model_root = None
        for child in linear_list_p: #go through the list
            if model_root == None:#if tree doesnt exist
                model_root = CFolderModel(child.guid, None)
                print("model_root is none")
            else:
                print("model_root isnt none", child.guid)
                model_parent = model_root.find_by_guid_tree(guid= child.parent.guid)
                new_model_child = CFolderModel(child.guid, model_parent)
                model_parent.add_child(child=new_model_child)
        return model_root

# ------------------------ main ------------------------
if __name__ == "__main__":
    file_path = "CFolderModel.txt"
    root_model = CFolderModel.instantiate_from_flat_file(file_path)   
    root_view = CController.map_from_model_to_view_treev3(root_model,view_root_global_p = None)
    print("printing view tree------------------------")
    CController.print_tree_view(view_p = root_view)
    print("printing model tree------------------------")
    CController.print_tree_model(model_p = root_model)
    
    '''
    view_list_global = []
    view_list_global = CController.map_from_model_tree_to_view_tree(root_model, view_list_global)
    for child in view_list_global:
        print(child.guid)
        
    view_obj = CFolderView("test", -1, -1, -1, -1, None)
    print("testing map_from_view_to_model_linear")
    model_root = CController.map_from_view_to_model_linear(linear_list_p = view_list_global)
    CController.print_tree_model(model_p = model_root)
    '''