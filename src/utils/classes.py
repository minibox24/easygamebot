import sqlite3


class GameUser:
    def __init__(self, con: sqlite3.Connection, userid: str) -> None:
        self.id: str = userid
        self.con = con
        self.cur = con.cursor()
        self.money = None
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
        cur.execute("INSERT INTO user VALUES(?, ?)", (userid, str(gift)))
        con.commit()

    def remove(self) -> None:
        self.cur.execute("DELETE FROM user WHERE id=?", (self.id,))
        self.con.commit()
        self.money = None

    def load(self) -> None:
        self.cur.execute("SELECT * FROM user WHERE id=?", (self.id,))
        data = self.cur.fetchone()

        if data:
            self.money = data[1]

    def commit(self):
        self.cur.execute(
            "UPDATE user SET money=? WHERE id=?", (str(self.money), self.id)
        )
        self.con.commit()
