class CPersonModel:
    def __init__(self, name: str, height: int):
        """Initialize a person with a name, height, and an empty children list."""
        self.name = name
        self.height = height
        self.children_list = []

    def __repr__(self):
        """Represent the object as a string."""
        return f"CPersonModel(name='{self.name}', height={self.height}, children={len(self.children_list)})"

    def find_tallest_tree(self, highest_person_p):
        highest_person = highest_person_p
        if self.height > highest_person:
            highest_person = self.height
        for child in self.children_list:
            highest_person = child.find_tallest_tree(highest_person) 
        return highest_person

    def find_by_name_recursive(self, name: str):
        """Recursively search for a person by name."""
        if self.name == name:
            return self
        for child in self.children_list:
            found = child.find_by_name_recursive(name)
            if found:
                return found
        return None

    def add_child(self, child: "CPersonModel"):
        """Add a child to this person."""
        self.children_list.append(child)

    def delete_child_by_index(self, index: int):
        """Delete a child by index."""
        if 0 <= index < len(self.children_list):
            del self.children_list[index]
        else:
            print(f"Index {index} is out of range for {self.name}.")

    def delete_child_by_name(self, name: str):
        """Delete all children (recursively) with a given name."""
        self.children_list = [child for child in self.children_list if child.name != name]
        for child in self.children_list:
            child.delete_child_by_name(name)

    def print_list_recursive(self, level=0):
        """Recursively print the tree structure with indentation."""
        print("  " * level + f"{self.name} (Height: {self.height})")
        for child in self.children_list:
            child.print_list_recursive(level + 1)

    @staticmethod
    def instantiate_people_from_flat_file(file_path: str):
        """
        Instantiate a tree of people from a comma-delimited flat file:
        Each line: name,height,parent
        'None' as parent marks the root node.
        """
        people = {}
        root = None

        try:
            # First pass: Create all people
            with open(file_path, "r") as file:
                for line in file:
                    parts = [p.strip() for p in line.strip().split(",")]
                    if len(parts) != 3:
                        print(f"Invalid line format: {line.strip()}")
                        continue

                    name, height_str, parent = parts
                    try:
                        height = int(height_str)
                    except ValueError:
                        print(f"Invalid height value in line: {line.strip()}")
                        continue

                    person = CPersonModel(name, height)
                    people[name] = person

                    if parent.lower() == "none":
                        root = person

            # Second pass: Assign children
            with open(file_path, "r") as file:
                for line in file:
                    parts = [p.strip() for p in line.strip().split(",")]
                    if len(parts) != 3:
                        continue
                    name, _, parent = parts
                    if parent.lower() != "none":
                        parent_person = people.get(parent)
                        if parent_person:
                            parent_person.add_child(people[name])
                        else:
                            print(f"Warning: Parent '{parent}' not found for '{name}'.")

            return root
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None


if __name__ == "__main__":
    # Path to the file
    file_path = "people.txt"

    # Build the tree
    root_person = CPersonModel.instantiate_people_from_flat_file(file_path)

    if root_person:
        print("\nFamily Tree:")
        root_person.print_list_recursive()
        tallest_person = root_person.find_tallest_tree(0)
        print(tallest_person)
        # Example: Search for a person
        search_name = "Alice"
        person = root_person.find_by_name_recursive(search_name)
        if person:
            print(f"\nFound person: {person}")
        else:
            print(f"\nPerson '{search_name}' not found.")
