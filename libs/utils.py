import utime

def format_time():
    year, month, day, hour, minute, second, _, _ = utime.localtime()
    # California PDT
    hour = (hour - 7) % 24
    suffix = "AM"
    if hour >= 12:
        suffix = "PM"

    display_hour = hour % 12

    if display_hour == 0:
        display_hour = 12

    return "{}-{:02d}-{:02d} {}:{:02d} {}".format(
        year,
        month,
        day,
        display_hour,
        minute,
        suffix
    )


