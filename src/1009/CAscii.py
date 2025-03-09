def ascii():
    file = open("ascii_test.txt", "r")
    while True:
        c = file.read(1) #c is single character
        #print(type(c))
        #print(ord("a"))
        if not c:   #if c == False
            break
        #print(c, end="")
        #print(chr(hex(ord(c)-1)), end="") encryption
        
        #print(chr(ord(c)+1), end="")    #ord to get ascii code of a string       encryption 
        
        #ord_c = ord(c)
       # print(type(ord_c))
        #chr to get a character of ascii code
        print(ord(c), end="")    #ord to get ascii code of a string 
        #msg = "a"
        #msg += "b"
        #print(msg)
#print(chr(0x62))
ascii()