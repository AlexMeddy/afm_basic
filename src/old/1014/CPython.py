import datetime
import mymodule
class CPython:
    def __init__(self, name_p, age_p):
        self.name = name_p
        self.age = age_p
        self.x = 300
        
    def python_variables_and_their_datatypes(self):
        number_l = 7
        name_l = "alex"
        print(type(number_l))
        print(type(name_l))

    def numbers(self):
        int_l = 6 #int
        float_l = 4.7 #float
        complex_l = complex("3+7j") #complex
        print("int_l = {} float_l {:f} complex_l = {}".format(int_l, float_l, complex_l))

    def casting(self):
        #ints
        a = int(1)   # a will be 1
        b = int(2.8) # b will be 2
        c = int("3") # c will be 3
        #strings
        d = str("s1") # d will be 's1'
        e = str(2)    # e will be '2'
        f = str(3.0)  # f will be '3.0'
        #floats
        g = float(1)     # g will be 1.0
        h = float(2.8)   # h will be 2.8
        i = float("3")   # i will be 3.0
        j = float("4.2") # j will be 4.2

    def strings(self):
        print("hello")
        a = "hi"
        print(a)
        #quotes in quotes 
        print("my name is 'Alex'") #you can quotes inside in a string as long as they dont match the quotes that are surrounding the string.

    def booleans_and_conditions(self):
        print(10 > 9) #prints true or false
        print(10 == 9) #prints true or false
        print(10 < 9) #prints true or false
        a = 200
        b = 33
        if b > a:
          print("b is greater than a")
        else:
          print("b is not greater than a")
        x = "Hello"
        y = 15

        print(bool(x))
        print(bool(y))

    def operators(self):
        print(10 + 5)
        print(12 - 7)
        print(11 * 9)
        print(45 / 5)

    def lists_and_for_loop(self):
        list_l = []
        list_l.append("green")
        list_l.append("red")
        list_l.append("blue")
        for cn in list_l:
            print(cn)
    
    def tuples(self):
        tuple_l = tuple(("yellow", "brown", "purple")) # note the double round-brackets
        print(tuple_l)
    
    def sets(self):
        set_l = set(("abc", 34, True, 40, "male"))
        print(len(set_l))
        print(set_l)
    
    def dictionary(self):
        dictionary_l = {
          "brand": "Ford",
          "electric": False,
          "year": 2015,
          "colors": ["red", "white", "blue"]
        }
        print(dictionary_l)
        print(type(dictionary_l))
    
    def while_loops(self):
        a_l = 1
        while a_l < 6:
            print(a_l)
            a_l += 1
        else:
            print("a_l is no longer less than 6")
    
    def example_function(self):
        print("example_function: hello!")
    
    def arrays(self):
        cars = []
        cars.append("Honda")
        cars.append("Ford")
        cars.append("Dodge")
        cars.append("Volvo")
        for cn in cars:
            print(cn)
        len_l = len(cars)
        print(len_l)
    
    def iterators(self):
        str_l = "apple"
        iter_l = iter(str_l)
        for a in iter_l:
            print(a)
            
    def scope_inner_function(self):
        print(self.x)
            
    def scope_function(self):
        self.scope_inner_function()
    
    def module(self):
        mymodule.greeting("Alex")

    def date_time(self):
        x = datetime.datetime(2017, 6, 8)
        print(x)

    def exception_handling(self):
        try:
            print(x)
        except NameError:
            print("Something went wrong")
        except:
            print("Something else went wrong")
    
    def user_input(self):
        name = input("Enter name:")
        print("name is: " + name)
        
    def string_formatting(self):
        a_l = "hello"
        print("a = {}".format(a_l))
        
py_obj_l = CPython("Alex", 11)
py_obj_l.string_formatting()