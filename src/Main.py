import cli
from schedule import schedule



#TODO
def main():
    sched= schedule.schedule()
    cli.cli(sched)

main()