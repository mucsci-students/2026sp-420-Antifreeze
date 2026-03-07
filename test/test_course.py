import sys
import os
import pytest
import types


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from src.model.schedule.course import course

class MockCourse:
    def __init__(self, course_id, credits=3, room=None, lab=None, conflicts=None, faculty=None):
        self.course_id = course_id
        self.credits = credits
        self.room = room or []
        self.lab = lab or []
        self.conflicts = conflicts or []
        self.faculty = faculty or []


class MockFaculty:
    def __init__(self, name):
        self.name = name
        self.course_preferences = {}


class MockConfig:
    def __init__(self):
        self.config = types.SimpleNamespace(
            courses=[
                MockCourse("CS101"),
                MockCourse("CS102", conflicts=["CS101"])
            ],
            labs=["LAB1", "LAB2"],
            rooms=["ROOM1", "ROOM2"],
            faculty=[MockFaculty("DrA"), MockFaculty("DrB")]
        )


# ---- Fixtures ----

@pytest.fixture
def test_config():
    return MockConfig()


@pytest.fixture
def course_obj():
    return course()


# ---- Tests ----

def test_validate_entry_add_success(course_obj, test_config):
    assert course_obj.validate_entry(test_config, "CS103", "add") is True


def test_validate_entry_add_duplicate(course_obj, test_config):
    assert course_obj.validate_entry(test_config, "CS101", "add") is False


def test_validate_entry_modify_missing(course_obj, test_config):
    assert course_obj.validate_entry(test_config, "CS999", "modify") is False


def test_existing_items_valid(course_obj, test_config):
    result = course_obj.existing_items(
        test_config,
        "CS200",
        ["ROOM1"],
        ["LAB1"],
        ["CS101"],
        ["DrA"]
    )
    assert result is True


def test_existing_items_invalid_room(course_obj, test_config):
    result = course_obj.existing_items(
        test_config,
        "CS200",
        ["BADROOM"],
        ["LAB1"],
        ["CS101"],
        ["DrA"]
    )
    assert result is False


def test_delete_course(course_obj, test_config):
    course_obj.delete_course(test_config, "CS101")
    ids = [c.course_id for c in test_config.config.courses]
    assert "CS101" not in ids


def test_modify_course(course_obj, test_config):
    course_obj.modify_course(
        test_config,
        "CS101",
        "CS201",
        4,
        ["ROOM1"],
        ["LAB1"],
        [],
        ["DrA"]
    )

    ids = [c.course_id for c in test_config.config.courses]
    assert "CS201" in ids
    assert "CS101" not in ids


def test_get_course_id(course_obj, test_config):
    ids = course_obj.get_course_id(test_config)
    assert ids == ["CS101", "CS102"]