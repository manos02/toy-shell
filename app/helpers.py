import os
import shutil

def parse(user_input):
    redirect = False
    single_opening = False
    double_opening = False
    has_content = False
    input_len = len(user_input)
    result = []
    temp = ""
    i = 0
    while i < input_len:
        if user_input[i] == "'" and not double_opening: # single quotes
            single_opening = not single_opening
            has_content = True
        elif user_input[i] == '"' and not single_opening: # double quotes
            double_opening = not double_opening
            has_content = True
        elif user_input[i] == "\\" and not single_opening: # in single quotes, it has not escaping behaviour
            next = i+1
            if next < len(user_input):
                temp += user_input[next]
                has_content = True
            i = next
        elif single_opening or double_opening:
            temp += user_input[i]
        elif user_input[i] == " ": # check for space
            if temp or has_content:
                result.append(temp)
                temp = ""
                has_content = False
        elif user_input[i] == ">":
            redirect=True
            if i and user_input[i-1] == "1":
                temp = temp[:-1] # remove the last character
                has_content = False
        else:
            temp += user_input[i]
            has_content = True
        i += 1
    if temp or has_content:
        result.append(temp)

    if redirect:
        return result[0:len(result)-1], result[-1]
    return result, None 

def is_executable(command_type, path_dirs):
    for path in path_dirs:
        if shutil.which(command_type, path=path):
            return path
    return False

def pwd():
    return os.getcwd()

def print_or_redirect(output, file):
    if not file:
        print(output.rstrip("\n"))
        return
    with open(file, "w") as f:
        f.write(output.rstrip("\n"))





    
