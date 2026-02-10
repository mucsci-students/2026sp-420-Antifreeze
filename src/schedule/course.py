from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

# TODO - create subclass details
class course():

    #TODO - initialize conflict subclass
    def __init__(self):
        return

    #TODO Implement feature
    def addCourse(self, config, scheduler, courseId: str, credits: int, room: list, lab: list, conflicts: list, faculty: list):
        return
    
    #TODO Implement feature
    def modifyCourse(self, config, scheduler, oldId: str, newId: str, credits: int, room: list,
                    lab: list, conflicts: list, faculty: list):
        return
    
    #TODO Implement feature
    def deleteCourse(self, config, scheduler, courseId: str):
        return
    