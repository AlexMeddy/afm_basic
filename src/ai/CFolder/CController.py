# ------------------------ controller ------------------------
from CFolderModel import CFolderModel
from CFolderView import CFolderView

class CController:
    # ------------------------ methods ------------------------
    def print_tree(model_p):
        print(model_p.guid)
        for child in model_p.children_list:
            child.print_tree(child)

    @staticmethod
    def map_from_model_to_view(model_p):
        if model_p.parent != None:
            parent = model_p.find_by_guid_tree(model_p.parent.guid)
            if parent:
                parent.add_child(model_p)
        return model_p
        
    @staticmethod
    def map_from_model_to_view_tree(model_p):
        model = CController.map_from_model_to_view(model_p)
        for child in model.children_list:
            model = CController.map_from_model_to_view_tree(child)
        return model


# ------------------------ main ------------------------
if __name__ == "__main__":
    file_path = "CFolderModel.txt"
    root_obj = CFolderModel.instantiate_from_flat_file(file_path)   
    print(root_obj.parent.guid)
    folder_model2 = CController.map_from_model_to_view_tree(root_obj)
    #if folder_model2:
    #   CController.print_tree(root_obj)

