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
        pass


# ------------------------ main ------------------------
if __name__ == "__main__":
    file_path = "CFolderModel.txt"
    folder_model = CFolderModel('r', None)
    folder_model.instantiate_from_flat_file(file_path)   
    folder_model = CController.map_from_model_to_view(folder_model)
    if folder_model:
        CController.print_tree(folder_model)

