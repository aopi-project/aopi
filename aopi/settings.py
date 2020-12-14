import os
from pathlib import Path
from typing import Union

from pydantic import BaseSettings, Field
from tabulate import tabulate

from aopi.arg_parser import parse_args


class Settings(BaseSettings):
    packages_dir: Path = Field("/tmp/aopi/packages")
    aopi_db_file: Path = Field("/tmp/aopi/db.sqlite")
    workers_count: int = 4
    pid_file: str = "/tmp/aopi/server.pid"
    reload: bool = False
    port: int = 8000
    host: str = "0.0.0.0"

    def prepare(self) -> None:
        def create_dir(filename: Union[Path, str]) -> None:
            base_dir = os.path.dirname(filename)
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

        create_dir(self.packages_dir)
        create_dir(self.aopi_db_file)
        create_dir(self.pid_file)

    @classmethod
    def from_args(cls) -> "Settings":
        cli_args = parse_args()
        params = {k: v for k, v in cli_args.__dict__.items() if v is not None}
        return Settings(**params)

    def pprint(self) -> None:
        print("Current settings:")
        safe_data = self.dict()
        print(tabulate(safe_data.items(), stralign="left", tablefmt="plain"))
        print()


settings = Settings.from_args()
settings.prepare()
