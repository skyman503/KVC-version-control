def hash_name(config, time):
    import hashlib
    return hashlib.sha224(str(time).encode()).hexdigest()


def get_file_name(path, name):
    from .datetime_helper import get_modification_date
    time = get_modification_date(path)
    new_name = str(name) + ' - ' + str(time)
    return new_name, time
