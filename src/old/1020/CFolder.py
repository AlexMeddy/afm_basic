class CFolder:
    def __init__(self, parent_folder_p, name_p):
        self.child_file_list = []
        self.parent_folder = parent_folder_p
        self.name = name_p
        self.child_folder_list = []
        