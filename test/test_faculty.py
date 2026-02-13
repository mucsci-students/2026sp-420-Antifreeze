from scheduler import (
    Scheduler,
    load_config_from_file,
    FacultyConfig,
    Faculty,
    Day,
    TimeRange,
    Course,
    Preference,
    Room,
    Lab
)

import pytest
import json
from src.schedule.faculty import faculty 

config = json.loads("example.json")

class testFaculty():

    #Tests to see if the addFaculty function works
    def testAdd(self, config):
        return