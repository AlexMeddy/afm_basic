# ------------------------ core class  ------------------------
from typing import List, Optional


class CFileModel:
    def __init__(self, name: str, parent: Optional["CFileModel"] = None):
        self.name: str = name
        self.file_list: List[CFileModel] = []
        self.tnof: int = 0   # total number of files (placeholder)
        self.parent: Optional[CFileModel] = parent

    # ------------------------ methods ------------------------
    def calc_tnof(self) -> int:
        """
        Mockup only. 
        Pretend to calculate total number of files (self + children).
        """
        self.tnof = 1 + sum(child.calc_tnof() for child in self.file_list)
        return self.tnof

    def print_list(self, indent: int = 0):
        """
        Print tree recursively.
        """
        print(" " * indent + f"- {self.name}")
        for child in self.file_list:
            child.print_list(indent + 2)

    def find_by_name_list(self, name: str) -> List["CFileModel"]:
        """
        Find all nodes with given name.
        """
        result = []
        if self.name == name:
            result.append(self)
        for child in self.file_list:
            result.extend(child.find_by_name_list(name))
        return result

    # ------------------------ instantiation ------------------------
    @classmethod
    def instantiate_from_flat_file(cls, filepath: str) -> Optional["CFileModel"]:
        """
        Reads character by character from FileModel.txt.
        Format: simple nested tree using braces.
        Example:
            root{
                folder1{
                    fileA
                    fileB
                }
                folder2{
                    fileC
                }
            }
        """
        with open(filepath, "r") as f:
            data = f.read()

        # parsing stack
        stack: List[CFileModel] = []
        current_name = ""
        root = None

        i = 0
        while i < len(data):
            ch = data[i]

            if ch.isalnum() or ch in ("_", ".", "-"):
                current_name += ch

            elif ch == "{":
                if current_name.strip():
                    node = cls(current_name.strip(), stack[-1] if stack else None)
                    if stack:
                        stack[-1].file_list.append(node)
                    else:
                        root = node
                    stack.append(node)
                    current_name = ""
            elif ch == "}":
                if current_name.strip():
                    node = cls(current_name.strip(), stack[-1] if stack else None)
                    stack[-1].file_list.append(node)
                    current_name = ""
                stack.pop()
            elif ch in ["\n", " ", "\t"]:
                if current_name.strip():
                    node = cls(current_name.strip(), stack[-1] if stack else None)
                    if stack:
                        stack[-1].file_list.append(node)
                    else:
                        root = node
                    current_name = ""
            i += 1

        return root


# ------------------------ sample file ------------------------
# Save this as FileModel.txt
"""
root{
    folder1{
        fileA
        fileB
    }
    folder2{
        fileC
        folder3{
            fileD
        }
    }
}
"""


# ------------------------ main ------------------------
if __name__ == "__main__":
    root = CFileModel.instantiate_from_flat_file("FileModel.txt")

    if root:
        print("File structure:")
        root.print_list()

        print("\nCalculating total number of files (mockup):")
        print(root.calc_tnof())

        print("\nFinding all 'fileC':")
        results = root.find_by_name_list("fileC")
        for r in results:
            print("Found:", r.name)
