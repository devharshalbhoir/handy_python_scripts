import shutil
import os
from datetime import datetime
import git  # pip install GitPython
from git import Repo
import sys


def move_worked_files(folder_path):
    try:
        base_dir = os.getcwd()
        repo = Repo(folder_path)
        active_branch = repo.active_branch.name + '_' + datetime.now().strftime('%d%b%y_%H')
        module_name = folder_path.split('\\').pop(-1)

        module_dir = os.path.join(base_dir, module_name)
        if not os.path.isdir(module_dir):
            print("creating repo : ", module_dir)
            os.makedirs(module_dir)

        branch_dir = os.path.join(module_dir, active_branch)
        if not os.path.isdir(branch_dir):
            print(f"creating branch_dir : {branch_dir}")
            os.makedirs(branch_dir)

        log_file = os.path.join(branch_dir, 'log.txt')

        if repo.untracked_files:
            untracked_dir = os.path.join(branch_dir, 'untracked')
            if not os.path.isdir(untracked_dir):
                func_print_lines(log_file, f"\n creating untracked_dir : {untracked_dir} \n")
                os.makedirs(untracked_dir)
            for item in repo.untracked_files:
                shutil.copy(os.path.join(folder_path, item), untracked_dir)
            func_print_lines(log_file, "\n The untracked files are : \n {}".format('\n  '.join(repo.untracked_files)))

        changed = [item.a_path for item in repo.index.diff(None)]
        if changed:
            changed_dir = os.path.join(branch_dir, 'changed')
            if not os.path.isdir(changed_dir):
                func_print_lines(log_file, f" \n creating changed_dir : {changed_dir} \n")
                os.makedirs(changed_dir)
            for item in changed:
                shutil.copy(os.path.join(folder_path, item), changed_dir)
            func_print_lines(log_file, "\n The modified files are : \n {}".format('\n  '.join(changed)))

    except git.exc.InvalidGitRepositoryError:
        print("No Git Repo Found")
    except Exception as e:
        print("Error Occurred : ", e)


def func_print_lines(log_file, lines):
    try:
        with open(log_file, mode='a') as file:
            file.write('\n')
            print(lines)
            file.write(lines)
    except Exception as e:
        print("Error occurred : ", e)


if __name__ == '__main__':
    move_worked_files(input("Enter the file path : \n"))
