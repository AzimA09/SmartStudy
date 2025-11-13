from datetime import datetime

def get_class_work_schedule():
    schedule = []

    print("---- Add classes or your work schedule ----")

    while True:
        from Scheduler import Event

        # prompt the user for event details
        title = input("Enter event name (ex: 'Math Class' or 'Work Shift'): ").strip()

        # class_schedule is only responsible for adding class or work events, study sessions can be planned elsewhere
        event_type = input("Enter event type (ex: 'class' or 'work'): ").strip().lower()

        # getting the date and times
        date_str = input("Enter date of event (YYYY-MM-DD): ").strip()
        start_str = input("Enter start time (HH:MM, 24-hour format): ").strip()
        end_str = input("Enter end time (HH:MM, 24-hour format): ").strip()

        try:
            start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
            end = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date/time format, please try again.\n")
            continue

        # assigning default priority based on event type
        priority = 3 if event_type == "class" else 2

        # create the Event object using Scheduler's formatting
        event = Event(
            title=title,
            start=start,
            end=end,
            priority=priority,
            event_type=event_type
        )

        # add to the list of Events
        schedule.append(event)
        print(f"Added {event_type} '{title}' from {start_str} to {end_str}.\n")

        # reprompt if the user has more events
        addMore = input("Add another event? (y/n): ").strip().lower()
        if addMore != "y":
            break

    return schedule