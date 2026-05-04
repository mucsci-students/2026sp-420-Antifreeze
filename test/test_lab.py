import sys
import os
import types
import pytest

from src.model.schedule.lab import lab

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

    def __init__(self, labs):
        self.config = self
        self.labs = list(labs)
        self.courses = []
        self.faculty = []


class MockCourse:
    """Minimal stand-in for a course with a lab assignment list."""

    def __init__(self, labs):
        self.lab = labs


class MockFaculty:
    """Minimal stand-in for a faculty member with lab preferences."""

    def __init__(self, prefs):
        self.lab_preferences = prefs


SAMPLE_CSV_CONTENT = """\
Schedule 1:
CMSC 140.01,Hardy,Roddy 136,None,MON 09:00-09:50,WED 09:00-10:50,FRI 09:00-09:50

CMSC 140.02,Hardy,Roddy 136,None,MON 12:00-12:50,WED 11:00-12:50,FRI 12:00-12:50

CMSC 152.01,Hardy,Roddy 140,Mac,MON 14:00-14:50,TUE 13:10-15:00^,FRI 14:00-14:50

CMSC 161.01,Zoppetti,Roddy 136,Linux,MON 11:00-11:50,THU 10:00-11:50^,FRI 11:00-11:50

CMSC 161.02,Wertz,Roddy 140,Linux,TUE 08:00-09:50^,THU 08:00-09:50

CMSC 161.03,Rogers,Roddy 136,Linux,TUE 17:40-19:30,THU 17:40-19:30

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


@pytest.fixture
def L():
    """Return a fresh lab instance for each test."""
    return lab()


@pytest.fixture
def sample_csv(tmp_path):
    """Write the sample CSV to a temp file and return its path."""
    f = tmp_path / "example.csv"
    f.write_text(SAMPLE_CSV_CONTENT)
    return str(f)


@pytest.fixture
def sample_schedule(L, sample_csv):
    """Pre-parsed schedule dict so CSV tests don't repeat the parse call."""
    return L.get_lab_schedule(sample_csv)


# validate_entry — add


class TestValidateEntryAdd:
    def test_valid_new_lab_returns_true(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "Windows", "add") is True

    def test_duplicate_lab_returns_false(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "Linux", "add") is False

    def test_empty_name_returns_false(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "", "add") is False


# validate_entry — modify


class TestValidateEntryModify:
    def test_existing_lab_returns_true(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "Linux", "modify") is True

    def test_nonexistent_lab_returns_false(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "Windows", "modify") is False

    def test_empty_name_returns_false(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "", "modify") is False


# validate_entry — delete


