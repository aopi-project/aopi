import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, dest="host", help="Application host")
    parser.add_argument("--port", type=int, dest="port", help="Application port")
    parser.add_argument(
        "-r",
        "--reload",
        action="store_true",
        dest="reload",
        help="Reload application on change (Only for Gunicorn workers)",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        dest="workers_count",
        help="Number of application processes. (Only for Gunicorn workers)",
    )
    parser.add_argument(
        "--pid-file",
        type=str,
        dest="pid_file",
        help="Path to file where to store "
        "server application ID. (Only for Gunicorn workers)",
    )
    parser.add_argument(
        "-d", "--database", type=str, dest="aopi_db_file", help="Database file"
    )
    parser.add_argument(
        "--packages",
        type=str,
        dest="packages_dir",
        help="Path to folder where to store actual packages",
    )
    return parser.parse_args()
