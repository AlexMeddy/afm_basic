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
Rename class Employee to CEmployee_light
Provide sample comma delimited file.
'''
import argparse
import csv
import argparse
from icecream import ic
from typing import Optional, List
from tools import build_tree_from_csv
from CEmployee_pattern import CEmployee_pattern





def main(args,root_obj_p):

    #1 print the whole tree from the top employee
    if args['method'] == 'print_recursive':
        if root_obj_p:
            root_obj_p.print_recursive()   

    #2 promote a chosen employee
    if args['method'] == 'chosen_employee.promote':
        chosen_employee_name = input ('enter chosen_employee_name:')
        chosen_employee_new_title = input ('enter chosen_employee_new_title:')
        chosen_employee = root_obj_p.find_by_name_recursive(chosen_employee_name)
        if chosen_employee != None:       
            chosen_employee.promote(chosen_employee_new_title)
        else:
            print("employee not found")
        root_obj_p.print_recursive()   
    
    #3 dismiss chosen employee
    if args['method'] == 'chosen_employee.dismiss':
        chosen_employee_name = input ('enter chosen_employee_name:')
        chosen_employee = root_obj_p.find_by_name_recursive(chosen_employee_name)
        if chosen_employee != None:  
            chosen_employee.dismiss() #mockup
        else:
            print("employee not found")
        root_obj_p.print_recursive()   

    #4 pay rise for everyone
    if args['method'] == 'chosen_employee.pay_rise_for_everyone':
        root_obj_p.pay_rise_recursive()
        root_obj_p.print_recursive()   

    #5 pay rise for subtree
    if args['method'] == 'chosen_employee.pay_rise_for_subtree':
        chosen_employee_name = input ('enter chosen_employee_name:')
        chosen_employee = root_obj_p.find_by_name_recursive(chosen_employee_name)
        root_obj_p.print_recursive()       
        if chosen_employee != None:
            chosen_employee.pay_rise_recursive()
        else:
            print("employee not found")
        root_obj_p.print_recursive()       
            
    #6 print guid of chosen employee
    if args['method'] == 'chosen_employee.print_guid_of_chosen_employee':
        chosen_employee_name = input ('enter chosen_employee_name:')
        chosen_employee = root_obj_p.find_by_name_recursive(chosen_employee_name)
        if chosen_employee != None:
            chosen_employee.print_guid() #mockup
        else:
            print("employee not found")
        root_obj_p.print_recursive() 

    #7 toggle activation state for a chosen employee
    if args['method'] == 'chosen_employee.toggle_activation_employee':
        chosen_employee_name = input ('enter chosen_employee_name:')
        chosen_employee = root_obj_p.find_by_name_recursive(chosen_employee_name)
        if chosen_employee != None:
            chosen_employee.toggle_activation_employee()
        else:
            print("employee not found")
        first_activated_employee = root_obj_p.find_first_employee_by_activation_status()
        print('first_activated_employee = ' + f'{first_activated_employee.name}')
        root_obj_p.print_recursive() 
        

    #8.1 run a chosen employee
    if args['method'] == 'chosen_employee.delete_chosen_employee':
        root_obj_p.calc_i_self_recursive(0)
        chosen_employee_name = input ('enter chosen_employee_name:')
        chosen_employee = root_obj_p.find_by_name_recursive(chosen_employee_name)
        if chosen_employee: #if employee exists
            if chosen_employee.parent == None: #if it is root
                root_obj_p = None #delete root from outside
            else:
                chosen_employee.delete(chosen_employee.i_self)
        else:
            print("employee not found")
        if root_obj_p:
            root_obj_p.print_recursive()



    #9 calculate the highest hourly rate
    if args['method'] == 'chosen_employee.calculate_highest_hourly_rate':
        #calc_highest_hourly_rate_recursive no needed because already given
        biggest_hourly_rate = root_obj_p.get_highest_hourly_rate_recursive(0) 
        print(biggest_hourly_rate)
        root_obj_p.print_recursive()   
        
    #9.1 calculate the highest annual leave balance
    if args['method'] == 'chosen_employee.calculate_highest_annual_leave':
        #calc_highest_annual_leave_recursive no needed because already given
        highest_annual_leave_p = root_obj_p.get_highest_annual_leave_recursive(0)
        print(highest_annual_leave_p)
        root_obj_p.print_recursive() 
        
    #9.2 calculate the highest bla
    if args['method'] == 'chosen_employee.calculate_highest_bla':
        #get_highest_bla_recursive no needed because already given
        highest_bla = root_obj_p.get_highest_bla_recursive(0)
        print(highest_bla)
        root_obj_p.print_recursive()
        
    #9.3 calculate the highest number of repeated titles #original  "calculate the title that repeats the most"
    if args['method'] == 'chosen_employee.calculate_biggest_norn2':
        root_obj_p.print_recursive()
        root_obj_p.calc_nort_recursive(root_obj_p)
        highest_nort = root_obj_p.get_biggest_nort_recursive(0)
        print(highest_nort)
        
        root_obj_p.print_recursive()
        
    #9.4 calculate the max number of employees working at same time
    if args['method'] == 'chosen_employee.calc_noewast_recursive':
        root_obj_p.calc_noewast_recursive(root_obj_p)
        max_noewast = root_obj_p.find_max_noewast_recursive(0)
        print(max_noewast)
        root_obj_p.print_recursive()
        
    #10 display in the  pygame top right corner the number of active employees
    if args['method'] == 'chosen_employee.count_noae_recursive':  
        chosen_employee_name = input ('enter chosen_employee_name:')
        chosen_employee = root_obj_p.find_by_name_recursive(chosen_employee_name)
        if chosen_employee != None:
            chosen_employee.toggle_activation()
        else:
            print("employee not found")    
        noae = root_obj_p.count_noae_recursive(0)
        print(noae)
        root_obj_p.print_recursive()
if __name__ == "__main__":
    
    root_obj = build_tree_from_csv("employees.csv")
    parser = argparse.ArgumentParser(description="Console App with Employee Tree")
    parser.add_argument('-m','--method', help='testing', required=True)
    args = vars(parser.parse_args())
    
    main(args,root_obj)
    
    

 
            