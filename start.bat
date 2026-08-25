@echo off
echo ======================================
echo Demarrage du Bot Envoie CV
echo ======================================

IF NOT EXIST "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

call venv\Scripts\activate
echo Verification des dependances...
pip install -r requirements.txt >nul

echo Lancement de l'application...
start http://127.0.0.1:5000
python app.py

pause
