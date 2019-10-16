import quatro
import config
import files
import tasks
from quatro import init_app_log_dir, log


def main():
    init_app_log_dir()
    log(f'Starting {__file__}')
    folders_config = config.Config()
    quatro.add_sql_files(folders_config)
    files.init_ord_directories(folders_config)
    files.init_cli_directories(folders_config)
    quatro.listen(folders_config, tasks.listen_task)


if __name__ == "__main__":
    main()
