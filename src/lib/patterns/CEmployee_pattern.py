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
        self.nort = 0 
        self.noewast = 0 
 


    def add_child(self, child):
        self.children.append(child)

    def calc_i_self(self, i_self_p):
        self.i_self = i_self_p

    def calc_i_self_recursive(self, i_self_p):
        self.calc_i_self(i_self_p)
        for i_child in range(len(self.children)):
            self.children[i_child].calc_i_self_recursive(i_child)

    def find_by_name_recursive(self, name):
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_by_name_recursive(name)
            if found:
                return found
        return None

    def print_recursive(self, level=0):
        print("    " * level + f"{self.name} ({self.title})  (${self.hourly_rate}) ({self.nort}) ({self.bla}))")
        for child in self.children:
            child.print_recursive(level + 1)

    def promote(self, new_title):
        self.title = new_title
    
    def dismiss(self):
        print(f'{self.name} dismissed') #mockup non recursive
        
    def pay_rise(self):
        self.hourly_rate *= 5
        print(f'{self.name} pay raised') #mockup recursive

    def pay_rise_recursive(self):
        self.pay_rise()
        for child in self.children:
            child.pay_rise_recursive()
            
    def print_guid(self):
        print(f'{self.name} guid tbd') #mockup

    def toggle_activation(self):
        if self.activation_status == 1:
            self.activation_status = 0
        else:
            self.activation_status = 1
        print(self.activation_status)
        
        
        
    def delete(self, index_employee_p):
        if self.i_self == index_employee_p:
            if self.parent:
                self.parent.children.pop(index_employee_p)
     
    
    def get_highest_hourly_rate_recursive(self, highest_hourly_rate_p):
        highest_hourly_rate = highest_hourly_rate_p
        if self.hourly_rate > highest_hourly_rate:
            highest_hourly_rate = self.hourly_rate
        for child in self.children:
            highest_hourly_rate = child.get_highest_hourly_rate_recursive(highest_hourly_rate) 
        return highest_hourly_rate
    
    def get_highest_annual_leave_recursive(self, highest_annual_leave_p):
        highest_annual_leave = highest_annual_leave_p
        if self.annual_leave > highest_annual_leave:
            highest_annual_leave = self.annual_leave
        for child in self.children:
            highest_annual_leave = child.get_highest_annual_leave_recursive(highest_annual_leave) 
        return highest_annual_leave
        
    def get_highest_bla_recursive(self, highest_bla_p):
        highest_bla = highest_bla_p
        if self.bla > highest_bla:
            highest_bla = self.bla
        for child in self.children:
            highest_bla = child.get_highest_bla_recursive(highest_bla) 
        return highest_bla
     
    def calc_bla(self):
        self.bla +=1
     
    def calc_bla_recursive(self):
        self.calc_bla()
        for child in self.children:
            child.calc_bla_recursive()
     
    
    
        
    #not needed, just for learning, get pattern
    def get_all_the_names_concatenated(self, all_the_names_concatenated_so_far_p):
        all_the_names_concatenated = all_the_names_concatenated_so_far_p
        all_the_names_concatenated = self.name + ', ' + all_the_names_concatenated
        for child in self.c_l:
            all_the_names_concatenated = child.get_all_the_names_concatenated(all_the_names_concatenated)         
        return all_the_names_concatenated
        
    def count_noae_recursive(self, noae_so_far_p):
        noae_so_far = noae_so_far_p
        if self.activation_status == 1: #matching
            noae_so_far +=1
        for child in self.children:
            noae_so_far = child.count_noae_recursive(noae_so_far)
        return noae_so_far
        
    #count pattern-------------------------------
    def count_nort_recursive(self, employee_title_p, nort_so_far_p):
        #nort_so_far = 0
        nort_so_far = nort_so_far_p        
        if self.title == employee_title_p:
            nort_so_far +=1
        for child in self.children:
            nort_so_far = child.count_nort_recursive(employee_title_p=employee_title_p, nort_so_far_p = nort_so_far)                         
        return nort_so_far
    
    def calc_nort(self, root_p):
        self.nort = root_p.count_nort_recursive(employee_title_p=self.title, nort_so_far_p=0)       
        
    def calc_nort_recursive(self, root_p):            
        self.calc_nort(root_p)
        for child in self.children:
            child.calc_nort_recursive(root_p=root_p)
            
    def find_biggest_nort_recursive(self, highest_norn_p):
        highest_norn = highest_norn_p
        if self.nort > highest_norn:
            highest_norn = self.nort
        for child in self.children:
            highest_norn = child.find_biggest_nort_recursive(highest_norn) 
        return highest_norn
    #count pattern-----------------------------   
    def count_noewast_recursive(self,noewast_so_far_p):
        noewast_so_far = noewast_so_far_p
        if self.noewast == 0: #matching to follow
            noewast_so_far +=1
        for child in self.children:
            noewast_so_far = child.count_noewast_recursive(noewast_so_far_p=noewast_so_far)
        return noewast_so_far
        
    def calc_noewast(self, root_p):
        self.noewast = root_p.count_noewast_recursive(0) #matching
    
    def calc_noewast_recursive(self, root_p):
        self.calc_noewast(root_p)
        for child in self.children:
            child.calc_noewast_recursive(root_p=root_p)
        
    def find_max_noewast_recursive(self, max_noewast_p):
        max_noewast = max_noewast_p
        if self.noewast > max_noewast:
            max_noewast = self.noewast
        for child in self.children:
            max_noewast = child.find_max_noewast_recursive(max_noewast) 
        return max_noewast
        
    def find_by_name(self, employee_name_p):
        found_employee = None
        if self.name == employee_name_p:
            found_employee = self
        return found_employee
        
    def find_by_activation_status(self):
        found_employee = None
        if self.activation_status == 1:
            found_employee = self
        return found_employee
        
    def find_by_name_recursive(self, employee_name_p):
        found_employee = None
        found_employee = self.find_by_name(employee_name_p)
        if found_employee == None: #not found
            for child in self.children:
                found_employee = child.find_by_name_recursive(employee_name_p)
                if found_employee != None: #if found
                    break
        return found_employee
        
    def find_by_activation_status_recursive(self):
        found_employee = None
        found_employee = self.find_by_activation_status()
        if found_employee == None: #not found
            for child in self.children:
                found_employee = child.find_by_activation_status_recursive()
                if found_employee != None: #found
                    break
        return found_employee
        