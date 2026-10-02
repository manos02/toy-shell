import sys
import os
import subprocess
from app.helpers import is_executable, parse, print_or_redirect, get_working_directory

def main():
    builtin_commands = ["type", "echo", "exit", "pwd", "cd"]

    # ENVIRONMENT VARIABLES
    path_var = os.getenv('PATH')
    home_path = os.getenv('HOME')

    path_dirs = path_var.split(os.pathsep)
    while True:
        sys.stdout.write("$ ")
        line = input()
        args, file_to_write = parse(line)
        if not args:
            continue
        command = args[0]
        if command == "exit":
            break
        elif command == "echo":
            out = " ".join(args[1:])
            print_or_redirect(out, file_to_write)
        elif command == "type":
            command_type = args[1]
            if command_type in builtin_commands:
                print(f"{command_type} is a shell builtin")
            elif path := is_executable(command_type, path_dirs):
                    print(f"{command_type} is {path}/{command_type}")
            else:
                print(f"{command_type} not found")
        elif command == "pwd":
            print(get_working_directory())
        elif command == "cd":
            path = args[1] if len(args) > 1 else "~"
            if path == "~": # handle home path
                path = home_path
            else:
                path = os.path.join(get_working_directory(), path)
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
        else:
            if is_executable(command, path_dirs):
                res = subprocess.run(args, capture_output=True, text=True)
                print_or_redirect(res.stderr.rstrip("\n"))
                print_or_redirect(res.stdout.rstrip("\n"), file_to_write)
            else:
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()
