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
    current_path = r'C:\Users\karol\Desktop\Projekty\test'
    #table= eval(table)
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


# make_dir(output)
def get_file_size(path):
    return os.path.getsize(path)