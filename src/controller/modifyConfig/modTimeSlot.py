from controller.modifyConfig.utilsCLI import prompt, endProg
import re

def modTimeSlot(sched):
    try:
        print("Re-enter full Time Slot Configuration")
        print("Press r and enter at any time to return.\n")

        TIME_RE = re.compile(r"^\d{2}:\d{2}$")

        def to_minutes(t):
            h, m = map(int, t.split(":"))
            return h * 60 + m

        # ---------- TIMES ----------
        times = {}

        for day in ["MON", "TUE", "WED", "THU", "FRI"]:
            blocks = []
            print(f"\nConfiguring time blocks for {day}")

            while True:
                start = prompt("Start time (HH:MM) or 'd'\n==> ")
                if start == "d":
                    break

                if not TIME_RE.match(start):
                    print("Invalid time format. Use HH:MM.")
                    continue

                end = prompt("End time (HH:MM)\n==> ")
                if not TIME_RE.match(end):
                    print("Invalid time format. Use HH:MM.")
                    continue

                start_min = to_minutes(start)
                end_min = to_minutes(end)

                if end_min <= start_min:
                    print("End time must be after start time.")
                    continue

                try:
                    spacing = int(prompt("Spacing (minutes)\n==> "))
                    if spacing <= 0:
                        raise ValueError
                except ValueError:
                    print("Spacing must be a positive integer.")
                    continue

                # overlap check
                overlap = False
                for blk in blocks:
                    blk_start = to_minutes(blk["start"])
                    blk_end = to_minutes(blk["end"])
                    if not (end_min <= blk_start or start_min >= blk_end):
                        overlap = True
                        break

                if overlap:
                    print("Time block overlaps an existing block for this day.")
                    continue

                block = {
                    "start": start,
                    "spacing": spacing,
                    "end": end
                }

                blocks.append(block)
                print(f"Current {day} blocks: {blocks}")

            times[day] = blocks

        # ---------- CLASS PATTERNS ----------
        classes = []
        print("\nConfiguring class meeting patterns")

        while True:
            credits = prompt("Enter class credits or 'd'\n==> ")
            if credits == "d":
                break

            try:
                credits = int(credits)
                if credits <= 0:
                    raise ValueError
            except ValueError:
                print("Credits must be a positive integer.")
                continue

            meetings = []

            while True:
                day = prompt("Meeting day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
                if day == "d":
                    break

                if day not in {"MON", "TUE", "WED", "THU", "FRI"}:
                    print("Invalid day.")
                    continue

                try:
                    duration = int(prompt("Duration (minutes)\n==> "))
                    if duration <= 0:
                        raise ValueError
                except ValueError:
                    print("Duration must be a positive integer.")
                    continue

                lab = prompt("Is this a lab? (y/n)\n==> ").lower()
                if lab not in {"y", "n"}:
                    print("Enter 'y' or 'n'.")
                    continue

                meeting = {
                    "day": day,
                    "duration": duration
                }
                if lab == "y":
                    meeting["lab"] = True

                meetings.append(meeting)
                print(f"Current meetings: {meetings}")

            entry = {
                "credits": credits,
                "meetings": meetings
            }

            start_time = prompt("Fixed start time (HH:MM) or 'd'\n==> ")
            if start_time != "d":
                if not TIME_RE.match(start_time):
                    print("Invalid start time format. Skipping fixed start time.")
                else:
                    entry["start_time"] = start_time

            disabled = prompt("Disable this pattern? (y/n)\n==> ").lower()
            if disabled == "y":
                entry["disabled"] = True

            classes.append(entry)
            print(f"Current class patterns: {classes}")

        # ---------- ASSIGN ----------
        sched.config.time_slot_config = {
            "times": times,
            "classes": classes
        }

        print("\nTime slot configuration updated.")

    except KeyboardInterrupt:
        print("\nReturning without modifying time slot configuration.")
        return
