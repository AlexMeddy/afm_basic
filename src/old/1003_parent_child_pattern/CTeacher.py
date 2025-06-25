import datetime
from CStudent import CStudent
student_test_obj = CStudent(2008)

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
 
