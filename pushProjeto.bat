@echo off
cd /d %~dp0
git add .
git commit -m "Atualização automática do projeto"
git push origin main
pause
