def prompt(msg):
    val = input(msg)
    if val.lower() == "r":
        raise KeyboardInterrupt
    return val

def endProg():
    quit()