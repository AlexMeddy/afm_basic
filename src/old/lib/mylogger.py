#C:\Users\medeirog\AppData\Local\Programs\Python\Python313\python.exe tree.py
import json
import pickle
from functools import wraps
indent_mult = 5
indent = -1
pad = '  '
import inspect
import re
import random

from jsondiff import diff
ansi_escape_colors = {
    4: "\033[44m",  # Blue_BG
    9: "\033[45m",  # Magenta_BG   
    10: "\033[42m",  # Green_BG
    8: "\033[43m",  # Yellow_BG
    12: "\033[41m",  # Red_BG

    6: "\033[37m",  # White
    #2: "\033[35m",  # Magenta
    
    7: "\033[33m",  # Yellow
    0: "\033[34m",  # Blue
    5: "\033[35m",  # Magenta
    1: "\033[36m",  # Cyan
    11: "\033[31m",  # Red
    2: "\033[32m",  # Green  
    
    14: "\033[47m",  # White_BG
    15: "\033[0m" ,   # Reset
    16: "\033[4m" ,#bold italic
    17: "\033[38;2;255;165;0m",  # orange
    18: "\033[1m", #bold
    19: "\033[46m",  # Cyan_BG
    20: "\033[30m\033[47m", #black letter white BG
    24: "\033[31m\033[47m", #black letter white BG
   
    21: "\033[30m\033[43m", #black letter yellow BG
    22: "\033[1m\033[3m\033[4m" ,#bold italic
    23: "\033[47m" ,#gray_BG
    30: "\033[30m\033[47m", #black letter white BG

    
}
ID_COLOR        =30
METHOD_COLOR    =20

#python code to list the type and values of the arguments using decorator
import inspect

def list_args_types_and_values_decorator(func):
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        bound_args = signature.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        for name, value in bound_args.arguments.items():
            arg_type = type(value)
            print(f"Argument: {name}, Type: {arg_type}, Value: {value}")
        
        return func(*args, **kwargs)
    
    return wrapper




def find_substring_indexes(T, S):
    indexes = []
    start = 0
    while start < len(T):
        pos = T.find(S, start)
        if pos == -1:
            break
        indexes.append(pos)
        start = pos + 1
    return indexes

# Example usage

DISPLAY_SELF        = 0b10000000
DISPLAY_PARAM       = 0b01000000
DISPLAY_STATE       = 0b00100000
DISPLAY_STD         = 0b01111111
DISPLAY_FULL        = 0b11111111
DISPLAY_COLORS      = 1

