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
        # Insert event
        self.events.append(event)
        # Adjust conflicting events
        self.adjust_conflicts()

    def adjust_conflicts(self):
        """Automatically adjust events to prevent overlaps"""
        # Sort by start time
        self.events.sort(key=lambda e: e.start)
        for i in range(len(self.events)-1):
            current = self.events[i]
            next_event = self.events[i+1]
            if current.conflicts_with(next_event):
                # Move the next event to the first available slot after current event
                duration = next_event.end - next_event.start
                next_event.start = current.end + timedelta(minutes=5)  # 5 min buffer
                next_event.end = next_event.start + duration

    def show_schedule(self):
        """Print the current study plan"""
        for event in self.events:
            print(f"{event.title}: {event.start.strftime('%Y-%m-%d %H:%M')} - {event.end.strftime('%Y-%m-%d %H:%M')}")

# Example Usage
if __name__ == "__main__":
    plan = StudyPlan()

    # Existing class/work schedule (would come from Story 1)
    plan.add_event(Event("Math Class", datetime(2025,11,10,9,0), datetime(2025,11,10,10,0)))
    plan.add_event(Event("Work Shift", datetime(2025,11,10,10,30), datetime(2025,11,10,13,0)))

    # New study session that conflicts with class
    plan.add_event(Event("Study Chemistry", datetime(2025,11,10,9,30), datetime(2025,11,10,11,0)))

    plan.show_schedule()
