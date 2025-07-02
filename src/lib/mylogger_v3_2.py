#C:\Users\medeirog\AppData\Local\Programs\Python\Python313\python.exe tree.py
import json
import pickle
import copy

from functools import wraps
indent_mult = 5
indent = -1
pad = '  '
last_msg = ''


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
    24: "\033[31m\033[47m", #black letter white BG
   
    22: "\033[1m\033[3m\033[4m" ,#bold italic
    23: "\033[47m" ,#gray_BG
    
    
    30: "\033[5m\033[37m", #flashing
    #31: "\033[5m\033[43m", #black letter yellow BG
    31: "\033[5;37;43m",
    32: "\033[30m\033[47m", #black letter white BG
    33: "\033[34m\033[47m", #black letter white BG

    
    40: "\033[30m\033[47m", #black letter white BG

    
}
COLOR_RESET     =15

ID_COLOR        =40
METHOD_COLOR    =32
CHANGE_COLOR    =31
RETURN_COLOR    =33


#python code to list the type and values of the arguments using decorator
import inspect

def list_args_types_and_values_decorator(func):
    def wrapper(self,*args, **kwargs):
        signature = inspect.signature(func)
        bound_args = signature.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        for name, value in bound_args.arguments.items():
            arg_type = type(value)
            myprint(f"Argument: {name}, Type: {arg_type}, Value: {value}")
        
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

DISPLAY_SELF        = 0b00000000
DISPLAY_SELF        = 0b00000000
DISPLAY_PARAM       = 0b01000000
DISPLAY_STATE       = 0b00100000
DISPLAY_STD         = 0b01111111
DISPLAY_FULL        = 0b11111111
DISPLAY_COLORS      = 0




def truncate_substring(text, S, E, n=16):
    # Regular expression to find the n-character long substring starting with S and ending with E
    pattern = re.escape(S) + r'(.{' + str(n - len(S) - len(E)) + '})' + re.escape(E)
    
    # Function to replace the found substring with a 3-character long substring
    def replace_match(match):
        return match.group(0)[:len(S)] + match.group(0)[len(S):len(S)+1] + E

    # Replace the matched substring in the text
    result = re.sub(pattern, replace_match, text)
    return result







