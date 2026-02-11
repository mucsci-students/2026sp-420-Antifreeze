from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig, CourseConfig

import conflict
import course
import faculty
import lab
import room

class schedule:
    def __init__(self):
<<<<<<< HEAD
        self.schedConflict = conflict.conflict()
        self.schedCourse = course.course()
        self.schedFaculty = faculty.faculty()
        self.schedLab = lab.lab()
        self.schedRoom = room.room()
        self.config = self.createEmptyConfig()
        self.configLoaded = False
        scheduler = Scheduler(self.config)


=======
        self.config = ""
        self.configLoaded = False
        self.scheduler = ""
        
    #TODO - wrap schedule into callable class
>>>>>>> add-delete-modify-Course
    #--------------#
    #FILE MANAGEMENT
    #TODO Implement feature
    def loadFile(self, fileName):
        try:
            self.config = load_config_from_file(CombinedConfig, fileName)
        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
<<<<<<< HEAD
        configLoaded = True
=======
        self.configLoaded = True
        self.scheduler = Scheduler(self.config)
>>>>>>> add-delete-modify-Course


    #TODO Implement feature
    def saveFile(self):
        return

    #TODO Implement feature
    def printFile(self):
        return

<<<<<<< HEAD
    #Creates an empty config file
    def createEmptyConfig():
        emptyConfig = {
            "config": {
                "rooms": [],
                "labs": [],
                "courses": [],
                "faculty": []
            },
            "time_slot_config": {
                "times": {
                    "MON": [],
                    "TUE": [],
                    "WED": [],
                    "THU": [],
                    "FRI": []
                },
                "classes": []
            },
            "limit": 100,
            "optimizer_flags": []
        }
        return emptyConfig   
        configLoaded = True
        
=======

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
    #SCHEDULER

    #TODO Implement feature
    def runScheduler(self):
        return

    #TODO Implement feature
    def displaySchedule(self):
        return
>>>>>>> add-delete-modify-Course
