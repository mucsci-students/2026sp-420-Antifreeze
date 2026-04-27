import sys
import os
import pytest


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.model.schedule.conflict import conflict


# Mock Classes
class MockCourse:
    def __init__(self, course_id, conflicts=None):
        self.course_id = course_id
        self.conflicts = conflicts or []


class MockInnerConfig:
    def __init__(self, courses):
        self.courses = courses


class MockConfig:
    def __init__(self, courses):
        self.config = MockInnerConfig(courses)


# Fixtures
@pytest.fixture
def sample_config():
    courses = [
        MockCourse("CMSC 140", ["CMSC 161"]),
        MockCourse("CMSC 161", []),
        MockCourse("CMSC 162", []),
        MockCourse("CMSC 362", ["CMSC 161", "CMSC 340"]),
    ]
    return MockConfig(courses)


@pytest.fixture
def conflict_obj():
    return conflict()


# validate_entry


def test_validate_entry_valid_add(conflict_obj, sample_config):
    result = conflict_obj.validate_entry(sample_config, "CMSC 140", "add", "CMSC 162")
    assert result is True


def test_validate_entry_course_not_found(conflict_obj, sample_config):
    result = conflict_obj.validate_entry(sample_config, "CMSC 999", "add", "CMSC 161")
    assert result is False


def test_validate_entry_conflict_already_exists(conflict_obj, sample_config):
    result = conflict_obj.validate_entry(sample_config, "CMSC 140", "add", "CMSC 161")
    assert result is False


def test_validate_entry_conflict_not_found_for_delete(conflict_obj, sample_config):
    result = conflict_obj.validate_entry(
        sample_config, "CMSC 140", "delete", "CMSC 162"
    )
    assert result is False


def test_validate_entry_conflict_exists(conflict_obj, sample_config):
    result = conflict_obj.validate_entry(
        sample_config, "CMSC 140", "delete", "CMSC 999"
    )
    assert result is False


# add_conflict


def test_add_conflict_success(conflict_obj, sample_config):
    conflict_obj.add_conflict(sample_config, "CMSC 161", "CMSC 162")
    course = next(c for c in sample_config.config.courses if c.course_id == "CMSC 161")
    assert "CMSC 162" in course.conflicts


def test_add_conflict_duplicate(conflict_obj, sample_config):
    conflict_obj.add_conflict(sample_config, "CMSC 140", "CMSC 161")
    course = next(c for c in sample_config.config.courses if c.course_id == "CMSC 140")
    assert course.conflicts.count("CMSC 161") == 1


def test_add_conflict_course_not_found(conflict_obj, sample_config, capsys):
    conflict_obj.add_conflict(sample_config, "CMSC 999", "CMSC 161")
    captured = capsys.readouterr()
    expected_output = "Course 'CMSC 999' not found — no changes made.\n"
    assert expected_output in captured


# delete_conflict


def test_delete_conflict_success(conflict_obj, sample_config):
    conflict_obj.delete_conflict(sample_config, "CMSC 140", "CMSC 161")
    course = next(c for c in sample_config.config.courses if c.course_id == "CMSC 140")
    assert "CMSC 161" not in course.conflicts


def test_delete_conflict_not_found(conflict_obj, sample_config):
    conflict_obj.delete_conflict(sample_config, "CMSC 161", "CMSC 162")
    course = next(c for c in sample_config.config.courses if c.course_id == "CMSC 161")
    assert "CMSC 162" not in course.conflicts


def test_delete_conflict_course_not_found(conflict_obj, sample_config, capsys):
    conflict_obj.delete_conflict(sample_config, "CMSC 999", "CMSC 161")
    captured = capsys.readouterr()
    expected_output = "Course 'CMSC 999' not found — no changes made.\n"
    assert expected_output in captured


# modify_conflict


def test_modify_conflict_success(conflict_obj, sample_config):
    conflict_obj.modify_conflict(sample_config, "CMSC 140", "CMSC 161", "CMSC 162")
    course = next(c for c in sample_config.config.courses if c.course_id == "CMSC 140")
    assert "CMSC 162" in course.conflicts
    assert "CMSC 161" not in course.conflicts


def test_modify_conflict_old_not_found(conflict_obj, sample_config):
    conflict_obj.modify_conflict(sample_config, "CMSC 161", "CMSC 140", "CMSC 162")
    course = next(c for c in sample_config.config.courses if c.course_id == "CMSC 161")
    assert "CMSC 162" not in course.conflicts


def test_mody_conflixt_new_duplicate(conflict_obj, sample_config):
    conflict_obj.modify_conflict(sample_config, "CMSC 362", "CMSC 340", "CMSC 161")
    course = next(c for c in sample_config.config.courses if c.course_id == "CMSC 362")
    assert course.conflicts.count("CMSC 161") == 1


def test_modify_conflict_course_not_found(conflict_obj, sample_config, capsys):
    conflict_obj.modify_conflict(sample_config, "CMSC 999", "CMSC 140", "CMSC 161")
    captured = capsys.readouterr()
    expected_output = "Course 'CMSC 999' not found — no changes made.\n"
    assert expected_output in captured
