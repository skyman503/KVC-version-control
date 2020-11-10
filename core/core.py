def update_logs(file, message):
    from .helpers.datetime_helper import get_current_datetime
    dt = get_current_datetime()
    l_message = '[ ' + dt + ' ]   ' + str(message)
    l_file = open(file, mode='a')
    l_file.write(l_message)
    return 1


def repo_init(config, current_path):
    import os
    from .helpers import database
    permission_to_make = True  # True if there is no kvc repository in working directory
    for root, directories, files in os.walk(os.path.abspath(current_path)):
        for directory in directories:
            if directory in config["local_repo_settings"]["name"]:
                print('\n', config["messages"]["error"]["existing_repository_in_current_directory"])
                permission_to_make = False
                break
    if permission_to_make:  # creating kvc files
        try:
            os.mkdir(config["local_repo_settings"]["name"][0])
        except (OSError, FileExistsError):
            print(config["messages"]["error"]["console_message"])
        else:
            try:
                temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
                os.mkdir((temp_path + config["local_repo_settings"]["sub_dir_names"]["archive"]))
                os.mkdir((temp_path + config["local_repo_settings"]["sub_dir_names"]["logs"]))
                os.mkdir((temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"]))
            except (OSError, FileExistsError):
                print('\n', config["messages"]["error"]["creating_directory"])
            else:
                logs_file = open((temp_path + config["local_repo_settings"]["sub_dir_names"]["logs"]+'\\'+'logs.txt'),
                                 mode='a')
                logs_file.close()
                database.create_default_db(config, current_path, str(os.getlogin()))

                update_logs(temp_path + config["local_repo_settings"]["sub_dir_names"]["logs"]+'\\'+'logs.txt',
                            config["messages"]["success"]["repository_created_successfully"])
    return None


def commit(config, ignore_config, head_config, current_path, message):
    from .helpers.files_structure import get_files_tree
    from os import getlogin
    from .helpers.database import create_commit, create_commit_db, check_if_file_in_db, add_file_db
    import sqlite3

    files_tree = get_files_tree(ignore_config, current_path)
    temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
    conn = sqlite3.connect(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'tree.db')
    commit_structure = []
    for file in files_tree:
        print(file)

    for file in files_tree:
        if file[3] == 'f':
            file_id = check_if_file_in_db(config, file[1], file[5], file[4], file[3], conn)
            if file_id == -1:
                file_id = add_file_db(config, conn, file)
        else:
            file_id = check_if_file_in_db(config, file[1], '', '', '', conn)
            if file_id == -1:
                file_id = add_file_db(config, conn, file)
        new_file = file.copy()
        new_file[0] = file_id
        temp_structure_path = new_file[2].split('\\')
        if len(temp_structure_path) > 1:
            temp_structure_path[-1] = file_id
            temp_structure_path_s = ''
            new_file[2] = temp_structure_path_s.join(temp_structure_path)
        else:
            new_file[2] = file_id
        commit_structure.append(new_file)
    print('---------------------------------------')
    for file in commit_structure:
        #print(file)
        pass

    branch_id = head_config["branch_id"]
    new_commit = create_commit(config, branch_id, getlogin(), message, files_tree)
    #print(new_commit)
    create_commit_db(conn, new_commit, config)
    return None