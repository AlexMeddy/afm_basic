
import time
from functools import wraps
from icecream import ic 
from termcolor import colored
from datetime import datetime
import pytz

#ic.configureOutput(includeContext=True, contextAbsPath=True)

DEBUG = True

def debug_log(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if DEBUG:
            func_start = time.time()
            ic()
            msg: str = ""
            name_attribute_value:str = ""
            self_name_tag:str = ""
            name_attribute_value_tag:str = ""
            obj_class_name_tag:str = ""

            if (len (args) > 0):
                name_attribute_value=getattr(args[0], 'name',"notfound__")
                self_name_tag = "sef.name=" if name_attribute_value!="notfound__" else ""
                name_attribute_value_tag = name_attribute_value if name_attribute_value!="notfound__" else ""
                obj_class_name_tag = {type(args[0]).__name__}

            timestamp = datetime.now(pytz.timezone("Australia/Brisbane")).strftime("%d/%m %H:%M:%S:%f")
          
            msg = f"{timestamp}:{colored('START>>', 'magenta')}({obj_class_name_tag}){self_name_tag}{colored(name_attribute_value_tag, 'blue')} {colored (function.__name__,'magenta')} ("
            
            #ic(function.__code__.co_varnames)
            #ic(args)
            #ic(function.__code__.co_varnames)
            for index, item in enumerate(args):
                if(function.__code__.co_varnames[0] == "self"):
                    if(index>0):
                        msg += f" ({colored(type(item).__qualname__, 'yellow')}){function.__code__.co_varnames[index]}={item}"
                else:
                    msg += f" ({colored(type(item).__qualname__, 'yellow')}){function.__code__.co_varnames[index]}={item}"
               
            msg+=")"
            print(msg)    
           
            #print(">>START", function.__name__,  " obj:",args[0].name, 
            #    {**dict(zip(function.__code__.co_varnames, args)), **kwargs)
        #print(function.__code__.co_varnames)
        #ic(getattr(self))


      
        result = function(*args, **kwargs)
        func_end = time.time()
        if DEBUG:
            timestamp = datetime.now(pytz.timezone("Australia/Brisbane")).strftime("%d/%m %H:%M:%S:%f")

            msg = f"{timestamp}:{colored('END>>>>', 'red')}({obj_class_name_tag}){self_name_tag}{colored(name_attribute_value_tag, 'blue')} {colored(function.__name__,'magenta')} "
            msg += f"return     ({colored(type(result).__qualname__,'yellow')}){result}        duration:{(func_end-func_start)*1000:3f}ms"
            print(msg)
        return result 
    return wrapper
 
class c2:
    nameer: str = "mee"

    @debug_log
    def first_example(self,a, b, c):
        print("bla c2") 
 
class c1:
    name: str = "mee"

    @debug_log
    def first_example(self,a, b, c):
        print("bla")
        self.w=1
        ass=1
        ab=ass
        ic(ass,ab)
        return 1  
    


@debug_log
def first_example(a, b, c):
    return 100

@debug_log
def second_example(d, e, f):
    return 200
    
"""
first_example(10, 11, 12)
first_example(c=12, a=10, b=11)
"""

if __name__ == "__main__":

    c2obj=c2()
    func_start = time.time()

    ic(c2obj.first_example(10, 11, "12"))

    c=c1()
    func_start = time.time()

    ic(c.first_example(10, 11, "12"))
    func_end = time.time()
    print(f"{func_end-func_start:0.3f}")

    func_start = time.time()

    ic(c.first_example(10, 11, "12"))
    func_end = time.time()
    print(f"{func_end-func_start:0.3f}")

    print("hi")