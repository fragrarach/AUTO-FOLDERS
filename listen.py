import re
from sigm import sigm_connect, log_connect
from files import create_dir, create_eng_sub_folders, copy_change_summary, \
    create_old_shortcut, create_eng_shortcut, create_supplier_shortcut


def init_cursors(channel=None):
    sigm_connection, sigm_db_cursor = sigm_connect(channel) if channel else sigm_connect()
    log_connection, log_db_cursor = log_connect()
    return sigm_connection, sigm_db_cursor, log_connection, log_db_cursor


# Split payload string, return named variables
def payload_handler(payload):
    record_type = payload.split(", ")[0]
    reference = payload.split(", ")[1]
    sigm_string = payload.split(", ")[2]
    user = re.findall(r'(?<=aSIGMWIN\.EXE u)(.*)(?= m)', sigm_string)[0]
    station = re.findall(r'(?<= w)(.*)$', sigm_string)[0]

    return record_type, reference, user, station


def listen(parent, channel=None):
    sigm_connection, sigm_db_cursor, log_connection, log_db_cursor = init_cursors(channel)

    while 1:
        try:
            sigm_connection.poll()
        except:
            print('Database cannot be accessed, PostgreSQL service probably rebooting')
            try:
                sigm_connection.close()
                sigm_connection, sigm_db_cursor = sigm_connect(channel)
                log_connection.close()
                log_connection, log_db_cursor = log_connect()
            except:
                pass
        else:
            sigm_connection.commit()
            while sigm_connection.notifies:
                notify = sigm_connection.notifies.pop()
                raw_payload = notify.payload

                record_type, reference, user, station = payload_handler(raw_payload)
                directory = create_dir(parent, record_type, reference)

                # Additional files/folders for parts
                if record_type == 'PRT':

                    eng_source = create_eng_sub_folders(parent, reference)
                    copy_change_summary(parent, eng_source, reference)
                    create_old_shortcut(eng_source)
                    create_eng_shortcut(eng_source, directory)
                    create_supplier_shortcut(parent, reference, directory)