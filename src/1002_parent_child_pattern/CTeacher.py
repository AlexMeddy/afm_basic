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
        

 
