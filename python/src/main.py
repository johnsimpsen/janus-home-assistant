from src.command.commands import run_command

if __name__ == "__main__":
    while True:
        input_command = input("Prompt: ")

        if input_command.lower() == "q":
            break

        run_command(input_command)