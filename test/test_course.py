import sys
import os
import types
import pytest


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


scheduler_stub = types.ModuleType("scheduler")
scheduler_stub.Scheduler = object
scheduler_stub.load_config_from_file = lambda *a, **kw: None
sys.modules.setdefault("scheduler", scheduler_stub)

scheduler_config_stub = types.ModuleType("scheduler.config")
scheduler_config_stub.CombinedConfig = object
sys.modules.setdefault("scheduler.config", scheduler_config_stub)


from src.model.schedule.course import course
