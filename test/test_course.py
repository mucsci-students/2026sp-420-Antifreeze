import sys
import os
import pytest
import types

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.model.schedule.course import course


# Mock Objects


class MockCourse:
    def __init__(
        self, course_id, credits=3, room=None, lab=None, conflicts=None, faculty=None
    ):
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
            courses=[MockCourse("CS101"), MockCourse("CS102", conflicts=["CS101"])],
            labs=["LAB1", "LAB2"],
            rooms=["ROOM1", "ROOM2"],
            faculty=[MockFaculty("DrA"), MockFaculty("DrB")],
        )


# Fixtures


@pytest.fixture
def test_config():
    return MockConfig()


@pytest.fixture
def course_obj():
    return course()


# validate_entry


class TestValidateEntry:
    def test_validate_entry_add_success(self, course_obj, test_config):
        assert course_obj.validate_entry(test_config, "CS103", "add") is True

    def test_validate_entry_add_duplicate(self, course_obj, test_config):
        assert course_obj.validate_entry(test_config, "CS101", "add") is False

    def test_validate_entry_modify_missing(self, course_obj, test_config):
        assert course_obj.validate_entry(test_config, "CS999", "modify") is False

    def test_validate_entry_modify_success(self, course_obj, test_config):
        assert course_obj.validate_entry(test_config, "CS101", "modify") is True

    def test_validate_entry_delete_success(self, course_obj, test_config):
        assert course_obj.validate_entry(test_config, "CS101", "delete") is True

    def test_validate_entry_delete_missing(self, course_obj, test_config):
        assert course_obj.validate_entry(test_config, "CS999", "delete") is False

    def test_validate_entry_add_empty_id(self, course_obj, test_config):
        assert course_obj.validate_entry(test_config, "", "add") is False


# existing_items


class TestExistingItems:
    def test_existing_items_valid(self, course_obj, test_config):
        result = course_obj.existing_items(
            test_config, "CS200", ["ROOM1"], ["LAB1"], ["CS101"], ["DrA"]
        )
        assert result is True

    def test_existing_items_invalid_room(self, course_obj, test_config):
        result = course_obj.existing_items(
            test_config, "CS200", ["BADROOM"], ["LAB1"], ["CS101"], ["DrA"]
        )
        assert result is False

    def test_invalid_lab(self, course_obj, test_config):
        result = course_obj.existing_items(
            test_config, "CS200", ["ROOM1"], ["BADLAB"], ["CS101"], ["DrA"]
        )
        assert result is False

    def test_invalid_conflict(self, course_obj, test_config):
        result = course_obj.existing_items(
            test_config, "CS200", ["ROOM1"], ["LAB1"], ["BADCOURSE"], ["DrA"]
        )
        assert result is False

    def test_invalid_faculty(self, course_obj, test_config):
        result = course_obj.existing_items(
            test_config, "CS200", ["ROOM1"], ["LAB1"], ["CS101"], ["FakeProfessor"]
        )
        assert result is False

    def test_duplicate_item(self, course_obj, test_config):
        result = course_obj.existing_items(
            test_config, "CS101", ["ROOM1"], ["LAB1"], ["CS101"], ["FakeProfessor"]
        )
        assert result is False


# delete_course


class TestDeleteCourse:
    def test_delete_course(self, course_obj, test_config):
        course_obj.delete_course(test_config, "CS101")
        ids = [c.course_id for c in test_config.config.courses]
        assert "CS101" not in ids

    def test_delete_reduces_count(self, course_obj, test_config):
        initial = len(test_config.config.courses)
        course_obj.delete_course(test_config, "CS101")
        assert len(test_config.config.courses) == initial - 1

    def test_delete_nonexistent_course_safe(self, course_obj, test_config):
        course_obj.delete_course(test_config, "CS999")
        assert len(test_config.config.courses) == 2

    def test_delete_removes_conflicts(self, course_obj, test_config):
        # CS102 initially conflicts with CS101
        course_obj.delete_course(test_config, "CS101")

        remaining = next(
            c for c in test_config.config.courses if c.course_id == "CS102"
        )
        assert "CS101" not in remaining.conflicts

    def test_delete_removes_faculty_preferences(self, course_obj, test_config):
        # simulate faculty preference for CS101
        test_config.config.faculty[0].course_preferences["CS101"] = 1

        course_obj.delete_course(test_config, "CS101")

        prefs = test_config.config.faculty[0].course_preferences
        assert "CS101" not in prefs


#  modify_course


class TestModifyCourse:
    def test_modify_course(self, course_obj, test_config):
        course_obj.modify_course(
            test_config, "CS101", "CS201", 4, ["ROOM1"], ["LAB1"], [], ["DrA"]
        )

        ids = [c.course_id for c in test_config.config.courses]
        assert "CS201" in ids
        assert "CS101" not in ids

    def test_modify_updates_credits(self, course_obj, test_config):
        course_obj.modify_course(
            test_config, "CS101", "CS201", 5, ["ROOM1"], ["LAB1"], [], ["DrA"]
        )

        c = next(c for c in test_config.config.courses if c.course_id == "CS201")
        assert c.credits == 5

    def test_modify_updates_rooms(self, course_obj, test_config):
        course_obj.modify_course(
            test_config, "CS101", "CS201", 3, ["ROOM2"], [], [], []
        )

        c = next(c for c in test_config.config.courses if c.course_id == "CS201")
        assert c.room == ["ROOM2"]

    def test_modify_missing_course_no_change(self, course_obj, test_config):
        original_ids = [c.course_id for c in test_config.config.courses]

        course_obj.modify_course(
            test_config, "DOESNOTEXIST", "NEWID", 3, [], [], [], []
        )

        new_ids = [c.course_id for c in test_config.config.courses]
        assert new_ids == original_ids


#  get_course_id


class TestGetCourseIds:
    def test_get_course_id(self, course_obj, test_config):
        ids = course_obj.get_course_id(test_config)
        assert ids == ["CS101", "CS102"]

    def test_returns_list(self, course_obj, test_config):
        ids = course_obj.get_course_id(test_config)
        assert isinstance(ids, list)

    def test_correct_length(self, course_obj, test_config):
        ids = course_obj.get_course_id(test_config)
        assert len(ids) == 2

    def test_empty_course_list(self, course_obj):
        cfg = MockConfig()
        cfg.config.courses = []
        ids = course_obj.get_course_id(cfg)
        assert ids == []

    def test_return_is_copy(self, course_obj, test_config):
        ids = course_obj.get_course_id(test_config)
        ids.append("FAKE")

        new_ids = course_obj.get_course_id(test_config)
        assert "FAKE" not in new_ids
