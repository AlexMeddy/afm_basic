msg_input = input("please enter a message: ")
for a in msg_input:
    print(a)
    char_p = ord(a)
    print(char_p)
    print("{0:b}".format(char_p))
