#!/bin/bash

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Ouvrir le navigateur par défaut
open http://localhost:5001 &

# Lancer le serveur Flask
python scrapper.py
