import os
import secrets
from pathlib import Path
from tempfile import gettempdir
from typing import Union

from databases import DatabaseURL
from loguru import logger
from pydantic import BaseModel, Field
from tabulate import tabulate

from aopi.arg_parser import LogLevel, parse_args

TEMP_DIR = Path(gettempdir())


class Settings(BaseModel):
    packages_dir: Path = Field(TEMP_DIR / "aopi/packages")
    aopi_db_url: str = Field(f"sqlite:///{TEMP_DIR}/aopi/db.sqlite")
    pid_file: Path = Field(TEMP_DIR / "aopi/server.pid")
    secret_file: Path = Field(TEMP_DIR / "aopi/secret")
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    log_level: LogLevel = Field(LogLevel.info)
    workers_count: int = 4
    reload: bool = False
    port: int = 8000
    host: str = "0.0.0.0"
    no_ui: bool = False
    enable_users: bool = False

    def prepare(self) -> None:
        def create_dir(filename: Union[Path, str], parent: bool = True) -> None:
            base_dir = filename
            if parent:
                base_dir = os.path.dirname(filename)
            if not os.path.exists(base_dir):
                logger.debug(f"Creating directory {base_dir}")
                os.makedirs(base_dir)

        create_dir(self.pid_file)
        create_dir(self.secret_file)
        create_dir(self.packages_dir, False)
        db_url = DatabaseURL(self.aopi_db_url)
        if db_url.dialect == "sqlite" and db_url.hostname is None:
            create_dir(db_url.database, True)
        if not self.secret_file.exists():
            self.secret_file.write_text(secrets.token_urlsafe(128))
        self.jwt_secret = self.secret_file.read_text()

    @classmethod
    def from_args(cls) -> "Settings":
        cli_args = parse_args()
        params = {k: v for k, v in cli_args.__dict__.items() if v is not None}
        return Settings(**params)

    def pprint(self) -> None:
        print("Current settings:")
        safe_data = self.dict(exclude={"jwt_secret"})
        print(tabulate(safe_data.items(), stralign="left", tablefmt="plain"))
        print()


settings = Settings.from_args()
settings.prepare()
