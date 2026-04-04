
from langchain.chat_models import init_chat_model
from langchain_core.tools import StructuredTool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from pydantic import BaseModel, Field

from model.AI.executor import *


# -------------------------
# GLOBAL STATE
# -------------------------

_scheduler = None
_agent = None


# -------------------------
# SCHEMAS (optional but useful)
# -------------------------

class NameSchema(BaseModel):
    name: str = Field(description="Name")

class RenameSchema(BaseModel):
    old_name: str
    new_name: str

class CourseSchema(BaseModel):
    course_id: str
    credits: int
    room: list[str]
    lab: list[str]
    conflicts: list[str]
    faculty: list[str]

class ScheduleSchema(BaseModel):
    limit: int
    optimize: bool


# -------------------------
# TOOL WRAPPERS (NO partial!)
# -------------------------

# FACULTY
def add_faculty_tool(
    name,
    maximum_credits,
    maximum_days,
    minimum_credits,
    unique_course_limit=1,
    times=None,
    course_preferences=None,
    room_preferences=None,
    lab_preferences=None,
    mandatory_days=None
):
    return add_faculty(
        _scheduler,
        name,
        maximum_credits,
        maximum_days,
        minimum_credits,
        unique_course_limit,
        times,
        course_preferences,
        room_preferences,
        lab_preferences,
        mandatory_days
    )

def modify_faculty_tool(
    old_name,
    new_name,
    maximum_credits,
    maximum_days,
    minimum_credits,
    unique_course_limit=1,
    times=None,
    course_preferences=None,
    room_preferences=None,
    lab_preferences=None,
    mandatory_days=None
):
    return modify_faculty(
        _scheduler,
        old_name,
        new_name,
        maximum_credits,
        maximum_days,
        minimum_credits,
        unique_course_limit,
        times,
        course_preferences,
        room_preferences,
        lab_preferences,
        mandatory_days
    )

def delete_faculty_tool(name):
    return delete_faculty(_scheduler, name)

def list_faculty_tool():
    return list_faculty(_scheduler)


# COURSES
def add_course_tool(course_id, credits, room, lab, conflicts, faculty):
    return add_course(_scheduler, course_id, credits, room, lab, conflicts, faculty)

def modify_course_tool(index, course_id, credits, room, lab, conflicts, faculty):
    return modify_course(_scheduler, index, course_id, credits, room, lab, conflicts, faculty)

def delete_course_tool(course_id):
    return delete_course(_scheduler, course_id)


# LABS
def add_lab_tool(name):
    return add_lab(_scheduler, name)

def modify_lab_tool(old_name, new_name):
    return modify_lab(_scheduler, old_name, new_name)

def delete_lab_tool(name):
    return delete_lab(_scheduler, name)


# ROOMS
def add_room_tool(name):
    return add_room(_scheduler, name)

def modify_room_tool(old_name, new_name):
    return modify_room(_scheduler, old_name, new_name)

def delete_room_tool(name):
    return delete_room(_scheduler, name)


# SCHEDULER
def run_scheduler_tool(limit, optimize):
    return run_scheduler(_scheduler, limit, optimize)

def get_schedule_tool(index):
    return get_schedule(_scheduler, index)


# -------------------------
# TOOL BUILDER
# -------------------------

def build_tools():
    return [
        StructuredTool.from_function(
            func=add_faculty_tool,
            name="add_faculty",
            description="Add faculty"
        ),
        StructuredTool.from_function(
            func=modify_faculty_tool,
            name="modify_faculty",
            description="Modify faculty"
        ),
        StructuredTool.from_function(
            func=delete_faculty_tool,
            name="delete_faculty",
            description="Delete faculty"
        ),
        StructuredTool.from_function(
            func=list_faculty_tool,
            name="list_faculty",
            description="List faculty"
        ),

        StructuredTool.from_function(
            func=add_course_tool,
            name="add_course",
            description="Add course"
        ),
        StructuredTool.from_function(
            func=modify_course_tool,
            name="modify_course",
            description="Modify course"
        ),
        StructuredTool.from_function(
            func=delete_course_tool,
            name="delete_course",
            description="Delete course"
        ),

        StructuredTool.from_function(
            func=add_lab_tool,
            name="add_lab",
            description="Add lab"
        ),
        StructuredTool.from_function(
            func=modify_lab_tool,
            name="modify_lab",
            description="Modify lab"
        ),
        StructuredTool.from_function(
            func=delete_lab_tool,
            name="delete_lab",
            description="Delete lab"
        ),

        StructuredTool.from_function(
            func=add_room_tool,
            name="add_room",
            description="Add room"
        ),
        StructuredTool.from_function(
            func=modify_room_tool,
            name="modify_room",
            description="Modify room"
        ),
        StructuredTool.from_function(
            func=delete_room_tool,
            name="delete_room",
            description="Delete room"
        ),

        StructuredTool.from_function(
            func=run_scheduler_tool,
            name="run_scheduler",
            description="Run scheduler"
        ),
        StructuredTool.from_function(
            func=get_schedule_tool,
            name="get_schedule",
            description="Get schedule"
        ),
    ]


# -------------------------
# AGENT FACTORY
# -------------------------

def get_agent(scheduler):
    global _agent, _scheduler

    if _agent is None:
        _scheduler = scheduler  # 🔥 inject scheduler ONCE

        model = init_chat_model("gpt-5-mini", model_provider="openai")

        tools = build_tools()

        _agent = create_agent(model=model, tools=tools)

    return _agent


# -------------------------
# ENTRY POINT
# -------------------------

def run_agent(scheduler, user_input: str):
    agent = get_agent(scheduler)

    result = agent.invoke({
        "messages": [HumanMessage(content=user_input)]
    })

    return result["messages"][-1].content