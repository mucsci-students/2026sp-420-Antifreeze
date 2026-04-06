# Prompt User Input
# Prompts the user for input and raises a KeyboardInterrupt if 'r' is entered
def prompt(msg):
    val = input(msg)
    if val.lower() == "r":
        raise KeyboardInterrupt
    return val


# End Program
# Immediately exits the program
def end_prog():
    quit()
