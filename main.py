import os
import shutil
from paths_info import POPULAR_CONFIGS
import csv
import time
import sys

INFO_MODULE = "paths_info.py"
CONFIG_FOLDER = "Configs"
INFO_FILE = "info.csv"
SYMLINKS_FILE = "symlink.csv"

def exit_prog(code=0):
    sys.exit(code)

def create_object(path, is_dir=False, need_to_print=True):
    if is_dir:
        os.makedirs(path, exist_ok=True)
    else:
        with open(path, "w", encoding="UTF-8"):
            pass
    if need_to_print:
        print(f"Successfully created {path}")


def clear():
    os.system("clear")


def pause(pause=1.5):
    time.sleep(pause)


def check_for_needed() -> list:
    dir = object_existence(CONFIG_FOLDER)
    info_file = object_existence(INFO_FILE)
    symlink_info_file = object_existence(SYMLINKS_FILE)
    return [dir, info_file, symlink_info_file]


def count_files_in_folder(root_folder=CONFIG_FOLDER):
    total = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        total += len(filenames)
    return total


def object_existence(path) -> bool:
    if os.path.exists(path):
        return True

    ans = input(f"Would you like to create ./{path} file for info storage? (Y/n) ")
    if ans in "Yy":
        try:
            is_dir = '.' not in os.path.basename(path)
            create_object(path, is_dir=is_dir)
            print()
            pause()
            clear()
            return True
        except Exception as e:
            print(f"Something went wrong: {e}")
            pause()
            clear()
            return False

    return False


def search_for_popular_configs():
    find_confs = []
    for prog, info in POPULAR_CONFIGS.items():
        prog_confs = [
            prog,
        ]  # First element - prog name
        for file in info["files"]:
            for path in info["paths"]:
                expanded_path = os.path.expanduser(path)
                full_path = os.path.join(expanded_path, file)
                if os.path.exists(full_path):
                    prog_confs.append(os.path.join(full_path))

        find_confs.append(prog_confs)

    return find_confs

def log_into_symlink_file(prog_name='Unknown', config_path='Unknown', symlink_path='Unknown', backup_file='No backup'):
    with open(SYMLINKS_FILE, "a", encoding="UTF-8", newline="") as symlink_file:
        writer = csv.writer(symlink_file, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [prog_name, config_path, symlink_path, backup_file]
        )

def log_into_file(prog_name="Unknown", source_path="Unknown", copy_path="Unknown"):
    with open(INFO_FILE, "a", encoding="UTF-8", newline="") as info_file:
        writer = csv.writer(info_file, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [prog_name, source_path, copy_path]
        )  # PROG_NAME SOURCE_CONF COPY_CONF


def show_found_confs(found_confs):
    print("Found:")
    for conf_info in found_confs:
        print(f"{len(conf_info) - 1} config-files for {conf_info[0]}:")
        for confs in conf_info[1:]:
            print(confs)

        print()


def copying_confs(find_confs, config_dir=False, info_file=False):
    if not config_dir:
        raise FileNotFoundError(
            f"Dir ./{CONFIG_FOLDER}/ not found. Program can create it. Reopen programm."
        )

    for conf_info in find_confs:
        prog_name = conf_info[0]
        prog_configs_folder = f"{CONFIG_FOLDER}/{prog_name}"
        create_object(prog_configs_folder, is_dir=True, need_to_print=False)

        for source_path in conf_info[1:]:

            try:

                copy_path = os.path.join(prog_configs_folder, os.path.basename(source_path))
                shutil.copy2(source_path, copy_path)
                was_symlink = os.path.islink(source_path)
                print(f"Copied '{source_path}'  into  '{copy_path}'")
                if was_symlink:
                    print(f'That was a symlink. Original file is on {os.readlink(source_path)}')
                if info_file:
                    log_into_file(conf_info[0], source_path, copy_path)
                else:
                    print(
                        f"{INFO_FILE} does not exists. Program cant log info about copied configs."
                    )
            except Exception as e:
                print(f"Something went wrong {e}")
    print('Done copying configs.')

def read_info_file(file) -> list:
    info_dict = {} 
    with open(file, "r", encoding="UTF-8", newline="") as info_file:
        reader = csv.reader(info_file, quoting=csv.QUOTE_ALL)
        for row in reader:
            if not row: 
                continue
            info_dict[tuple(row)] = row

    return list(info_dict.values())  # No duplicates in paths


