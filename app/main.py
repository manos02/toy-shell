import shutil
import sys
import os

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
            inp = command.split()
            print(" ".join(inp[1:]))
        elif command.startswith("type"):
            command_type = command.split()[1] 
            if command_type in builtin_commands:
                print(f"{command_type} is a shell builtin")
            else:
                found = False
                for dir in path_dirs:
                    if shutil.which(command_type, path=dir):
                        print(f"{command_type} is {dir}/{command_type}")
                        found = True
                        break
                if not found:
                    print(f"{command_type} not found")
        else:
            print(f"{command}: command not found")
           


if __name__ == "__main__":
    main()