def mylogger(log_level_p=DISPLAY_STD,display_colors_p=1):


    def decorator(func):

        #@wraps(func)
        def wrapper(*args, **kwargs):
            global indent
            global indent_mult
            global pad 
            global DISPLAY_COLORS
            global last_operation
            global indent_previous  
      
            if (not display_colors_p or not DISPLAY_COLORS):
                DISPLAY_COLORS   = 0
                for i in range (25):
                    ansi_escape_colors[i] =  "\033[0m"
            #ansi_escape_colors[CHANGE_COLOR] = "\033[30m\033[43m"
            #ansi_escape_colors[ID_COLOR] = "\033[30m\033[47m"
            #ansi_escape_colors[METHOD_COLOR] = "\033[30m\033[47m"
            
                

            indent+=1
  

            msg = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{'-'*80}{ansi_escape_colors[COLOR_RESET]}' 
            msg=add_tree_ident(msg)
            myprint(msg)  

            
            signature = inspect.signature(func)
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            self_str = ''
            args_desc = '{'
            i=0
            for name, value in bound_args.arguments.items():
                arg_type = str(type(value)).replace('<class \'','').replace('\'>','').replace('__main__.','')                       
                if ('self' in name and (log_level_p & DISPLAY_SELF)):
                    args_desc+=f'{',' if i else ''}\'{name}({arg_type})\':{value}({arg_type})'
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
            copied_dict = args[0].__dict__# copy.deepcopy(args[0].__dict__)

            args0_fixed = str(copied_dict).replace('\'','\"').replace('None','\"None\"')
            args0_fixed = truncate_memory_address(args0_fixed)
       
            #myprint(args0_fixed)
            dictionary_previous = json.loads(args0_fixed)
            
            
            
            """
            myprint('args[0].__class__:-----------'+str(args[0].__class__))
            class_members = inspect.getmembers(args[0].__class__)
            myprint(f"Members of {str(args[0].__class__)}:")
            """
            """
            for name, value in class_members:
                if not inspect.ismethod(name) or 1:          
                    if not name.startswith('_'):
                        myprint(f" ---- {name}: {value}")
            """
            for i in inspect.getmembers(args[0]):
                if not i[0].startswith('_'):
                    if not inspect.ismethod(i[1]): 
                        #myprint('---------------',i[0],i[1])
            
                        dictionary_previous[str(i[0])] = str(i[1]) if str(i[0]) not in dictionary_previous else dictionary_previous[str(i[0])]

            """
            frame = inspect.currentframe().f_back

            for i in frame.getmembers(args0_fixed):
                if not i[0].startswith('_'):
                    if not frame.ismethod(i[1]): 
                        dictionary_previous[str(i[0])] = str(i[1]) if str(i[0]) not in dictionary_previous else dictionary_previous[str(i[0])]
            """

            
            name_tmp = f'{ansi_escape_colors[ID_COLOR]}\'{dictionary_previous['guid']}\'{ansi_escape_colors[COLOR_RESET]}'
            object_name = f'{ansi_escape_colors[20]}{object_name}{ansi_escape_colors[COLOR_RESET]}'
            
            msg2 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[indent]}{object_name}\
{ansi_escape_colors[indent]}({name_tmp}\
{ansi_escape_colors[indent]}).\
[{self_str}]\
{ansi_escape_colors[COLOR_RESET]}{ansi_escape_colors[indent]}.\
{ansi_escape_colors[20]}{args[0].__class__.__name__}\
{ansi_escape_colors[COLOR_RESET]}:\
{ansi_escape_colors[20]}\
{ansi_escape_colors[METHOD_COLOR]}{func.__name__}\
{ansi_escape_colors[COLOR_RESET]}({args_desc})\
        line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[COLOR_RESET]}'      
            #msg += f'line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[COLOR_RESET]}'

            
            msg2=add_tree_ident(msg2)
            msg2=msg2.replace('\'\"','\'').replace('\"\'','\'').replace('[\"','[\'').replace('\"]','\']')     
            START = "\'x"
            END = "\'"
            PREF = ansi_escape_colors[ID_COLOR]
            POSF = ansi_escape_colors[15]
            msg2=modified_string = add_prefix_postfix(msg2, START, END,PREF, POSF)   
            
            msg2=truncate_substring(msg2,'.',',',n=18)
            msg2=truncate_substring(msg2,'.','}',n=18)
            msg2=truncate_substring(msg2,'.','\'',n=18)            
            
            myprint(msg2)     
            
            
            if (log_level_p & DISPLAY_STATE):
                msg1 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[20]}{'State   '}\
{ansi_escape_colors[COLOR_RESET]}{ansi_escape_colors[COLOR_RESET]}:{dictionary_previous}\
{ansi_escape_colors[COLOR_RESET]}'   
         
                msg1=add_tree_ident(msg1)
                
                #msg1=replace_and_modify_substring(msg1, '\'guid\': ', ',',ansi_escape_colors[20],ansi_escape_colors[COLOR_RESET])
                #msg1=replace_and_modify_substring(msg1, '[\'x', '\"]','x'+ansi_escape_colors[ID_COLOR],ansi_escape_colors[COLOR_RESET])
               
                START = "\'x"
                END = "\'"
                PREF = ansi_escape_colors[ID_COLOR]
                POSF = ansi_escape_colors[15]
                msg1= add_prefix_postfix(msg1, START, END,PREF, POSF)          

                START = "guid\': '"
                END = "\',"
                PREF = ansi_escape_colors[ID_COLOR]
                POSF = ansi_escape_colors[15]
                msg1= replace_and_modify_substring(msg1, START, END,PREF, POSF)

                msg1=truncate_substring(msg1,'.',',')
                msg1=truncate_substring(msg1,'.','}')
                msg1=truncate_substring(msg1,'.','\'')
       
                
                myprint(msg1) 



            
            

            
        
            #myprint(f'Running {func.__name__} with args: {args}, kwargs: {kwargs}\n')

      
            result = func(*args, **kwargs)
       
            args0_fixed = str(args[0].__dict__).replace('\'','\"').replace('None','\"None\"')
            args0_fixed = truncate_memory_address(args0_fixed)
       
            #myprint(args0_fixed)
            dictionary_post = json.loads(args0_fixed)   

            for i in inspect.getmembers(args[0]):
                if not i[0].startswith('_'):
                    if not inspect.ismethod(i[1]): 
                        #myprint('---------------',i[0],i[1])
            
                        dictionary_post[str(i[0])] = str(i[1]) if str(i[0]) not in dictionary_post else dictionary_post[str(i[0])]

            escape_color = ansi_escape_colors[COLOR_RESET]
         
            differences = ''+str(diff(dictionary_previous,dictionary_post))
         
            if (dictionary_post != dictionary_previous):
                escape_color += ansi_escape_colors[CHANGE_COLOR]
                msg3 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[20]}{'State Change:'}\
{escape_color}{differences}{ansi_escape_colors[COLOR_RESET]}'
                msg3 = msg3.replace('\t','')
                msg3=add_tree_ident(msg3)
                msg3=truncate_substring(msg3,'.',',')
                msg3=truncate_substring(msg3,'.','}')      

                
                myprint(msg3)
 

                msg1 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[20]}{'NewState'}\
{ansi_escape_colors[COLOR_RESET]}{ansi_escape_colors[COLOR_RESET]}:{dictionary_post}\
{ansi_escape_colors[COLOR_RESET]}'   
                msg1=add_tree_ident(msg1)
                #msg1=replace_and_modify_substring(msg1, '\'guid\': ', ',',ansi_escape_colors[20],ansi_escape_colors[COLOR_RESET])
                #msg1=replace_and_modify_substring(msg1, '\'x', ',',ansi_escape_colors[ID_COLOR]+'x',ansi_escape_colors[COLOR_RESET])
               
                START = "\'x"
                END = "\'"
                PREF = ansi_escape_colors[ID_COLOR]
                POSF = ansi_escape_colors[15]
                msg1=modified_string = add_prefix_postfix(msg1, START, END,PREF, POSF)


                
                START = "guid\': '"
                END = "\',"
                PREF = ansi_escape_colors[ID_COLOR]
                POSF = ansi_escape_colors[15]
                msg1= replace_and_modify_substring(msg1, START, END,PREF, POSF)
               
                msg1=truncate_substring(msg1,'.',',')
                msg1=truncate_substring(msg1,'.','}')

                myprint(msg1) 
             

            if result != None or 1:
                result_type_str=''
                result_type_str_temp=f'{type(result)}'.split('.')
                #print('result_type_str_temp '+str(result_type_str_temp)) 

                if (len (result_type_str_temp) >1):
                    result_type_str_temp = result_type_str_temp[1]
                    #print('result_type_str_temp 325 '+str(result_type_str_temp)) 
                    result_type_str_temp=f'{result_type_str_temp}'.split('\'')
                    if (len (result_type_str_temp) >1):
                        result_type_str_temp=result_type_str_temp[0]
                        result_type_str=':'+str(result_type_str_temp)
                        #print('result_type_str '+str(result_type_str)) 
                else:
                    result_type_str=f'{type(result)}'.replace('class ','').replace('<\'',':').replace('\'>','')
                #print (type(result))
                result_str = f'{(truncate_memory_address(str(result)).replace('\"','\''))}'
              
                msg_return = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{ansi_escape_colors[20]}{'Return'}\
{ansi_escape_colors[COLOR_RESET]}:{ansi_escape_colors[RETURN_COLOR] if 'None' not in result_str else ansi_escape_colors[20]  }{result_str}\
{ansi_escape_colors[COLOR_RESET]}{result_type_str}'   
                msg_return=add_tree_ident(msg_return)  
                #msg_return = truncate_memory_address(msg_return).replace('\"','\'')
                
                
                START = "\'x"
                END = "\'"
                PREF = ansi_escape_colors[ID_COLOR]
                POSF = ansi_escape_colors[15]
                #msg_return= add_prefix_postfix(msg_return, START, END,PREF, POSF)         
                myprint(msg_return)
                
    


  
            
            msg = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|{'-'*80}{ansi_escape_colors[COLOR_RESET]}' 
            msg=add_tree_ident(msg)
            myprint(msg)          

            
            tmp = ansi_escape_colors[indent]
            ansi_escape_colors[indent] = ansi_escape_colors[5]
            ansi_escape_colors[5] = tmp

            indent-=1

      

            return result

        return wrapper
    return decorator
        
    
