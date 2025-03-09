import sys
sys.path.append("..\\lib")
from camlog import debug_log
from icecream import ic 

class person:
    pass
class CDummy: 
    #name:str = ""
    def __init__(self, name_p:str):
        self.name = name_p
    def f (self, obj_p:person, str_p:str):
        print("CDummy:f")
        ic(obj_p,str_p)
    @debug_log
    def f2 (self, obj_p:person, str_p:str):
        ic(obj_p,str_p)
@debug_log    
def foo (obj_p:person, str_p:str):
    ic(obj_p,str_p)

if __name__ == '__main__':
    a = 3
    b = 11
    c = 42
    foo(obj_p = CDummy("dummy"), str_p ="bla")
    dummy_obj = CDummy("dummy")    
    dummy_obj.f(obj_p = CDummy("dummy"), str_p ="bla")
    dummy_obj.f2(obj_p = CDummy("dummy"), str_p ="bla")