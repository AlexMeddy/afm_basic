import datetime
from CStudent import CStudent
from CTeacher import CTeacher
student_list_l = []

'''
student_list_l.append(CStudent(2007))
student_list_l.append(CStudent(1995))
student_list_l.append(CStudent(2010))

year_l = 2024
for cn in student_list:
    total_age_l = cn.calculate_age(year_l, cn.dob) #i want to calculate age of 1 student
    print("total age = {:d}".format(total_age_l))

teacher_test_obj_l = CTeacher()
student_list_l = teacher_test_obj_l.load()
teacher_test_obj_l.student_list = student_list_l
cd_l = datetime.datetime.now()
cy_l = cd_l.year
total_age_l = teacher_test_obj_l.calculate_age_of_all_students(cy_p = cy_l)
if len(teacher_test_obj_l.student_list) > 0:
    avg_age_l = total_age_l / len(teacher_test_obj_l.student_list)
    print("total age = {:d}, avg_age_l = {:f}".format(total_age_l, avg_age_l))
'''
teacher_test_obj_l = CTeacher()
#which_node_l = teacher_test_obj_l.find_student("t")
#print(which_node_l)
student_list_l = teacher_test_obj_l.calculate_attendance()
print("TESTING 1003 start")
for cn in student_list_l:
    print("name = {} attendance = {:d}".format(cn.name, cn.attendance))
print("TESTING 1003 end")