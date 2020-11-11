def hash_name(config, time):
    import hashlib
    return hashlib.sha224(str(time).encode()).hexdigest()


def get_file_name(path, name):
    from .datetime_helper import get_modification_date
    time = get_modification_date(path)
    new_name = str(name) + ' - ' + str(time)
    return new_name, time


def set_file_name(path, new_name):
    from os import rename
    path_list = path.split('\\')
    path_list[-1] = new_name
    new_path = path_list[0]
    for x in range(1, len(path_list)):
        new_path = new_path + '\\' + path_list[x]
    rename(path, new_path)
    return new_path
