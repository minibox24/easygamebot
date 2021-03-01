import sqlite3
from typing import List, Dict, Union
import json


def connect_database(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='users'")
    if cur.fetchone()[0] == 0:
        print("DB 셋업 (users)")
        cur.execute(
            "CREATE TABLE users ("
            "id text, money text, items integer,"
            "join_time text, check_time text, stock text)"
        )
        con.commit()

    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='stocks'")
    if cur.fetchone()[0] == 0:
        print("DB 셋업 (stocks)")
        cur.execute(
            "CREATE TABLE stocks(name text, price text, cap text, history text)"
        )
        con.commit()

    return con


def init_stock(con: sqlite3.Connection, stocks: List[str], stock_default_price: int):
    stocks = list(set(stocks))
    if len(stocks) > 10:
        exit("주식 개수는 10개 이하여야합니다.")

    cur = con.cursor()
    cur.execute("SELECT * FROM stocks")
    db_stocks = list(map(lambda x: x[0], cur.fetchall()))

    create_stocks = []
    del_stocks = []

    for i in stocks:
        if i not in db_stocks:
            create_stocks.append(i)

    for i in db_stocks:
        if i not in stocks:
            del_stocks.append(i)

    if del_stocks:
        for i in del_stocks:
            print(f"주식 [{i}] 삭제")
            cur.execute("DELETE FROM stocks WHERE name=?", (i,))

        cur.execute("SELECT * FROM users")

        for i in cur.fetchall():
            data = json.loads(i[4])
            for j in del_stocks:
                if data.get(j):
                    del data[j]

            cur.execute(
                "UPDATE users SET stock=? WHERE id=?",
                (json.dumps(data, ensure_ascii=False), i[0]),
            )

        con.commit()

    if create_stocks:
        for i in create_stocks:
            print(f"주식 [{i}] 생성")
            cur.execute(
                "INSERT INTO stocks VALUES (?, ?, ?, ?)",
                (i, str(stock_default_price), "0", "[]"),
            )

        cur.execute("SELECT * FROM users")

        for i in cur.fetchall():
            data = json.loads(i[4])
            for j in create_stocks:
                data[j] = []

            cur.execute(
                "UPDATE users SET stock=? WHERE id=?",
                (json.dumps(data, ensure_ascii=False), i[0]),
            )

        con.commit()


def get_stock_info(
    con: sqlite3.Connection, name: str
) -> Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]:
    cur = con.cursor()

    cur.execute("SELECT * FROM stocks WHERE name=?", (name,))
    data = cur.fetchone()

    if data:
        return {
            "price": int(data[1]),
            "cap": int(data[2]),
            "history": json.loads(data[3]),
        }
    else:
        raise NameError(f"Not Found Stock: {name}")
