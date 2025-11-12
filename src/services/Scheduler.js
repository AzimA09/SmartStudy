# scheduler.py
from datetime import datetime, timedelta
from typing import List, Dict, Any
from class_schedule import get_class_work_schedule  # Import Story 1's real implementation

class Event:
    def __init__(self, title: str, start: datetime, end: datetime, priority: int = 1, event_type: str = "study"):
        self.title = title
        self.start = start  # datetime object
        self.end = end      # datetime object
        self.priority = priority  # higher number = higher priority
        self.type = event_type    # "class", "work", "study"
        self.conflicts = False    # Story 3 flag
        self.conflict_info: str | None = None 

    def conflicts_with(self, other: "Event") -> bool:
        """Return True if two events overlap in time"""
        return self.start < other.end and other.start < self.end

    def __repr__(self) -> str:
        status = " (CONFLICT!)" if self.conflicts else ""
        return ( f"{self.type.upper()} {self.title}: "
                f"{self.start.strftime('%Y-%m-%d %H:%M')} - "
                f"{self.end.strftime('%H:%M')}{status}")

class StudyPlan:
    """Manages all scheduled events and detects or resolves conflicts."""
    def __init__(self):
        self.events: List[Event] = []  # list of Event objects

    def add_event(self, event: Event) -> List[Dict[str, Any]]:
        """Add event and adjust plan if needed, Returns a list of conflict reports (empty if none)."""
        self.events.append(event)
        return self._resolve_conflicts()

    def _resolve_conflicts(self) -> List[Dict[str, Any]]:
        """Detect and resolve event overlaps by shifting lower-priority events."""
        self.events.sort(key=lambda e: (e.start, -e.priority))
        conflict_reports: List[Dict[str, Any]] = []
        for i in range(len(self.events)-1):
            current = self.events[i]
            next_event = self.events[i+1]
            if not current.conflicts_with(next_event):
                continue
            next_event.conflicts = True
            old_start = next_event.start
            duration = next_event.end - next_event.start
            buffer = timedelta(minutes=5)
            if next_event.priority <= current.priority:
                """ Shift the lower-priority event after the current one. """
                shift = current.end - next_event.start + buffer
                next_event.start += shift
                next_event.end += shift
            else:
                shift = next_event.end - current.start + buffer
                current.start += shift
                current.end += shift
            msg = (
                f"'{next_event.title}' overlapped with '{current.title}'. "
                f"Shifted from {old_start.strftime('%H:%M')} to {next_event.start.strftime('%H:%M')}."
            )
            next_event.conflict_info = msg
            conflict_reports.append({
                "event": next_event.title,
                "conflicts_with": current.title,
                "original_start": old_start,
                "new_start": next_event.start,
                "message": msg
            })
        return conflict_reports

    def refresh_study_plan(self, updated_event: Event) -> None:
        print(f"\n[Dynamic Update Triggered] '{updated_event.title}' has been updated. Refreshing study plan...\n")

        """Remove old version of the event"""
        self.events = [e for e in self.events if e.title != updated_event.title]

        """Add updated event and re-sort"""
        self.events.append(updated_event)
        self.events.sort(key=lambda e: (e.start, -e.priority))

        """Re-run conflict resolution"""
        self._resolve_conflicts()

        """Confirmation message"""
        print(f"Study plan successfully refreshed for '{updated_event.title}'\n")

    def show_schedule(self) -> None:
        """Print the current study plan"""
        print("\n=== SmartStudy Schedule ===")
        for e in self.events:
            print(e)
        print("=" * 40)

# -------------------------
# Test Story 2 & 3 & 4
# -------------------------
if __name__ == "__main__":
    plan = StudyPlan()

    # Get class/work schedule from Story 1
    initial_events = get_class_work_schedule()  # Story 1’s function provides real events
    for event in initial_events:
        plan.add_event(event)

    # Add a new study session
    study_event = Event(
        title="Study Chemistry",
        start=datetime(2025, 11, 10, 9, 30),
        end=datetime(2025, 11, 10, 11, 0)
    )
    plan.add_event(study_event)

    plan.show_schedule()

    print("\n--- Updating 'Study Chemistry' event time ---")

    updated_event = Event(
        title="Study Chemistry",
        start=datetime(2025, 11, 10, 10, 30),  # new start time
        end=datetime(2025, 11, 10, 12, 0),     # new end time
        event_type="study"
    )

    plan.refresh_study_plan(updated_event)
    plan.show_schedule()

