import os

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

def get_faculty_details_tool(name):
    return get_faculty_details(_scheduler, name)


# COURSES
def get_course_details_tool(course_id):
    return get_course_details(_scheduler, course_id)

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
            description=(
                "Add a faculty member. "
                "mandatory_days, times, course_preferences, room_preferences, and lab_preferences are all optional. "
                "Always pass mandatory_days as a plain list of day strings, e.g. ['MON', 'TUE']. Never ask the user for a format — just use a list."
            )
        ),
        StructuredTool.from_function(
            func=modify_faculty_tool,
            name="modify_faculty",
            description=(
                "Modify an existing faculty member. "
                "ALWAYS call get_faculty_details first to retrieve current values, then apply only the user's requested changes and preserve all other fields exactly. "
                "Never ask the user to re-supply fields that weren't changed. "
                "Always pass mandatory_days as a plain list of day strings, e.g. ['MON', 'TUE']. Never ask the user for a format — just use a list."
            )
        ),
        StructuredTool.from_function(
            func=delete_faculty_tool,
            name="delete_faculty",
            description="Delete faculty"
        ),
        StructuredTool.from_function(
            func=list_faculty_tool,
            name="list_faculty",
            description="List all faculty names"
        ),
        StructuredTool.from_function(
            func=get_faculty_details_tool,
            name="get_faculty_details",
            description="Get full details for a single faculty member by name. Always call this before modifying a faculty member so you have all current field values."
        ),

        StructuredTool.from_function(
            func=get_course_details_tool,
            name="get_course_details",
            description="Get full details for a single course by course_id, including its index. Always call this before modifying a course so you have all current field values and the required index."
        ),
        StructuredTool.from_function(
            func=add_course_tool,
            name="add_course",
            description=(
                "Add a course. "
                "room, lab, conflicts, and faculty are all list fields — always pass them as plain lists of strings, "
                "e.g. ['Roddy 136', 'Roddy 150']. If the user provides a single value, still wrap it in a list. "
                "Never ask the user for a specific format — just use a list."
            )
        ),
        StructuredTool.from_function(
            func=modify_course_tool,
            name="modify_course",
            description=(
                "Modify an existing course by index. "
                "ALWAYS call get_course_details first to retrieve the current values and index, then apply only the user's requested changes and preserve all other fields exactly. "
                "Never ask the user to re-supply fields that weren't changed. "
                "room, lab, conflicts, and faculty are all list fields — always pass them as plain lists of strings, e.g. ['Roddy 136', 'Roddy 150']. "
                "Never ask the user for a specific format — just use a list."
            )
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

        system_prompt = (
            "You are a scheduling assistant. Be concise. "
            "When you run the scheduler or generate schedules, do NOT list the schedule contents in your reply. "
            "Simply confirm how many schedules were generated (e.g. '1 schedule generated. You can now view it in the GUI.'). "
            "The user can view schedules directly in the application. "
            "For all other actions (add, modify, delete), give a brief one-sentence confirmation."
        )

        _agent = create_agent(model=model, tools=tools, system_prompt=system_prompt)

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