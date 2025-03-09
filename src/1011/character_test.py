from CHuffman import CHuffman
from CCharacter import CCharacter
test_obj = CHuffman()
test_obj.calculate_input_string()
for cn in test_obj.char_list:
    print("ascii = {:d} frequency = {:d}, {}".format(cn.ascii_a, cn.frequency))