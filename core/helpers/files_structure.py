import os


def get_files_tree(ignore_config, current_path):
    from .datetime_helper import get_modification_date
    structure = []
    _arr = []
    index = 0
    for root, dirs, files in os.walk(current_path):
        if index > 0:
            ignored = False
            rel_path = os.path.relpath(root, current_path)
            tmp_root = root.split('\\')
            compressed_path = [x for x in rel_path.split('\\')]
            new_path = ''
            for x in compressed_path:
                if len(_arr) > 0:
                    for y in _arr:
                        if str(x) in y[1]:
                            new_path += str(y[2]) + '/'
                            break
            new_path += str(index)
            temp = [os.path.basename(root), compressed_path, index, new_path]
            _arr.append(temp)
            temp = [index, os.path.basename(root), new_path, 'd', get_modification_date(root), root]
            for component in tmp_root:
                if component in ignore_config["ignored"]["directories_names"]:
                    ignored = True
            if not ignored:
                structure.append(temp)
        index += 1
        for file in files:
            ignored2 = False
            file_rel_path = os.path.relpath(root, current_path)
            tmp_root_2 = root.split('\\')
            file_compressed_path = [x for x in file_rel_path.split('\\')]
            new_path_2 = ''
            if file_compressed_path != ['.']:
                for x in file_compressed_path:
                    if len(_arr) > 0:
                        for y in _arr:
                            if str(x) in y[1]:
                                new_path_2 += str(y[2]) + '/'
                                break
            new_path_2 += str(index)
            temp2 = [file, file_compressed_path, index, new_path_2]
            _arr.append(temp2)
            if file.split('.')[1] in ignore_config["ignored"]["file_extensions"]:
                ignored2 = True
            temp2 = [index, file, new_path_2, 'f', get_modification_date(root+'\\'+file), get_file_size(root+'\\'+file),
                     (root+'\\'+file)]
            for name2 in ignore_config["ignored"]["directories_names"]:
                if name2 in tmp_root_2:
                    ignored2 = True
            if not ignored2:
                structure.append(temp2)
            index += 1
    return structure


# generating from table
def make_dir(table):
    current_path = r'C:\Users\karol\Desktop\Projekty\testowy'
    table= eval(table)
    for row in table:
        row_path = current_path
        temp_structure = [x for x in row[2].split('/')]
        for i in range(len(temp_structure)):
            if i == (len(temp_structure) - 1):
                if row[3] == 'f':
                    row_path += '\\' + row[1]
                    temp_file = open(row_path, mode='a')
            else:
                for y in table:
                    if str(y[0]) == temp_structure[i]:
                        row_path += '\\' + y[1]
                        if not os.path.exists(row_path):
                            os.mkdir(row_path)


def erase_directory_content(path):
    import os
    import shutil
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def erase_directory_content_ignore(path, ignore_config):
    import os
    import shutil
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        file_structure = file_path.split('\\')
        if (filename in ignore_config["ignored"]["directories_names"] or (filename.split('.')[-1] in ignore_config["ignored"]["file_extensions"])) and filename in file_structure:
            continue
        else:

            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    return 1


def copy_file_and_move_to_archive(config, current_path, file_path, new_name, ignore_config):
    from shutil import copyfile
    from .files_naming import set_file_name
    temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
    temp_path2 = temp_path + config["local_repo_settings"]["sub_dir_names"]["temp"]
    erase_directory_content(temp_path2)
    copyfile(file_path, (temp_path2+'\\'+'tmp.tmp'))
    set_file_name((temp_path2+'\\'+'tmp.tmp'), new_name)
    copyfile((temp_path2+'\\'+new_name),
             (temp_path + config["local_repo_settings"]["sub_dir_names"]["archive"]+'\\'+new_name))
    return 1


def copy_file_and_move_to_repo(config, current_path, file_path, name, f_type, archive_name):
    from shutil import copyfile
    temp_path = current_path + "\\" + config["local_repo_settings"]["name"][0] + '\\'
    temp_path = temp_path + config["local_repo_settings"]["sub_dir_names"]["archive"] + '\\' + archive_name
    file_path = file_path + name + '.' + f_type
    copyfile(temp_path, file_path)
    return 1


def build_repository_from_structure(config, conn, current_path, structure, ignore_config):
    from .database import get_file_by_id
    erase_directory_content_ignore(current_path, ignore_config)
    structure = eval(structure)
    for row in structure:
        row_path = current_path
        temp_structure = [x for x in row[2].split('/')]
        for i in range(len(temp_structure)):
            if i == (len(temp_structure) - 1):
                if row[3] == 'f':
                    row_path += '\\'
                    file_object = get_file_by_id(config, conn, row[0])
                    copy_file_and_move_to_repo(config, current_path, row_path, file_object[0][1], file_object[0][2],
                                               file_object[0][3])
            else:
                for component in structure:
                    if str(component[0]) == temp_structure[i]:
                        row_path += '\\' + component[1]
                        if not os.path.exists(row_path):
                            os.mkdir(row_path)


def get_file_size(path):
    return os.path.getsize(path)





