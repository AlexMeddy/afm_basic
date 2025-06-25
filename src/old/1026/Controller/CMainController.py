import sys
import argparse
sys.path.append("..\\Model")
sys.path.append("..\\..\\lib")
from CDescendantModel import CDescendantModel
from icecream import ic
from camlog import debug_log


class CMainController:
    
if __name__ == "__main__": 
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'print':
        ic(args['test'])
                