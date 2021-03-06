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
    subprocess.call(f"{PYPATH} -m pip install inquirer", shell=False)
    import inquirer
try:
    import keyboard
except ImportError:
    subprocess.call(f"{PYPATH} -m pip install keyboard", shell=False)
    import keyboard
try:
    import click
except ImportError:
    subprocess.call(f"{PYPATH} -m pip install click", shell=False)
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
            choices=["1. 종료", "2. 서버 실행", "3. 모듈 설치", "4. 설정 보기"],
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
        subprocess.call(f"{PYPATH} run.py", shell=False)
    elif choice == "3. 모듈 설치":
        click.clear()
        print("모듈을 설치합니다.....")
        subprocess.call(f"{PYPATH} -m pip install -r requirements.txt", shell=False)
        click.clear()
        select_interface()
    elif choice == "4. 설정 보기":
        click.clear()
        settings()
        keyboard.wait("enter")
        click.clear()
        select_interface()
    else:
        click.clear()
        select_interface()


def loadjson(src):
    with open(src, "r", encoding="utf-8") as f:
        return json.load(f)


def savejson(src, data):
    with open(src, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def settings():
    print("[EasyGameBot Launcher]\n\n")
    print("설정 (config.json)\n")
    config_data = loadjson("config.json")
    print("Bot (봇)\n\n")
    print(f'토큰 : {config_data["bot"]["token"]}\n')
    print(f'접두사 : {config_data["bot"]["prefix"]}\n')
    print(f'상테 메세지 : {config_data["bot"]["status"]}\n')
    print(f'파일 로드 : {len(config_data["bot"]["extensions"])}개 로드\n')
    print(f'답장 맨션 : {config_data["bot"]["reply_mention"]}\n\n')
    print("관리자 웹 (admin_tool)\n")
    print(f'호스트 : {config_data["admin_tool"]["host"]}\n')
    print(f'포트 : {config_data["admin_tool"]["port"]}\n')
    print(f'비밀번호 : {config_data["admin_tool"]["password"]}\n')
    print(
        f'웹 주소 : http://{config_data["admin_tool"]["host"]}:{config_data["admin_tool"]["port"]}\n'
    )
    print("\n\n Enter를 누르세요")


# ================================================================================== #

click.clear()
select_interface()
