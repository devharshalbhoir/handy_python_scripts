#!/bin/bash
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
import os
import shutil
from colorama import Fore, Back, Style


def sort_move_files(path, operation_value):
    if operation_value == '1':  # if Dest will add new folder
        subdir = f"Downloads_bkp_{datetime.now().strftime('%d_%b_%y')}"
        dest = os.path.join(path, subdir)
        if not os.path.exists(dest):
            os.mkdir(dest)
    elif operation_value == '2':
        dest = path  # If DEST is the same as PATH
    elif operation_value == '3':
        dest = input("Enter the Destination file path : \n")
        check_dir(dest)
    else:
        print(Fore.RED + "Wrong operation selected")
        sys.exit(1)

    # This will create a properly organized list with all the filename that is
    # there in the directory
    list_ = os.listdir(path)

    # This will go through each and every file
    for file_ in list_:
        name, ext = os.path.splitext(file_)
        ext = ext[1:]  # This is going to store the extension type

        if ext == '':
            continue  # This forces the next iteration, if it is the directory

        # This will move the file to the directory where the name 'ext' already exists
        dest_path = f"{dest}/{ext}"
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        dest_file_name = f"{dest}/{ext}/{file_}"
        source_file_name = f"{path}/{file_}"

        # check if the file already exists in the folder
        if os.path.exists(dest_file_name):
            # if the file exists, find a new name by appending a number to the file name
            i = 1
            while True:
                new_file_name = f"{os.path.splitext(dest_file_name)[0]}_{i}{os.path.splitext(dest_file_name)[1]}"
                new_dest_path = os.path.join(dest_path, new_file_name)
                if os.path.exists(new_dest_path):
                    i += 1
                else:
                    dest_file_name = new_dest_path
                    break

        shutil.move(source_file_name, dest_file_name)
        print(Fore.GREEN + f"\n Files moved from {path} to {dest}")


def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        print(Fore.RED + "Folder Path Doesn't Exist")
        sys.exit(1)


if __name__ == '__main__':
    file_path = input("Enter the source file path : \n")
    check_dir(file_path)
    operation = input("Select any operation :\n "
                      "    1. New Folder : \n"
                      "     2. Same Folder: \n"
                      "     3. Different Path: \n")
    sort_move_files(file_path, operation)
    # G:\BKP\work\Walplast\Desktop\Documentation
    # G:\BKP\work\Walplast\Documents\Download_BKP\attachments
    # C:\Users\ADMIN\Downloads
    # C:\HRSHL\Docs\Downloads_bkp
