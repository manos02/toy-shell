import os
import shutil

def parse(user_input):
    special_characters = ["\\", '"']
    redirect = False
    single_opening = False
    double_opening = False
    has_content = False
    redirect_has_one = False
    # if the previous character was a backlash so we treat the next one as literal character
    backlash_before = False 
    result = []
    temp = ""
    for i, c in enumerate(user_input):
        if backlash_before:
            temp += c
            has_content = True
            backlash_before = False
        elif c == "'" and not double_opening: # single quotes
            single_opening = not single_opening
            has_content = True
        elif c == '"' and not single_opening: # double quotes
            double_opening = not double_opening
            has_content = True
        elif c == "\\" and not single_opening: # in single quotes, it has not escaping behaviour
            backlash_before = True
        elif single_opening or double_opening:
            temp += c
        elif c == " ": # check for space
            if temp or has_content:
                result.append(temp)
                temp = ""
                has_content = False
        elif c == "1" and not double_opening and not single_opening:
            redirect_has_one = i
            temp += c
        elif c == ">" and not double_opening and not single_opening:
            redirect=True
            if redirect_has_one == i-1:
                temp = temp[:-1]
        else:
            temp += c
            has_content = True
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





    
