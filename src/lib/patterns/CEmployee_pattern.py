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
import random

class CEmployee_pattern:
    def __init__(self, name, title, hourly_rate,annual_leave_p,bla_p,parent=None):
        self.name = name
        self.title = title
        self.parent = parent
        self.hourly_rate = int(hourly_rate)
        self.children = []
        self.activation_status = 0 #starts off as -1 when calculated later
        self.i_self = -1
        self.annual_leave = int(annual_leave_p)
        self.bla = int(bla_p)
        self.norn = 0 


    def add_child(self, child):
        self.children.append(child)

    def calc_i_self(self, i_self_p):
        self.i_self = i_self_p
        for i_child in range(len(self.children)):
            self.children[i_child].calc_i_self(i_child)

    def find_by_name_recursive(self, name):
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_by_name_recursive(name)
            if found:
                return found
        return None

    def print_tree_recursive(self, level=0):
        print("    " * level + f"{self.name} ({self.title})  (${self.hourly_rate}) ({self.norn}))")
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
            
    def print_guid(self):
        print(f'{self.name} guid tbd') #mockup

    def toggle_activation_employee(self):
        if self.activation_status == 1:
            self.activation_status = 0
        else:
            self.activation_status = 1
        print(self.activation_status)
        
    def find_first_employee_by_activation_status(self):
        if self.activation_status == 1:
            return self
        for child in self.children:
            first_activated_employee = child.find_by_name_recursive(name)
            if first_activated_employee:
                return first_activated_employee
        return None
        
    def delete_chosen_employee(self, index_employee_p):
        if self.i_self == index_employee_p:
            self.parent.children.pop(index_employee_p)
    
    def calculate_highest_hourly_rate_tree(self, highest_hourly_rate_p):
        highest_hourly_rate = highest_hourly_rate_p
        if self.hourly_rate > highest_hourly_rate:
            highest_hourly_rate = self.hourly_rate
        for child in self.children:
            highest_hourly_rate = child.calculate_highest_hourly_rate_tree(highest_hourly_rate) 
        return highest_hourly_rate
    
    def calculate_highest_annual_leave_p(self, highest_annual_leave_p):
        highest_annual_leave = highest_annual_leave_p
        if self.annual_leave > highest_annual_leave:
            highest_annual_leave = self.annual_leave
        for child in self.children:
            highest_annual_leave = child.calculate_highest_annual_leave_p(highest_annual_leave) 
        return highest_annual_leave
        
    def calculate_highest_bla_p(self, highest_bla_p):
        highest_bla = highest_bla_p
        if self.bla > highest_bla:
            highest_bla = self.bla
        for child in self.children:
            highest_bla = child.calculate_highest_bla_p(highest_bla) 
        return highest_bla
        
    def get_biggest_norn_recursive(self, highest_norn_p):
        highest_norn = highest_norn_p
        if self.norn > highest_norn:
            highest_norn = self.norn
        for child in self.children:
            highest_norn = child.get_biggest_norn_recursive(highest_norn) 
        return highest_norn
        
    def calc_norn(self):
        self.norn = random.randint(1, 10)
        
    def calc_norn_recursive(self):
        self.calc_norn()
        for child in self.children:
            child.calc_norn_recursive()
    
'''    
    def delete_chosen_employee(self, index_employee_p):
        for i in range(len(self.children)):
            if 
'''