import os
from comtypes.client import CreateObject
from comtypes.persist import IPersistFile
from comtypes.shelllink import ShellLink
from shutil import copyfile
from config import Config
from sql import all_ord_nos


# Generate top level reference folder
def create_dir(parent, record_type, reference):
    directory = f'{parent}\\{record_type}\\{reference}'
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f'Created directory : {directory}')
    else:
        print(f'Directory already exists : {directory}')
    return directory


def extend_dir(reference, directory):
    eng_source = create_eng_sub_folders(Config.DOC_DIR, reference)
    copy_change_summary(Config.DOC_DIR, eng_source, reference)
    create_old_shortcut(eng_source)
    create_eng_shortcut(eng_source, directory)
    create_supplier_shortcut(Config.DOC_DIR, reference, directory)


# Generate engineering source folder and current, future and old sub folders
def create_eng_sub_folders(parent, reference):
    eng_source = f'{parent}\\SOURCE FILES\\ENGINEERING\\{reference}'
    eng_sub_folders = ['Current', 'Future', 'Old']
    if not os.path.exists(eng_source):
        os.makedirs(eng_source)
    for sub_folder in eng_sub_folders:
        sub_folder_path = F'{eng_source}\\{sub_folder}'
        if not os.path.exists(sub_folder_path):
            os.makedirs(sub_folder_path)
    return eng_source


# Create a copy of the change summary excel file from the template
def copy_change_summary(parent, eng_source, reference):
    template_file = f'{parent}\\SOURCE FILES\\TEMPLATES\\CHANGE SUMMARY.xlsm'
    template_dest = f'{eng_source}\\Current\\{reference} CHANGE SUMMARY.xlsm'
    copyfile(template_file, template_dest)


# Create internal shortcut from 'current' sub folder to 'old' sub folder
def create_old_shortcut(eng_source):
    source = f'{eng_source}\\Old'
    eng_dest = f'{eng_source}\\Current\\Old.lnk'
    s = CreateObject(ShellLink)
    s.SetPath(source)
    p = s.QueryInterface(IPersistFile)
    p.Save(eng_dest, True)


# Create shortcut from reference folder to source folder
def create_eng_shortcut(eng_source, directory):
    s = CreateObject(ShellLink)
    s.SetPath(eng_source)
    p = s.QueryInterface(IPersistFile)
    p.Save(directory + r'\ENGINEERING.lnk', True)


def create_supplier_shortcut(parent, reference, directory):
    sup_source = f'{parent}\\SOURCE FILES\\SUPPLIER INFO\\{reference}'
    if not os.path.exists(sup_source):
        os.makedirs(sup_source)
    s = CreateObject(ShellLink)
    s.SetPath(sup_source)
    p = s.QueryInterface(IPersistFile)
    p.Save(directory + r'\SUPPLIER INFO.lnk', True)


def init_ord_directories():
    record_type = 'ORD'
    ord_nos = all_ord_nos()
    for ord_no in ord_nos:
        reference = ord_no[0]
        create_dir(Config.DOC_DIR, record_type, reference)
