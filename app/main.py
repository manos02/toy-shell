import shutil
import sys
import os
import subprocess

def main():
    builtin_commands = ["type", "echo", "exit"]
    path_var = os.getenv('PATH') # get the PATH env variable

    path_dirs = path_var.split(os.pathsep)
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo"):
            content = command.split()[1:] # get everything after the "echo"
            print(" ".join(content))
        elif command.startswith("type"):
            command_type = command.split()[1] 
            if command_type in builtin_commands:
                print(f"{command_type} is a shell builtin")
            else:
                if dir := is_executable(command_type, path_dirs):
                    print(f"{command_type} is {dir}/{command_type}")
                else:
                    print(f"{command_type} not found")
            continue
        elif command.startswith("custom_exe"):
            command_list = command.split()
            program_name = command_list[0]
            if dir := is_executable(program_name, path_dirs):
                out = subprocess.call(command_list)
                if out != 0: # return code
                    print(out)
                continue
        else:
            print(f"{command}: command not found")

def is_executable(command_type, path_dirs):
    for dir in path_dirs:
        if shutil.which(command_type, path=dir):
            return dir
    return False

if __name__ == "__main__":
    main()
