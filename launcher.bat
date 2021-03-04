@echo off

title EasyGameBot Launcher

:TEXT
echo EasyGameBot Launcher
echo GitHub https://github.com/minibox24/easygamebot
echo.
echo 0. 종료
echo 1. 서버 실행
echo 2. 모듈 설치
echo.

goto MAIN

:MAIN
set /p input=">>> "

if /i "%input%" == "0" goto EXIT
if /i "%input%" == "1" goto RUN
if /i "%input%" == "2" goto INSTALL

goto MAIN

:RUN
echo 서버를 실행합니다.
python run.py
echo.
goto TEXT

:INSTALL
echo 모듈을 설치합니다.
python -m pip install -r requirements.txt
echo 모듈 설치를 완료했습니다.
echo.
goto TEXT

:EXIT