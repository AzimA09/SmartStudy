import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from scheduler import Event, StudyPlan
from class_schedule import get_class_work_schedule

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



"""
test_scheduler.py
Author: Azim Ahmed
Teammate Code Under Test: Nya McCowan

Test cases for Story 3: Detect Schedule Conflicts
1. Basic overlap detection
2. Priority-based shifting
3. Multi-event conflict chain
"""

class TestSchedulerConflicts(unittest.TestCase):

    @patch("scheduler.Event")
    def test_basic_overlap(self, mock_event):
        """
        Test Case 1:
        Ensures the scheduler correctly detects a basic overlap and flags the conflict.
        """
        plan = StudyPlan()

        # Mock event objects
        event_a = MagicMock()
        event_b = MagicMock()

        # Define start/end times for conflict simulation
        event_a.start = datetime(2025, 11, 12, 10, 0)
        event_a.end   = datetime(2025, 11, 12, 11, 0)
        event_b.start = datetime(2025, 11, 12, 10, 30)
        event_b.end   = datetime(2025, 11, 12, 11, 30)

        event_a.priority = 3
        event_b.priority = 1

        # conflict_with logic determines overlap
        event_a.conflicts_with.return_value = True
        event_b.conflicts_with.return_value = True

        mock_event.side_effect = [event_a, event_b]

        plan.add_event(event_a)
        conflicts = plan.add_event(event_b)

        self.assertEqual(len(conflicts), 1)
        self.assertTrue(event_b.conflicts)

    @patch("scheduler.Event")
    def test_priority_shifting(self, mock_event):
        """
        Test Case 2:
        Lower-priority event should shift after the higher-priority event + 5-minute buffer.
        """
        plan = StudyPlan()

        high = MagicMock()
        low = MagicMock()

        high.start = datetime(2025, 11, 15, 12, 0)
        high.end   = datetime(2025, 11, 15, 14, 0)
        high.priority = 2

        low.start = datetime(2025, 11, 15, 13, 0)
        low.end   = datetime(2025, 11, 15, 14, 0)
        low.priority = 1

        # Simulated overlap
        high.conflicts_with.return_value = True
        low.conflicts_with.return_value = True

        mock_event.side_effect = [high, low]

        plan.add_event(high)
        plan.add_event(low)

        expected_new_start = high.end + timedelta(minutes=5)
        self.assertEqual(low.start, expected_new_start)
        self.assertTrue(low.conflicts)

    @patch("scheduler.Event")
    def test_conflict_chain(self, mock_event):
        """
        Test Case 3:
        Ensures multiple overlapping study events shift one after another
        (chain reaction conflict).
        """
        plan = StudyPlan()

        a = MagicMock()
        b = MagicMock()
        c = MagicMock()

        # Original times
        a.start = datetime(2025, 11, 20, 9, 0)
        a.end   = datetime(2025, 11, 20, 10, 0)
        a.priority = 3

        b.start = datetime(2025, 11, 20, 9, 30)
        b.end   = datetime(2025, 11, 20, 10, 30)
        b.priority = 1

        c.start = datetime(2025, 11, 20, 10, 15)
        c.end   = datetime(2025, 11, 20, 11, 0)
        c.priority = 1

        # Simulate all overlap relationships
        a.conflicts_with.return_value = True
        b.conflicts_with.return_value = True
        c.conflicts_with.return_value = True

        mock_event.side_effect = [a, b, c]

        plan.add_event(a)
        plan.add_event(b)
        plan.add_event(c)

        # Event B shifts after Event A + 5 minutes
        expected_b_start = a.end + timedelta(minutes=5)

        # Event C shifts after B finishes + 5 minutes
        b_duration = b.end - b.start
        expected_c_start = expected_b_start + b_duration + timedelta(minutes=5)

        self.assertEqual(b.start, expected_b_start)
        self.assertEqual(c.start, expected_c_start)
        self.assertTrue(b.conflicts)
        self.assertTrue(c.conflicts)
"""
test_studyplan_refresh.py
Author: Samantha Reilly
Teammate Code Under Test: Azim Ahmed

Test cases for Story 4: Dynamic Refresh of Study Plan
1. Updating an event replaces the old instance
2. Updating an event resorts the schedule
3. Updating an event triggers conflict resolution
"""
class TestStudyPlanRefresh(unittest.TestCase):

    @patch("scheduler.Event")
    def test_replace_old_event(self, mock_event):
        """
        Test Case 1:
        Updating an existing event should remove the old
        instance and insert the updated version.
        """
        plan = StudyPlan()

        old = MagicMock()
        updated = MagicMock()

        old.title = "Study Chemistry"
        updated.title = "Study Chemistry"

        plan.add_event(old)

        plan.refresh_study_plan(updated)

        # Only updated event should remain
        self.assertEqual(len(plan.events), 1)
        self.assertIs(plan.events[0], updated)

    @patch("scheduler.Event")
    def test_resort_after_update(self, mock_event):
        """
        Test Case 2:
        Updating an event should trigger re-sorting of the study plan.
        """
        plan = StudyPlan()

        e1 = MagicMock()
        e2 = MagicMock()
        updated = MagicMock()

        e1.title = "Math Study"
        e2.title = "Study Chemistry"
        updated.title = "Study Chemistry"

        # Original ordering
        e1.start = datetime(2025, 11, 10, 8, 0)
        e2.start = datetime(2025, 11, 10, 9, 0)

        # Updated event moves earlier
        updated.start = datetime(2025, 11, 10, 7, 30)

        plan.add_event(e1)
        plan.add_event(e2)

        plan.refresh_study_plan(updated)

        self.assertEqual(plan.events[0], updated)
        self.assertEqual(plan.events[1], e1)

    @patch("scheduler.Event")
    def test_conflict_resolution_after_update(self, mock_event):
        """
        Test Case 3:
        Updating an event should retrigger the conflict resolver
        and shift overlapping lower-priority events.
        """
        plan = StudyPlan()

        a = MagicMock()
        b = MagicMock()
        updated = MagicMock()

        # Event A (higher priority)
        a.title = "Event A"
        a.priority = 3
        a.start = datetime(2025, 12, 1, 9, 0)
        a.end   = datetime(2025, 12, 1, 10, 0)

        # Original B (lower priority)
        b.title = "Study Chemistry"
        b.priority = 1
        b.start = datetime(2025, 12, 1, 10, 15)
        b.end   = datetime(2025, 12, 1, 11, 0)

        # Updated B overlaps A
        updated.title = "Study Chemistry"
        updated.priority = 1
        updated.start = datetime(2025, 12, 1, 9, 30)
        updated.end   = datetime(2025, 12, 1, 11, 0)

        # Simulate overlap logic
        a.conflicts_with.return_value = True
        updated.conflicts_with.return_value = True

        plan.add_event(a)
        plan.add_event(b)

        plan.refresh_study_plan(updated)

        expected_start = a.end + timedelta(minutes=5)

        self.assertEqual(updated.start, expected_start)
        self.assertTrue(updated.conflicts)

# -----------------------------
# Run All Tests
# -----------------------------
if __name__ == "__main__":
    unittest.main()
