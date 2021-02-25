import sqlite3
from typing import Dict, Union, List
from json import load


def get_config() -> Dict[str, Dict[str, Union[str, int, List[str]]]]:
    with open("./config.json", encoding="utf-8") as f:
        return load(f)


def connect_database(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)

    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='user'")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "CREATE TABLE user(id text, money text, join_time text, check_time text)"
        )
        con.commit()

    return con
