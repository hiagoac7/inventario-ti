@echo off
REM ============================================================
REM  Build do Coletor TI - gera o .exe e prepara a pasta dist
REM  Basta dar duplo clique neste arquivo.
REM ============================================================
setlocal
cd /d "%~dp0"

echo.
echo === Coletor TI - Build ===
echo Pasta: %cd%
echo.

REM --- Garante que o PyInstaller esta instalado ---
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar o PyInstaller. Verifique se o Python esta no PATH.
        pause
        exit /b 1
    )
)

REM --- Limpa build anterior ---
echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

REM --- Gera o executavel ---
echo.
echo Compilando coletor.exe ...
python -m PyInstaller coletor.spec
if errorlevel 1 (
    echo.
    echo [ERRO] Falha na compilacao.
    pause
    exit /b 1
)

REM --- Copia os arquivos que o programa precisa para o lado do .exe ---
echo.
echo Copiando arquivos de apoio para dist\ ...
if exist usuarios.csv (
    copy /y usuarios.csv dist\ >nul
    echo  - usuarios.csv copiado
) else (
    echo  [AVISO] usuarios.csv nao encontrado na pasta.
)

if exist inventario_ti.db (
    copy /y inventario_ti.db dist\ >nul
    echo  - inventario_ti.db copiado
) else (
    echo  [INFO] inventario_ti.db nao encontrado - sera criado automaticamente no primeiro uso.
)

echo.
echo === CONCLUIDO ===
echo Executavel pronto em: %cd%\dist\coletor.exe
echo Distribua a pasta dist inteira (exe + usuarios.csv + .db).
echo.
pause
endlocal
