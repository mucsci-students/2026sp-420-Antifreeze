import sys
import os
import types
import pytest

from src.model.schedule.time_slot_config import time_slot_config

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

scheduler_stub = types.ModuleType("scheduler")
setattr(scheduler_stub, "Scheduler", object)
setattr(scheduler_stub, "load_config_from_file", lambda *a, **kw: None)
sys.modules.setdefault("scheduler", scheduler_stub)

scheduler_config_stub = types.ModuleType("scheduler.config")
setattr(scheduler_config_stub, "CombinedConfig", object)


# Mock objects


class MockTimeSlotConfig:
    """Stand-in for the time_slot_config section of the real config."""

    def __init__(self, times=None, classes=None):
        self.times = times if times is not None else {}
        self.classes = classes if classes is not None else []


class MockConfig:
    """Lightweight stand-in for the top-level config object."""

    def __init__(self, times=None, classes=None):
        self.time_slot_config = MockTimeSlotConfig(times, classes)


# Helper builders


def make_times_config():
    """Returns a MockConfig with realistic time grid data."""
    return MockConfig(
        times={
            "MON": [{"start": "08:00", "spacing": 60, "end": "19:00"}],
            "TUE": [
                {"start": "08:00", "spacing": 60, "end": "12:00"},
                {"start": "13:10", "spacing": 60, "end": "17:10"},
                {"start": "17:10", "spacing": 30, "end": "19:40"},
            ],
            "WED": [{"start": "08:00", "spacing": 60, "end": "19:00"}],
            "THU": [
                {"start": "08:00", "spacing": 60, "end": "12:00"},
                {"start": "13:10", "spacing": 60, "end": "17:10"},
            ],
            "FRI": [{"start": "08:00", "spacing": 60, "end": "17:00"}],
        }
    )


def make_classes_config():
    """Returns a MockConfig with realistic class pattern data."""
    return MockConfig(
        classes=[
            {
                "credits": 3,
                "meetings": [
                    {"day": "MON", "duration": 50},
                    {"day": "WED", "duration": 50},
                    {"day": "FRI", "duration": 50},
                ],
            },
            {
                "credits": 3,
                "meetings": [
                    {"day": "TUE", "duration": 75},
                    {"day": "THU", "duration": 75},
                ],
            },
            {
                "credits": 4,
                "meetings": [
                    {"day": "MON", "duration": 110, "lab": True},
                    {"day": "WED", "duration": 110},
                ],
                "start_time": "16:00",
            },
            {
                "credits": 4,
                "meetings": [
                    {"day": "TUE", "duration": 110, "lab": True},
                    {"day": "THU", "duration": 110},
                ],
            },
            {
                "credits": 4,
                "meetings": [
                    {"day": "MON", "duration": 110, "lab": True},
                    {"day": "FRI", "duration": 110},
                ],
                "disabled": True,
            },
        ]
    )


def make_full_config():
    """Returns a MockConfig with both times and classes populated."""
    cfg = make_times_config()
    cfg.time_slot_config.classes = make_classes_config().time_slot_config.classes
    return cfg


# Fixtures


@pytest.fixture
def T():
    return time_slot_config()


@pytest.fixture
def times_cfg():
    return make_times_config()


@pytest.fixture
def classes_cfg():
    return make_classes_config()


@pytest.fixture
def full_cfg():
    return make_full_config()


# validate_time_entry — add


class TestValidateTimeEntryAdd:
    def test_valid_day_returns_true(self, T, times_cfg):
        assert T.validate_time_entry(times_cfg, "MON", "add") is True

    def test_new_day_with_no_existing_ranges_returns_true(self, T):
        cfg = MockConfig(times={})
        assert T.validate_time_entry(cfg, "FRI", "add") is True

    def test_invalid_day_returns_false(self, T, times_cfg):
        assert T.validate_time_entry(times_cfg, "SUN", "add") is False

    def test_lowercase_day_is_accepted(self, T, times_cfg):
        assert T.validate_time_entry(times_cfg, "mon", "add") is True


# validate_time_entry — modify


