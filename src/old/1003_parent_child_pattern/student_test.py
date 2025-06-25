import datetime
from CStudent import CStudent
student_test_obj = CStudent()

'''
dob_l = 2008
year_l = 2024
age_l = student_test_obj.calculate_age(year_p = year_l, dob_p = dob_l)
print("age = {:d}".format(age_l))
'''
def main_bubble():
    while 1:
        #input DOB and name
        dob_l = input("please enter a date of birth: ")
        #cy_l gets current year
        cd_l = datetime.datetime.now()
        cy_l = cd_l.year
        print(cy_l)
        age_l = student_test_obj.calculate_age(year_p = cy_l, dob_p = int(dob_l))
        #print age
        print("age = {:d}".format(age_l))
        
main_bubble()