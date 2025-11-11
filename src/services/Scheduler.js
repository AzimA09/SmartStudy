# scheduler.py
from datetime import datetime, timedelta
from class_schedule import get_class_work_schedule  # Import Story 1's real implementation

class Event:
    def __init__(self, title, start, end, priority=1):
        self.title = title
        self.start = start  # datetime object
        self.end = end      # datetime object
        self.priority = priority  # higher number = higher priority

    def conflicts_with(self, other):
        """Check if two events overlap"""
        return self.start < other.end and other.start < self.end

class StudyPlan:
    def __init__(self):
        self.events = []  # list of Event objects

    def add_event(self, event):
        """Add event and adjust plan if needed"""
        self.events.append(event)
        self.adjust_conflicts()

    def adjust_conflicts(self):
        """Automatically adjust events to prevent overlaps"""
        self.events.sort(key=lambda e: e.start)
        for i in range(len(self.events)-1):
            current = self.events[i]
            next_event = self.events[i+1]
            if current.conflicts_with(next_event):
                duration = next_event.end - next_event.start
                next_event.start = current.end + timedelta(minutes=5)
                next_event.end = next_event.start + duration

    def show_schedule(self):
        """Print the current study plan"""
        for event in self.events:
            print(f"{event.title}: {event.start.strftime('%Y-%m-%d %H:%M')} - {event.end.strftime('%Y-%m-%d %H:%M')}")

# -------------------------
# Test Story 2
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
