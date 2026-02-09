from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

class schedule:
    def __init__(self):
        config = ""
        configLoaded = False
        scheduler = ""
        
    #TODO - wrap schedule into callable class
    #--------------#
    #FILE MANAGEMENT
    #TODO Implement feature
    def loadFile(self, fileName):
        try:
            config = load_config_from_file(CombinedConfig, fileName)
        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
        configLoaded = True
        scheduler = Scheduler(config)


    #TODO Implement feature
    def saveFile(self):
        return

    #TODO Implement feature
    def printFile(self):
        return


    #--------------#
    #LABS
    #TODO Implement feature
    def addLab(self):
        # Manuel was here
        return

    #TODO Implement feature
    def deleteLab(self):
        return

    #TODO Implement feature
    def modifyLab(self):
        return


    #--------------#
    #ROOMS
    #TODO Implement feature
    def addRoom(self):
        return

    #TODO Implement feature
    def deleteRoom(self):
        return

    #TODO Implement feature
    def modifyRoom(self):
        return

    #--------------#
    #CONFLICT
    #TODO Implement feature
    def addConflict(self):
        return

    #TODO Implement feature
    def deleteConflict(self):
        return

    #TODO Implement feature
    def modifyConflict(self):
        return

    #--------------#
    #FACULTY
    #TODO Implement feature
    def addFaculty(self):
        return

    #TODO Implement feature
    def deleteFaculty(self):
        return

    #TODO Implement feature
    def modifyFaculty(self):
        return

    #--------------#
    #COURSE
    #TODO Implement feature
    def addCourse(self):
        return

    #TODO Implement feature
    def deleteCourse(self):
        return

    #TODO Implement feature
    def modifyCourse(self):
        return


    #--------------#
    #SCHEDULER

    #TODO Implement feature
    def runScheduler(self):
        return

    #TODO Implement feature
    def displaySchedule(self):
        return
