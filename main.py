import os
import shutil
from paths_info import POPULAR_CONFIGS
import csv
import time

CONFIG_FOLDER = 'Configs'
INFO_FILE = 'info.csv'

def create_dir(path):
    os.mkdir(path)
    print(f'Succefully created {path}')

def create_file(path):
    with open(path, 'w', encoding='UTF-8'):
        pass
    print(f'Succefully created {path}')

def clear(): 
    os.system('clear')

def pause(pause=1.5):
    time.sleep(pause)

def check_for_needed() -> list:
    dir = config_dir_existence()
    file = info_file_existence()
    return [dir, file]

def info_file_existence() -> bool:
    if os.path.exists(INFO_FILE):
        return True

    ans = input(f'Would you like to create ./{INFO_FILE} file for info storage? (Y/n) ')
    if ans in " Yy":
        try:
            create_file(INFO_FILE)
            print()
            pause()
            clear()
            return True
        except Exception as e:
            print(f'Something went wrong: {e}')
            pause()
            clear()
            return False

    return False

def config_dir_existence() -> bool:
    if os.path.exists(f'./{CONFIG_FOLDER}'):
        return True

    ans = input(f'Would you like to create ./{CONFIG_FOLDER}/ dir for config storage? (Y/n) ')
    if ans in " Yy":
        try:
            create_dir(CONFIG_FOLDER)
            print()
            pause()
            clear()
            return True
        except Exception as e:
            print(f'Something went wrong: {e}')
            pause()
            clear()
            return False
    return False    

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

def log_into_file(prog_name='Unknown', source_path='Unknown', copy_path='Unknown'):
    with open(INFO_FILE, 'a', encoding='UTF-8') as info_file:
        writer = csv.writer(info_file)
        writer.writerow([prog_name, source_path, copy_path]) # PROG_NAME SOURCE_CONF COPY_CONF


def show_finded_confs(finded_confs):
    print('Найдено:')
    for conf_info in finded_confs:
        print(f'{len(conf_info) - 1} конфиг-файлов для {conf_info[0]}:')
        for confs in conf_info[1:]:
            print(confs)

        print()

def copying_confs(find_confs, config_dir=False, info_file=False):
    if not config_dir:
        raise FileNotFoundError(f'Dir ./{CONFIG_FOLDER}/ not found. Programm can create it. Reopen programm.')

    for conf_info in find_confs:
        for path in conf_info[1:]:
            try:
                copy_path = f"Configs/{os.path.basename(path)}"
                shutil.copy(path, copy_path)
                print(f'Скопирован конфиг {path} в {copy_path}')
                if info_file:
                    log_into_file(conf_info[0], path, copy_path)
                else:
                    print(f"{INFO_FILE} does not exists. Programm cant log info about copied configs.")
            except Exception as e:
                print(f'Something went wrong {e}')

def read_info_file():
    info_set = set()
    with open(INFO_FILE, 'r', encoding='UTF-8') as info_file:
        reader = csv.reader(info_file)    
        for row in reader:
            info_set.add(tuple(row))
    
    return info_set 

def main(config_dir_ex, info_file_ex):
    
    popular_confs = search_for_popular_configs()
    show_finded_confs(popular_confs)
    
    ans = input('Do you want to copy finded configs? (Y/n) ')
    if ans in ' Yy':
        copying_confs(popular_confs, config_dir=config_dir_ex, info_file=info_file_ex)
    
    for row in read_info_file():
        print(row)
        
    
   
if __name__ == "__main__":
    d, f = check_for_needed()
    main(d, f)
    

