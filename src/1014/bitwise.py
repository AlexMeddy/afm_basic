def one_point_one():  
    number_input = int(input("please enter a number: "))
    print(bin(number_input))
    number_input = int(number_input) >> 1
    print("shifted number = {:d} binary code of shifted number = {}".format(number_input, bin(number_input)))

def one_point_two():  
    number_input = int(input("please enter a number: "))
    print(bin(number_input))
    number_input = int(number_input) << 1
    print("shifted number = {:d} binary code of shifted number = {}".format(number_input, bin(number_input)))

def two_point_one():
    number_input = int(input("please enter a number: "))
    print(bin(number_input))
    number_of_shifts_input = int(input("please enter an amount of shifts: "))
    number_input = int(number_input) << int(number_of_shifts_input)
    print("shifted number = {:d} binary code of shifted number = {}".format(number_input, bin(number_input)))

def two_point_two():
    number_input = int(input("please enter a number: "))
    print(bin(number_input))
    number_of_shifts_input = int(input("please enter an amount of shifts: "))
    number_input = int(number_input) >> int(number_of_shifts_input)
    print("shifted number = {:d} binary code of shifted number = {}".format(number_input, bin(number_input)))
    
one_point_two()