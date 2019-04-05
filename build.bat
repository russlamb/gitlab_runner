REM Change working directory  to the source folder
pushd C:\source
REM clear build directories
rmdir build /S /Q
rmdir __pycache__ /S /Q
rmdir dist /S /Q
REM build main.py to dist folder as a single executable called sql_runner.exe 
pyinstaller main.py -F -n sql_runner.exe --hidden-import gitlab --hidden-import gitlab.v4 --hidden-import gitlab.v4.objects -i icon.ico
REM return to previous working directory
popd