def mylogger(log_level_p=DISPLAY_STD,display_colors_p=1):


    def decorator(func):

        #@wraps(func)
        def wrapper(*args, **kwargs):
            global indent
            global indent_mult
            global pad 
            global DISPLAY_COLORS
      
            if (not display_colors_p or not DISPLAY_COLORS):
                DISPLAY_COLORS   = 0
                for i in range (50):
                    ansi_escape_colors[i] =  "\033[0m"
            ansi_escape_colors[21] = "\033[30m\033[43m"
            ansi_escape_colors[ID_COLOR] = "\033[30m\033[47m"
            ansi_escape_colors[METHOD_COLOR] = "\033[30m\033[47m"
            
                

            indent+=1
  

            msg = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{'-'*80}{ansi_escape_colors[15]}' 
            msg=add_tree_ident(msg)
            print(msg)  

            
            signature = inspect.signature(func)
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            self_str = ''
            args_desc = '{'
            i=0
            for name, value in bound_args.arguments.items():
                arg_type = str(type(value)).replace('<class \'','').replace('\'>','').replace('__main__.','')
                if ('self' in name and (log_level_p & DISPLAY_SELF)):
                    args_desc+=f'{',' if i else ''}\'{name}({arg_type})\':\'{value}({arg_type})\''
                    i+=1
                elif 'self' not in name:    
                    args_desc+=f'{',' if i else ''}\'{name}({arg_type})\':\'{value}\''
                    i+=1                 
                if ('self' in name):
                    self_str = f'{value}'    
                    
            args_desc += '}'
            self_str = truncate_memory_address(self_str)

     
            args_desc=truncate_memory_address(args_desc)
            args_desc=args_desc.replace(' ','')
            args_desc=args_desc.replace('{}','')
            if (not log_level_p & DISPLAY_PARAM):
                args_desc = ''
   
            
            #python code to display the object name that that invokes a method using  a decorator

            object_name='?'
            frame = inspect.currentframe().f_back
            local_vars = frame.f_locals
            for var_name, var_value in local_vars.items():
                if var_value is args[0]:
                    object_name = f'{var_name}'
                    break
         
            
            
            
            
            #std_header = calc_log_header(args[0],' ')

            args0_fixed = str(args[0].__dict__).replace('\'','\"').replace('None','\"None\"')
            args0_fixed = truncate_memory_address(args0_fixed)
       
            #print(args0_fixed)
            dictionary_previous = json.loads(args0_fixed)
            name_tmp = f'{ansi_escape_colors[ID_COLOR]}\'{dictionary_previous['name']}\'{ansi_escape_colors[15]}'
            object_name = f'{ansi_escape_colors[20]}{object_name}{ansi_escape_colors[15]}'
            
            msg2 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[indent]}{object_name}\
{ansi_escape_colors[indent]}({name_tmp}\
{ansi_escape_colors[indent]}).\
{ansi_escape_colors[20]}[{self_str}]\
{ansi_escape_colors[15]}{ansi_escape_colors[indent]}.\
{ansi_escape_colors[20]}{args[0].__class__.__name__}\
{ansi_escape_colors[15]}:\
{ansi_escape_colors[20]}\
{ansi_escape_colors[METHOD_COLOR]}{func.__name__}\
{ansi_escape_colors[15]}({args_desc})\
        line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[15]}'      
            #msg += f'line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[15]}'

            
            msg2=add_tree_ident(msg2)
            print(msg2)     
            
            
            if (log_level_p & DISPLAY_STATE):
                msg1 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[20]}{'State'}\
{ansi_escape_colors[15]}{ansi_escape_colors[15]}:{dictionary_previous}\
{ansi_escape_colors[15]}'   
         
                msg1=add_tree_ident(msg1)
                
                msg1=replace_and_modify_substring(msg1, '\'name\': ', ',',ansi_escape_colors[20],ansi_escape_colors[15])

                print(msg1) 



            
            

            
        
            #print(f'Running {func.__name__} with args: {args}, kwargs: {kwargs}\n')

      
            result = func(*args, **kwargs)
       
            args0_fixed = str(args[0].__dict__).replace('\'','\"').replace('None','\"None\"')
            args0_fixed = truncate_memory_address(args0_fixed)
       
            #print(args0_fixed)
            dictionary_post = json.loads(args0_fixed)   

            escape_color = ansi_escape_colors[15]
         
            differences = ':'+str(diff(dictionary_previous,dictionary_post))
         
            if (dictionary_post != dictionary_previous):
                escape_color += ansi_escape_colors[21]
                msg3 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[20]}{'State Change'}\
{escape_color}{differences}{ansi_escape_colors[15]}'
                msg3 = msg3.replace('\t','')
                msg3=add_tree_ident(msg3)
                print(msg3)
 

                msg1 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[20]}{'State'}\
{ansi_escape_colors[15]}{ansi_escape_colors[15]}:{dictionary_post}\
{ansi_escape_colors[15]}'   
                msg1=add_tree_ident(msg1)
                msg1=replace_and_modify_substring(msg1, '\'name\': ', ',',ansi_escape_colors[20],ansi_escape_colors[15])

                print(msg1) 
                
            msg4 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|\
{'-'*80}\
{ansi_escape_colors[15]}' 
            msg4=add_tree_ident(msg4)
            print(msg4)      
            
            
            tmp = ansi_escape_colors[indent]
            ansi_escape_colors[indent] = ansi_escape_colors[5]
            ansi_escape_colors[5] = tmp

            indent-=1


            return result

        return wrapper
    return decorator
        
    
def mylog_section(msg_p): 
 
    msg2 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent if indent > -1 else 15]}{'|' if indent > -1 else ''}{ansi_escape_colors[15]}'
 
    
 
    #msg = pad*indent*indent_mult+ansi_escape_colors[indent if indent > -1 else 15]+('|' if indent > -1 else '') +ansi_escape_colors[15]

 
    #msg+=msg_p
    msg_p=msg_p.upper()
    #msg2+=f'{ansi_escape_colors[indent if indent > -1 else 15]}{msg_p:#^80}'
    msg2+=f'{ansi_escape_colors[indent if indent > -1 else 15]}{'-   '*10}{msg_p}{'   -'*10}'
 
    
    msg2+=f' line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[15]}'

    #print ('msg2'+msg2)
    #print ('msg'+msg)
  
    
    msg = add_tree_ident(msg2) 

    print(msg)
       
 
def mylog_sectionv2(msg_p):  
    #https://www.geeksforgeeks.org/python/print-colors-python-terminal/
    pad_l = f'{pad*indent*indent_mult}\033[1m\033[3m{'':-^80}\033[0m'
    
    
    pad_l = add_tree_ident(pad_l) 

    
    print(pad_l)   
    msg_l = f'{pad*indent*indent_mult}\033[1m\033[3m|{msg_p.upper():^78}|\033[0m'
    msg_l = add_tree_ident(msg_l) 
   
    
    print(msg_l) 
    print(pad_l)   

 

def truncate_memory_address(text):
    def replacer(match):
        substring = match.group(0)[1:-1]
        
        integer_value = int(f'{substring[-3:]}', 16)
        
        integer_value = f'\"x{substring[-3:]}\"'

        #print (integer_value)
        #return f'{substring[-3:]}'
        return f'{integer_value}'
       
        
    return re.sub(r'<[^>]*>', replacer, text)

