from sigm import add_sql_files, dev_check
from files import init_ord_directories
from listen import init_cursors, listen


def main():
    channel = 'folders'
    sigm_connection, sigm_db_cursor, log_connection, log_db_cursor = init_cursors(channel)

    add_sql_files()

    parent = r'Z:\SIGMWIN.DTA\DEV\Documents' if dev_check() else r'E:\DATA\Fortune\SIGMWIN.DTA\QuatroAir\Documents'

    init_ord_directories(parent, sigm_db_cursor)

    listen(parent, channel)


if __name__ == "__main__":
    main()