def mylog_section(msg_p): 
    global indent
    global indent_mult
    global pad 
    global DISPLAY_COLORS

    
    msg2 = f'{pad*indent*indent_mult}{ansi_escape_colors[indent if indent > -1 else 15]}{'|' if indent > -1 else ''}{ansi_escape_colors[COLOR_RESET]}'
 
    
 
    #msg = pad*indent*indent_mult+ansi_escape_colors[indent if indent > -1 else 15]+('|' if indent > -1 else '') +ansi_escape_colors[COLOR_RESET]

 
    #msg+=msg_p
    msg_p=msg_p.upper()
    #msg2+=f'{ansi_escape_colors[indent if indent > -1 else 15]}{msg_p:#^80}'
    msg2+=f'{ansi_escape_colors[indent if indent > -1 else 15]}{'-   '*10}{msg_p}{'   -'*10}'
 
    
    msg2+=f' line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[COLOR_RESET]}'

    #myprint ('msg2'+msg2)
    #myprint ('msg'+msg)
  
    
    msg = add_tree_ident(msg2) 
    msg2 = '-'*len(msg)
    #myprint(msg2)
    
            
    print(msg)
    
    
    
       
def myprint(msg_p):
    global last_msg
    
    if (last_msg != msg_p):
        print (msg_p)

    last_msg = msg_p

