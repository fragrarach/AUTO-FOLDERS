import os
import re
from comtypes.client import CreateObject
from comtypes.persist import IPersistFile
from comtypes.shelllink import ShellLink
from shutil import copyfile
from statements import all_ord_nos


# Generate top level reference folder
def create_dir(config, record_type, reference):
    directory = f'{config.DOC_DIR}\\{record_type}\\{reference}'
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f'Created directory : {directory}')
    else:
        print(f'Directory already exists : {directory}')
    return directory


def extend_dir(config, prt_no, prt_folder):
    eng_folder = create_eng_sub_folders(config, prt_no)
    copy_change_summary(config, eng_folder, prt_no)
    create_old_shortcut(eng_folder)
    create_eng_shortcut(eng_folder, prt_folder)
    create_supplier_shortcut(config, prt_no, prt_folder)


# Generate engineering source folder and current, future and old sub folders
def create_eng_sub_folders(config, prt_no):
    eng_folder = f'{config.ENG_DIR}\\{prt_no}'
    eng_sub_folders = ['Current', 'Future', 'Old']
    if not os.path.exists(eng_folder):
        os.makedirs(eng_folder)
    for sub_folder in eng_sub_folders:
        sub_folder_path = F'{eng_folder}\\{sub_folder}'
        if not os.path.exists(sub_folder_path):
            os.makedirs(sub_folder_path)
    return eng_folder


# Create a copy of the change summary excel file from the template
def copy_change_summary(config, eng_folder, prt_no):
    template_file = f'{config.SOURCE_DIR}\\TEMPLATES\\CHANGE SUMMARY.xlsm'
    template_dest = f'{eng_folder}\\Current\\{prt_no} CHANGE SUMMARY.xlsm'
    copyfile(template_file, template_dest)


# Create internal shortcut from 'current' sub folder to 'old' sub folder
def create_old_shortcut(eng_folder):
    source = f'{eng_folder}\\Old'
    eng_dest = f'{eng_folder}\\Current\\Old.lnk'
    s = CreateObject(ShellLink)
    s.SetPath(source)
    p = s.QueryInterface(IPersistFile)
    p.Save(eng_dest, True)


# Create shortcut from reference folder to source folder
def create_eng_shortcut(eng_folder, prt_folder):
    s = CreateObject(ShellLink)
    s.SetPath(eng_folder)
    p = s.QueryInterface(IPersistFile)
    p.Save(prt_folder + r'\ENGINEERING.lnk', True)


def create_supplier_shortcut(config, prt_no, prt_folder):
    sup_source = f'{config.SUP_DIR}\\{prt_no}'
    if not os.path.exists(sup_source):
        os.makedirs(sup_source)
    s = CreateObject(ShellLink)
    s.SetPath(sup_source)
    p = s.QueryInterface(IPersistFile)
    p.Save(prt_folder + r'\SUPPLIER INFO.lnk', True)


def init_ord_directories(config):
    record_type = 'ORD'
    ord_nos = all_ord_nos(config)
    for ord_no in ord_nos:
        reference = ord_no[0]
        create_dir(config, record_type, reference)
    print('Order directory init complete.\n')


def rename_prt_no(config, old_prt_no, new_prt_no):
    part_folder = config.DOC_DIR + f'\\PRT\\{old_prt_no}'
    eng_folder = config.ENG_DIR + f'\\{old_prt_no}'
    sup_folder = config.SUP_DIR + f'\\{old_prt_no}'
    acc_folder = config.ACC_DIR + f'\\{old_prt_no}'
    pics_folder = config.PICS_DIR + f'\\{old_prt_no}'

    print(f'Renaming folders for part renaming from {old_prt_no} to {new_prt_no}')

    if os.path.exists(eng_folder):
        new_eng_folder = config.ENG_DIR + f'\\{new_prt_no}'
        os.rename(eng_folder, new_eng_folder)
        print(f'Engineering folder renamed from {eng_folder} to {new_eng_folder}')

    if os.path.exists(sup_folder):
        new_sup_folder = config.SUP_DIR + f'\\{new_prt_no}'
        os.rename(sup_folder, new_sup_folder)
        print(f'Engineering folder renamed from {sup_folder} to {new_sup_folder}')

    if os.path.exists(part_folder):
        new_part_folder = config.DOC_DIR + f'\\PRT\\{new_prt_no}'
        os.rename(part_folder, new_part_folder)
        print(f'Part folder renamed from {part_folder} to {new_part_folder}')

        eng_shortcut = new_part_folder + r'\ENGINEERING.lnk'
        new_eng_folder = config.ENG_DIR + f'\\{new_prt_no}'
        if os.path.exists(eng_shortcut):
            os.remove(eng_shortcut)
            create_eng_shortcut(new_eng_folder, new_part_folder)
            print(f'Generated shortcut to engineering folder in part folder')

        sup_shortcut = new_part_folder + r'\SUPPLIER INFO.lnk'
        if os.path.exists(sup_shortcut):
            os.remove(sup_shortcut)
            create_supplier_shortcut(config, new_prt_no, new_part_folder)
            print(f'Generated shortcut to supplier folder in part folder')

    if os.path.exists(acc_folder):
        new_acc_folder = config.ACC_DIR + f'\\{new_prt_no}'
        os.rename(acc_folder, new_acc_folder)
        print(f'Accessory folder renamed from {acc_folder} to {new_acc_folder}')

    if os.path.exists(pics_folder):
        new_pics_folder = config.PICS_DIR + f'\\{new_prt_no}'
        os.rename(pics_folder, new_pics_folder)
        print(f'Pictures folder renamed from {pics_folder} to {new_pics_folder}')

    if os.path.exists(config.UNIT_DIR):
        for folder in os.listdir(config.UNIT_DIR):
            unit_list = config.UNIT_DIR + f'\\{folder}\\List.txt'
            if os.path.exists(unit_list):
                if old_prt_no in open(unit_list).read():
                    with open(unit_list, "r") as file:
                        file_data = file.readlines()

                    for index, line in enumerate(file_data):
                        file_data[index] = re.sub(rf'^{old_prt_no}$', new_prt_no, line)

                    with open(unit_list, "w") as file:
                        file.writelines(file_data)
                    print(f'Renamed part number in worksheet {folder} unit list')

    if os.path.exists(config.MANUAL_DIR):
        for folder in os.listdir(config.MANUAL_DIR):
            manual_list = config.MANUAL_DIR + f'\\{folder}\\ACTIVE.txt'
            if os.path.exists(manual_list):
                if old_prt_no in open(manual_list).read():
                    with open(manual_list, "r") as file:
                        file_data = file.readlines()

                    for index, line in enumerate(file_data):
                        file_data[index] = re.sub(rf'^{old_prt_no}$', new_prt_no, line)

                    with open(manual_list, "w") as file:
                        file.writelines(file_data)
                    print(f'Renamed part number in manual {folder} unit list')

    print(f'Renaming complete for part renaming from {old_prt_no} to {new_prt_no}\n')