def replace_first_substring(text):
    # Use regular expression to find the first substring between ':' and ','
    match = re.search(r':(.*?),', text)
    
    if match:
        substring = match.group(1)  # Extract the substring without ':' and ','
        new_substring = f"\033[34m{substring}\033[0m"
        text = text.replace(f":{substring},", f":{new_substring},", 1)
    
    return text
#write a python code to replace the first substring S between start_s and end_s and prefix S with PRF and sufix S with POF
def replace_and_modify_substring(text, start_s, end_s, PRF, POF):
    start_index = text.find(start_s)
    if start_index == -1:
        return text  # Return the original text if start_s is not found
    
    start_index += len(start_s)
    end_index = text.find(end_s, start_index)
    if end_index == -1:
        return text  # Return the original text if end_s is not found
    
    substring = text[start_index:end_index]
    modified_substring = PRF + substring + POF
    
    # Replace the original substring with the modified substring
    new_text = text[:start_index] + modified_substring + text[end_index:]
    
    return new_text


#   
def add_tree_ident(msg_p):
    msg_l = '' 
    for i in reversed(range(0, indent)):
        idx = len(pad)*i*indent_mult
        pipe_l = ansi_escape_colors[i] + '|'+ansi_escape_colors[15]
        msg_p = msg_p[:idx]+ pipe_l  + msg_p[idx+2:]  
        #msg_l = msg_p[:idx]+ansi_escape_colors[i] + '|' +ansi_escape_colors[15]  + msg_p[idx+1:]  

    return msg_p
    
def myic(*args):
    param_text = inspect.stack()
    param_text = (find_first_substring(str(param_text), 'myic(',')'))
    param_text = param_text.split(',')
 
    #print(find_first_substring(str(text), 'a',')'))


    sig = inspect.signature(myic)
 
    msg = f'{pad*indent*indent_mult}\
{ansi_escape_colors[indent if indent > -1 else 15]}\
{'|' if indent > -1 else ''}\
myic:{ansi_escape_colors[15]}'
    #print (msg)

 
    params = list(sig.parameters.keys())
    for i, arg in enumerate(args):
        if i>0:
            msg += ','      
        param_text[i] = param_text[i].replace('\'','')   
        msg += f'{param_text[i]}'
        if arg != param_text[i]:
            msg += f'={arg}'

          
            
    msg = truncate_memory_address(msg)
       
    msg += f'      line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[15]}'
    
    msg = add_tree_ident(msg) 

    print(msg)
       
def mylog(msg_p,line_p=1):   
    global indent
    global indent_mult
    global pad 

    msg = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}{'|'}{ansi_escape_colors[15]}{msg_p.replace('\t', '').replace(' ', '')} '
    if (line_p):
        msg+=f'{ansi_escape_colors[15]} line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_back.f_lineno}{ansi_escape_colors[15]}'
    #    msg = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|START:{func.__name__}(){ansi_escape_colors[15]} line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[15]}'


    msg = add_tree_ident(msg)
    print(msg) 

def mylog_header(object_p, parameter_list_p,line_p=1):

    """
    std_header     = f'{object_p.__dict__}' 
    std_header =  truncate_memory_address(std_header)
    parameter_list_l = parameter_list_p.split(',')
    for p in parameter_list_l:      
        std_header =  replace_first_substringv2(std_header,f'{p}\':',',')
    #std_header =  replace_first_substringv2(std_header,'ps\':',',')
    """
    if (line_p):
        std_header = 'mylog_header:'  
    std_header += calc_log_header(object_p, parameter_list_p)

    mylog(std_header,line_p)    
    #print(self.__dict__)  



def calc_log_header(object_p, parameter_list_p):
    """
    std_header     = f'name=\033[34m {self.name} \033[0m, \
                            ps={self.ps.name if self.ps else 'none'},\
                             width={self.width} ,\
                            \033[33m resized_width={self.resized_width} \033[0m ' 
    """
    std_header     = f'{object_p.__dict__}' 
    

    #print (std_header)
  
    
    std_header =  truncate_memory_address(std_header)
    """
    parameter_list_l = parameter_list_p.split('|')
    for p in parameter_list_l:      
        std_header =  replace_first_substringv2(std_header,f'{p}\':',',')
    """
    return (std_header)    


def print_argument_names(**kwargs):
    for name,value in kwargs.items():
        print(f'Argument name: {name}, Argument value: {value}')

# Example usage
def example_function(**kwargs):
    print_argument_names(**kwargs)

# Call the example function with named arguments

def find_first_substring(text, start_s, end_s):
    # Use regular expression to find the first substring between start_s and end_s
    pattern = re.escape(start_s) + r'(.*?)' + re.escape(end_s)
    match = re.search(pattern, text)
    
    if match:
        substring = match.group(1)  # Extract the substring without start_s and end_s
        text = substring
    
    return text
    

            
if __name__ == "__main__":
    mylog_section ('mylog')
