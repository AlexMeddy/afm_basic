import pickle

class Food():
    def __init__(self, name_p):
        self.name = name_p
        self.protein = 0
        self.carbs = 0
        self.fat = 0
    
    def calc_calories(self):
        calories = self.protein*4 + self.carbs*4 + self.fat*9
        return calories

