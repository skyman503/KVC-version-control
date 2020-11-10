import datetime


def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_modification_date(path):
    import os
    import platform
    if platform.system() == 'Windows':
        return os.path.getmtime(path)
    else:
        stat = os.stat(path)
        return stat.st_mtime