class TestValidateTimeEntryModify:
    def test_valid_index_returns_true(self, T, times_cfg):
        assert T.validate_time_entry(times_cfg, "MON", "modify", range_index=0) is True

    def test_out_of_bounds_index_returns_false(self, T, times_cfg):
        assert T.validate_time_entry(times_cfg, "MON", "modify", range_index=5) is False

    def test_negative_index_returns_false(self, T, times_cfg):
        assert (
            T.validate_time_entry(times_cfg, "MON", "modify", range_index=-1) is False
        )

    def test_missing_index_returns_false(self, T, times_cfg):
        assert (
            T.validate_time_entry(times_cfg, "MON", "modify", range_index=None) is False
        )

    def test_empty_day_list_returns_false(self, T):
        cfg = MockConfig(times={"MON": []})
        assert T.validate_time_entry(cfg, "MON", "modify", range_index=0) is False

    def test_invalid_day_returns_false(self, T, times_cfg):
        assert T.validate_time_entry(times_cfg, "SUN", "modify", range_index=0) is False


# validate_time_entry — delete


class TestValidateTimeEntryDelete:
    def test_valid_index_returns_true(self, T, times_cfg):
        assert T.validate_time_entry(times_cfg, "TUE", "delete", range_index=1) is True

    def test_out_of_bounds_index_returns_false(self, T, times_cfg):
        assert (
            T.validate_time_entry(times_cfg, "TUE", "delete", range_index=10) is False
        )

    def test_missing_index_returns_false(self, T, times_cfg):
        assert (
            T.validate_time_entry(times_cfg, "TUE", "delete", range_index=None) is False
        )

    def test_day_not_in_times_returns_false(self, T):
        cfg = MockConfig(
            times={"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}
        )
        assert T.validate_time_entry(cfg, "FRI", "delete", range_index=0) is False


# add_time


class TestAddTime:
    def test_new_range_is_appended(self, T, times_cfg):
        T.add_time(times_cfg, "MON", "19:00", 60, "22:00")
        assert len(times_cfg.time_slot_config.times["MON"]) == 2

    def test_appended_range_has_correct_values(self, T, times_cfg):
        T.add_time(times_cfg, "MON", "19:00", 60, "22:00")
        added = times_cfg.time_slot_config.times["MON"][-1]
        assert added == {"start": "19:00", "spacing": 60, "end": "22:00"}

    def test_duplicate_range_is_not_appended(self, T, times_cfg):
        T.add_time(times_cfg, "MON", "08:00", 60, "19:00")
        assert len(times_cfg.time_slot_config.times["MON"]) == 1

    def test_invalid_day_makes_no_change(self, T, times_cfg):
        original_keys = set(times_cfg.time_slot_config.times.keys())
        T.add_time(times_cfg, "SUN", "08:00", 60, "12:00")
        assert set(times_cfg.time_slot_config.times.keys()) == original_keys

    def test_add_to_day_with_no_existing_entry(self, T):
        cfg = MockConfig(times={})
        T.add_time(cfg, "WED", "09:00", 30, "11:00")
        assert "WED" in cfg.time_slot_config.times
        assert len(cfg.time_slot_config.times["WED"]) == 1

    def test_lowercase_day_is_normalised(self, T):
        cfg = MockConfig(times={})
        T.add_time(cfg, "fri", "10:00", 60, "14:00")
        assert "FRI" in cfg.time_slot_config.times


# modify_time


class TestModifyTime:
    def test_range_is_updated(self, T, times_cfg):
        T.modify_time(times_cfg, "MON", 0, "09:00", 30, "15:00")
        updated = times_cfg.time_slot_config.times["MON"][0]
        assert updated == {"start": "09:00", "spacing": 30, "end": "15:00"}

    def test_count_stays_the_same(self, T, times_cfg):
        original_count = len(times_cfg.time_slot_config.times["TUE"])
        T.modify_time(times_cfg, "TUE", 1, "14:00", 45, "18:00")
        assert len(times_cfg.time_slot_config.times["TUE"]) == original_count

    def test_other_ranges_unchanged(self, T, times_cfg):
        original_first = dict(times_cfg.time_slot_config.times["TUE"][0])
        T.modify_time(times_cfg, "TUE", 1, "14:00", 45, "18:00")
        assert times_cfg.time_slot_config.times["TUE"][0] == original_first

    def test_nonexistent_day_makes_no_change(self, T):
        cfg = MockConfig(
            times={"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}
        )
        T.modify_time(cfg, "FRI", 0, "09:00", 30, "11:00")
        # FRI not present — MON should be untouched
        assert cfg.time_slot_config.times["MON"][0]["start"] == "08:00"

    def test_out_of_bounds_index_makes_no_change(self, T, times_cfg):
        original = dict(times_cfg.time_slot_config.times["MON"][0])
        T.modify_time(times_cfg, "MON", 99, "10:00", 30, "12:00")
        assert times_cfg.time_slot_config.times["MON"][0] == original


# delete_time


class TestDeleteTime:
    def test_range_is_removed(self, T, times_cfg):
        T.delete_time(times_cfg, "TUE", 0)
        # TUE originally had 3 ranges
        assert len(times_cfg.time_slot_config.times["TUE"]) == 2

    def test_correct_range_is_removed(self, T, times_cfg):
        # Remove the first TUE range (08:00-12:00); second range should now be at index 0
        T.delete_time(times_cfg, "TUE", 0)
        assert times_cfg.time_slot_config.times["TUE"][0]["start"] == "13:10"

    def test_deleting_only_range_leaves_empty_list(self, T, times_cfg):
        T.delete_time(times_cfg, "MON", 0)
        assert times_cfg.time_slot_config.times["MON"] == []

    def test_nonexistent_day_makes_no_change(self, T):
        cfg = MockConfig(
            times={"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}
        )
        T.delete_time(cfg, "FRI", 0)
        assert len(cfg.time_slot_config.times["MON"]) == 1

    def test_out_of_bounds_index_makes_no_change(self, T, times_cfg):
        original_count = len(times_cfg.time_slot_config.times["MON"])
        T.delete_time(times_cfg, "MON", 99)
        assert len(times_cfg.time_slot_config.times["MON"]) == original_count


#  get_times


class TestGetTimes:
    def test_returns_a_dict(self, T, times_cfg):
        assert isinstance(T.get_times(times_cfg), dict)

    def test_contains_all_days(self, T, times_cfg):
        result = T.get_times(times_cfg)
        assert set(result.keys()) == {"MON", "TUE", "WED", "THU", "FRI"}

    def test_empty_config_returns_empty_dict(self, T):
        cfg = MockConfig(times={})
        assert T.get_times(cfg) == {}

    def test_tue_has_three_ranges(self, T, times_cfg):
        assert len(T.get_times(times_cfg)["TUE"]) == 3

    def test_mon_has_one_range(self, T, times_cfg):
        assert len(T.get_times(times_cfg)["MON"]) == 1


# validate_class_entry — add


class TestValidateClassEntryAdd:
    def test_valid_add_returns_true(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}, {"day": "WED", "duration": 50}]
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=3, meetings=meetings)
            is True
        )

    def test_zero_credits_returns_false(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}]
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=0, meetings=meetings)
            is False
        )

    def test_negative_credits_returns_false(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}]
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=-1, meetings=meetings)
            is False
        )

    def test_none_credits_returns_false(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}]
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=None, meetings=meetings)
            is False
        )

    def test_empty_meetings_returns_false(self, T, classes_cfg):
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=3, meetings=[]) is False
        )

    def test_none_meetings_returns_false(self, T, classes_cfg):
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=3, meetings=None)
            is False
        )

    def test_invalid_day_in_meeting_returns_false(self, T, classes_cfg):
        meetings = [{"day": "SUN", "duration": 50}]
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=3, meetings=meetings)
            is False
        )

    def test_zero_duration_returns_false(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 0}]
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=3, meetings=meetings)
            is False
        )

    def test_negative_duration_returns_false(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": -10}]
        assert (
            T.validate_class_entry(classes_cfg, "add", credits=3, meetings=meetings)
            is False
        )


# validate_class_entry — modify / delete


class TestValidateClassEntryModifyDelete:
    def test_valid_modify_index_returns_true(self, T, classes_cfg):
        assert T.validate_class_entry(classes_cfg, "modify", class_index=0) is True

    def test_valid_delete_index_returns_true(self, T, classes_cfg):
        assert T.validate_class_entry(classes_cfg, "delete", class_index=4) is True

    def test_out_of_bounds_modify_returns_false(self, T, classes_cfg):
        assert T.validate_class_entry(classes_cfg, "modify", class_index=99) is False

    def test_negative_index_returns_false(self, T, classes_cfg):
        assert T.validate_class_entry(classes_cfg, "delete", class_index=-1) is False

    def test_none_index_returns_false(self, T, classes_cfg):
        assert T.validate_class_entry(classes_cfg, "modify", class_index=None) is False

    def test_empty_classes_list_returns_false(self, T):
        cfg = MockConfig(classes=[])
        assert T.validate_class_entry(cfg, "delete", class_index=0) is False


# validate_class_entry — modify / delete


class TestValidateClassEntryNeither:
    def test_invalid_call_to_validate_class_entry(self, T, classes_cfg):
        assert T.validate_class_entry(classes_cfg, "neither", class_index=None) is True


# add_class


class TestAddClass:
    def test_count_increases_by_one(self, T, classes_cfg):
        initial = len(classes_cfg.time_slot_config.classes)
        meetings = [{"day": "MON", "duration": 50}]
        T.add_class(classes_cfg, 3, meetings)
        assert len(classes_cfg.time_slot_config.classes) == initial + 1

    def test_added_class_has_correct_credits(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}]
        T.add_class(classes_cfg, 3, meetings)
        added = classes_cfg.time_slot_config.classes[-1]
        assert added["credits"] == 3

    def test_added_class_has_correct_meetings(self, T, classes_cfg):
        meetings = [{"day": "TUE", "duration": 75}, {"day": "THU", "duration": 75}]
        T.add_class(classes_cfg, 3, meetings)
        added = classes_cfg.time_slot_config.classes[-1]
        assert added["meetings"] == meetings

    def test_start_time_included_when_provided(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 110}]
        T.add_class(classes_cfg, 4, meetings, start_time="16:00")
        added = classes_cfg.time_slot_config.classes[-1]
        assert added["start_time"] == "16:00"

    def test_start_time_omitted_when_none(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}]
        T.add_class(classes_cfg, 3, meetings)
        added = classes_cfg.time_slot_config.classes[-1]
        assert "start_time" not in added

    def test_disabled_flag_included_when_true(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 110}]
        T.add_class(classes_cfg, 4, meetings, disabled=True)
        added = classes_cfg.time_slot_config.classes[-1]
        assert added["disabled"] is True

    def test_disabled_flag_omitted_when_false(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}]
        T.add_class(classes_cfg, 3, meetings, disabled=False)
        added = classes_cfg.time_slot_config.classes[-1]
        assert "disabled" not in added

    def test_add_to_empty_list(self, T):
        cfg = MockConfig(classes=[])
        meetings = [{"day": "WED", "duration": 50}]
        T.add_class(cfg, 3, meetings)
        assert len(cfg.time_slot_config.classes) == 1


