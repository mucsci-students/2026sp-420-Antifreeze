
def printModCourseMenu():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Add Course")
    print("2: Modify Course")
    print("3: Remove Course")
    print("r: return to main\n==> ",end="")

def ModCourseMenuMain(sched):
    while(True):
        printModCourseMenu()
        userCommand = input()
        if(userCommand == "1"):
            addCourse(sched)
        elif(userCommand == "2"):
            modCourse(sched)
        elif(userCommand == "3"):
            delCourse(sched)
        elif(userCommand.lower() == "r"):
            return

def delCourse(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter Course name to delete\n==> ",end="")
        name = input()
        
        if (name.lower() == "r"):
            return
        sched.Course.deleteCourse(sched.config, name)


def addCourse(sched):
    while(True):
        print("press r and page through prompts to return to main")
        print("Enter Course ID to add\n==> ",end="")
        name = input()
        
        print("Enter credits\n==> ",end="")        
        credits = input()

        print("Enter rooms\n==> ",end="")        
        rooms = input()

        print("Enter labs\n==> ",end="")
        labs = input()

        print("Enter conflicts\n==> ",end="")        
        conflicts = input()

        print("Enter faculty\n==> ",end="")        
        faculty = input()
        
        fields = [
            name, credits, rooms, labs,
            conflicts, faculty
        ]

        if any(str(x).lower() == "r" for x in fields):
            return
        sched.Course.addCourse(name, credits, rooms, labs, conflicts, faculty)


def modCourse(sched):
     while(True):
        print("press r and page through prompts to return to main")
        print("Enter Course ID to modify\n==> ",end="")
        name = input()
        
        print("Enter new credits\n==> ",end="")        
        credits = input()

        print("Enter new rooms\n==> ",end="")        
        rooms = input()

        print("Enter new labs\n==> ",end="")
        labs = input()

        print("Enter new conflicts\n==> ",end="")        
        conflicts = input()

        print("Enter new faculty\n==> ",end="")        
        faculty = input()
        
        fields = [
            name, credits, rooms, labs,
            conflicts, faculty
        ]

        if any(str(x).lower() == "r" for x in fields):
            return
        sched.Course.modifyCourse(name, credits, rooms, labs, conflicts, faculty)
