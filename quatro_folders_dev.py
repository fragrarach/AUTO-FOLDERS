import quatro
import config
import files
import tasks


def main():
    folders_config = config.Config()
    quatro.add_sql_files(folders_config)
    files.init_ord_directories(folders_config)
    quatro.listen(folders_config, tasks.listen_task)


if __name__ == "__main__":
    main()
