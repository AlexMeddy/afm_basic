def encrypt():
    enc_input_file = open("input_encrypt.txt", "r")
    enc_output_file = open("output_encrypt.txt", "a")
    while True:
        sc = enc_input_file.read(1) #c is single character
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
        enc_output_file.write(enc_sc_str)

def decrypt():
    enc_input_file = open("output_encrypt.txt", "r")
    enc_output_file = open("output_decrypt.txt", "a")
    while True:
        sc = enc_input_file.read(1) #c is single character
        print(sc)
        #print(type(c))
        #print(ord("a"))
        if not sc:   #if c == False
            break
        ord_sc_int = ord(sc) #string to int
        print(ord_sc_int)
        enc_ord_sc_int = ord_sc_int -1
        print(enc_ord_sc_int)
        enc_sc_str = chr(enc_ord_sc_int) #int to string
        print(enc_sc_str)
        enc_output_file.write(enc_sc_str)

encrypt()
decrypt()