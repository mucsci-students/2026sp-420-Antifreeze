import schedule as s

def main():
    sche = s.schedule()
    sche.load("example.json")

def testAdd(sche: s.schedule):
    #should see this in the config
    sche.addFaculty("")

    #