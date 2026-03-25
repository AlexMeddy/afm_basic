class CDebugLog:
    debug_mode = -1
    @staticmethod     
    def print_log(msg_p, type_p):
        if type_p == CDebugLog.debug_mode:
            print(msg_p)
 