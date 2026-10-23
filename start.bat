@echo off
setlocal
call "%~dp0play.bat" %*
exit /b %ERRORLEVEL%
