def set_reminder(event, time):
    with open("data/reminders.txt", "a") as file:
        file.write(f"{event} at {time}\n")
    return f"Reminder set for {event} at {time}"
