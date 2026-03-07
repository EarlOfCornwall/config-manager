import os
import shutil
from paths_info import POPULAR_CONFIGS

def create_dir(path):
    os.mkdir(path)
    print(f'Succefully created {path}')

def create_file(path):
    with open(path, 'w', encoding='UTF-8'):
        pass
    print(f'Succefully created {path}')

def clear(): 
    os.system('clear')

def check_for_needed() -> list:
    dir = config_dir_existence()
    file = info_file_existence()
    return [dir, file]

def info_file_existence() -> bool:
    if os.path.exists('./info.txt'):
        return True

    ans = input('Would you like to create ./info.txt file for info storage? (Y/n) ')
    if ans in " Yy":
        try:
            create_file('info.txt')
            return True
        except Exception as e:
            print(f'Something went wrong: {e}')
            return False
    return False

def config_dir_existence() -> bool:
    if os.path.exists('./Configs'):
        return True

    ans = input('Would you like to create ./Configs/ dir for config storage? (Y/n) ')
    if ans in " Yy":
        try:
            create_dir("Configs")
            return True
        except Exception as e:
            print(f'Something went wrong: {e}')
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

def show_finded_confs(finded_confs):
    print('Найдено:')
    for conf_info in finded_confs:
        print(f'{len(conf_info) - 1} конфиг-файлов для {conf_info[0]}:')
        for confs in conf_info[1:]:
            print(confs)

        print()

def copying_confs(find_confs, config_dir=False):
    if not config_dir:
        raise FileNotFoundError('Dir ./Configs/ not found. Programm can create it. Reopen programm.')

    for conf_info in find_confs:
        for path in conf_info[1:]:
            try:
                shutil.copy(path, f"Configs/{os.path.basename(path)}")
                print(f'Скопирован конфиг {path} в Configs/{os.path.basename(path)}')
            except Exception as e:
                print(f'Something went wrong {e}')

def main(config_dir_ex, info_file_ex):
    
    popular_confs = search_for_popular_configs()
    show_finded_confs(popular_confs)
    
    ans = input('Do you want to copy finded configs? (Y/n) ')
    if ans in ' Yy':
        copying_confs(popular_confs, config_dir=config_dir_ex)
    
   
if __name__ == "__main__":
    d, f = check_for_needed()
    main(d, f)
    

