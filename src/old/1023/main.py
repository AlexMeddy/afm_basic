from CDescendant import CDescendant
import sys
sys.path.append("..\\lib")
from CMyDot import CMyDot
from icecream import ic
from camlog import debug_log


def output_print_tree_breadth(descendant_obj_p, plot_obj_p):
    print("output_print_tree_breadth:")
    for cn_descendant in descendant_obj_p.descendant_list:
        plot_obj_p.plot_edge(descendant_obj_p.name, cn_descendant.name)
        print("parent name: {} descendant name: {} ".format(descendant_obj_p.name, cn_descendant.name))
    for cn_descendant in descendant_obj_p.descendant_list:
        output_print_tree_breadth(cn_descendant, plot_obj_p)
     
def populate_tree_recursive(descendant_name_parent_p, root_p):
    while 1:
        descendant_name_child = input("for parent: {} enter the name of the new child: ".format(descendant_name_parent_p.name))
        if descendant_name_child == "end":
            for cn_child in descendant_name_parent_p.descendant_list:
                print("parent name: {} child name: {} ".format(descendant_name_parent_p.name, cn_child.name))
                populate_tree_recursive(cn_child, root_p)
            break
        else:
            descendant_name_parent_p.descendant_list.append(CDescendant(descendant_name_child)) 
            plot_obj_l = CMyDot("root")
            output_print_tree_breadth(root_p, plot_obj_l)

def add_child(root_obj_ptr_p):
    parent_obj = None
    input_parent_name = input("enter the name of the parent of the child: ")
    input_child_name = input("for parent: {} enter the name of the new child: ".format(input_parent_name))
    if input_parent_name != root_obj_ptr_p.name:
        parent_obj = root_obj_ptr_p.find_descendant_by_namev2(input_parent_name)
    else:
        parent_obj = root_obj_ptr_p
    parent_obj.descendant_list.append(CDescendant(input_child_name)) 
    plot_obj_l = CMyDot("root")
    output_print_tree_breadth(root_obj_ptr_p, plot_obj_l)
            
    
def run_loop_view():
    root_obj = CDescendant("root")
    while 1:
        print("---------------select 1 option----------------")
        print("build tree = 1")
        print("clean tree = 2")
        print("delete child = 3")
        print("delete mypopchild = 4")
        print("add a child = 5")
        print("exit = 9")
        event_input = int(input())
        print("-------------------------------")
        if event_input == 1:
            print("----------------populate_tree_recursive------------")
            populate_tree_recursive(root_obj, root_obj)
            print("---------------------------------------------------")
        elif event_input == 2:
            print("----------------clean tree------------")
            root_obj.descendant_list = []
            plot_obj_l = CMyDot("root")
            output_print_tree_breadth(root_obj, plot_obj_l)
            print("---------------------------------------------------")
        elif event_input == 3:
            print("----------------delete child------------")
            flag_child_found = -1
            descendant_parent_name = input("enter parent name: ")
            descendant_child_name = input("enter child name: ")
            descendant_parent = root_obj.find_descendant_by_namev2(descendant_parent_name)
            print("before loop")
            for i in range(len(descendant_parent.descendant_list)):
                print("after loop")
                print("before check")
                if descendant_parent.descendant_list[i].name == descendant_child_name:
                    print("after check")
                    flag_child_found = 1
                    break
            if flag_child_found == 1: #or i < len(descendant_parent.descendant_list)
                descendant_parent.descendant_list.pop(i)
                output_print_tree_breadth(root_obj, plot_obj_l)
            print("----------------------------------------")
        elif event_input == 4:
            print("----------------delete mypopchild------------")
            descendant_list2 = []
            descendant_parent_name = input("enter parent name: ")
            descendant_name = input("enter descendant name you want to delete: ")
            descendant_parent = root_obj.find_descendant_by_namev2(descendant_parent_name)
            for cn in descendant_parent.descendant_list:
                if cn.name != descendant_name:
                    descendant_list2.append(cn)
            descendant_parent.descendant_list = descendant_list2
            output_print_tree_breadth(root_obj, plot_obj_l)
            print("---------------------------------------------------")  
        elif event_input == 5:
            add_child(root_obj)
        elif event_input == 9:
            break

def delete_many_children(root_obj_p, child_name_input_p):
    descendant_list2 = []
    for cn_descendant in root_obj_p.descendant_list:
        print("cn_descendant.name = {}".format(cn_descendant.name))
        if cn_descendant.name != child_name_input_p:
            descendant_list2.append(cn_descendant)
    root_obj_p.descendant_list = descendant_list2
    for cn_descendant in root_obj_p.descendant_list:
        delete_many_children(cn_descendant, child_name_input_p)
    for cn in root_obj_p.descendant_list:
        print("cn.name = {}".format(cn.name))
    
#output_print_tree_breadth(root_obj, dot_obj)

def output_print_tree_depth(parent_obj_p):
    print("parent name: {} ".format(parent_obj_p.name))
    for cn_descendant in parent_obj_p.descendant_list:
        dot_obj.plot_edge(parent_obj_p.name, cn_descendant.name)
        output_print_tree_depth(cn_descendant, plot_obj_p)




root_obj = CDescendant("root")
root_obj2 = CDescendant("root")

root_obj.descendant_list.append(CDescendant("vo neiva"))
root_obj.descendant_list.append(CDescendant("bla"))
root_obj.descendant_list.append(CDescendant("bla"))
root_obj.descendant_list[0].descendant_list.append(CDescendant("gildo"))
root_obj.descendant_list[0].descendant_list.append(CDescendant("anna"))

