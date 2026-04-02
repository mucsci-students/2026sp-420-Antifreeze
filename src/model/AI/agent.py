# AI agent module for the scheduling assistant.
# Builds LangChain StructuredTools that wrap all scheduler operations,
# constructs a stateful agent with a system prompt, and exposes run_agent()
# as the single entry point for the chat route.
#
# Global state: _scheduler and _agent are initialised once on the first
# call to get_agent() and reused for the lifetime of the process.

import json
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


# -------------------------
# TIME SLOT CONFIG
# -------------------------

def get_time_slot_config_tool():
    return get_time_slot_config(_scheduler)

def add_time_range_tool(day, start, spacing, end):
    return add_time_range(_scheduler, day, start, spacing, end)

def modify_time_range_tool(day, index, start, spacing, end):
    return modify_time_range(_scheduler, day, index, start, spacing, end)

def delete_time_range_tool(day, index):
    return delete_time_range(_scheduler, day, index)

def add_class_pattern_tool(credits, meetings, start_time=None, disabled=False):
    return add_class_pattern(_scheduler, credits, meetings, start_time, disabled)

def modify_class_pattern_tool(index, credits, meetings, start_time=None, disabled=False):
    return modify_class_pattern(_scheduler, index, credits, meetings, start_time, disabled)

def delete_class_pattern_tool(index):
    return delete_class_pattern(_scheduler, index)


# SCHEDULER
def run_scheduler_tool(limit, optimize):
    return run_scheduler(_scheduler, limit, optimize)

def get_schedule_tool(index):
    return get_schedule(_scheduler, index)


# -------------------------
# TOOL BUILDER
# -------------------------

# Constructs the full list of StructuredTools for the agent.
# Each tool wraps a module-level function that delegates to the shared
# _scheduler instance. Descriptions guide the agent on argument format
# and when to call each tool.
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
            func=open_schedule_tool,
            name="open_schedule",
            description="Open the schedule tab",
            return_direct=True 
        )
        StructuredTool.from_function(
            func=get_time_slot_config_tool,
            name="get_time_slot_config",
            description=(
                "Get the full time slot configuration, including all per-day time ranges "
                "(times grid) and all class meeting patterns. Call this before modifying "
                "any time slot entry to find the correct index."
            )
        ),
        StructuredTool.from_function(
            func=add_time_range_tool,
            name="add_time_range",
            description=(
                "Add a time range to a day's availability grid. "
                "day must be MON, TUE, WED, THU, or FRI. "
                "start and end must be HH:MM strings (e.g. '08:00'). "
                "spacing is the slot interval in minutes (e.g. 30)."
            )
        ),
        StructuredTool.from_function(
            func=modify_time_range_tool,
            name="modify_time_range",
            description=(
                "Modify an existing time range by day and 0-based index. "
                "Call get_time_slot_config first to find the correct index."
            )
        ),
        StructuredTool.from_function(
            func=delete_time_range_tool,
            name="delete_time_range",
            description=(
                "Delete a time range by day and 0-based index. "
                "Call get_time_slot_config first to find the correct index."
            )
        ),
        StructuredTool.from_function(
            func=add_class_pattern_tool,
            name="add_class_pattern",
            description=(
                "Add a class meeting pattern. "
                "credits is a positive integer. "
                "meetings is a list of dicts with keys: day (MON/TUE/etc.), duration (minutes), lab (bool, optional). "
                "start_time is optional (HH:MM string). disabled is optional bool."
            )
        ),
        StructuredTool.from_function(
            func=modify_class_pattern_tool,
            name="modify_class_pattern",
            description=(
                "Modify an existing class pattern by 0-based index. "
                "Call get_time_slot_config first to find the correct index."
            )
        ),
        StructuredTool.from_function(
            func=delete_class_pattern_tool,
            name="delete_class_pattern",
            description=(
                "Delete a class meeting pattern by 0-based index. "
                "Call get_time_slot_config first to find the correct index."
            )
        ),
    ]


# -------------------------
# AGENT FACTORY
# -------------------------

# Returns the singleton agent, creating it on first call.
# Injects the scheduler into module-level state so all tool wrappers
# can reach it without needing it passed per-call.
# Parameters: scheduler - shared Schedule instance
def get_agent(scheduler):
    global _agent, _scheduler

    if _agent is None:
        _scheduler = scheduler  # inject scheduler once at agent creation

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

# Sends a user message to the agent and returns the final reply string.
# Initialises the agent on first call via get_agent().
# Parameters: scheduler - shared Schedule instance, user_input - message from the user
# Returns: str - the agent's natural-language response
def run_agent(scheduler, user_input: str):
    agent = get_agent(scheduler)

    result = agent.invoke({
        "messages": [HumanMessage(content=user_input)]
    })

    last = result["messages"][-1].content

    if isinstance(last, dict):
        return last

    if isinstance(last, str):
        try:
            parsed = json.loads(last)
            return parsed
        except:
            return last

    return last