import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo"):
            inp = command.split()
            print(" ".join(inp[1:]))
            # print("\n")
        else:
            print(f"{command}: command not found")
    


if __name__ == "__main__":
    main()
