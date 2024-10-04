from flask import Flask, request, jsonify
import logging
from script import replace_placeholders
import json
import re
import os
from logging.handlers import RotatingFileHandler

# Initialisation des logs
def init_logging():
    log_dir = './logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, 'log.txt')
    log_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)

    logging.basicConfig(handlers=[log_handler],
                        level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')

init_logging()

# Créer l'objet Flask
app = Flask(__name__)

# Définir la route pour le webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    logging.debug("""
    *********************************************************************************************************
               ********************************** Start app.py **********************************
    *********************************************************************************************************""")
    
    # Récupérer les données brutes envoyées par Freshdesk
    try:
        raw_data = request.data.decode('utf-8')  # Récupère les données brutes
        logging.debug(f"app.py :\n Données brutes reçues : {raw_data}")
    except Exception as e:
        logging.error(f"app.py :\n Erreur lors de la récupération des données brutes : {e}", exc_info=True)
        return jsonify({"app.py :\n error": "Erreur lors de la récupération des données brutes"}), 400
            
    if raw_data:
    # Traiter les données JSON ou la chaîne brute
        try:
            replace_placeholders(raw_data)
            return '************************************ app.py : End ************************************\n', 500
        except Exception as e:
            return f'app.py : Erreur interne du serveur : {e}\n', 500
    else:
        return 'app.py : raw_data inexistant', 400

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

