# ------------------------ controller ------------------------
from CFolderModel import CFolderModel
from CFolderView import CFolderView

class CController:
    # ------------------------ methods ------------------------
    def print_tree(model_p):
        print(model_p.guid, model_p.x, model_p.y)
        for child in model_p.children_list:
            CController.print_tree(child)

    @staticmethod
    def map_from_model_to_viewv2(model_p):
        if model_p.parent != None:
            parent = model_p.find_by_guid_tree(model_p.parent.guid)
            view = CFolderView(model_p.guid, -1, -1, -1, -1, model_p.parent)
            print(view.guid)
            if parent:
                parent.add_child(model_p)
        else:
            view = CFolderView(model_p.guid, -1, -1, -1, -1, None)
            print(view.guid)
        return model_p
        
    @staticmethod
    def map_from_model_to_view(model_p):
        view_obj = None
        view_obj = CFolderView(model_p.guid, -1, -1, -1, -1, model_p.parent)
        return view_obj
        
        
    @staticmethod
    def map_from_model_to_view_tree(model_p, view_root_so_far_p):
        view_root_so_far = view_root_so_far_p
        if view_root_so_far == None:
            view_root_so_far = CController.map_from_model_to_view(model_p)
        else:
            view_parent = view_root_so_far.find_by_guid_tree(model_p.parent.guid)
            new_view_node = CFolderView(model_p.guid, -1, -1, -1, -1, view_parent)
            view_parent.add_child(new_view_node)
        for child in model_p.children_list:
            view_root_so_far = CController.map_from_model_to_view_tree(child, view_root_so_far)
        return view_root_so_far


# ------------------------ main ------------------------
if __name__ == "__main__":
    file_path = "CFolderModel.txt"
    root_model = CFolderModel.instantiate_from_flat_file(file_path)   
    root_view = CController.map_from_model_to_view_tree(root_model,view_root_so_far_p = None)
    if root_view:
       CController.print_tree(root_view)

