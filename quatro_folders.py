from sigm import add_sql_files
from files import init_ord_directories
from listen import listen


def main():
    add_sql_files()
    init_ord_directories()
    listen()


if __name__ == "__main__":
    main()
