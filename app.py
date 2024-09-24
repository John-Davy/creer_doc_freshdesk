from flask import Flask, request, jsonify
import logging
from script import replace_placeholders, TEMPLATE_PATH
import json
import re
import os

# Configurer le module de logging
logs_directory = './logs'
logs_file = os.path.join(logs_directory, 'log_createDoc.txt')

# Vérification et création du dossier avant le démarrage de l'application Flask
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

# Configurer le module de logging pour écrire dans log_createDoc.txt
logging.basicConfig(filename=logs_file,
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Créer l'objet Flask
app = Flask(__name__)

# Définir la route pour le webhook
@app.route('/webhook', methods=['POST'])
def webhook():
        
    try:
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
    except Exception as e:
        logging.error(f"script.py : Erreur lors de la création du directory './logs' : {e}")
        raise
    
    logging.debug("********************************** Start app.py **********************************")
    # Récupérer les données brutes envoyées par Freshdesk
    try:
        raw_data = request.data.decode('utf-8')  # Récupère les données brutes
        logging.debug(f"app.py : Données brutes reçues : {raw_data}")
    except Exception as e:
        logging.error(f"app.py : Erreur lors de la récupération des données brutes : {e}")
        return jsonify({"app.py : error": "Erreur lors de la récupération des données brutes"}), 400

    # Traiter les données JSON ou la chaîne brute
    if raw_data:
        try:
            pdf_path = replace_placeholders(TEMPLATE_PATH, raw_data)
            logging.info(f'app.py : PDF généré à l\'emplacement {pdf_path}')
            return 'app.py : Succès', 200
        except Exception as e:
            logging.error(f'app.py : Erreur lors du traitement du webhook : {e}')
            return 'app.py : Erreur interne du serveur', 500
    else:
        return 'app.py : Format de données non reconnu', 400

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

