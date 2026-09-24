import shutil
import sys
import os
import subprocess
import re

def main():
    builtin_commands = ["type", "echo", "exit", "pwd"]

    # ENVIRONMENT VARIABLES
    path_var = os.getenv('PATH')
    home_path = os.getenv('HOME')

    path_dirs = path_var.split(os.pathsep)
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo"):
            content_str = command[5:] # get everything after the "echo"
            content_str = parser(content_str) 
            print(content_str)
        elif command.startswith("type"):
            command_type = split_input_parts(command, index=1)
            if command_type in builtin_commands:
                print(f"{command_type} is a shell builtin")
            else:
                if path := is_executable(command_type, path_dirs):
                    print(f"{command_type} is {path}/{command_type}")
                else:
                    print(f"{command_type} not found")
            continue
        elif command.startswith("custom_exe"):
            command_list = split_input_parts(command)
            program_name = command_list[0]
            if is_executable(program_name, path_dirs):
                subprocess.run(command_list)
                continue
        elif command == "pwd":
            print(pwd())
        elif command.startswith("cd"):
            path = split_input_parts(command, index=1)
            if path == "~": # handle home path
                path = home_path
            else:
                path = os.path.join(pwd(), path)
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
        elif command.startswith("cat"):
            command = command[4:]
            commands = command.split("'")
            commands = [parser("'" + x + "'") for x in commands if x != ' ']
            result = subprocess.run(["cat", *commands], capture_output=True, text=True)
            print(result.stdout, end="")
        else:
            print(f"{command}: command not found")

def remove_extra(inp):
    return re.sub(' +', ' ', inp)

def parser(inp:str):
    opening = False
    res = ""
    temp = ""
    for i in range(len(inp)):
        if inp[i] != "'":
            temp += inp[i]
        else:
            if not opening:
                res += remove_extra(temp)
                temp = ""
                opening = True
            else: 
                res += temp
                temp = ""
                opening = False
    res += remove_extra(temp)
    return res

def is_executable(command_type, path_dirs):
    for path in path_dirs:
        if shutil.which(command_type, path=path):
            return path
    return False

def pwd():
    return os.getcwd()

def split_input_parts(inp:str, index=None, range=False):
    inp = inp.split()
    inp_len = len(inp)
    if index:
        if index > inp_len:
            raise IndexError(f"Index: {index} is greater than {inp_len}")
        if range:
            return inp[index:]
        else:
            return inp[index]
    return inp
if __name__ == "__main__":
    main()
