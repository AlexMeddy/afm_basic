import sys
sys.path.append("..\\Controller")
from Controller import CMainController

class CMainView:
    def main_loop(self):
        while 1:
            print("add a child = 1")
            event_input = int(input())
            if event_input == 1:
                print("bla")
            
if __name__ == "__main__":      
    view_obj = CMainView()
    view_obj.main_loop()