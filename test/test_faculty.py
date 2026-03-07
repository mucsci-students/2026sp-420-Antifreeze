import sys
import os
import types
import pytest


# Point Python at the project root so src.model.schedule.faculty resolves

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


# Minimal stubs so faculty.py can be imported without the real 'scheduler' package

scheduler_stub = types.ModuleType("scheduler")

class _FacultyConfig:
    """Minimal stand-in for the real FacultyConfig."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

scheduler_stub.FacultyConfig  = _FacultyConfig
scheduler_stub.Faculty        = str
scheduler_stub.Day            = str
scheduler_stub.TimeRange      = str
scheduler_stub.Course         = str
scheduler_stub.Preference     = int
scheduler_stub.Room           = str
scheduler_stub.Lab            = str
sys.modules.setdefault("scheduler", scheduler_stub)


# Import the class under test

from src.model.schedule.faculty import faculty



# Helpers

class MockFacultyMember:
    """Mirrors the real FacultyConfig object — only .name is needed here."""
    def __init__(self, name):
        self.name = name


class MockConfig:
    """Lightweight stand-in for the real config object."""
    def __init__(self, names):
        self.config = self
        self.faculty = [MockFacultyMember(n) for n in names]
class MockCourse:
    def __init__(self, faculty):
        self.faculty = faculty


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

ALL_FACULTY = ["Zoppetti", "Hardy", "Hogg", "Xie", "Rogers", "Wertz", "Hobbs", "Yang", "Schwartz"]


# Fixtures

@pytest.fixture
def F():
    return faculty()


@pytest.fixture
def sample_csv(tmp_path):
    f = tmp_path / "example.csv"
    f.write_text(SAMPLE_CSV_CONTENT)
    return str(f)


@pytest.fixture
def sample_schedule(F, sample_csv):
    return F.get_faculty_schedule(sample_csv)



# validate_entry — add

class TestValidateEntryAdd:
    def test_valid_new_faculty_returns_true(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "NewProf", "add") is True

    def test_duplicate_faculty_returns_false(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "Zoppetti", "add") is False

    def test_duplicate_is_case_insensitive(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "zoppetti", "add") is False

    def test_empty_name_returns_false(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "", "add") is False



# validate_entry — modify

class TestValidateEntryModify:
    def test_existing_faculty_returns_true(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "Zoppetti", "modify") is True

    def test_nonexistent_faculty_returns_false(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "NoOne", "modify") is False

    def test_modify_is_case_insensitive(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "HARDY", "modify") is True

    def test_empty_name_returns_false(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "", "modify") is False


# validate_entry — delete

class TestValidateEntryDelete:
    def test_existing_faculty_returns_true(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "Hardy", "delete") is True

    def test_nonexistent_faculty_returns_false(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "NoOne", "delete") is False

    def test_delete_is_case_insensitive(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "ZOPPETTI", "delete") is True

    def test_empty_name_returns_false(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert F.validate_entry(cfg, "", "delete") is False
    def test_delete_cascade_removes_from_courses(self, F):
        cfg = MockConfig(["Zoppetti"])

        cfg.config.courses = [
            MockCourse(["Zoppetti", "Hardy"])
        ]

        F.delete_faculty(cfg, "Zoppetti")

        assert "Zoppetti" not in cfg.config.courses[0].faculty


# get_faculty_ids

class TestGetFacultyIds:
    def test_returns_a_list(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert isinstance(F.get_faculty_ids(cfg), list)

    def test_contains_correct_names(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        assert set(F.get_faculty_ids(cfg)) == {"Zoppetti", "Hardy"}

    def test_length_matches_config(self, F):
        cfg = MockConfig(ALL_FACULTY)
        assert len(F.get_faculty_ids(cfg)) == len(ALL_FACULTY)

    def test_empty_config_returns_empty_list(self, F):
        cfg = MockConfig([])
        assert F.get_faculty_ids(cfg) == []

    def test_names_preserve_original_casing(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        names = F.get_faculty_ids(cfg)
        assert "Zoppetti" in names and "Hardy" in names

    def test_returned_list_is_a_copy(self, F):
        cfg = MockConfig(["Zoppetti", "Hardy"])
        ids = F.get_faculty_ids(cfg)
        ids.append("Phantom")
        assert not any(m.name == "Phantom" for m in cfg.config.faculty)


# get_faculty_schedule — structure

class TestGetFacultyScheduleStructure:
    def test_returns_a_dict(self, F, sample_csv):
        assert isinstance(F.get_faculty_schedule(sample_csv), dict)

    def test_values_are_lists(self, sample_schedule):
        assert all(isinstance(v, list) for v in sample_schedule.values())

    def test_all_faculty_keys_present(self, sample_schedule):
        expected = {"Zoppetti", "Hardy", "Hogg", "Xie", "Rogers", "Wertz", "Hobbs", "Yang"}
        assert expected.issubset(sample_schedule.keys())

    def test_schwartz_not_present(self, sample_schedule):
        # Schwartz has no courses in the CSV
        assert "Schwartz" not in sample_schedule



# get_faculty_schedule — per-faculty entry counts

class TestGetFacultyScheduleEntryCounts:
    def test_zoppetti_has_three_courses(self, sample_schedule):
        # CMSC 161.01, CMSC 362.01, CMSC 476.01
        assert len(sample_schedule["Zoppetti"]) == 3

    def test_hardy_has_three_courses(self, sample_schedule):
        # CMSC 140.01, CMSC 140.02, CMSC 152.01
        assert len(sample_schedule["Hardy"]) == 3

    def test_hogg_has_two_courses(self, sample_schedule):
        # CMSC 162.01, CMSC 380.01
        assert len(sample_schedule["Hogg"]) == 2

    def test_xie_has_three_courses(self, sample_schedule):
        # CMSC 330.01, CMSC 366.01, CMSC 366.02
        assert len(sample_schedule["Xie"]) == 3

    def test_yang_has_three_courses(self, sample_schedule):
        # CMSC 340.01, CMSC 340.02, CMSC 453.01
        assert len(sample_schedule["Yang"]) == 3

    def test_rogers_has_one_course(self, sample_schedule):
        assert len(sample_schedule["Rogers"]) == 1

    def test_wertz_has_one_course(self, sample_schedule):
        assert len(sample_schedule["Wertz"]) == 1

    def test_hobbs_has_one_course(self, sample_schedule):
        assert len(sample_schedule["Hobbs"]) == 1


# get_faculty_schedule — entry field correctness (spot-check Zoppetti 161.01)

class TestGetFacultyScheduleEntryFields:
    @pytest.fixture
    def entry_161_01(self, sample_schedule):
        """Spot-check CMSC 161.01 assigned to Zoppetti."""
        return next(
            (e for e in sample_schedule["Zoppetti"]
             if e["course_id"] == "CMSC 161" and e["section"] == "01"),
            None
        )

    def test_entry_exists(self, entry_161_01):
        assert entry_161_01 is not None

    def test_entry_is_a_dict(self, entry_161_01):
        assert isinstance(entry_161_01, dict)

    def test_has_course_id_key(self, entry_161_01):
        assert "course_id" in entry_161_01

    def test_has_section_key(self, entry_161_01):
        assert "section" in entry_161_01

    def test_has_room_key(self, entry_161_01):
        assert "room" in entry_161_01

    def test_has_lab_key(self, entry_161_01):
        assert "lab" in entry_161_01

    def test_has_meetings_key(self, entry_161_01):
        assert "meetings" in entry_161_01

    def test_course_id_is_correct(self, entry_161_01):
        assert entry_161_01["course_id"] == "CMSC 161"

    def test_section_is_correct(self, entry_161_01):
        assert entry_161_01["section"] == "01"

    def test_room_is_correct(self, entry_161_01):
        assert entry_161_01["room"] == "Roddy 136"

    def test_lab_is_correct(self, entry_161_01):
        assert entry_161_01["lab"] == "Linux"

    def test_has_three_meeting_slots(self, entry_161_01):
        assert len(entry_161_01["meetings"]) == 3

    def test_lab_meeting_contains_caret_marker(self, entry_161_01):
        assert any("^" in m for m in entry_161_01["meetings"])



# get_faculty_schedule — spot-check other faculty members

class TestGetFacultyScheduleSpotChecks:
    def test_hardy_has_cmsc_152(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 152" and e["section"] == "01"
            for e in sample_schedule["Hardy"]
        )

    def test_hardy_cmsc_140_01_has_no_lab(self, sample_schedule):
        entry = next(
            (e for e in sample_schedule["Hardy"]
             if e["course_id"] == "CMSC 140" and e["section"] == "01"),
            None
        )
        assert entry is not None
        assert entry["lab"] == "None"

    def test_hobbs_teaches_cmsc_420(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 420"
            for e in sample_schedule["Hobbs"]
        )

    def test_wertz_teaches_cmsc_161(self, sample_schedule):
        assert any(
            e["course_id"] == "CMSC 161"
            for e in sample_schedule["Wertz"]
        )

    def test_yang_has_cmsc_340_section_01_and_02(self, sample_schedule):
        sections = {
            e["section"] for e in sample_schedule["Yang"]
            if e["course_id"] == "CMSC 340"
        }
        assert sections == {"01", "02"}

    def test_xie_has_cmsc_366_twice(self, sample_schedule):
        count = sum(
            1 for e in sample_schedule["Xie"]
            if e["course_id"] == "CMSC 366"
        )
        assert count == 2



# get_faculty_schedule — edge cases

class TestGetFacultyScheduleEdgeCases:
    def test_empty_csv_returns_empty_dict(self, F, tmp_path):
        f = tmp_path / "empty.csv"
        f.write_text("Schedule 1:\n\n")
        assert F.get_faculty_schedule(str(f)) == {}

    def test_single_row_produces_one_faculty_key(self, F, tmp_path):
        f = tmp_path / "single.csv"
        f.write_text(
            "Schedule 1:\n"
            "CMSC 999.01,TestProf,Roddy 200,None,MON 10:00-10:50\n\n"
        )
        result = F.get_faculty_schedule(str(f))
        assert list(result.keys()) == ["TestProf"]

    def test_single_row_produces_one_entry(self, F, tmp_path):
        f = tmp_path / "single.csv"
        f.write_text(
            "Schedule 1:\n"
            "CMSC 999.01,TestProf,Roddy 200,None,MON 10:00-10:50\n\n"
        )
        result = F.get_faculty_schedule(str(f))
        assert len(result["TestProf"]) == 1