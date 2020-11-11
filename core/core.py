def update_logs(file, message):
    from .helpers.datetime_helper import get_current_datetime
    dt = get_current_datetime()
    l_message = '[ ' + dt + ' ]   ' + str(message)
    l_file = open(file, mode='a')
    l_file.write(l_message)
    return 1


def head_update(config, current_path, new_branch, new_commit):
    from json import load, dump
    temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
    with open(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'head.json', mode='r') \
            as head_file:
        head_data = load(head_file)
    if new_branch != '':
        head_data["branch_id"] = new_branch
    if new_commit != '':
        head_data["current_commit"] = new_commit
    with open(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'head.json', mode='w') \
            as head_file:
        dump(head_data, head_file)
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
                os.mkdir((temp_path + config["local_repo_settings"]["sub_dir_names"]["temp"]))

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


def commit(config, ignore_config, current_path, message):
    from .helpers.files_structure import get_files_tree
    from os import getlogin
    from json import load
    from .helpers.database import create_commit, create_commit_db, check_if_file_in_db, add_file_db, get_commit_by_id, get_commit_by_name
    import sqlite3

    files_tree = get_files_tree(ignore_config, current_path)
    temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
    with open(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'head.json', mode='r') \
            as head_config_file:
        head_config = load(head_config_file)
    conn = sqlite3.connect(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'tree.db')
    commit_structure = []
    for file in files_tree:
        if file[3] == 'f':
            file_id = check_if_file_in_db(config, file[1], file[5], file[4], file[3], conn)
            if file_id == -1:
                file_id = add_file_db(config, current_path, conn, file, ignore_config)
        else:
            file_id = check_if_file_in_db(config, file[1], '', '', '', conn)
            if file_id == -1:
                file_id = add_file_db(config, current_path, conn, file, ignore_config)
        new_file = file.copy()
        new_file[0] = file_id
        temp_structure_path = new_file[2].split('/')
        if len(temp_structure_path) > 1:
            prev_id = str(check_if_file_in_db(config, files_tree[int(temp_structure_path[0])-1][1], '', '', '', conn))
            temp_structure_path_s = prev_id
            for component in range(1, (len(temp_structure_path)-1)):
                tmp_id = '/' + str(check_if_file_in_db(config, files_tree[int(temp_structure_path[component])-1][1], ''
                                                       , '', '', conn))
                temp_structure_path_s += tmp_id
            temp_structure_path_s = temp_structure_path_s + '/' + str(file_id)
            new_file[2] = temp_structure_path_s
        else:
            new_file[2] = str(file_id)
        commit_structure.append(new_file)
    branch_id = head_config["branch_id"]
    new_commit = create_commit(config, branch_id, getlogin(), message, commit_structure)
    commit_id = create_commit_db(conn, new_commit, config)
    commit_object = get_commit_by_id(config, conn, commit_id)
    update_logs(temp_path + config["local_repo_settings"]["sub_dir_names"]["logs"] + '\\' + 'logs.txt',
                (str(commit_object[0][2])+' '+config["messages"]["success"]["commit_created_successfully"]))
    head_update(config, current_path, '', commit_object[0][2])
    return None


def commit_jump(config, current_path, commit_name, ignore_config):
    import sqlite3
    from .helpers.database import get_commit_by_name
    from .helpers.files_structure import build_repository_from_structure, make_dir
    temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
    conn = sqlite3.connect(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'tree.db')
    if commit_name == 'prev':
        from json import load
        with open(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'head.json', mode='r') \
                as head_config_file:
            head_config = load(head_config_file)
            commit_name = head_config["current_commit"]
    commit_object = get_commit_by_name(config, conn, commit_name)
    if not commit_object:
        print("Commit of given name do not exist")
    else:
        #make_dir(commit_object[0][6])
        build_repository_from_structure(config, conn, current_path, commit_object[0][6], ignore_config)
        head_update(config, current_path, '', commit_object[0][2])
    return 1

def commit_list(scale, amount):
    pass