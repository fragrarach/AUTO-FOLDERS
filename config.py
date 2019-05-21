from quatro import sigm_connect, log_connect, dev_check


class Config:
    LISTEN_CHANNEL = 'folders'

    def __init__(self):
        self.sigm_connection, self.sigm_db_cursor = sigm_connect(Config.LISTEN_CHANNEL)
        self.log_connection, self.log_db_cursor = log_connect()

    DOC_DIR = r'E:\DATA\Fortune\SIGMWIN.DTA\QuatroAir\Documents' if not dev_check() else r'Z:\SIGMWIN.DTA\DEV\Documents'
    SOURCE_DIR = DOC_DIR + f'\\SOURCE FILES'
    ENG_DIR = SOURCE_DIR + f'\\ENGINEERING'
    SUP_DIR = SOURCE_DIR + f'\\SUPPLIER INFO'
    ACC_DIR = SOURCE_DIR + f'\\ACCESSORY WORKSHEET'
    PICS_DIR = SOURCE_DIR + f'\\PICTURES'
    UNIT_DIR = SOURCE_DIR + f'\\UNIT WORKSHEET'
    MANUAL_DIR = SOURCE_DIR + f'\\MANUAL'
