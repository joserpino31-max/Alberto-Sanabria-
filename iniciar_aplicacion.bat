@echo off
chcp 65001 > nul
title Sistema de Personal - Escuela Alberto Sanabria (MPPE)

echo =========================================================================
echo    SISTEMA DE CONTROL DE PERSONAL - ESCUELA "ALBERTO SANABRIA"
echo    Ministerio del Poder Popular para la Educacion (MPPE)
echo =========================================================================
echo.
echo Iniciando servidor local en http://127.0.0.1:5000...
echo.

cd /d "%~dp0"

start "" http://127.0.0.1:5000

python app.py

pause
