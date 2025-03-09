msg_input = input("please enter a message: ")
for mychar in msg_input:
    char_l = ord(mychar)
    print("binary = {}".format(bin(char_l)))
    mybyte_l = char_l
    if mybyte_l & 0b00000001: #if bit 0 is on
        print("character = {} bit 0 is on".format(mychar))
    else:
        print("character = {} bit 0 is NOT on".format(mychar))
    if mybyte_l & 0b00000010: #if bit 1 is on
        print("character = {} bit 1 is on".format(mychar))
    else:
        print("character = {} bit 1 is NOT on".format(mychar))
    if mybyte_l & 0b00000100: #if bit 2 is on
        print("character = {} bit 2 is on".format(mychar))
    else:
        print("character = {} bit 2 is NOT on".format(mychar))
    if mybyte_l & 0b00001000: #if bit 3 is on
        print("character = {} bit 3 is on".format(mychar))
    else:
        print("character = {} bit 3 is NOT on".format(mychar))
    if mybyte_l & 0b00010000: #if bit 4 is on
        print("character = {} bit 4 is on".format(mychar))
    else:
        print("character = {} bit 4 is NOT on".format(mychar))
    if mybyte_l & 0b00100000: #if bit 5 is on
        print("character = {} bit 5 is on".format(mychar))
    else:
        print("character = {} bit 5 is NOT on".format(mychar))
    if mybyte_l & 0b01000000: #if bit 6 is on
        print("character = {} bit 6 is on".format(mychar))
    else:
        print("character = {} bit 6 is NOT on".format(mychar))
    if mybyte_l & 0b10000000: #if bit 7 is on
        print("character = {} bit 7 is on".format(mychar))
    else:
        print("character = {} bit 7 is NOT on".format(mychar))