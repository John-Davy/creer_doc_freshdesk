from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
from script import replace_placeholders
import os

API_KEY = 'jkGhphxMKSTd6UowRta' # clé API freshdesk

# Vérification et création du dossier de logs
logs_directory = './logs'
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
logs_file = os.path.join(logs_directory, 'app.log')
    
# Configurer le module de logging avec limite de taille du fichier log
log_handler = RotatingFileHandler(logs_file, maxBytes=10000, backupCount=5)
logging.basicConfig(handlers=[log_handler], 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')



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
            errors_occurred = replace_placeholders(raw_data)
            if not errors_occurred :
                return 'Succès', 200
            else :
                return 'Error interne au script.py', 500
        except Exception as e:
            logging.error(f'app.py :\n Erreur lors du traitement du webhook : {e}', exc_info=True)
            return 'app.py :\n Erreur interne du serveur', 500
    else:
        return 'app.py : raw_data inexistant', 400

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

