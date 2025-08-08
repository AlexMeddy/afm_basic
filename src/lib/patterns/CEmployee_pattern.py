'''
create a console python app, encapsulated in a class named CConsoleApp with main function. 
And 1 generic arg --do_sth as placeholder only.
Include a recursive python class to represent an Employee with the attrbiutes name,
title and parent (as an Employe object), and with method find and display the tree (idented).
Avoi 
Add code to instantiate the tree
from a comma delimited file.  Instantiate the tree inside CConsoleApp constructor.
Add a method to promote an Employee.
Postfix each recursive method with _recursive.
Avoid static methods.
Rename class Employee to CEmployee_pattern
Provide sample comma delimited file.
'''

class CEmployee_pattern:
    def __init__(self, name, title, hourly_rate,parent=None):
        self.name = name
        self.title = title
        self.parent = parent
        self.hourly_rate = int(hourly_rate)
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def find_by_name_recursive(self, name):
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_by_name_recursive(name)
            if found:
                return found
        return None

    def print_tree_recursive(self, level=0):
        print("    " * level + f"{self.name} ({self.title})  (${self.hourly_rate}))")
        for child in self.children:
            child.print_tree_recursive(level + 1)

    def promote(self, new_title):
        self.title = new_title
    
    def dismiss(self):
        print(f'{self.name} dismissed') #mockup non recursive
        
    def pay_rise_recursive(self):
        print(f'{self.name} pay raised') #mockup recursive
        self.hourly_rate *= 5
        for child in self.children:
            child.pay_rise_recursive()
