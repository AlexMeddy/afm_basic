import argparse
from icecream import ic

class CBus:
    def __init__(self, name_p)
        self.name = name_p
        self.x = 0
        self.y = 0
        self.h = 0
        self.w = 0
        
if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    parser = argparse.ArgumentParser(description='CMainController')
    parser.add_argument('-t','--test', help='testing', required=True)
    args = vars(parser.parse_args())
    if args['test'] == 'calc_xy':
        root = CBus("root")
        root.length = 0
        a = CBus("a")
        a.length = 1
        a.w = 50
        a.h = 50