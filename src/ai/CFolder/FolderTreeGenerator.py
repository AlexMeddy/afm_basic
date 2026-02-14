"""
make a python program to write the file system of my computer into a flat file
-with a limit
-make it so it writes the name of the folder followed by the parent followed by the size of the folder in bytes (e.g. C,None,100 or Program Files,C,90)
"""
import os

output_file = "CFolderModel.txt"
root = "C:\\Program Files"
LIMIT = 1000

count = 0

with open(output_file, "w", encoding="utf-8") as f:

    for current_path, dirs, files in os.walk(root):

        if count >= LIMIT:
            break

        # Folder name
        folder_name = os.path.basename(current_path)
        if folder_name == "":
            folder_name = current_path.replace("\\", "").replace(":", "")

        # Parent name
        parent_path = os.path.dirname(current_path)
        parent_name = os.path.basename(parent_path)
        if parent_name == "":
            parent_name = "None"

        # Size is always 1
        size_str = "001"

        line = folder_name + "," + parent_name + "," + size_str
        f.write(line + "\n")

        count += 1


print("Done.")