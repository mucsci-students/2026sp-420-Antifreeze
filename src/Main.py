#Program Entry File
#Initializes the scheduling system and starts the CLI

from controller import cli
from model.schedule import schedule as sch



#Main Entry Point
#Initializes the scheduler and launches the command-line interface
#Example usage: main()
def main():
    sched = sch.Schedule()
    cli.cli(sched)

main()