chcp 65001
@echo off
set "PATH=%CD%\envs\facefusion;%CD%\envs\facefusion\Library\mingw-w64\bin;%CD%\envs\facefusion\Library\usr\bin;%CD%\envs\facefusion\Library\bin;%CD%\envs\facefusion\Scripts;%CD%\envs\facefusion\bin;%CD%;%PATH%";
python run.py --execution-providers cuda --skip-download --open-browser