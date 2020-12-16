import os
from pathlib import Path
from tempfile import gettempdir
from typing import Union

from databases import DatabaseURL
from loguru import logger
from pydantic import BaseSettings, Field
from tabulate import tabulate

from aopi.arg_parser import LogLevel, parse_args

TEMP_DIR = gettempdir()


class Settings(BaseSettings):
    packages_dir: Path = Field(f"{TEMP_DIR}/aopi/packages")
    aopi_db_url: str = Field(f"sqlite:///{TEMP_DIR}/aopi/db.sqlite")
    pid_file: Path = Field(f"{TEMP_DIR}/aopi/server.pid")
    log_level: LogLevel = Field(LogLevel.info)
    workers_count: int = 4
    reload: bool = False
    port: int = 8000
    host: str = "0.0.0.0"

    def prepare(self) -> None:
        def create_dir(filename: Union[Path, str], parent: bool = False) -> None:
            base_dir = filename
            if parent:
                base_dir = os.path.dirname(filename)
            if not os.path.exists(base_dir):
                logger.debug(f"Creating directory {base_dir}")
                os.makedirs(base_dir)

        create_dir(self.packages_dir)
        create_dir(self.pid_file, True)
        db_url = DatabaseURL(self.aopi_db_url)
        if db_url.dialect == "sqlite" and db_url.hostname is None:
            create_dir(db_url.database, True)

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
