import os
import logging
import json
from docx import Document
from datetime import datetime
import subprocess

# Configuration des templates
TEMPLATES = {
    'Mobile Phone': './templates/template_recommandations_Mobile_Phone.docx',
    'Tablet': './templates/template_recommandations_Tablet.docx',
    'Laptop': './templates/template_recommandations_Laptop.docx'
}

# Chemin vers les logs
log_dir = './logs/log_et_templates'
os.makedirs(log_dir, exist_ok=True)  # Crée le répertoire s'il n'existe pas

# Configuration des logs avec rotation
log_handler = logging.FileHandler(os.path.join(log_dir, 'logs.txt'))
logging.basicConfig(handlers=[log_handler],
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Fonction pour valider le JSON
def validate_json(data):
    required_fields = ['Appareil', 'Date', 'Email_D', 'Cl_type', 'Used_by', 'serial_number_50000227369']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Champs manquants dans le JSON : {', '.join(missing_fields)}")
    try:
        json.loads(data.get('custom_fields', '{}'))
    except json.JSONDecodeError:
        raise ValueError("custom_fields n'est pas un JSON valide")

# Fonction pour créer les placeholders
def create_placeholders(cl_type, data, custom_fields):
    placeholders = {
        '{{Appareil}}': data['Appareil'],
        '{{Date}}': format_date(data['Date']),
        '{{Email}}': data['Email_D'],
        '{{Cl_type}}': data['Cl_type'],
        '{{Used_by}}': data['Used_by'],
        '{{serial_number}}': custom_fields.get('serial_number_50000227369', '...')
    }
    if cl_type == 'Mobile Phone':
        placeholders.update({
            '{{Numéro_de_téléphone}}': custom_fields.get('numro_de_tlphone_50000227396', '...'),
            '{{IMEI}}': custom_fields.get('imei_number_50000227396', '...'),
            '{{PIN}}': custom_fields.get('pin_code_50000227396', '...'),
            '{{PUK}}': custom_fields.get('puk_code_50000227396', '...'),
            '{{Lock}}': custom_fields.get('lock_code_50000227396', '...')
        })
    return placeholders

# Fonction pour formater la date
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b, %Y %H:%M GMT %z')
        return date_obj.strftime('%d/%m/%Y')
    except Exception as e:
        logging.error(f"Erreur lors du formatage de la date : {e}")
        return '...'

# Fonction principale pour remplacer les placeholders
def replace_placeholders(expected_template, template_path, data):
    logging.info(f"Utilisation du template : {expected_template}")

    # Conversion de custom_fields de string JSON à dictionnaire
    try:
        custom_fields = json.loads(data.get('custom_fields', '{}'))
    except json.JSONDecodeError as e:
        logging.error(f"Erreur lors de la conversion de custom_fields : {e}")
        return None

    # Validation des champs essentiels
    missing_fields = []
    for field in ['serial_number_50000227369']:
        if field not in custom_fields:
            missing_fields.append(field)
    
    if missing_fields:
        logging.error(f"Champs manquants dans le JSON : {', '.join(missing_fields)}")
        return None  # Option de retourner None si des champs sont manquants ou continuer avec des valeurs par défaut

    # Création du document à partir du template
    try:
        doc = Document(template_path)

        # Remplacement des placeholders dans le document
        placeholders = {
            '{{Appareil}}': data.get('Appareil', 'Inconnu'),
            '{{Date}}': data.get('Date', 'Inconnue'),
            '{{Email}}': data.get('Email_D', 'Inconnue'),
            '{{Cl_type}}': data.get('Cl_type', 'Inconnu'),
            '{{Used_by}}': data.get('Used_by', 'Inconnu'),
            '{{serial_number}}': custom_fields.get('serial_number_50000227369', 'Inconnu')
        }

        for paragraph in doc.paragraphs:
            for placeholder, value in placeholders.items():
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, value)

        # Sauvegarde du document modifié
        docx_output = f"./documents_finaux/{data.get('Used_by', 'default')}_{expected_template}.docx"
        doc.save(docx_output)
        logging.info(f"Document Word sauvegardé sous : {docx_output}")

        # Conversion en PDF
        pdf_output = docx_output.replace('.docx', '.pdf')
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_output])
        logging.info(f"Document PDF sauvegardé sous : {pdf_output}")

        # Suppression du fichier .docx
        os.remove(docx_output)
        logging.info(f"Fichier Word supprimé : {docx_output}")

        return pdf_output

    except Exception as e:
        logging.error(f"Erreur dans replace_placeholders : {e}")
        return None

# Fonction pour sauvegarder le document dans un sous-dossier
def save_document(cl_type, device_name, user, doc):
    final_dir = os.path.join('./documents_finaux', user)
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    save_path = os.path.join(final_dir, f'{cl_type}_{device_name}.docx')
    doc.save(save_path)
    logging.info(f'Document sauvegardé à : {save_path}')
    return save_path

# Fonction pour convertir le document en PDF et supprimer le fichier .docx
def convert_to_pdf(docx_path):
    try:
        result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path],
                                capture_output=True, text=True)
        if result.returncode == 0:
            pdf_path = docx_path.replace('.docx', '.pdf')
            logging.info(f'Conversion réussie en PDF : {pdf_path}')
            os.remove(docx_path)  # Suppression du fichier .docx après conversion
            logging.info(f'Fichier DOCX supprimé : {docx_path}')
        else:
            logging.error(f"Erreur lors de la conversion en PDF : {result.stderr}")
    except Exception as e:
        logging.error(f"Erreur lors de la conversion en PDF : {e}")

