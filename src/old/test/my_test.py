from pydantic import BaseModel
import argparse
import pickle
from pickle_serialize import Food
from icecream import ic
from CPerson import CPerson
import random
import pygame
pygame.init()
w_width, w_height = 800, 800
window = pygame.display.set_mode((w_width, w_height))
window.fill((255, 255, 255))
red = ( 200,  60,   60)


class User(BaseModel):
    name: str
    account_id: int


if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='my_test')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'pj_s':
        user = User(name="Alex", account_id = 12)
        print(user)
        user_json_str = user.json()
        print(user_json_str)
        f = open("json_test_file.txt", "w")
        f.write(user_json_str)
    if args['test'] == 'pj_l':
        f = open("json_test_file.txt", "r")
        json_user_obj = f.read()
        print(json_user_obj)
        user = User.parse_raw(json_user_obj)
        print(user)
    if args['test'] == 'p_s':
        f1 = Food('cheese')
        f1.protein = 9
        f1.carbs = 1
        f1.fat = 9
        f2 = Food('chicken')
        f2.protein = 8
        f2.carbs = 1
        f2.fat = 5
        f3 = Food('watermelon')
        f3.protein = 8
        f3.carbs = 1
        f3.fat = 0
        p1 = CPerson('alex')
        #p1.food_list.append(f1)
        #p1.food_list.append(f2)
        p1.food_list = [f1, f2, f3]
        ic(f1)
        with open('pickle_file.txt', 'wb') as file:
            pickle.dump(p1, file)           
        for cn in p1.food_list:
            ic(p1.name, cn.name)
    if args['test'] == 'p_l':
        with open('pickle_file.txt', 'rb') as file:
            p1 = pickle.load(file) 
        run = True
        window_width, window_height = pygame.display.get_surface().get_size()
        ic(window_width, window_height)
        v_layers = 2
        h_layers = len(p1.food_list)
        rect_height = window_height / v_layers
        rect_width = window_width / h_layers
        rect_width *= 0.3
        rect_height *= 0.3
        y = window_height / 2
        xa = window_width/2
        ya = 0
        x1 = 0
        x2 = x1 + rect_width
        x3 = x2 + rect_width
        ic(rect_width, rect_height)
        while run:        
            pygame.draw.rect(window, (0, 255, 255),(xa, ya, rect_width, rect_height), 3) 
            pygame.draw.rect(window, (0, 255, 0),(x1,y,rect_width,rect_height), 3)
            pygame.draw.rect(window, (255, 0, 0),(x2,y,rect_width,rect_height), 3)
            pygame.draw.rect(window, (0, 0, 255),(x3,y,rect_width,rect_height), 3)
            for cn in p1.food_list:
                ic(p1.name, cn.name)
            pygame.display.update()
            input("enter q to quit: ")
            run =False
        #pygame.quit()