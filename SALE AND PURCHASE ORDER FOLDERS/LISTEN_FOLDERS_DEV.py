import os
import datetime
import re
import pythoncom
from comtypes.client import CreateObject
from comtypes.persist import IPersistFile
from comtypes.shelllink import ShellLink
import psycopg2
import psycopg2.extras
import psycopg2.extensions

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

conn_sigm = psycopg2.connect("host='192.168.0.250' dbname='QuatroAir' user='SIGM' port='5493'")
curs_sigm = conn_sigm.cursor()
conn_sigm.set_client_encoding("latin1")
conn_sigm.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs_sigm.execute("LISTEN folders;")

parent = r'E:\DATA\Fortune\SIGMWIN.DTA\QuatroAir\Documents'

while 1:
    conn_sigm.poll()
    conn_sigm.commit()
    while conn_sigm.notifies:
        notify = conn_sigm.notifies.pop()
        payload = notify.payload

        record_type = payload.split(", ")[0]
        reference = payload.split(", ")[1]
        sigm_string = payload.split(", ")[2]
        user = re.findall(r'(?<=aSIGMWIN\.EXE u)(.*)(?= m)', sigm_string)[0]
        station = re.findall(r'(?<= w)(.*)$', sigm_string)[0]

        log = open(
            "E:\DATA\Fortune\SIGMWIN.DTA\QuatroAir\Documents\REFERENCE FILES\AUTOMATED FILE MANAGEMENT\SALE AND PURCHASE ORDER FOLDERS\log.txt",
            "a")
        timestamp = datetime.datetime.now()
        log_message = f'Folder created for {record_type} {reference} by {user} on workstation {station} at {timestamp}\n'
        log.write(log_message)
        log.close()
        print(log_message)

        directory = parent + '\\' + record_type + '\\' + reference
        if not os.path.exists(directory):
            os.makedirs(directory)

        if record_type == 'PRT':

            eng_source = f'{parent}\SOURCE FILES\ENGINEERING\{reference}'
            if not os.path.exists(eng_source):
                os.makedirs(eng_source)
            s = CreateObject(ShellLink)
            s.SetPath(eng_source)
            p = s.QueryInterface(IPersistFile)
            p.Save(directory + '\\ENGINEERING.lnk', True)

            sup_source = f'{parent}\SOURCE FILES\SUPPLIER INFO\{reference}'
            if not os.path.exists(sup_source):
                os.makedirs(sup_source)
            s = CreateObject(ShellLink)
            s.SetPath(sup_source)
            p = s.QueryInterface(IPersistFile)
            p.Save(directory + '\\SUPPLIER INFO.lnk', True)
