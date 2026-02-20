"""
make a python program to write the file system of my computer into a flat file
-with a limit
-make it so it writes the name of the folder followed by the parent followed by the size of the folder in bytes (e.g. C,None,100 or Program Files,C,90)
"""
import os
import time

output_file = "CFolderModel.txt"
root = "C:\\local alex\\test"
LIMIT = 10


def get_folder_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_folder_size(entry.path)
    except:
        pass
    return total


def resize(size):
    return int(size ** 0.3)

while True:
    time.sleep(1)
    count = 0

    with open(output_file, "w", encoding="utf-8") as f:

        for current_path, dirs, files in os.walk(root):

            if count >= LIMIT:
                break

            # limit to 2 folders only
            dirs[:] = dirs[:10]

            # --- folder name ---
            if current_path == root:
                folder_name = "test"
            else:
                folder_name = os.path.basename(current_path)

            # --- parent name ---
            if current_path == root:
                parent_name = "None"
            else:
                parent_name = os.path.basename(os.path.dirname(current_path))

            # --- get real size ---
            real_size = get_folder_size(current_path)

            # --- resize ---
            size = resize(real_size)

            if size < 1:
                size = 1

            line = f"{folder_name},{parent_name},{size}"
            f.write(line + "\n")
            
            print(line)

            count += 1

    print("Flat file generated successfully.")


