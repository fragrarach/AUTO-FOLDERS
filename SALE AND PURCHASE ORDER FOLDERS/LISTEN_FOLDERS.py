import os
import datetime
import re
import psycopg2.extensions
from sigm import sigm_conn, log_conn, add_sql_files
from comtypes.client import CreateObject
from comtypes.persist import IPersistFile
from comtypes.shelllink import ShellLink
from shutil import copyfile


# PostgreSQL DB connection configs
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


# Split payload string, return named variables
def payload_handler(payload):
    record_type = payload.split(", ")[0]
    reference = payload.split(", ")[1]
    sigm_string = payload.split(", ")[2]
    user = re.findall(r'(?<=aSIGMWIN\.EXE u)(.*)(?= m)', sigm_string)[0]
    station = re.findall(r'(?<= w)(.*)$', sigm_string)[0]

    return record_type, reference, user, station


# Log file creation
def log_handler(record_type, reference, user, station, parent):
    timestamp = datetime.datetime.now()
    log_message = \
        f'Folder created for {record_type} {reference} by {user} on workstation {station} at {timestamp}\n'
    print(log_message)

    # TODO : Convert from log file to table on LOG DB
    log = open(
        f"{parent}\REFERENCE FILES\AUTOMATED FILE MANAGEMENT\SALE AND PURCHASE ORDER FOLDERS\log.txt",
        "a")
    log.write(log_message)
    log.close()


# Generate top level reference folder
def create_dir(parent, record_type, reference):
    directory = f'{parent}\\{record_type}\\{reference}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


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


def main():
    channel = 'folders'
    global conn_sigm, sigm_query, conn_log, log_query
    conn_sigm, sigm_query = sigm_conn(channel)
    conn_log, log_query = log_conn()

    add_sql_files()

    parent = r'E:\DATA\Fortune\SIGMWIN.DTA\QuatroAir\Documents'
    while 1:
        try:
            conn_sigm.poll()
        except:
            print('Database cannot be accessed, PostgreSQL service probably rebooting')
            try:
                conn_sigm.close()
                conn_sigm, sigm_query = sigm_conn()
                conn_log.close()
                conn_log, log_query = log_conn()
            except:
                pass
        else:
            conn_sigm.commit()
            while conn_sigm.notifies:
                notify = conn_sigm.notifies.pop()
                raw_payload = notify.payload

                record_type, reference, user, station = payload_handler(raw_payload)
                log_handler(record_type, reference, user, station, parent)
                directory = create_dir(parent, record_type, reference)

                # Additional files/folders for parts
                if record_type == 'PRT':

                    eng_source = create_eng_sub_folders(parent, reference)
                    copy_change_summary(parent, eng_source, reference)
                    create_old_shortcut(eng_source)
                    create_eng_shortcut(eng_source, directory)
                    create_supplier_shortcut(parent, reference, directory)


main()
