import shutil
import sys
import os
import subprocess
import re

def main():
    builtin_commands = ["type", "echo", "exit", "pwd", "cd"]

    # ENVIRONMENT VARIABLES
    path_var = os.getenv('PATH')
    home_path = os.getenv('HOME')

    path_dirs = path_var.split(os.pathsep)
    while True:
        sys.stdout.write("$ ")
        line = input()
        args = parser(line)
        if not args:
            continue
        command = args[0]
        if command == "exit":
            break
        elif command == "echo":
            print(" ".join(args[1:]))
        elif command == "type":
            command_type = args[1]
            if command_type in builtin_commands:
                print(f"{command_type} is a shell builtin")
            elif path := is_executable(command_type, path_dirs):
                    print(f"{command_type} is {path}/{command_type}")
            else:
                print(f"{command_type} not found")
        elif command == "pwd":
            print(pwd())
        elif command == "cd":
            path = args[1] if len(args) > 1 else "~"
            if path == "~": # handle home path
                path = home_path
            else:
                path = os.path.join(pwd(), path)
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
        else:
            if is_executable(command, path_dirs):
                subprocess.run(args)
            else:
                print(f"{command}: command not found")
def parser(inp):
    single_opening = False
    double_opening = False
    has_content = False
    # if the previous character was a backlash so we treat the next one as literal character
    backlash_before = False 
    result = []
    temp = ""
    for c in inp:
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


if __name__ == "__main__":
    main()
