import sys
import os
import subprocess
from app.helpers import is_executable, parse, pwd

def main():
    builtin_commands = ["type", "echo", "exit", "pwd", "cd"]

    # ENVIRONMENT VARIABLES
    path_var = os.getenv('PATH')
    home_path = os.getenv('HOME')

    path_dirs = path_var.split(os.pathsep)
    while True:
        sys.stdout.write("$ ")
        line = input()
        args = parse(line)
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

if __name__ == "__main__":
    main()
