import os
import pathlib
from paths_info import POPULAR_CONFIGS

def clear(): 
    os.system('clear')

def search_for_popular_configs():
    find_confs = []
    for prog, info in POPULAR_CONFIGS.items():
        prog_confs = [prog,] # 1 element - prog name
        for file in info['files']:
            for path in info['paths']:
                expanded_path = os.path.expanduser(path)
                full_path = os.path.join(expanded_path, file)
                if os.path.exists(full_path): 
                    prog_confs.append(os.path.join(full_path))
        
        find_confs.append(prog_confs)

    return find_confs

def main():
    find_confs = search_for_popular_configs()
    print('Найдено:')
    for conf_info in find_confs:
        print(f'{len(conf_info) - 1} конфиг-файлов для {conf_info[0]}:')
        for confs in conf_info[1:]:
            print(confs)

        print()

main()
        
