"""
test_scheduler.py
Test cases 1, 2, and 3.
- Event creation (1)
- Auto-adjustment of overlapping events (2)
- Conflict flagging and messages (3)
"""

import unittest
from unittest.mock import patch, MagicMock
from scheduler import Event, StudyPlan
from datetime import datetime
from class_schedule import get_class_work_schedule


# -----------------------------
# Test Case 1: Event Creation
# -----------------------------
def test_event_creation():
    """
    Tests that program correctly creates Event objects with proper fields.
    """

    test_event = Event(
        title="Math Class",
        start=datetime(2025, 11, 9, 10, 0),
        end=datetime(2025, 11, 9, 11, 15),
        priority=3,
        event_type="class"
    )

    assert test_event.title == "Math Class"
    assert test_event.type == "class"
    assert test_event.priority == 3
    assert test_event.start == datetime(2025, 11, 9, 10, 0)
    assert test_event.end == datetime(2025, 11, 9, 11, 15)

    print("Test Case 1 Passed: Event creation validated.")


# -----------------------------
# Test Case 2: Auto-adjustment Logic
# -----------------------------
def test_auto_adjustment():
    """
    Tests that lower-priority events get moved to avoid conflicts.
    """

    plan = StudyPlan()

    event_a = Event(
        title="Physics Class",
        start=datetime(2025, 11, 10, 9, 0),
        end=datetime(2025, 11, 10, 10, 0),
        priority=3,
        event_type="class"
    )

    event_b = Event(
        title="Study Session",
        start=datetime(2025, 11, 10, 9, 30),
        end=datetime(2025, 11, 10, 10, 30),
        priority=1,
        event_type="study"
    )

    plan.add_event(event_a)
    conflicts = plan.add_event(event_b)

    expected_start = datetime(2025, 11, 10, 10, 5)
    expected_end = datetime(2025, 11, 10, 11, 5)

    assert event_b.start == expected_start
    assert event_b.end == expected_end
    assert len(conflicts) == 1

    print("Test Case 2 Passed: Auto-adjustment moved event correctly.")


# -----------------------------
# Test Case 3: Conflict Tracking
# -----------------------------
def test_conflict_tracking():
    """
    Tests that overlapping events are flagged and conflict messages are created.
    """

    plan = StudyPlan()

    work_event = Event(
        title="Work Shift",
        start=datetime(2025, 11, 12, 13, 0),
        end=datetime(2025, 11, 12, 15, 0),
        priority=2,
        event_type="work"
    )

    gym_event = Event(
        title="Gym Session",
        start=datetime(2025, 11, 12, 14, 0),
        end=datetime(2025, 11, 12, 15, 0),
        priority=1,
        event_type="study"
    )

    plan.add_event(work_event)
    conflicts = plan.add_event(gym_event)

    assert gym_event.conflicts is True
    assert gym_event.conflict_info is not None
    assert len(conflicts) == 1

    print("Test Case 3 Passed: Conflict tracking validated.")

"""
test_class_schedule.py
Author: Nya McCowan
Teammates Code: Maija Hirata

Test cases for get_class_work_schedule():
1. Adding a single class event
2. Adding a single work event
3. Adding two events consecutively
"""
class TestClassSchedule(unittest.Testcase):

    @patch("class_schedule.Event")
    @patch("builtins.input")
    def test_add_one_class_event(self, mock_input, mock_event):
        """
        Test adding exactly one CLASS event.
        """
        mock_input.side_effect = ["Math Class", "class", "2025-02-10", "09:00", "10:15", "n"] 
        mock_event.return_value = MagicMock()
        schedule = get_class_work_schedule()
        self.assertEqual(len(schedule), 1)
        mock_event.assert_called_with(title = "Math Class", start=datetime(2025, 2, 10, 9, 0), end=datetime(2025, 2, 10, 10, 15), priority=3, event_type="class")

    @patch("class_schedule.Event")
    @patch("builtins.input")
    def test_add_one_work_event(self, mock_input, mock_event):
        """
        Test adding exactly one WORK event.
        """
        mock_input.side_effect = ["Work Shift", "work", "2025-03-01", "14:00", "18:00", "n"] 
        mock_event.return_value = MagicMock()
        schedule = get_class_work_schedule()
        self.assertEqual(len(schedule), 1)
        mock_event.assert_called_with(title = "Work Shift", start=datetime(2025, 3, 1, 14, 0), end=datetime(2025, 3, 1, 18, 0), priority=2, event_type="work")

    @patch("class_schedule.Event")
    @patch("builtins.input")
    def test_add_two_events(self, mock_input, mock_event):
        """
        Test that two events can be added consecutively.
        """
        mock_input.side_effect = ["Chemistry Class", "class", "2025-01-15", "08:00", "09:15", "y", "Morning Shift", "work", "2025-01-15", "10:00", "12:00", "n"] 
        mock_event.side_effect = [MagicMock(), MagicMock()]
        schedule = get_class_work_schedule()
        self.assertEqual(len(schedule), 2)
        self.assertEqual(mock_event.call_count, 2)
        mock_event.assert_any_call(title = "Chemistry Class", start=datetime(2025, 1, 15, 8, 0), end=datetime(2025, 1, 15, 9, 15), priority=3, event_type="class")
        mock_event.assert_any_call(title = "Morning Shift", start=datetime(2025, 1, 15, 10, 0), end=datetime(2025, 1, 15, 12, 0), priority=2, event_type="work")

# -----------------------------
# Run All Tests
# -----------------------------
if __name__ == "__main__":
    unittest.main()
