import shutil
import sys
import os
import subprocess

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
            content = split_input_parts(command, take_from=1) # get everything after the "echo"
            print(" ".join(content))
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
            if path := is_executable(program_name, path_dirs):
                out = subprocess.call(command_list)
                if out != 0: # success return code, do not output
                    print(out)
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
        else:
            print(f"{command}: command not found")

def is_executable(command_type, path_dirs):
    for path in path_dirs:
        if shutil.which(command_type, path=path):
            return path
    return False

def pwd():
    return os.getcwd()

def split_input_parts(inp:str, index=None, take_from=None):
    inp = inp.split()
    if index:
        return inp[index]
    if take_from:
        return inp[take_from:]
    return inp
if __name__ == "__main__":
    main()
