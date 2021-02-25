import sqlite3
import time


class GameUser:
    def __init__(self, con: sqlite3.Connection, userid: str) -> None:
        self.id: str = userid
        self.con = con
        self.cur = con.cursor()

        self.money: int = None
        self.join_time: float = None
        self.check_time: float = None

        self.load()

    @staticmethod
    def exist_user(con: sqlite3.Connection, userid: str) -> bool:
        cur = con.cursor()

        cur.execute("SELECT * FROM user WHERE id=?", (userid,))

        if cur.fetchone():
            return True

        return False

    @staticmethod
    def join(con: sqlite3.Connection, userid: str, gift: int = 10000) -> None:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO user VALUES(?, ?, ?, ?)",
            (userid, str(gift), str(time.time()), "0.0"),
        )
        con.commit()

    def remove(self) -> None:
        self.cur.execute("DELETE FROM user WHERE id=?", (self.id,))
        self.con.commit()
        self.money = None

    def load(self) -> None:
        self.cur.execute("SELECT * FROM user WHERE id=?", (self.id,))
        data = self.cur.fetchone()

        if data:
            self.money = int(data[1])
            self.join_time = float(data[2])
            self.check_time = float(data[3])

    def commit(self):
        self.cur.execute(
            "UPDATE user SET money=?, check_time=? WHERE id=?",
            (str(self.money), str(self.check_time), self.id),
        )
        self.con.commit()
