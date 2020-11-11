import sqlite3


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def create_commit(config, branch_id, user, message, structure):
    from .files_naming import hash_name
    from .datetime_helper import get_current_datetime
    date = get_current_datetime()
    name = hash_name(config, date)
    return branch_id, name, date, user, message, str(structure)


def create_commit_db(conn, commit, config):
    commit_creation_sql = config["database"]["insert_data"]["commit"]
    c = conn.cursor()
    c.execute(commit_creation_sql, commit)
    conn.commit()
    return c.lastrowid


def create_branch(name, user, alive):
    from . datetime_helper import get_current_datetime
    return name, get_current_datetime(), '', user, alive


def create_branch_db(conn, branch, config):
    branch_creation_sql = config["database"]["insert_data"]["branch"]
    c = conn.cursor()
    c.execute(branch_creation_sql, branch)
    conn.commit()
    return c.lastrowid


def add_initial_db(config, current_path, conn):
    from .files_naming import get_file_name
    from .files_structure import get_file_size
    from .datetime_helper import get_current_datetime
    from os import getlogin

    initial_name = config["local_repo_settings"]["initial_file_name"]
    new_name = get_file_name(current_path, initial_name)
    file_creation_sql = config["database"]["insert_data"]["file"]
    file_data = (initial_name.split('.')[0], initial_name.split('.')[-1], new_name[0], get_current_datetime(),
                 str(new_name[1]), getlogin(), get_file_size(current_path))
    c = conn.cursor()
    c.execute(file_creation_sql, file_data)
    conn.commit()
    return c.lastrowid


def check_if_file_in_db(config, file_name, file_size, file_mod_date, file_type, conn):
    c = conn.cursor()
    c.execute(config["database"]["find_data"]["file"])
    records = c.fetchall()
    for record in records:
        if file_type == 'f':
            if (file_name == record[1]+'.'+record[2]) and (file_size == record[7]) \
                    and (str(file_mod_date) == record[5]):
                return record[0]
        else:
            if file_name == record[1]:
                return record[0]
    return -1


def get_commit_by_id(config, conn, commit_id):
    c = conn.cursor()
    c.execute(config["database"]["find_data"]["commit_by_id"], (commit_id,))
    commit_object = c.fetchall()
    return commit_object


def get_commit_by_name(config, conn, commit_name):
    c = conn.cursor()
    c.execute(config["database"]["find_data"]["commit_by_name"], (commit_name,))
    commit_object = c.fetchall()
    return commit_object


def get_file_by_id(config, conn, file_id):
    c = conn.cursor()
    c.execute(config["database"]["find_data"]["file_by_id"], (file_id,))
    file_object = c.fetchall()
    return file_object


def add_file(config, tree_record):
    from .files_naming import get_file_name
    from .datetime_helper import get_current_datetime
    from os import getlogin
    if tree_record[3] == 'd':
        full_name = tree_record[1]
        name = full_name
        file_format = 'directory'
        size = 0
    else:
        full_name = tree_record[1]
        name = tree_record[1].split('.')[0]
        file_format = tree_record[1].split('.')[1]
        size = tree_record[5]
    arch_name = get_file_name(tree_record[-1], full_name)[0]
    c_date = get_current_datetime()
    m_date = str(tree_record[4])
    return name, file_format, arch_name, c_date, m_date, getlogin(), size


def add_file_db(config, current_path, conn, tree_record, ignore_config):
    from .files_structure import copy_file_and_move_to_archive
    c = conn.cursor()
    data = add_file(config, tree_record)
    c.execute(config["database"]["insert_data"]["file"], data)
    conn.commit()
    if data[1] != 'directory':
        copy_file_and_move_to_archive(config, current_path, tree_record[6], data[2], ignore_config)
    return c.lastrowid


def create_default_db(config, current_path, user):
    from json import dump
    temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
    '''Creating new sqlite database'''
    try:
        with open(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'head.json', mode='w') \
                as head_json_file:
            initial_head_data = {"branch_id": 1, "current_commit": "."}
            dump(initial_head_data, head_json_file)
        conn = sqlite3.connect(temp_path + config["local_repo_settings"]["sub_dir_names"]["tree"] + '\\' + 'tree.db')
        if conn is not None:
            create_table(conn, config["database"]["initialization"]["create_tables"]["branches_sql"])
            create_table(conn, config["database"]["initialization"]["create_tables"]["commits_sql"])
            create_table(conn, config["database"]["initialization"]["create_tables"]["files_sql"])

            branch_master = create_branch("master", user, True)
            branch_master_id = create_branch_db(conn, branch_master, config)
            initial_commit = create_commit(config, branch_master_id, user, "repository created", structure='1')
            initial_commit_id = create_commit_db(conn, initial_commit, config)
            initial_welcome_file = open((current_path + '\\' + config["local_repo_settings"]["initial_file_name"]), mode='a')
            initial_welcome_file.write('Your repository was created')
            initial_welcome_file.close()
            add_initial_db(config, (current_path + '\\' + config["local_repo_settings"]["initial_file_name"]), conn)
            check_if_file_in_db(config,1,1,1,1,conn)
    except sqlite3.Error as e:
        print(e)


