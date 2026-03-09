import os
import shutil
from paths_info import POPULAR_CONFIGS
import csv
import time

CONFIG_FOLDER = "Configs"
INFO_FILE = "info.csv"


def create_dir(path, need_to_print=True):
    os.makedirs(path, exist_ok=True)
    if need_to_print:
        print(f"Succefully created {path}")


def create_file(path, need_to_print=True):
    with open(path, "w", encoding="UTF-8"):
        pass
    if need_to_print:
        print(f"Succefully created {path}")


def clear():
    os.system("clear")


def pause(pause=1.5):
    time.sleep(pause)


def check_for_needed() -> list:
    dir = config_dir_existence()
    file = info_file_existence()
    return [dir, file]


def count_files_in_folder(root_folder=CONFIG_FOLDER):
    total = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        total += len(filenames)
    return total


def info_file_existence() -> bool:
    if os.path.exists(INFO_FILE):
        return True

    ans = input(f"Would you like to create ./{INFO_FILE} file for info storage? (Y/n) ")
    if ans in " Yy":
        try:
            create_file(INFO_FILE)
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


def config_dir_existence() -> bool:
    if os.path.exists(f"./{CONFIG_FOLDER}"):
        return True

    ans = input(
        f"Would you like to create ./{CONFIG_FOLDER}/ dir for config storage? (Y/n) "
    )
    if ans in " Yy":
        try:
            create_dir(CONFIG_FOLDER)
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


def log_into_file(prog_name="Unknown", source_path="Unknown", copy_path="Unknown"):
    with open(INFO_FILE, "a", encoding="UTF-8", newline="") as info_file:
        writer = csv.writer(info_file, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [prog_name, source_path, copy_path]
        )  # PROG_NAME SOURCE_CONF COPY_CONF


def show_finded_confs(finded_confs):
    print("Founded:")
    for conf_info in finded_confs:
        print(f"{len(conf_info) - 1} config-files for {conf_info[0]}:")
        for confs in conf_info[1:]:
            print(confs)

        print()


def copying_confs(find_confs, config_dir=False, info_file=False):
    if not config_dir:
        raise FileNotFoundError(
            f"Dir ./{CONFIG_FOLDER}/ not found. Programm can create it. Reopen programm."
        )

    for conf_info in find_confs:
        prog_name = conf_info[0]
        prog_configs_folder = f"{CONFIG_FOLDER}/{prog_name}"
        create_dir(prog_configs_folder, need_to_print=False)

        for source_path in conf_info[1:]:

            try:
                copy_path = f"{prog_configs_folder}/{os.path.basename(source_path)}"
                shutil.copy2(source_path, copy_path)
                print(f"Copied '{source_path}'  into  '{copy_path}'")
                if info_file:
                    log_into_file(conf_info[0], source_path, copy_path)
                else:
                    print(
                        f"{INFO_FILE} does not exists. Programm cant log info about copied configs."
                    )
            except Exception as e:
                print(f"Something went wrong {e}")


def read_info_file() -> set:
    info_set = set()
    with open(INFO_FILE, "r", encoding="UTF-8", newline="") as info_file:
        reader = csv.reader(info_file, quoting=csv.QUOTE_ALL)
        for row in reader:
            info_set.add(tuple(row))

    return info_set  # No duplicates in paths


def turn_source_configs_to_symlink(config_dir=False, info_file=False):
    if not config_dir or not info_file:
        raise FileNotFoundError(
            f"There is no {CONFIG_FOLDER} or {INFO_FILE}. Cant turn configs into symlinks"
        )

    info = read_info_file()
    if len(info) != count_files_in_folder():
        raise ValueError(
            "Mismatch between the number of records and saved configs. Something went wrong."
        )

    for row in info:
        prog_name, source_path, copy_path = row

        print(
            f"Do you agree with turning {source_path} to symlink with path on {copy_path}?"
        )
        ans = input(
            f"{source_path} will be deleted. If {copy_path} is corrupted you can loose your config. (N/y) "
        )
        if ans and ans in "Yy":
            try:
                if os.path.exists(source_path):
                    os.remove(source_path)
                os.symlink(os.path.abspath(copy_path), source_path)
                print(
                    f"Succefully create {source_path}(symlink) -> {copy_path}(config)"
                )
            except Exception as e:
                print(f"Something went wrong: {e}")

        pause()
        clear()


def return_from_config_dir(config_dir=False, info_file=False):
    if not config_dir or not info_file:
        raise FileNotFoundError(
            f"There is no {CONFIG_FOLDER} or {INFO_FILE}. Cant return configs."
        )

    info = read_info_file()  # (PROG, SOURCE, COPY)
    for row in info:
        prog_name, source_path, copy_path = row
        print(f"For {prog_name}:")
        print(f"Move '{copy_path}' to '{source_path}'")
        try:
            shutil.move(copy_path, source_path)
        except Exception as e:
            print(f"Something went wrong for file {row[2]}: {e}")

    ans = input(f"Do you want to clear {INFO_FILE}? (N/y) ")
    if ans and ans in "yY":
        with open(INFO_FILE, "w") as f:
            pass
        print("Cleared.")


def main(config_dir_ex, info_file_ex):

    popular_confs = search_for_popular_configs()
    show_finded_confs(popular_confs)
    print()
    pause()

    ans = input("Do you want to copy finded configs? (Y/n) ")
    clear()
    if ans in " Yy":
        copying_confs(popular_confs, config_dir=config_dir_ex, info_file=info_file_ex)
        pause(len(popular_confs))
        clear()

    print(f"Now you have {count_files_in_folder()} configs in {CONFIG_FOLDER}/")
    ans = input("Do you want to return configs on their place? (N/y) ")
    clear()
    if ans and ans in "yY":
        return_from_config_dir(config_dir_ex, info_file_ex)


if __name__ == "__main__":
    d, f = check_for_needed()
    main(d, f)
