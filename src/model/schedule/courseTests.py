import schedule as s

def main():
    sche = s.schedule()

    sche.loadFile('ex.json')
    sche.returnConfig()
    sche.addCourse("DhruvyNimic",4,["Roddy 136"],[],[],[])
    sche.addCourse("DhruvyNimic",4,[],[],[],[])
    sche.returnConfig()
    sche.modifyCourse("DhruvyNimic",2,["Roddy 136"],[],[],[])
    sche.returnConfig()
    #sche.deleteCourse("DhruvyNimic")
    #sche.deleteCourse("DhruvyNimic")
    #sche.returnConfig()

main()