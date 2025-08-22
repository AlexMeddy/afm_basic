class CCharacterModel:
    def __init__(self, name: str, frequency: int = 1):
        self.name = name
        self.frequency = frequency

    def calc_frequency(self):
        self.frequency +=1

    def __repr__(self):
        return f"CCharacterModel(name='{self.name}', frequency={self.frequency})"


class CCharacterModelListManager:
    def __init__(self):
        self.characters = []

    def find_by_name(self, name: str):
        """Return the character with the given name, or None if not found."""
        for char in self.characters:
            if char.name == name:
                return char
        return None

    def add_child(self, character: CCharacterModel):
        """Add a CCharacterModel to the list."""
        self.characters.append(character)

    def delete_child_by_index(self, index: int):
        """Delete a character by its index in the list."""
        if 0 <= index < len(self.characters):
            del self.characters[index]
        else:
            print(f"Index {index} is out of range.")

    def delete_child_by_name(self, name: str):
        """Delete all characters with the given name."""
        self.characters = [char for char in self.characters if char.name != name]

    def print_list(self):
        """Print all characters in the list."""
        for idx, char in enumerate(self.characters):
            print(f"{idx}: {char}")

    def read_file_char_by_char(self, file_path: str):
        """
        Reads a flat file character by character and prints each character.
        """
        try:
            with open(file_path, "r") as file:
                while True:
                    char = file.read(1)
                    if not char:  # End of file
                        break
                    print(char, end="")
                    print(type(char))
                    character_obj = self.find_by_name(char)
                    if character_obj != None:
                        character_obj.calc_frequency()
                    else:
                        self.add_child(CCharacterModel(char))
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")


if __name__ == "__main__":
    # Example usage
    manager = CCharacterModelListManager()

    # Read a file character by character (uncomment and replace 'example.txt' with a real file path)
    manager.read_file_char_by_char("example.txt")
    manager.print_list()