class TestValidateEntryDelete:
    def test_existing_lab_returns_true(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "Mac", "delete") is True

    def test_nonexistent_lab_returns_false(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "Windows", "delete") is False

    def test_empty_name_returns_false(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert L.validate_entry(cfg, "", "delete") is False


# add_lab


class TestAddLab:
    def test_new_lab_is_appended(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.add_lab(cfg, "Windows")
        assert "Windows" in cfg.config.labs

    def test_count_increases_by_one(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.add_lab(cfg, "Windows")
        assert len(cfg.config.labs) == 3

    def test_duplicate_is_not_appended(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.add_lab(cfg, "Linux")
        assert cfg.config.labs.count("Linux") == 1


# delete_lab


class TestDeleteLab:
    def test_lab_is_removed(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.delete_lab(cfg, "Linux")
        assert "Linux" not in cfg.config.labs

    def test_count_decreases_by_one(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.delete_lab(cfg, "Linux")
        assert len(cfg.config.labs) == 1

    def test_deleting_nonexistent_lab_is_safe(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.delete_lab(cfg, "Linux")
        L.delete_lab(cfg, "Linux")  # already gone — must not raise
        assert len(cfg.config.labs) == 1

    def test_delete_removes_lab_from_courses(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        cfg.config.courses = [MockCourse(["Linux", "Mac"]), MockCourse(["Linux"])]
        L.delete_lab(cfg, "Linux")
        assert "Linux" not in cfg.config.courses[0].lab
        assert "Linux" not in cfg.config.courses[1].lab

    def test_delete_removes_lab_preferences(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        cfg.config.faculty = [MockFaculty({"Linux": 1, "Mac": 2})]
        L.delete_lab(cfg, "Linux")
        assert "Linux" not in cfg.config.faculty[0].lab_preferences


# modify_lab


class TestModifyLab:
    def test_old_name_is_removed(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.modify_lab(cfg, "Linux", "Linux_0")
        assert "Linux" not in cfg.config.labs

    def test_new_name_is_present(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.modify_lab(cfg, "Linux", "Linux_0")
        assert "Linux_0" in cfg.config.labs

    def test_count_stays_the_same(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.modify_lab(cfg, "Linux", "Linux_0")
        assert len(cfg.config.labs) == 2

    def test_order_is_preserved(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.modify_lab(cfg, "Linux", "Linux_0")
        assert cfg.config.labs[0] == "Linux_0"

    def test_nonexistent_old_name_leaves_list_unchanged(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.modify_lab(cfg, "DoesNotExist", "Anything")
        assert len(cfg.config.labs) == 2

    def test_collision_with_existing_name_leaves_list_unchanged(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        L.modify_lab(cfg, "Linux", "Mac")  # "Mac" already exists
        assert "Linux" in cfg.config.labs

    def test_modify_updates_course_labs(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        cfg.config.courses = [MockCourse(["Linux"])]
        L.modify_lab(cfg, "Linux", "Linux_0")
        assert "Linux_0" in cfg.config.courses[0].lab
        assert "Linux" not in cfg.config.courses[0].lab

    def test_modify_updates_faculty_preferences(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        cfg.config.faculty = [MockFaculty({"Linux": 1})]
        L.modify_lab(cfg, "Linux", "Linux_0")
        prefs = cfg.config.faculty[0].lab_preferences
        assert "Linux_0" in prefs
        assert "Linux" not in prefs


# get_lab_ids


class TestGetLabIds:
    def test_returns_a_list(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert isinstance(L.get_lab_ids(cfg), list)

    def test_contains_correct_labs(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert set(L.get_lab_ids(cfg)) == {"Linux", "Mac"}

    def test_length_matches_config(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        assert len(L.get_lab_ids(cfg)) == 2

    def test_empty_config_returns_empty_list(self, L):
        cfg = MockConfig([])
        assert L.get_lab_ids(cfg) == []

    def test_returned_list_is_a_copy(self, L):
        cfg = MockConfig(["Linux", "Mac"])
        ids = L.get_lab_ids(cfg)
        ids.append("Phantom")
        assert "Phantom" not in cfg.config.labs


# get_lab_schedule — structure


class TestGetLabScheduleStructure:
    def test_returns_a_dict(self, sample_schedule):
        assert isinstance(sample_schedule, dict)

    def test_linux_key_present(self, sample_schedule):
        assert "Linux" in sample_schedule

    def test_mac_key_present(self, sample_schedule):
        assert "Mac" in sample_schedule

    def test_none_lab_rows_excluded(self, sample_schedule):
        assert "None" not in sample_schedule

    def test_empty_lab_rows_excluded(self, sample_schedule):
        assert "" not in sample_schedule


# get_lab_schedule — Linux entries


class TestGetLabScheduleLinux:
    def test_linux_has_eight_entries(self, sample_schedule):
        # CMSC 161 (×3), CMSC 162, CMSC 340 (×2), CMSC 362, CMSC 476
        assert len(sample_schedule["Linux"]) == 8

    def test_cmsc_161_01_is_in_linux(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 161" and e["section"] == "01"
            for e in sample_schedule["Linux"]
        )

    def test_cmsc_476_01_is_in_linux(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 476" and e["section"] == "01"
            for e in sample_schedule["Linux"]
        )

    def test_cmsc_140_no_lab_not_in_linux(self, sample_schedule):
        course_ids = [e["course_id"] for e in sample_schedule["Linux"]]
        assert "CMSC 140" not in course_ids


# get_lab_schedule — Mac entries


class TestGetLabScheduleMac:
    def test_mac_has_seven_entries(self, sample_schedule):
        # CMSC 152, CMSC 330, CMSC 366 (×2), CMSC 380, CMSC 420, CMSC 453
        assert len(sample_schedule["Mac"]) == 7

    def test_cmsc_152_01_is_in_mac(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 152" and e["section"] == "01"
            for e in sample_schedule["Mac"]
        )

    def test_cmsc_420_01_is_in_mac(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 420" and e["section"] == "01"
            for e in sample_schedule["Mac"]
        )


# get_lab_schedule — entry field correctness (spot-check CMSC 161.01)


class TestGetLabScheduleEntryFields:
    @pytest.fixture
    def entry_161_01(self, sample_schedule):
        return next(
            (
                e
                for e in sample_schedule["Linux"]
                if e["course_id"] == "CMSC 161" and e["section"] == "01"
            ),
            None,
        )

    def test_entry_exists(self, entry_161_01):
        assert entry_161_01 is not None

    def test_has_course_id_key(self, entry_161_01):
        assert "course_id" in entry_161_01

    def test_has_section_key(self, entry_161_01):
        assert "section" in entry_161_01

    def test_has_faculty_key(self, entry_161_01):
        assert "faculty" in entry_161_01

    def test_has_room_key(self, entry_161_01):
        assert "room" in entry_161_01

    def test_has_meetings_key(self, entry_161_01):
        assert "meetings" in entry_161_01

    def test_faculty_is_zoppetti(self, entry_161_01):
        assert entry_161_01["faculty"] == "Zoppetti"

    def test_room_is_roddy_136(self, entry_161_01):
        assert entry_161_01["room"] == "Roddy 136"

    def test_has_three_meeting_slots(self, entry_161_01):
        assert len(entry_161_01["meetings"]) == 3

    def test_lab_meeting_contains_caret_marker(self, entry_161_01):
        assert any("^" in m for m in entry_161_01["meetings"])


# get_lab_schedule — edge cases


class TestGetLabScheduleEdgeCases:
    def test_empty_csv_returns_empty_dict(self, L, tmp_path):
        f = tmp_path / "empty.csv"
        f.write_text("Schedule 1:\n\n")
        assert L.get_lab_schedule(str(f)) == {}

    def test_all_none_lab_rows_returns_empty_dict(self, L, tmp_path):
        f = tmp_path / "none_labs.csv"
        f.write_text(
            "Schedule 1:\nCMSC 140.01,Hardy,Roddy 136,None,MON 09:00-09:50\n\n"
        )
        assert L.get_lab_schedule(str(f)) == {}
