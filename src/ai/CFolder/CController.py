from CFolderModel import CFolderModel
from CFolderView import CFolderView

class CController:
    def __init__(self):
        pass

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
    def map_from_model_to_view(model_p, view_root_global_p):
        view_root_global = view_root_global_p
        if view_root_global == None: #if this tree exists
            view_root_global = CFolderView(model_p.guid, -1, -1, -1, -1, model_p.parent)
        else:
            view_parent = view_root_global.find_by_guid_tree(model_p.parent.guid)
            new_view_node = CFolderView(model_p.guid, -1, -1, -1, -1, view_parent)
            view_parent.add_child(new_view_node)
        return view_root_global
        
    @staticmethod
    def map_from_model_to_view_tree(model_p, view_root_global_p):
        view_root_global = CController.map_from_model_to_view(model_p, view_root_global_p)
        for child in model_p.children_list:
            view_root_global = CController.map_from_model_to_view_tree(child, view_root_global)
        return view_root_global


# ------------------------ main ------------------------
if __name__ == "__main__":
    file_path = "CFolderModel.txt"
    root_model = CFolderModel.instantiate_from_flat_file(file_path)   
    root_view = CController.map_from_model_to_view_tree(root_model,view_root_global_p = None)
    print(root_view.guid)
    print("printing view tree------------------------")
    CController.print_tree_view(root_view)
    print("printing model tree------------------------")
    CController.print_tree_model(root_model)
