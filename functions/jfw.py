def timeDuration(start, end):
    duration = end - start
    days, duration = divmod(duration, 86400)
    hours, duration = divmod(duration, 3600)
    minutes, seconds = divmod(duration, 60)
    return int(days), int(hours), int(minutes), int(seconds)