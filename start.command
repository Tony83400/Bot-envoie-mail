#!/bin/bash
# Ce script permet de démarrer l'application sur Mac en un double-clic.
# Il se place automatiquement dans le dossier du script.
cd "$(dirname "$0")"

echo "======================================"
echo "Démarrage du Bot Envoie CV"
echo "======================================"

# Vérifie si Python 3 est installé
if ! command -v python3 &> /dev/null
then
    echo "Python 3 n'est pas installé. Veuillez l'installer pour continuer."
    read -n 1 -s -r -p "Appuyez sur une touche pour quitter..."
    exit 1
fi

# Création de l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel (cela peut prendre quelques secondes)..."
    python3 -m venv venv
fi

# Activation de l'environnement virtuel
source venv/bin/activate

# Installation des dépendances
echo "Vérification des dépendances..."
pip install -r requirements.txt > /dev/null

# Lancement de l'application
echo "Lancement de l'application sur http://127.0.0.1:5000..."
(sleep 2 && open http://127.0.0.1:5000) &
python3 app.py

# Garder la fenêtre ouverte en cas d'erreur
read -n 1 -s -r -p "L'application s'est arrêtée. Appuyez sur une touche pour fermer..."
