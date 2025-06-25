import argparse
from icecream import ic

class CMisc:
    deepest_level = -1
    def fibo(n_p, parent_depth_p):
        call_depth = parent_depth_p + 1 #calc_iden needs call_depth
        ic(call_depth, parent_depth_p)
        print(f'{CMisc.calc_iden(call_depth)}[start] fibo n_p={n_p}, call_depth={call_depth}')
        if CMisc.deepest_level == -1 or CMisc.deepest_level < call_depth:
            CMisc.deepest_level = call_depth
        print(f'{CMisc.calc_iden(call_depth)}[middle] deepest_level = {CMisc.deepest_level}')
        if n_p <= 0:
            res = 0
        elif n_p==1:
            res = 1        
        else:
            res = CMisc.fibo(n_p-1, call_depth) + CMisc.fibo(n_p-2, call_depth)
        print(f'{CMisc.calc_iden(call_depth)}[ end ] fibo n_p={n_p}, call_depth={call_depth}')
        return res
    
    def fibo2(n_p):
        if n_p <= 0:
            res = 0
        elif n_p==1:
            res = 1  
        else:
            res = CMisc.fibo2(n_p-1) + CMisc.fibo2(n_p-2)
        return res
    
    def calc_iden(nested_depth_p):
        return "----" * nested_depth_p
    
if __name__ == "__main__":              
    parser = argparse.ArgumentParser(description='my_test')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'fibo':
        fibo_r = CMisc.fibo(n_p = 6, parent_depth_p = -1)
        ic(fibo_r)
        ic(CMisc.deepest_level)
    if args['test'] == 'fibo2':
        fibo_r = CMisc.fibo2(n_p = 5)
        ic(fibo_r)    