# modify_class


class TestModifyClass:
    def test_credits_are_updated(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 60}]
        T.modify_class(classes_cfg, 0, 5, meetings)
        assert classes_cfg.time_slot_config.classes[0]["credits"] == 5

    def test_meetings_are_updated(self, T, classes_cfg):
        new_meetings = [{"day": "TUE", "duration": 90}]
        T.modify_class(classes_cfg, 0, 3, new_meetings)
        assert classes_cfg.time_slot_config.classes[0]["meetings"] == new_meetings

    def test_count_stays_the_same(self, T, classes_cfg):
        initial = len(classes_cfg.time_slot_config.classes)
        meetings = [{"day": "MON", "duration": 50}]
        T.modify_class(classes_cfg, 0, 3, meetings)
        assert len(classes_cfg.time_slot_config.classes) == initial

    def test_start_time_added_when_provided(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 110}]
        T.modify_class(classes_cfg, 0, 4, meetings, start_time="17:00")
        assert classes_cfg.time_slot_config.classes[0]["start_time"] == "17:00"

    def test_start_time_omitted_when_none(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 50}]
        T.modify_class(classes_cfg, 0, 3, meetings, start_time=None)
        assert "start_time" not in classes_cfg.time_slot_config.classes[0]

    def test_disabled_flag_set_when_true(self, T, classes_cfg):
        meetings = [{"day": "MON", "duration": 110}]
        T.modify_class(classes_cfg, 0, 4, meetings, disabled=True)
        assert classes_cfg.time_slot_config.classes[0]["disabled"] is True

    def test_other_entries_unchanged(self, T, classes_cfg):
        original_second = dict(classes_cfg.time_slot_config.classes[1])
        meetings = [{"day": "MON", "duration": 50}]
        T.modify_class(classes_cfg, 0, 3, meetings)
        assert classes_cfg.time_slot_config.classes[1] == original_second

    def test_out_of_bounds_index_makes_no_change(self, T, classes_cfg):
        original = list(classes_cfg.time_slot_config.classes)
        meetings = [{"day": "MON", "duration": 50}]
        T.modify_class(classes_cfg, 99, 3, meetings)
        assert classes_cfg.time_slot_config.classes == original