def turn_source_configs_to_symlink(config_dir=False, info_file=False, symlink_info_file=False):
    if not config_dir or not info_file:
        raise FileNotFoundError(
            f"There is no {CONFIG_FOLDER} or {INFO_FILE}. Cant turn configs into symlinks"
        )

    info = read_info_file(INFO_FILE)
    if len(info) != count_files_in_folder():
        print(f'WARNING: Mismatch between the number of records (in {INFO_FILE}) and saved configs')
        print(f"{len(info)} - records, {count_files_in_folder()} - files.")
        ans = input("Continue anyway? (N/y) ")
        if ans not in 'Yy' and ans != '':
            return

    for row in info:
        clear()
        prog_name, source_path, copy_path = row

        print(
            f"Do you agree with turning {source_path} to symlink with path on {copy_path}?"
        )
        ans = input(
            f"{source_path} will be deleted. If {copy_path} is corrupted you can lose your config. (N/y) "
        )
        if ans and ans in "Yy":
            backup_path = 'No backup'
            try:
                if os.path.exists(source_path):
                    backup_path = source_path + '.backup'
                    shutil.copy2(source_path, backup_path)
                    print(f'Created backup file for {source_path} on {backup_path}')
                    os.remove(source_path)
                os.symlink(os.path.abspath(copy_path), source_path)
                
                print(
                    f"Successfully create {source_path}(symlink) -> {copy_path}(config)"
                )
                if symlink_info_file:
                    config_path = copy_path
                    symlink_path = source_path
                    log_into_symlink_file(prog_name, config_path, symlink_path, backup_path)

            except Exception as e:
                print(f"Something went wrong: {e}")
                
                if os.path.exists(backup_path):
                    print("Restoring from backup")
                    try:
                        shutil.move(backup_path, source_path)
                        print("Restored")
                    except Exception:
                        print(f"Restore failed. You can do it manually. {backup_path} - path for backup")
                        pause(1)

    pause()  
    clear()
    print('Done.')
    if symlink_info_file: print(f'Info about saved symlinks is in {SYMLINKS_FILE}')


def return_from_config_dir(config_dir=False, info_file=False):
    if not config_dir or not info_file:
        raise FileNotFoundError(
            f"There is no {CONFIG_FOLDER} or {INFO_FILE}. Cant return configs."
        )

    info = read_info_file(INFO_FILE)  # (PROG, SOURCE, COPY)
    for row in info:
        clear()
        prog_name, source_path, copy_path = row
        if os.path.exists(source_path) or os.path.islink(source_path):
            ans = input(f"{source_path} exists. Overwrite? (N/y) ")
            if ans not in "Yy" and ans != '':
                print("Skip")
                continue
        try:
            if os.path.islink(source_path) or os.path.isfile(source_path):
                os.remove(source_path)
        except Exception as e:
            print(f"Something went wrong: {e}")
            print(f"Skip.")
            continue

        print(f"For {prog_name}:")
        print(f"Move '{copy_path}' to '{source_path}'")
        try:
            shutil.move(copy_path, source_path)
        except Exception as e:
            print(f"Something went wrong for file {copy_path} moving to path {source_path}: {e}")

    ans = input(f"Do you want to clear {INFO_FILE}? (N/y) ")
    if ans and ans in "yY":
        with open(INFO_FILE, "w") as f:
            pass
        print("Cleared.")

def menu(config_dir_ex, info_file_ex, symlink_info_file_ex):
    print("Config manager")
    print()
    print(f"Configs stored in {CONFIG_FOLDER} ({'Created' if config_dir_ex else 'Not found'})")
    print(f"Info stored in {INFO_FILE} (for configs. {'Created' if info_file_ex else 'Not found'})") 
    print(f"And {SYMLINKS_FILE} (for symlinks. {'Created' if symlink_info_file_ex else 'Not found'})")
    print()
    print(f"1. Search and Copy configs (Only with info in {INFO_MODULE})")
    print("2. Deploy symlinks")
    print("3. Return configs")
    print("4. Check statistics")
    print("5. Exit")
    
    
    choice = input("Select options (1-5): ")
    menu_choices(choice, config_dir_ex=config_dir_ex, info_file_ex=info_file_ex, symlink_info_file_ex=symlink_info_file_ex)
    

def menu_choices(choice, config_dir_ex=False, info_file_ex=False, symlink_info_file_ex=False):
    if choice == '1':
        configs = search_for_popular_configs()
        show_found_confs(configs)

        print()
        ans = input('Copy found configs? (Y/n) ')
        if ans in 'Yy':
            copying_confs(configs, config_dir=config_dir_ex, info_file=info_file_ex)
        input('\nPress ENTER to continue')
                

    elif choice == '2':
        try:
            turn_source_configs_to_symlink(config_dir=config_dir_ex, info_file=info_file_ex, symlink_info_file=symlink_info_file_ex)
        except Exception as e:
            print(f'Something went wrong: {e}')
        input('\nPress ENTER to continue')        
    
    elif choice == '3':
        try:
            return_from_config_dir(config_dir=config_dir_ex, info_file=info_file_ex)
        except Exception as e:
            print(f'Something went wrong: {e}')
        input('\nPress ENTER to continue')

    elif choice == '4':
        print('Statistics:')
        if config_dir_ex:
            print(f"You have {count_files_in_folder()} configs in {CONFIG_FOLDER}")
        if info_file_ex:
            print(f"{len(read_info_file(INFO_FILE))} records in {INFO_FILE}")
        if symlink_info_file_ex:
            print(f"{len(read_info_file(SYMLINKS_FILE))} records in {SYMLINKS_FILE}")
        if not any([config_dir_ex, info_file_ex, symlink_info_file_ex]):
            print('No statistics available')
        input('\nPress ENTER to continue')

    elif choice == '5':
        print('Goodbye.')
        exit_prog()

    else:
        print('Invalid option. Please enter 1-5')
        pause(1)
        return

def main(config_dir_ex, info_file_ex, symlink_info_file_ex):

    while True:
        clear()
        menu(config_dir_ex=config_dir_ex, info_file_ex=info_file_ex, symlink_info_file_ex=symlink_info_file_ex)


if __name__ == "__main__":
    clear()
    d, f, s = check_for_needed() # Dir for configs, Info file for configs. Info file for symlinks.
    main(d, f, s)
