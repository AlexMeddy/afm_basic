import datetime
from CStudent import CStudent
student_test_obj = CStudent(1, "t")

class CTeacher:
    def __init__(self):
        self.student_list = []
        
    def calculate_age_of_all_students(self, cy_p):
        print("calculate_age_of_all_students: cy_p = {:d}".format(cy_p))
        total_age_l = 0
        for cn in self.student_list:    #testing and printing age of student  
            each_student_age_l = cy_p - cn.dob
            print("dob = {:d}, each_student_age_l = {:d}".format(cn.dob, each_student_age_l))
            #total_age_l = total_age_l + each_student_age_l
            total_age_l += each_student_age_l
        print("total_age_l = {:d}".format(total_age_l))
        #needs to be calculated
        return total_age_l
        
    def load(self):
        '''
        student_list_l = []
        file = open('student_list.txt', 'r')
        lines = file.readlines()
        for line in lines:
            print(line)
            dob_l = line
            self.student_list.append(CStudent(dob_l))
        for cn in self.student_list:
            print("{:d}\n".format(cn.dob))
        return self.student_list
        '''
        student_list_l = []
        file = open('student_list.txt', 'r')
        lines = file.readlines()
        #print("TESTING file = {}".format(str(file)))
        #print("TESTING lines = {}".format(str(lines)))
        for line in lines:
            print(line)
            dob_l = line
            student_list_l.append(CStudent(int(dob_l)))
        #for testing only, remove if needed -------------------------------------
        for cn in student_list_l:
            print("TESTING {:d}\n".format(cn.dob))
        return student_list_l
 
    def find_student(self, name_p):
        print("TESTING 1006 name_p = {}".format(name_p))
        print("TESTING 1008 start")
        for a in name_p:
            print(a)
        print("TESTING 1008 end")
        print("TESTING 1005 start")
        for cn in self.student_list:
            print("name = {} attendance = {:d}".format(cn.name, cn.attendance))
        print("TESTING 1005 end")        
        which_node_l = None
        for cn in self.student_list:
            if cn.name == name_p:
                print("TESTING 1007")
                which_node_l = cn
                break
        return which_node_l
        
    def calculate_attendance(self):
        self.student_list = []
        file = open('att_report.txt', 'r') 
        lines = file.readlines()           
        for line in lines:  #1
            print(line) # each line has a student name
            x = line.split(",") #returns list of sub strings
            name_l = x[0]
            attendance_number_l = x[1]
            print("TESTING 1009-----------------------name_l = {}, attendance_number_l = {:d}".format(name_l, int(attendance_number_l)))           
            which_node = self.find_student(name_l)   #2            
            print("list size = {:d}".format(len(self.student_list)))
            if which_node == None:
                CStudent_obj_l = CStudent(0, name_l)
                #self.student_list.append(CStudent(0, name_p)) #3
                self.student_list.append(CStudent_obj_l) #3
                CStudent_obj_l.attendance += int(attendance_number_l)    #4
                print("TESTING 1002 start")
                for cn in self.student_list:
                    print("name = {} attendance = {:d}".format(cn.name, cn.attendance))
                print("TESTING 1002 end")
            else:
                which_node.attendance += int(attendance_number_l)    #4.2
                print("TESTING 1004 start")
                for cn in self.student_list:
                    print("name = {} attendance = {:d}".format(cn.name, cn.attendance))
                print("TESTING 1004 end")
        print("TESTING 1001 start")
        for cn in self.student_list:
            print("name = {} attendance = {:d}".format(cn.name, cn.attendance))
        print("TESTING 1001 end")
        return self.student_list
        print(which_node)
        
