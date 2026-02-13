import cli
from schedule import schedule as sch



#TODO
def main():
    sched = sch.schedule()
    cli.cli(sched)

main()