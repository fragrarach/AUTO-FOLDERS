from quatro import add_sql_files, listen, configuration as c
from config import Config
from files import init_ord_directories, init_cli_directories
from tasks import listen_task
from quatro import init_app_log_dir, log


def main():
    c.config = Config(__file__)
    c.config.get_directories()
    init_app_log_dir()
    log(f'Starting {__file__}')
    c.config.sql_connections()
    add_sql_files()
    init_ord_directories()
    init_cli_directories()
    listen(listen_task)


if __name__ == "__main__":
    main()
