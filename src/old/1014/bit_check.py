def three_point_one():
    input_str = input("please enter a string: ")
    for c in input_str:
        char_l = ord(c)
        char_bin_l = bin(char_l)
        print("binary code of string = {}".format(char_bin_l))
        byte_l = char_l
        print("byte = {:08b} type = {}".format(byte_l, type(byte_l)))
        binary_mask = 0b00000001
        for cn in range(0, 8):
            print("------------------start of bit loop------------------------")
            bm = 0b00000001 << cn
            print("bm = {:08b} type = {}".format(bm, type(bm)))
            print("binary mask = {:08b} type = {}".format(binary_mask, type(binary_mask)))
            if byte_l & bm == bm:
                print("bit{:d} is on".format(cn))
            else:
                print("bit{:d} is NOT on".format(cn))
            binary_mask <<= 1

            print("------------------end of bit loop------------------------")
                
                    
three_point_one()
        