def run():
    import sys, os, json
    from core import core

    args = []  # arguments and commands given via console
    system_path = ''  # path with location of this directory
    current_path = os.getcwd()

    for s_path in sys.path:
        if s_path[-3:] == 'kvc':
            system_path = s_path
    with open(os.path.join(system_path, r"configs\config.json")) as json_data_file:
        config = json.load(json_data_file)
    with open(os.path.join(system_path, r"configs\ignore.json")) as json_data_file:
        ignore_config = json.load(json_data_file)
    with open(os.path.join(system_path, r"configs\head.json")) as json_data_file:
        head_config = json.load(json_data_file)

    for arg in sys.argv:
        args.append(arg)

    if len(args) < 2:
        print("kvc - ", config["version"])
    else:
        '''Finding correct function'''
        if args[1] == 'init':
            core.repo_init(config, current_path)  # kvc init
        elif args[1] == 'commit':
            core.commit(config, ignore_config, head_config, current_path, 'e')

    return None


if __name__ == '__main__':
    run()
