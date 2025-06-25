class CMessage:
    def __init__(self):
        self.msg = ""
    def encrypt(self):
        file = open("msg_flat_file.txt", "r")
        while True:
            sc = file.read(1) #c is single character
            print(sc)
            #print(type(c))
            #print(ord("a"))
            if not sc:   #if c == False
                break
            ord_sc_int = ord(sc) #string to int
            print(ord_sc_int)
            enc_ord_sc_int = ord_sc_int +1
            print(enc_ord_sc_int)
            enc_sc_str = chr(enc_ord_sc_int) #int to string
            print(enc_sc_str)
            self.msg += enc_sc_str
        return self.msg