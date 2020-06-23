from quatro import sigm_connect, log_connect, dev_check
from os.path import dirname, abspath


class Config:
    LISTEN_CHANNEL = 'folders'

    def __init__(self, main_file_path):
        self.main_file_path = main_file_path
        self.parent_dir = dirname(abspath(main_file_path))
        self.sigm_connection = None
        self.sigm_db_cursor = None
        self.log_connection = None
        self.log_db_cursor = None
        self.DOC_DIR = None
        self.SOURCE_DIR = None
        self.ENG_DIR = None
        self.SUP_DIR = None
        self.ACC_DIR = None
        self.PICS_DIR = None
        self.UNIT_DIR = None
        self.MANUAL_DIR = None

    def set_directories(self):
        self.DOC_DIR = r'E:\DATA\Fortune\SIGMWIN.DTA\QuatroAir\Documents' if not dev_check() else r'Z:\SIGMWIN.DTA\DEV\Documents'
        self.SOURCE_DIR = self.DOC_DIR + f'\\SOURCE FILES'
        self.ENG_DIR = self.SOURCE_DIR + f'\\ENGINEERING'
        self.SUP_DIR = self.SOURCE_DIR + f'\\SUPPLIER INFO'
        self.ACC_DIR = self.SOURCE_DIR + f'\\ACCESSORY WORKSHEET'
        self.PICS_DIR = self.SOURCE_DIR + f'\\PICTURES'
        self.UNIT_DIR = self.SOURCE_DIR + f'\\UNIT WORKSHEET'
        self.MANUAL_DIR = self.SOURCE_DIR + f'\\MANUAL'

    def sql_connections(self):
        self.sigm_connection, self.sigm_db_cursor = sigm_connect(Config.LISTEN_CHANNEL)
        self.log_connection, self.log_db_cursor = log_connect()


if __name__ == "__main__":
    Config(__file__)
