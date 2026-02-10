from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

# TODO - create subclass details
class conflict():

    #TODO - initialize conflict subclass
    def __init__(self):
        return

    #TODO Implement feature
    def addConflict(self, config, scheduler, courseId: str, conflictId: str):
        return
    
    #TODO Implement feature
    def modifyConflict(self, config, scheduler, courseId: str, oldConflictId: str, newConflictId: str):
        return
    
    #TODO Implement feature
    def deleteConflict(self, config, scheduler, courseId: str, conflictId: str):
        return
    