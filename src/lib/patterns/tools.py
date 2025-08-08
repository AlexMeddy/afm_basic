'''
create a console python app, encapsulated in a class named CConsoleApp with main function. 
And 1 generic arg --do_sth as placeholder only.
Include a recursive python class to represent an Employee with the attrbiutes name,
title and parent (as an Employe object), and with method find and display the tree (idented). 
Add code to instantiate the tree from a comma delimited file. 
Instantiate the tree inside CConsoleApp constructor.
Add a method to promote an Employee.
Postfix each recursive method with _recursive.
Rename class Employee to CEmployee_patterns
Provide sample comma delimited file.
Add type checking to CEmployee_patterns
Avoid static methods.
'''
import argparse
import csv
from typing import Optional, List
from CEmployee_pattern import CEmployee_pattern


def build_tree_from_csv(csv_file):
    employees: dict[str, CEmployee_pattern] = {}
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # First pass: create all employee objects
    for row in rows:
        name = row['name']
        title = row['title']
        hourly_rate = row['hourly_rate']

        employees[name] = CEmployee_pattern(name, title,hourly_rate)

    # Second pass: assign parents and build tree
    for row in rows:
        name = row['name']
        parent_name = row['parent']
        if parent_name:
            parent = employees[parent_name]
            employees[name].parent = parent
            parent.add_child(employees[name])
        else:
            root = employees[name]
    
    return root