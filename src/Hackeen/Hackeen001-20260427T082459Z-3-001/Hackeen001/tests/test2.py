    
def open_door():
    print("trying to open_door")
    door_open_status = None
    try:
        with open(r"C:\Users\alexf\afm_basic\src\ai\CFolder\output\2_c_to_s_msg.bin", "rb") as file:
            door_open_status = file.read()
            print("at this point door_open_status is open")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except OSError as e:
        print(f"Could not open file: {e}")
    return door_open_status
   
    
def get_into_car():
    print("get_into_car")
    
if __name__ == "__main__":
    door_lock_status = open_door()
    if door_lock_status != None:
        print("open door")
        get_into_car()
    else:
        print("cant open the door")
    