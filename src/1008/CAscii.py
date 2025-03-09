def ascii():
    file = open("ascii_test.txt", "r")
    while True:
        c = file.read(1) #c is single character
        if not c:   #if c == False
            break
        #print(c, end="")
        #print(chr(hex(ord(c)-1)), end="")
        #print(chr(ord(c)+1), end="")    #ord to get ascii code of a character
        #chr to get a character of ascii code
        print(hex(ord(c)), end="")    #ord to get ascii code of a character
        
#print(chr(0x62))
ascii()