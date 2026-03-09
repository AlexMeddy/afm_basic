class CDebugLog:
    @staticmethod
    def print_log(msg_p, type_p):
        if type_p == 0: #main
            print(msg_p)
        elif type_p == 1: #socket
            print(msg_p)