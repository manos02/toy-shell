import os
import shutil

def parse(user_input):
    single_opening = False
    double_opening = False
    has_content = False
    # if the previous character was a backlash so we treat the next one as literal character
    backlash_before = False 
    result = []
    temp = ""
    for c in user_input:
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
        elif single_opening or double_opening:
            temp += c
        elif c == "\\" and not single_opening: # in single quotes, it has not escaping behaviour
            backlash_before = True
        elif c == " ": # check for space
            if temp or has_content:
                result.append(temp)
                temp = ""
                has_content = False
        else:
            temp += c
            has_content = True
    if temp or has_content:
        result.append(temp)
    return result

def is_executable(command_type, path_dirs):
    for path in path_dirs:
        if shutil.which(command_type, path=path):
            return path
    return False

def pwd():
    return os.getcwd()