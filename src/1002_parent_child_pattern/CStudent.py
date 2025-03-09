
class CStudent:
    def __init__(self, dob_p):
        self.dob = dob_p
        
    def calculate_age(self, year_p, dob_p):     #1 single student
        #print("year_p = {:d} type = {}, dob_p = {:d}, type = {}".format(year_p, type(year_p) , dob_p, type(dob_p)))
        age_l = year_p - dob_p
        return age_l