# delete_class


class TestDeleteClass:
    def test_count_decreases_by_one(self, T, classes_cfg):
        initial = len(classes_cfg.time_slot_config.classes)
        T.delete_class(classes_cfg, 0)
        assert len(classes_cfg.time_slot_config.classes) == initial - 1

    def test_correct_entry_is_removed(self, T, classes_cfg):
        # Remove index 0 (the 3-credit MWF pattern); index 0 should now be the TuTh 3-credit
        T.delete_class(classes_cfg, 0)
        first = classes_cfg.time_slot_config.classes[0]
        assert first["meetings"][0]["day"] == "TUE"

    def test_deleting_last_entry_leaves_empty_list(self, T):
        cfg = MockConfig(
            classes=[{"credits": 3, "meetings": [{"day": "MON", "duration": 50}]}]
        )
        T.delete_class(cfg, 0)
        assert cfg.time_slot_config.classes == []

    def test_out_of_bounds_index_makes_no_change(self, T, classes_cfg):
        initial = len(classes_cfg.time_slot_config.classes)
        T.delete_class(classes_cfg, 99)
        assert len(classes_cfg.time_slot_config.classes) == initial

    def test_negative_index_makes_no_change(self, T, classes_cfg):
        initial = len(classes_cfg.time_slot_config.classes)
        T.delete_class(classes_cfg, -1)
        assert len(classes_cfg.time_slot_config.classes) == initial


