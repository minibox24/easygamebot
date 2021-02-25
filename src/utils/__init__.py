from typing import Dict, Union, List
from json import load
from datetime import datetime


def get_config() -> Dict[str, Dict[str, Union[str, int, List[str]]]]:
    with open("./config.json", encoding="utf-8") as f:
        return load(f)


def timestamp_to_timestr(timestamp: float) -> str:
    dt = datetime.fromtimestamp(timestamp)
    ampm = "오전" if dt.hour < 12 else "오후"
    hour = dt.hour if dt.hour <= 12 else dt.hour - 12
    return f"{dt.year}년 {dt.month}월 {dt.day}일 {ampm} {hour}시 {dt.minute}분 {dt.second}초"


def seconds_to_timestr(second: int) -> str:
    h = 0
    m = 0

    if second >= 3600:
        h = second // 3600
        second -= h * 3600

    if second >= 60:
        m = second // 60
        second -= m * 60

    timetuple = []
    if h != 0:
        timetuple.append(f"{h}시간")
    if m != 0:
        timetuple.append(f"{m}분")
    if second != 0:
        timetuple.append(f"{second}초")

    return " ".join(timetuple)


def format_money(money: int, unit: str) -> str:
    return f"{format(money, ',')}{unit}"
