import sys
import os
import types
import pytest

from src.model.schedule.room import room

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

scheduler_stub = types.ModuleType("scheduler")
setattr(scheduler_stub, "Scheduler", object)
setattr(scheduler_stub, "load_config_from_file", lambda *a, **kw: None)
sys.modules.setdefault("scheduler", scheduler_stub)

scheduler_config_stub = types.ModuleType("scheduler.config")
setattr(scheduler_config_stub, "CombinedConfig", object)
sys.modules.setdefault("scheduler.config", scheduler_config_stub)


# Mock objects


class MockConfig:
    """Lightweight stand-in for the real config object."""

    def __init__(self, rooms):
        self.config = self
        self.rooms = list(rooms)
        self.courses = []
        self.faculty = []


class MockCourse:
    """Minimal stand-in for a course with a room assignment list."""

    def __init__(self, rooms):
        self.room = rooms


class MockFaculty:
    """Minimal stand-in for a faculty member with room preferences."""

    def __init__(self, prefs):
        self.room_preferences = prefs


SAMPLE_CSV_CONTENT = """\
Schedule 1:
CMSC 140.01,Hardy,Roddy 136,None,MON 09:00-09:50,WED 09:00-10:50,FRI 09:00-09:50

CMSC 140.02,Hardy,Roddy 136,None,MON 12:00-12:50,WED 11:00-12:50,FRI 12:00-12:50

CMSC 152.01,Hardy,Roddy 140,Mac,MON 14:00-14:50,TUE 13:10-15:00^,FRI 14:00-14:50

CMSC 161.01,Zoppetti,Roddy 136,Linux,MON 11:00-11:50,THU 10:00-11:50^,FRI 11:00-11:50

CMSC 161.02,Wertz,Roddy 140,Linux,TUE 08:00-09:50^,THU 08:00-09:50

CMSC 161.03,Rogers,Roddy 136,Linux,TUE 17:40-19:30,THU 17:40-19:30^

CMSC 162.01,Hogg,Roddy 140,Linux,MON 11:00-11:50,TUE 10:00-11:50^,FRI 11:00-11:50

CMSC 330.01,Xie,Roddy 147,Mac,MON 09:00-09:50,THU 09:00-10:50^,FRI 09:00-09:50

CMSC 340.01,Yang,Roddy 147,Linux,MON 11:00-11:50,WED 11:00-12:50^,FRI 11:00-11:50

CMSC 340.02,Yang,Roddy 147,Linux,MON 10:00-10:50,WED 09:00-10:50^,FRI 10:00-10:50

CMSC 362.01,Zoppetti,Roddy 136,Linux,MON 15:00-15:50,THU 14:10-16:00^,FRI 15:00-15:50

CMSC 366.01,Xie,Roddy 140,Mac,MON 13:00-13:50,WED 13:00-14:50^,FRI 13:00-13:50

CMSC 366.02,Xie,Roddy 140,Mac,MON 12:00-12:50,WED 11:00-12:50^,FRI 12:00-12:50

CMSC 380.01,Hogg,Roddy 140,Mac,MON 09:00-09:50,WED 09:00-10:50^,FRI 09:00-09:50

CMSC 420.01,Hobbs,Roddy 140,Mac,MON 16:00-17:50^,WED 16:00-17:50

CMSC 453.01,Yang,Roddy 147,Mac,MON 14:00-14:50,THU 13:10-15:00^,FRI 14:00-14:50

CMSC 476.01,Zoppetti,Roddy 136,Linux,MON 13:00-13:50,WED 13:00-14:50^,FRI 13:00-13:50

"""


# Fixtures


@pytest.fixture
def R():
    """Return a fresh room instance for each test."""
    return room()


@pytest.fixture
def sample_csv(tmp_path):
    """Write the sample CSV to a temp file and return its path."""
    f = tmp_path / "example.csv"
    f.write_text(SAMPLE_CSV_CONTENT)
    return str(f)


@pytest.fixture
def sample_schedule(R, sample_csv):
    """Pre-parsed schedule dict so CSV tests don't repeat the parse call."""
    return R.get_room_schedule(sample_csv)


# validate_entry — add


class TestValidateEntryAdd:
    def test_valid_new_room_returns_true(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "Roddy 150", "add") is True

    def test_duplicate_room_returns_false(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "Roddy 136", "add") is False

    def test_empty_name_returns_false(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "", "add") is False


# validate_entry — modify


class TestValidateEntryModify:
    def test_existing_room_returns_true(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "Roddy 136", "modify") is True

    def test_nonexistent_room_returns_false(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "Roddy 999", "modify") is False

    def test_empty_name_returns_false(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "", "modify") is False


# validate_entry — delete


