from flask import Flask, request
import logging
from script import replace_placeholders, TEMPLATES  # Importez la fonction et les templates

app = Flask(__name__)

# Configurer le logging pour app.py
log_handler = logging.FileHandler('./logs/app.log')
logging.basicConfig(handlers=[log_handler],
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data is None:
        logging.error('Aucune donnée JSON reçue')
        return 'Aucune donnée JSON reçue', 400

    cl_type = data.get('Cl_type')
    if cl_type not in TEMPLATES:
        logging.error(f"Type d'actif non géré : {cl_type}")
        return 'Type d\'actif non géré', 400

    try:
        pdf_path = replace_placeholders(cl_type, TEMPLATES[cl_type], data)
        logging.info(f'PDF généré à l\'emplacement {pdf_path}')
        return 'Succès', 200
    except Exception as e:
        logging.error(f'Erreur lors du traitement du webhook : {e}')
        return 'Erreur interne du serveur', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

