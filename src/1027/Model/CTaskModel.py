import random

class CTaskModel:
    def __init__(self, name: str):
        self.name = name
        self.number_of_parallel_tasks = 1  # Initialize as 1

    def calc_number_of_parallel_tasks(self):
        self.number_of_parallel_tasks = random.randint(0,10)

    def __repr__(self):
        return f"CTaskModel(name='{self.name}', number_of_parallel_tasks={self.number_of_parallel_tasks})"


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
        """Return the task with the given name, or None if not found."""
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def add_child(self, task: CTaskModel):
        """Add a CTaskModel to the list."""
        self.tasks.append(task)

    def delete_child_by_index(self, index: int):
        """Delete a task by its index in the list."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            print(f"Index {index} is out of range.")

    def delete_child_by_name(self, name: str):
        """Delete all tasks with the given name."""
        self.tasks = [task for task in self.tasks if task.name != name]

    def print_list(self):
        """Print all tasks in the list."""
        for idx, task in enumerate(self.tasks):
            print(f"{idx}: {task}")


if __name__ == "__main__":
    # Example usage
    manager = CTaskModelListManager()

    # Add some tasks
    manager.add_child(CTaskModel("Task1"))
    manager.add_child(CTaskModel("Task2"))
    manager.add_child(CTaskModel("Task3"))

    manager.calc_number_of_parallel_tasks_list()
    biggest_nopt = manager.find_biggest_nopt_list()
    print(biggest_nopt)

    print("Initial task list:")
    manager.print_list()

