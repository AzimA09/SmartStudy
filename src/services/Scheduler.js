# scheduler.py
from datetime import datetime, timedelta

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
        # Sort events by start time
        self.events.sort(key=lambda e: e.start)
        for i in range(len(self.events)-1):
            current = self.events[i]
            next_event = self.events[i+1]
            if current.conflicts_with(next_event):
                # Move the next event to the first available slot after current
                duration = next_event.end - next_event.start
                next_event.start = current.end + timedelta(minutes=5)  # 5 min buffer
                next_event.end = next_event.start + duration

    def show_schedule(self):
        """Print the current study plan"""
        for event in self.events:
            print(f"{event.title}: {event.start.strftime('%Y-%m-%d %H:%M')} - {event.end.strftime('%Y-%m-%d %H:%M')}")

# Function for Story 1 integration
def get_class_work_schedule():
    """
    This function will be implemented in Story 1.
    For now, it just returns an empty list.
    """
    return []

# Test Story 2
if __name__ == "__main__":
    plan = StudyPlan()

    # Get class/work schedule from Story 1 (currently empty)
    initial_events = get_class_work_schedule()
    for event in initial_events:
        plan.add_event(event)

    # Example: adding a study session
    study_event = Event(
        title="Study Chemistry",
        start=datetime(2025, 11, 10, 9, 30),
        end=datetime(2025, 11, 10, 11, 0)
    )
    plan.add_event(study_event)

    plan.show_schedule()
