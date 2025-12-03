"""
test_scheduler.py
Test cases 1, 2, and 3.
- Event creation (1)
- Auto-adjustment of overlapping events (2)
- Conflict flagging and messages (3)
"""

from scheduler import Event, StudyPlan
from datetime import datetime


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


# -----------------------------
# Run All Tests
# -----------------------------
if __name__ == "__main__":
    print("Running SmartStudy test suite...\n")

    test_event_creation()
    test_auto_adjustment()
    test_conflict_tracking()

    print("\nAll tests passed successfully!")
