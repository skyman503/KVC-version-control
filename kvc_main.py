def run():
    import sys
    import os
    from json import load
    from core import core

    args = []  # arguments and commands given via console
    system_path = ''  # path with location of this directory
    current_path = os.getcwd()

    for s_path in sys.path:
        if s_path[-3:] == 'kvc':
            system_path = s_path
    with open(os.path.join(system_path, r"configs\config.json")) as json_data_file:
        config = load(json_data_file)
    with open(os.path.join(system_path, r"configs\ignore.json")) as json_data_file:
        ignore_config = load(json_data_file)

    for arg in sys.argv:
        args.append(arg)

    if len(args) < 2:
        print("kvc - ", config["version"])
    else:
        '''Finding correct function'''
        if args[1] == 'init':
            core.repo_init(config, current_path)  # kvc init
        elif args[1] == 'commit-list':
            core.commit_list(config, current_path, 1)  # 1- same branch
        elif args[1] == 'commit-list-full':
            core.commit_list(config, current_path, 2)  # 2- all branches
        elif args[1] == 'commit-prev':
            core.commit_jump(config, current_path, 'prev', ignore_config)
        elif args[1] == 'commit-jump':
            if len(args) > 2:
                core.commit_jump(config, current_path, args[2], ignore_config)
            else:
                print("No jump occurred(invalid commit name)")
        elif args[1] == 'commit':
            if len(args) > 2:
                s = ' '
                message = s.join(args[2:])
            else:
                message = 'default message'
            core.commit(config, ignore_config, current_path, message)
        elif args[1] == 'branch-creation':
            if len(args) > 2:
                core.branch_create(config, current_path, args[2])
            else:
                print("Branch won't be created(name not specified)")
        elif args[1] == 'branch-swap':
            if len(args) > 2:
                core.branch_swap(config, current_path, args[2], ignore_config)
            else:
                print("Branch wasn't changed(name not specified)")
        elif args[1] == 'branch-merge':
            if len(args) > 2:
                core.branch_merge(config, current_path, args[2], args[3])
            else:
                print("Branch wasn't changed(name not specified)")
    return None


if __name__ == '__main__':
    run()
