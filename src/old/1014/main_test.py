def encrypt_string(msg_p):
    enc_str_l = ""
    for c in msg_p:
        ascii_char_l = ord(c)
        print("ascii_char_l = {:d} type = {}".format(ascii_char_l, type(ascii_char_l)))
        enc_ascii_char_l = ascii_char_l +1
        print("enc_ascii_char_l = {:d} type = {}".format(enc_ascii_char_l, type(enc_ascii_char_l)))
        enc_char_l = chr(enc_ascii_char_l)
        print("enc_char_l = {} type = {}".format(enc_char_l, type(enc_char_l)))
        enc_str_l += enc_char_l
        print("enc_str_l = {} type = {}".format(enc_str_l, type(enc_str_l)))
    return enc_str_l 

def decrypt_string(msg_p):
    dec_str_l = ""
    for c in msg_p:
        enc_ascii_char_l = ord(c)
        print("enc_ascii_char_l = {:d} type = {}".format(enc_ascii_char_l, type(enc_ascii_char_l)))
        ascii_char_l = enc_ascii_char_l -1
        print("ascii_char_l = {:d} type = {}".format(ascii_char_l, type(ascii_char_l)))
        dec_char_l = chr(ascii_char_l)
        print("dec_char_l = {} type = {}".format(dec_char_l, type(dec_char_l)))
        dec_str_l += dec_char_l
        print("dec_str_l = {} type = {}".format(dec_str_l, type(dec_str_l)))
    return dec_str_l    
    
msg_input = input("please enter a msg: ")
enc_str_l = encrypt_string(msg_input)
print("final enc {}".format(enc_str_l))
un_enc_str_l = decrypt_string(enc_str_l)
        