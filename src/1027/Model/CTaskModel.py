import random


class CTaskModel:
    def __init__(self, name: str, st: int = 1, et: int = 1):
        self.name = name
        self.number_of_parallel_tasks = 1  # Always start with 1
        self.st = st  # Start time as integer
        self.et = et  # End time as integer

    def calc_number_of_parallel_tasks(self):
        self.number_of_parallel_tasks = random.randint(1, 10)


    def __repr__(self):
        return (f"CTaskModel(name='{self.name}', "
                f"number_of_parallel_tasks={self.number_of_parallel_tasks}, "
                f"st={self.st}, et={self.et})")


class CTaskModelListManager:
    def __init__(self):
        self.tasks = []

    def calc_number_of_parallel_tasks_list(self):       
        for child in self.tasks:
            child.calc_number_of_parallel_tasks()
            
    def find_biggest_nopt_list(self):
        highest_nopt = 0
        for child in self.tasks:
            if child.number_of_parallel_tasks > highest_nopt:
                highest_nopt = child.number_of_parallel_tasks
        return highest_nopt

    def find_by_name(self, name: str):
        """Find and return a task by name."""
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def add_child(self, task: CTaskModel):
        """Add a task to the list."""
        self.tasks.append(task)

    def delete_child_by_index(self, index: int):
        """Delete a task by index."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            print(f"Index {index} is out of range.")

    def delete_child_by_name(self, name: str):
        """Delete all tasks with the given name."""
        self.tasks = [task for task in self.tasks if task.name != name]

    def print_list(self):
        """Print all tasks in the list."""
        if not self.tasks:
            print("No tasks available.")
        else:
            for idx, task in enumerate(self.tasks):
                print(f"{idx}: {task}")

    def instantiate_tasks_from_flat_file(self, file_path: str):
        """
        Instantiate tasks from a comma-delimited flat text file.
        Each line can contain multiple task names separated by commas.
        """
        try:
            with open(file_path, "r") as file:
                for line in file:
                    print('printing line: ', line)
                    names = [name.strip() for name in line.strip().split(",")]
                    for name in names:
                        if name:  # Skip empty names
                            self.add_child(CTaskModel(name))
            print(f"Tasks successfully loaded from '{file_path}'.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")


if __name__ == "__main__":
    manager = CTaskModelListManager()

    # Path to the flat file
    file_path = "example.txt"

    # Instantiate tasks from the flat file
    manager.instantiate_tasks_from_flat_file(file_path)
    
    manager.calc_number_of_parallel_tasks_list()
    biggest_nopt = manager.find_biggest_nopt_list()
    print(biggest_nopt)

    # Print all tasks
    print("\nLoaded Tasks:")
    manager.print_list()