# get_classes


class TestGetClasses:
    def test_returns_a_list(self, T, classes_cfg):
        assert isinstance(T.get_classes(classes_cfg), list)

    def test_length_matches_config(self, T, classes_cfg):
        assert len(T.get_classes(classes_cfg)) == 5

    def test_empty_config_returns_empty_list(self, T):
        cfg = MockConfig(classes=[])
        assert T.get_classes(cfg) == []

    def test_first_entry_has_credits_key(self, T, classes_cfg):
        assert "credits" in T.get_classes(classes_cfg)[0]

    def test_first_entry_has_meetings_key(self, T, classes_cfg):
        assert "meetings" in T.get_classes(classes_cfg)[0]

    def test_disabled_entry_has_disabled_key(self, T, classes_cfg):
        # Index 4 is the disabled entry
        assert T.get_classes(classes_cfg)[4].get("disabled") is True

    def test_start_time_entry_has_start_time_key(self, T, classes_cfg):
        # Index 2 has start_time
        assert T.get_classes(classes_cfg)[2].get("start_time") == "16:00"


# Integration: add then delete, modify then get


class TestTimeIntegration:
    def test_add_then_delete_restores_count(self, T, times_cfg):
        original_count = len(times_cfg.time_slot_config.times["MON"])
        T.add_time(times_cfg, "MON", "20:00", 30, "22:00")
        T.delete_time(times_cfg, "MON", original_count)  # remove the just-added one
        assert len(times_cfg.time_slot_config.times["MON"]) == original_count

    def test_modify_then_get_reflects_change(self, T, times_cfg):
        T.modify_time(times_cfg, "FRI", 0, "10:00", 45, "16:00")
        result = T.get_times(times_cfg)["FRI"][0]
        assert result == {"start": "10:00", "spacing": 45, "end": "16:00"}


class TestClassIntegration:
    def test_add_then_delete_restores_count(self, T, classes_cfg):
        initial = len(classes_cfg.time_slot_config.classes)
        meetings = [{"day": "FRI", "duration": 50}]
        T.add_class(classes_cfg, 1, meetings)
        T.delete_class(classes_cfg, initial)  # remove the just-added one
        assert len(classes_cfg.time_slot_config.classes) == initial

    def test_modify_then_get_reflects_change(self, T, classes_cfg):
        new_meetings = [{"day": "WED", "duration": 100}]
        T.modify_class(classes_cfg, 1, 2, new_meetings)
        result = T.get_classes(classes_cfg)[1]
        assert result["credits"] == 2
        assert result["meetings"] == new_meetings
