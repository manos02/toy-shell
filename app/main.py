import sys


def main():
    commands = ["type", "echo", "exit"]
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
            if command_type in commands:
                print(f"{command_type} is a shell builtin")
            else:
                print(f"{command_type} not found")
        else:
            print(f"{command}: command not found")
           


if __name__ == "__main__":
    main()
