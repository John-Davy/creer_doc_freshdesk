import os
import logging
from docx import Document
from datetime import datetime
import subprocess
import json

# Chemins vers les différents templates en fonction du type d'actif
TEMPLATES = {
    'Mobile Phone': './templates/template_recommandations_Mobile_Phone.docx',
    'Laptop': './templates/template_recommandations_Laptop.docx',
    'Tablet': './templates/template_recommandations_Tablet.docx'
}

# Initialisation des logs
def init_logging():
    log_dir = './logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, 'log_et_templates.log'),
                        level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

init_logging()

def get_unique_filename(file_path):
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path
    while os.path.isfile(new_file_path):
        new_file_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_file_path

def convert_to_json(data_string):
    """Convertit la chaîne de custom_fields en JSON."""
    try:
        json_data = json.loads(data_string)
        return json_data
    except json.JSONDecodeError as e:
        logging.error(f"Erreur lors de la conversion en JSON : {e}")
        return {}

def replace_placeholders(cl_type, doc_path, data):
    try:
        custom_fields = convert_to_json(data.get("custom_fields", "{}"))

        # Charger le document Word
        doc = Document(doc_path)

        placeholders = {
            '{{Appareil}}': data.get('Appareil', 'Inconnu'),
            '{{Date}}': format_date(data.get('Date', '')),
            '{{Email_D}}': data.get('Email_D', ''),
            '{{Cl_type}}': data.get('Cl_type', ''),
            '{{Nom}}': data.get('Used_by', 'Inconnu'),  # Correction: Remplacement de {{Nom}} par Used_by
            '{{Numéro_de_série}}': custom_fields.get('serial_number_50000227369', '...................')
        }

        # Gestion spécifique pour Mobile Phone
        if cl_type == 'Mobile Phone':
            placeholders.update({
                '{{Numéro_de_téléphone}}': custom_fields.get('numro_de_tlphone_50000227396', '...................'),
                '{{IMEI}}': custom_fields.get('imei_number_50000227396', '...................'),
                '{{PIN}}': custom_fields.get('pin_code_50000227396', '...................'),
                '{{PUK}}': custom_fields.get('puk_code_50000227396', '...................'),
                '{{Lock}}': custom_fields.get('lock_code_50000227396', '...................')
            })

        # Remplacer les placeholders dans le document
        for paragraph in doc.paragraphs:
            for key, value in placeholders.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(key, value)

        # Créer le dossier pour enregistrer le PDF
        used_by = data.get('Used_by', 'Inconnu')
        output_dir = f'./documents_finaux/{used_by}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Enregistrer le fichier modifié
        docx_filename = f'{used_by}_{cl_type}.docx'
        docx_path = os.path.join(output_dir, docx_filename)
        docx_path = get_unique_filename(docx_path)
        doc.save(docx_path)

        # Convertir en PDF
        pdf_filename = f'{used_by}_{cl_type}.pdf'
        pdf_path = os.path.join(output_dir, pdf_filename)
        pdf_path = get_unique_filename(pdf_path)

        if convert_docx_to_pdf(docx_path, pdf_path):
            # Supprimer le fichier DOCX après la conversion
            os.remove(docx_path)
            logging.debug(f"Fichier DOCX supprimé : {docx_path}")
            return pdf_path
        else:
            logging.error("Échec de la conversion en PDF.")
            return None

    except Exception as e:
        logging.error(f"Erreur dans replace_placeholders : {e}")
        return None

def convert_docx_to_pdf(docx_path, pdf_path):
    try:
        result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path, '--outdir', os.path.dirname(pdf_path)],
                                capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            logging.error(f"Erreur lors de la conversion en PDF : {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Erreur lors de la conversion en PDF : {e}")
        return False

def format_date(date_str):
    try:
        if date_str:
            date_obj = datetime.strptime(date_str, '%a, %d %b, %Y %H:%M GMT %z')
            return date_obj.strftime('%d.%m.%Y')
        else:
            return '...................'
    except ValueError as e:
        logging.error(f"Erreur de format de date : {e}")
        return '...................'

