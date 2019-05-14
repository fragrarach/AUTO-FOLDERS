import re
from sigm import sigm_connect, log_connect
from config import Config
from files import create_dir, extend_dir, rename_prt_no


# Split payload string, return named variables
def payload_handler(payload):
    record_type = payload.split("], [")[0][1:]
    reference = payload.split("], [")[1]
    sigm_string = payload.split("], [")[-1][:-1]
    user = re.findall(r'(?<=aSIGMWIN\.EXE u)(.*)(?= m)', sigm_string)[0]
    station = re.findall(r'(?<= w)(.*)$', sigm_string)[0]

    return record_type, reference, user, station


def listen():
    while 1:
        try:
            Config.SIGM_CONNECTION.poll()
        except:
            print('Database cannot be accessed, PostgreSQL service probably rebooting')
            try:
                Config.SIGM_CONNECTION.close()
                Config.SIGM_CONNECTION, Config.SIGM_DB_CURSOR = sigm_connect(Config.LISTEN_CHANNEL)
                Config.LOG_CONNECTION.close()
                Config.LOG_CONNECTION, Config.LOG_DB_CURSOR = log_connect()
            except:
                pass
        else:
            Config.SIGM_CONNECTION.commit()
            while Config.SIGM_CONNECTION.notifies:
                notify = Config.SIGM_CONNECTION.notifies.pop()
                raw_payload = notify.payload

                record_type, reference, user, station = payload_handler(raw_payload)

                if record_type != 'PRT RENAME':
                    directory = create_dir(record_type, reference)
                    # Additional files/folders for parts
                    if record_type == 'PRT':
                        prt_no = reference
                        prt_folder = directory
                        extend_dir(prt_no, prt_folder)
                else:
                    old_prt_no = reference.split("}, {")[0][1:]
                    new_prt_no = reference.split("}, {")[1][:-1]
                    rename_prt_no(old_prt_no, new_prt_no)


if __name__ == "__main__":
    listen()
