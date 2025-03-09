import sys
sys.path.append("View")
from CMainView import CMainView

if __name__ == "__main__":      
    view_obj = CMainView()
    view_obj.main_loop()