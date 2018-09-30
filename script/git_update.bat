@echo off
echo. ©³©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©·
echo. ©§     0. checkout and update    ©§
echo. ©§     1. checkout               ©§
echo. ©§     2. update                 ©§
echo. ©§     3. clone                  ©§
echo. ©§     4. setVersion             ©§
echo. ©§     5. merge                  ©§
echo. ©§     6. tag                    ©§
echo. ©»©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¥©¿
set /P choice=Make a choice:
if %choice% equ 0 ( goto branch
) else if %choice% equ 1 ( goto branch
) else if %choice% equ 2 ( goto branch
) else if %choice% equ 3 ( goto clone
) else if %choice% equ 4 ( goto version
) else if %choice% equ 5 ( goto merge
) else if %choice% equ 6 ( goto tag
)

:branch
set /P branch=Input branch to update:
if %choice% equ 1 (
 echo. checkout %branch%
 python pygit.py --checkout %branch%
) else if %choice% equ 2 (
 echo. update %branch%
 python pygit.py --update %branch%
)else if %choice% equ 0 (
 echo. checkout and update %branch%
 python pygit.py %branch%
)
goto :eof

:version
set /P version=Input Version:
echo. %version%
python pygit.py --version %version%
goto :eof

:clone
python pygit.py --clone
goto :eof

:merge
set /P from=merge from:
set /P to=merge to:
echo. merge from %from% to %to%
python pygit.py --merge %from% %to%
goto :eof

:tag
set /P branch=branch to tag:
set /P tag=tag:
echo. tag %tag% in branch %branch%
python pygit.py --tag %branch% %tag%
goto :eof