root_obj.descendant_list[0].descendant_list[0].descendant_list.append(CDescendant("alex"))
root_obj.descendant_list[0].descendant_list[0].descendant_list.append(CDescendant("julio"))

root_obj.descendant_list[0].descendant_list[0].descendant_list[0].descendant_list.append(CDescendant("pablo"))
root_obj.descendant_list[0].descendant_list[0].descendant_list[0].descendant_list[0].descendant_list.append(CDescendant("garfield"))

'''
number_of_descendants = root_obj.descendant_list[0].descendant_list[0].descendant_list[0].descendant_list[0].calculate_number_of_descendants()
print("descendant name = {} number_of_descendants = {:d}".
format(root_obj.descendant_list[0].descendant_list[0].descendant_list[0].descendant_list[0].name, number_of_descendants))

number_of_descendants = root_obj.descendant_list[0].descendant_list[0].descendant_list[0].calculate_number_of_descendants()
print("descendant name = {} number_of_descendants = {:d}".
format(root_obj.descendant_list[0].descendant_list[0].descendant_list[0].name, number_of_descendants))

number_of_descendants = root_obj.descendant_list[0].descendant_list[0].descendant_list[1].calculate_number_of_descendants()
print("descendant name = {} number_of_descendants = {:d}".
format(root_obj.descendant_list[0].descendant_list[0].descendant_list[1].name, number_of_descendants))

number_of_descendants = root_obj.descendant_list[0].descendant_list[0].calculate_number_of_descendants()
print("descendant name = {} number_of_descendants = {:d}".
format(root_obj.descendant_list[0].descendant_list[0].name, number_of_descendants))

number_of_descendants = root_obj.descendant_list[0].descendant_list[1].calculate_number_of_descendants()
print("descendant name = {} number_of_descendants = {:d}".
format(root_obj.descendant_list[0].descendant_list[1].name, number_of_descendants))

number_of_descendants = root_obj.calculate_number_of_descendants()
print("descendant name = {} number_of_descendants = {:d}".
format(root_obj.name, number_of_descendants))

###############################################################
print("----------------start of find testing here------------")
input_name = "bla"
rc = root_obj.find_descendant_by_name(input_name)
if rc == 1:
    print("calling: {} found: {}".format(root_obj.name, input_name))
else:
    print("calling: {} not found: {}".format(root_obj.name, input_name))

print("----------------start of find testing here------------")
input_name = "vo neiva"
rc = root_obj.find_descendant_by_name(input_name)
if rc == 1:
    print("calling: {} found: {}".format(root_obj.name, input_name))
else:
    print("calling: {} not found: {}".format(root_obj.name, input_name))

print("----------------start of find testing here------------")
input_name = "pablo"
rc = root_obj.find_descendant_by_name(input_name)
if rc == 1:
    print("calling: {} found: {}".format(root_obj.name, input_name))
else:
    print("calling: {} not found: {}".format(root_obj.name, input_name))
    
print("----------------start of find testing here------------")
input_name = "anna"
descendant_ptr_l = root_obj.find_descendant_by_namev2(input_name)
if descendant_ptr_l != None:
    descendant_ptr_l.age = 10
    print("calling: {} found: {}".format(root_obj.name, input_name))
    print("descendant: {} before age change: {}".format(root_obj.name, descendant_ptr_l.age))
    descendant_ptr_l.age = 49
    print("descendant: {} after age change: {}".format(root_obj.name, descendant_ptr_l.age))
else:
    print("calling: {} not found: {}".format(root_obj.name, input_name))

print("----------------start of find testing here------------")
input_name = "gildo"
descendant_ptr_l = root_obj.find_descendant_by_namev2(input_name)
if descendant_ptr_l != None:
    descendant_ptr_l.age = 35
    print("calling: {} found: {}".format(root_obj.name, input_name))
    print("descendant: {} before age change: {}".format(root_obj.name, descendant_ptr_l.age))
    descendant_ptr_l.age = 52
    print("descendant: {} after age change: {}".format(root_obj.name, descendant_ptr_l.age))
else:
    print("calling: {} not found: {}".format(root_obj.name, input_name))

input_name = "pablo"
print("----------------start of findv2 testing here------------")
descendant_ptr_l = root_obj.find_descendant_by_namev2(input_name)
if descendant_ptr_l != None:
    descendant_ptr_l.age = 1
    print("calling: {} found: {}".format(root_obj.name, input_name))
    print("descendant: {} before age change: {}".format(root_obj.name, descendant_ptr_l.age))
    descendant_ptr_l.age = 3
    print("descendant: {} after age change: {}".format(root_obj.name, descendant_ptr_l.age))
else:
    print("calling: {} not found: {}".format(root_obj.name, input_name))

input_name = "julio"
print("----------------start of findv2 testing here------------")
descendant_ptr_l = root_obj.find_descendant_by_namev2(input_name)
if descendant_ptr_l != None:
    descendant_ptr_l.descendant_list.append(CDescendant("ty"))
else:
    print("calling: {} not found: {}".format(root_obj.name, input_name))

while 1:
    dot_obj = CMyDot("root")
    output_print_tree_depth(root_obj, dot_obj)
    input_name = input("enter parent name: ")
    input_child_name = input("enter child name: ")
    print("----------------start of findv2 testing here------------")
    descendant_ptr_l = root_obj.find_descendant_by_namev2(input_name)
    if descendant_ptr_l != None:
        descendant_ptr_l.descendant_list.append(CDescendant(input_child_name))
    else:
        print("calling: {} not found: {}".format(root_obj.name, input_name))
'''
run_loop_view()
#child_name_input = input("enter child name: ")
#delete_many_children(root_obj, child_name_input)
#output_print_tree_breadth(root_obj, dot_obj)