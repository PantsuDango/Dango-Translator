cd /d %~dp0
echo on
set QPT_COLOR=False
set QPT_MODE=Debug
cls
"./Python/python.exe" -c "import sys;sys.path.append('./Python');sys.path.append('./Python/Lib/site-packages');sys.path.append('./Python/Scripts');import qpt.run as run"
pause