class TestValidateEntryDelete:
    def test_existing_room_returns_true(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "Roddy 140", "delete") is True

    def test_nonexistent_room_returns_false(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "Roddy 999", "delete") is False

    def test_empty_name_returns_false(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert R.validate_entry(cfg, "", "delete") is False


# add_room


class TestAddRoom:
    def test_new_room_is_appended(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])
        R.add_room(cfg, "Roddy 147")
        assert "Roddy 147" in cfg.config.rooms

    def test_count_increases_by_one(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])
        R.add_room(cfg, "Roddy 147")
        assert len(cfg.config.rooms) == 3

    def test_duplicate_is_not_appended(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])
        R.add_room(cfg, "Roddy 136")
        assert cfg.config.rooms.count("Roddy 136") == 1

    def test_empty_name_is_not_appended(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])
        R.add_room(cfg, "")
        assert "" not in cfg.config.rooms


# delete_room


class TestDeleteRoom:
    def test_room_is_removed(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.delete_room(cfg, "Roddy 136")
        assert "Roddy 136" not in cfg.config.rooms

    def test_count_decreases_by_one(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.delete_room(cfg, "Roddy 136")
        assert len(cfg.config.rooms) == 2

    def test_deleting_nonexistent_room_is_safe(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.delete_room(cfg, "Roddy 136")
        R.delete_room(cfg, "Roddy 136")  # already gone — must not raise
        assert len(cfg.config.rooms) == 2

    def test_empty_name_is_safe(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.delete_room(cfg, "")  # must not raise
        assert len(cfg.config.rooms) == 3

    def test_delete_removes_room_from_courses(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])

        cfg.config.courses = [
            MockCourse(["Roddy 136", "Roddy 140"]),
            MockCourse(["Roddy 136"]),
        ]

        R.delete_room(cfg, "Roddy 136")

        assert "Roddy 136" not in cfg.config.courses[0].room
        assert "Roddy 136" not in cfg.config.courses[1].room

    def test_delete_removes_room_preferences(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])

        cfg.config.faculty = [MockFaculty({"Roddy 136": 1, "Roddy 140": 2})]

        R.delete_room(cfg, "Roddy 136")

        assert "Roddy 136" not in cfg.config.faculty[0].room_preferences


# modify_room


class TestModifyRoom:
    def test_old_name_is_removed(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "Roddy 136", "Roddy 150")
        assert "Roddy 136" not in cfg.config.rooms

    def test_new_name_is_present(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "Roddy 136", "Roddy 150")
        assert "Roddy 150" in cfg.config.rooms

    def test_count_stays_the_same(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "Roddy 136", "Roddy 150")
        assert len(cfg.config.rooms) == 3

    def test_order_is_preserved(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "Roddy 136", "Roddy 150")
        assert cfg.config.rooms[0] == "Roddy 150"

    def test_nonexistent_old_name_leaves_list_unchanged(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "Roddy 999", "Roddy 200")
        assert len(cfg.config.rooms) == 3

    def test_collision_with_existing_name_leaves_list_unchanged(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "Roddy 136", "Roddy 140")  # "Roddy 140" already exists
        assert "Roddy 136" in cfg.config.rooms

    def test_empty_new_name_leaves_list_unchanged(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "Roddy 136", "")
        assert "Roddy 136" in cfg.config.rooms

    def test_empty_old_name_leaves_list_unchanged(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        R.modify_room(cfg, "", "Roddy 200")
        assert len(cfg.config.rooms) == 3

    def test_modify_updates_course_rooms(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])

        cfg.config.courses = [MockCourse(["Roddy 136"])]

        R.modify_room(cfg, "Roddy 136", "Roddy 200")

        assert "Roddy 200" in cfg.config.courses[0].room
        assert "Roddy 136" not in cfg.config.courses[0].room

    def test_modify_updates_faculty_preferences(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140"])

        cfg.config.faculty = [MockFaculty({"Roddy 136": 1})]

        R.modify_room(cfg, "Roddy 136", "Roddy 200")

        prefs = cfg.config.faculty[0].room_preferences

        assert "Roddy 200" in prefs
        assert "Roddy 136" not in prefs


# get_room_ids


class TestGetRoomIds:
    def test_returns_a_list(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert isinstance(R.get_room_ids(cfg), list)

    def test_contains_correct_rooms(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert set(R.get_room_ids(cfg)) == {"Roddy 136", "Roddy 140", "Roddy 147"}

    def test_length_matches_config(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        assert len(R.get_room_ids(cfg)) == 3

    def test_empty_config_returns_empty_list(self, R):
        cfg = MockConfig([])
        assert R.get_room_ids(cfg) == []

    def test_returned_list_is_a_copy(self, R):
        cfg = MockConfig(["Roddy 136", "Roddy 140", "Roddy 147"])
        ids = R.get_room_ids(cfg)
        ids.append("epic awesome room Dr. Killian give us a 100% please")
        assert (
            "epic awesome room Dr. Killian give us a 100% please"
            not in cfg.config.rooms
        )


class TestGetRoomScheduleStructure:
    """Verify the top-level structure of the parsed room schedule dict."""

    def test_returns_a_dict(self, sample_schedule):
        assert isinstance(sample_schedule, dict)

    def test_roddy_136_key_present(self, sample_schedule):
        assert "Roddy 136" in sample_schedule

    def test_roddy_140_key_present(self, sample_schedule):
        assert "Roddy 140" in sample_schedule

    def test_roddy_147_key_present(self, sample_schedule):
        assert "Roddy 147" in sample_schedule


# get_room_schedule — Roddy 136 entries


class TestGetRoomScheduleRoddy136:
    def test_has_six_entries(self, sample_schedule):
        # CMSC 140 (×2), CMSC 161.01, CMSC 161.03, CMSC 362, CMSC 476
        assert len(sample_schedule["Roddy 136"]) == 6

    def test_cmsc_140_01_is_present(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 140" and e["section"] == "01"
            for e in sample_schedule["Roddy 136"]
        )

    def test_cmsc_476_01_is_present(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 476" and e["section"] == "01"
            for e in sample_schedule["Roddy 136"]
        )

    def test_cmsc_152_not_present(self, sample_schedule):
        course_ids = [e["course_id"] for e in sample_schedule["Roddy 136"]]
        assert "CMSC 152" not in course_ids


# get_room_schedule — Roddy 140 entries


class TestGetRoomScheduleRoddy140:
    def test_has_seven_entries(self, sample_schedule):
        # CMSC 152, CMSC 161.02, CMSC 162, CMSC 366 (×2), CMSC 380, CMSC 420
        assert len(sample_schedule["Roddy 140"]) == 7

    def test_cmsc_420_01_is_present(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 420" and e["section"] == "01"
            for e in sample_schedule["Roddy 140"]
        )

    def test_cmsc_476_not_present(self, sample_schedule):
        course_ids = [e["course_id"] for e in sample_schedule["Roddy 140"]]
        assert "CMSC 476" not in course_ids


# get_room_schedule — Roddy 147 entries


class TestGetRoomScheduleRoddy147:
    def test_has_four_entries(self, sample_schedule):
        # CMSC 330, CMSC 340x2, CMSC 453
        assert len(sample_schedule["Roddy 147"]) == 4

    def test_cmsc_340_01_is_present(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 340" and e["section"] == "01"
            for e in sample_schedule["Roddy 147"]
        )

    def test_cmsc_453_01_is_present(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 453" and e["section"] == "01"
            for e in sample_schedule["Roddy 147"]
        )


# get_room_schedule — entry field correctness


class TestGetRoomScheduleEntryFields:
    @pytest.fixture
    def entry_161_01(self, sample_schedule):
        """Spot-check CMSC 161.01: Zoppetti, Roddy 136, Linux."""
        return next(
            (
                e
                for e in sample_schedule["Roddy 136"]
                if e["course_id"] == "CMSC 161" and e["section"] == "01"
            ),
            None,
        )

    @pytest.fixture
    def entry_140_01(self, sample_schedule):
        """Spot-check CMSC 140.01: Hardy, Roddy 136, None lab."""
        return next(
            (
                e
                for e in sample_schedule["Roddy 136"]
                if e["course_id"] == "CMSC 140" and e["section"] == "01"
            ),
            None,
        )

    def test_entry_161_01_exists(self, entry_161_01):
        assert entry_161_01 is not None

    def test_has_course_id_key(self, entry_161_01):
        assert "course_id" in entry_161_01

    def test_has_section_key(self, entry_161_01):
        assert "section" in entry_161_01

    def test_has_faculty_key(self, entry_161_01):
        assert "faculty" in entry_161_01

    def test_has_lab_key(self, entry_161_01):
        assert "lab" in entry_161_01

    def test_has_meetings_key(self, entry_161_01):
        assert "meetings" in entry_161_01

    def test_faculty_is_zoppetti(self, entry_161_01):
        assert entry_161_01["faculty"] == "Zoppetti"

    def test_lab_is_linux(self, entry_161_01):
        assert entry_161_01["lab"] == "Linux"

    def test_has_three_meeting_slots(self, entry_161_01):
        assert len(entry_161_01["meetings"]) == 3

    def test_cmsc_140_01_lab_field_is_none_string(self, entry_140_01):
        assert entry_140_01["lab"] == "None"

    def test_cmsc_140_01_has_three_meeting_slots(self, entry_140_01):
        assert len(entry_140_01["meetings"]) == 3


# get_room_schedule — edge cases


class TestGetRoomScheduleEdgeCases:
    def test_empty_csv_returns_empty_dict(self, R, tmp_path):
        f = tmp_path / "empty.csv"
        f.write_text("Schedule 1:\n\n")
        assert R.get_room_schedule(str(f)) == {}

    def test_single_row_produces_one_room_key(self, R, tmp_path):
        f = tmp_path / "single.csv"
        f.write_text("Schedule 1:\nCMSC 999.01,Prof,Roddy 200,None,MON 10:00-10:50\n\n")
        result = R.get_room_schedule(str(f))
        assert list(result.keys()) == ["Roddy 200"]

    def test_single_row_produces_one_entry(self, R, tmp_path):
        f = tmp_path / "single.csv"
        f.write_text("Schedule 1:\nCMSC 999.01,Prof,Roddy 200,None,MON 10:00-10:50\n\n")
        result = R.get_room_schedule(str(f))
        assert len(result["Roddy 200"]) == 1