def truncate_memory_address(text):
    def replacer(match):
        substring = match.group(0)[1:-1]
        
        integer_value = int(f'{substring[-3:]}', 16)
        
        integer_value = f'\"x{substring[-3:]}\"'

        #myprint (integer_value)
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
        pipe_l = ansi_escape_colors[i] + '|'+ansi_escape_colors[COLOR_RESET]
        msg_p = msg_p[:idx]+ pipe_l  + msg_p[idx+2:]  
        #msg_l = msg_p[:idx]+ansi_escape_colors[i] + '|' +ansi_escape_colors[COLOR_RESET]  + msg_p[idx+1:]  

    return msg_p
    
def myic(*args):
    param_text = inspect.stack()
    param_text = (find_first_substring(str(param_text), 'myic(',')'))
    param_text = param_text.split(',')
 
    #myprint(find_first_substring(str(text), 'a',')'))


    sig = inspect.signature(myic)
 
    msg = f'{pad*indent*indent_mult}\
{ansi_escape_colors[indent if indent > -1 else 15]}\
{'|' if indent > -1 else ''}\
myic:{ansi_escape_colors[COLOR_RESET]}'
    #myprint (msg)

 
    params = list(sig.parameters.keys())
    for i, arg in enumerate(args):
        if i>0:
            msg += ','      
        param_text[i] = param_text[i].replace('\'','')   
        msg += f'{param_text[i]}'
        if arg != param_text[i]:
            msg += f'={arg}'

          
            
    msg = truncate_memory_address(msg)
       
    msg += f'      line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[COLOR_RESET]}'
    
    msg = add_tree_ident(msg) 

    myprint(msg)
       
def mylog(msg_p,line_p=1):   
    global indent
    global indent_mult
    global pad 

    msg = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}{'|'}{ansi_escape_colors[COLOR_RESET]}{msg_p.replace('\t', '').replace(' ', '')} '
    if (line_p):
        msg+=f'{ansi_escape_colors[COLOR_RESET]} line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_back.f_lineno}{ansi_escape_colors[COLOR_RESET]}'
    #    msg = f'{pad*indent*indent_mult}{ansi_escape_colors[indent]}|START:{func.__name__}(){ansi_escape_colors[COLOR_RESET]} line {ansi_escape_colors[16]}{inspect.currentframe().f_back.f_lineno}{ansi_escape_colors[COLOR_RESET]}'


    msg = add_tree_ident(msg)
    myprint(msg) 

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
    #myprint(self.__dict__)  



def calc_log_header(object_p, parameter_list_p):
    """
    std_header     = f'name=\033[34m {self.name} \033[0m, \
                            ps={self.ps.name if self.ps else 'none'},\
                             width={self.width} ,\
                            \033[33m resized_width={self.resized_width} \033[0m ' 
    """
    std_header     = f'{object_p.__dict__}' 
    

    #myprint (std_header)
  
    
    std_header =  truncate_memory_address(std_header)
    """
    parameter_list_l = parameter_list_p.split('|')
    for p in parameter_list_l:      
        std_header =  replace_first_substringv2(std_header,f'{p}\':',',')
    """
    return (std_header)    


def print_argument_names(**kwargs):
    for name,value in kwargs.items():
        myprint(f'Argument name: {name}, Argument value: {value}')

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

#python code to add a prefix PREF and a postfix POSF, to all substrings of S starting with START and finishing with END   
def add_prefix_postfix(S, START, END, PREF, POSF):
    result = ""
    i = 0
    while i < len(S):
        if S[i:i+len(START)] == START:
            start_index = i
            end_index = S.find(END, start_index + len(START))
            if end_index != -1:
                result += PREF + S[start_index:end_index+len(END)] + POSF
                i = end_index + len(END)
            else:
                result += S[i]
                i += 1
        else:
            result += S[i]
            i += 1
    return result



            
if __name__ == "__main__":
    mylog_section ('mylog')
    # Example usage
    S = "[\'x990\', \'x550\', \'x050\', \'x5A0\']"
    START = "\'x"
    END = "\'"
    PREF = ansi_escape_colors[ID_COLOR]
    POSF = ansi_escape_colors[15]

    modified_string = add_prefix_postfix(S, START, END,PREF, POSF)
    myprint(modified_string)