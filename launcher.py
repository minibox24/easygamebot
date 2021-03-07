import subprocess
import time
import json
import sys
import os

MSYS2 = sys.platform.startswith("win") and ("GCC" in sys.version)
APP_ENGINE = "APPENGINE_RUNTIME" in os.environ and "Development/" in os.environ.get(
    "SERVER_SOFTWARE", ""
)
WIN = sys.platform.startswith("win") and not APP_ENGINE and not MSYS2
PYPATH = sys.executable
try:
    import inquirer
except ImportError:
    subprocess.call(f"{PYPATH} -m pip install inquirer", shell=platform_settings())
    import inquirer
try:
    import click
except ImportError:
    subprocess.call(f"{PYPATH} -m pip install click", shell=platform_settings())
    import click

# ================================================================================== #
# util functions #
def select_interface():
    print("[EasyGameBot Launcher]\n")
    print("프로그래밍을 몰라도 쉽게 나만의 디스코드 게임봇을.\n\n")
    print("GitHub: https://github.com/minibox24/easygamebot\n\n")
    select_menu = [
        inquirer.List(
            "MENU",
            message="메뉴를 선택하세요",
            choices=["1. 종료", "2. 서버 실행", "3. 모듈 설치"],
        ),
    ]
    choice = inquirer.prompt(select_menu)
    case(choice["MENU"])


def isatty(stream):
    try:
        return stream.isatty()
    except Exception:
        return False


def case(choice: str):
    if choice == "1. 종료":
        exit()
    elif choice == "2. 서버 실행":
        click.clear()
        print("서버를 실행합니다....")
        subprocess.call(f"{PYPATH} run.py", shell=platform_settings())
    elif choice == "3. 모듈 설치":
        click.clear()
        print("모듈을 설치합니다.....")
        subprocess.call(f"{PYPATH} -m pip install -r requirements.txt", shell=platform_settings())
        click.clear()
        select_interface()
    else:
        click.clear()
        select_interface()


def loadjson(src):
    with open(src, "r", encoding="utf-8") as f:
        return json.load(f)

def platform_settings():
    if not isatty(sys.stdout):
        return True
    if WIN:
        return False
    else:
        return True

def savejson(src, data):
    with open(src, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# ================================================================================== #

click.clear()
select_interface()
