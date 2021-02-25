import sqlite3


def connect_database(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='users'")
    if cur.fetchone()[0] == 0:
        print("DB 셋업 (users)")
        cur.execute(
            "CREATE TABLE users ("
            "id text, money text, join_time text,"
            "check_time text, stock text)"
        )
        con.commit()

    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='stocks'")
    if cur.fetchone()[0] == 0:
        print("DB 셋업 (stocks)")
        cur.execute("CREATE TABLE stocks(name text, history text)")
        con.commit()

    return con
