from flask import Flask, request
import logging
import os
from script import replace_placeholders, TEMPLATES

# Initialiser l'application Flask
app = Flask(__name__)

# Initialisation du système de logs
def init_logging():
    log_dir = './logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, 'app.log'),
                        level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

init_logging()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data is None:
        logging.error('Aucune donnée JSON reçue')
        return 'Aucune donnée JSON reçue', 400

    try:
        cl_type = data.get('Cl_type', 'Unknown')
        if cl_type not in TEMPLATES:
            logging.error(f'Type d\'actif non supporté : {cl_type}')
            return 'Type d\'actif non supporté', 400

        template_path = TEMPLATES[cl_type]
        pdf_path = replace_placeholders(cl_type, template_path, data)

        if pdf_path:
            logging.info(f'PDF généré avec succès : {pdf_path}')
            return 'Succès', 200
        else:
            logging.error('Échec de la génération du PDF')
            return 'Erreur lors de la génération du PDF', 500

    except Exception as e:
        logging.error(f'Erreur lors du traitement du webhook : {str(e)}')
        return 'Erreur interne du serveur', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

