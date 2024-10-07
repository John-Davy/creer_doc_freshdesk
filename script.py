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

<<<<<<< HEAD
# Initialisation des logs
def init_logging():
    log_dir = './logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
=======
# Définir le chemin du template
TEMPLATE = {"Mobile Phone" : './templates/template_recommandations_Mobile_Phone.docx',
            "Laptop" : './templates/template_recommandations_Laptop.docx',
            "Tablet" : './templates/template_recommandations_Tablet.docx'}
>>>>>>> main

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

<<<<<<< HEAD
def convert_to_json(data_string):
    """Convertit la chaîne de custom_fields en JSON."""
    try:
        json_data = json.loads(data_string)
        return json_data
=======


def open_doc(doc_path):
    """ Crée une instance du template et la renvoie """
    try:
        if not os.path.isfile(doc_path):
            raise FileNotFoundError(f"Le fichier template n'existe pas à l'emplacement : {doc_path}")
        doc = Document(doc_path)
        return doc
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors du chargement du document : {e}", exc_info=True)
        raise

def create_json(raw_data):
    """ Converti la chaine de caractère et renvoie un object JSON """
    try:
        data = json.loads(raw_data)
>>>>>>> main
    except json.JSONDecodeError as e:
        logging.error(f"Erreur lors de la conversion en JSON : {e}")
        return {}

def replace_placeholders(cl_type, doc_path, data):
    try:
<<<<<<< HEAD
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
=======
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors de la création du répertoire {path} : {e}", exc_info=True)
        raise

def create_placeholders(cl_type, data, custom_fields):
    """ Crée le dictionnaire avec les bonnes clefs et valeurs pour remplir le doc """

    placeholders = {}
    
    if cl_type == 'Mobile Phone' :
        placeholders = {
            '{{Numéro_de_téléphone}}': '0' + str(
                custom_fields.get('numro_de_tlphone_50000227396', '.....................') or '.....................'),
            '{{IMEI}}': (
                custom_fields.get('imei_number_50000227396', '.....................') or '.....................'),
            '{{PIN}}': (
                custom_fields.get('pin_code_50000227396', '.....................') or '.....................'),
            '{{PUK}}': (
                custom_fields.get('puk_code_50000227396', '.....................') or '.....................'),
            '{{Lock}}': (
                custom_fields.get('lock_code_50000227396', '.....................') or '.....................')
        }
    elif cl_type not in ['Tablet', 'Laptop', 'Mobile Phone']:
        raise ValueError("Le type d'actif reçu n'est pas géré par ce script")
    
    
    placeholders["{{Date}}"] = format_date(str(data.get('Date', 'date_is_None'))) or format_date(str(datetime.now()))
    placeholders["{{Nom}}"] = data.get('Used_by', '.....................') or '.....................'
    placeholders["{{Appareil}}"] = data.get('Appareil', '.....................') or '.....................' 
    
    placeholders["{{Numéro_de_série}}"] = custom_fields.get('serial_number_50000227369', '.....................') or '.....................'
        
    return placeholders

def replace_placeholders(raw_data):
    """ Remplace les données dans le document template, modifie son nom, et l'enregistre au bon endroit """
    
    try:
        # création des JSON
        data = create_json(raw_data)
        custom_fields = create_json(data.get("custom_fields"))
            
        # récupère le type d'actif
        cl_type = data.get('Cl_type', 'type pas pris en charge') or 'type pas pris en charge'
      
        # définir doc_path le chemin du fichier template à remplir
        try :
            doc_path = TEMPLATE[cl_type]
        except Exception as e :
            logging.error(f"\nValeur de cl_type = {cl_type}, erreur {e}\n")
        
        # créer les champs à insérer dans le doc
        placeholders = create_placeholders(cl_type, data, custom_fields)

        # ouvrir doc template
        doc = open_doc(doc_path)
        
        # créer les dossiers de destination
        create_dir('./documents_finaux')
        create_dir(os.path.join('./documents_finaux', placeholders["{{Nom}}"]))
        dossier_nom = os.path.join('./documents_finaux', placeholders["{{Nom}}"])

        docx_path = get_unique_filename(os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Appareil}}"]}_{placeholders["{{Nom}}"]}.docx'))
        pdf_path = get_unique_filename(os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Appareil}}"]}_{placeholders["{{Nom}}"]}.pdf'))
>>>>>>> main

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

<<<<<<< HEAD
        # Convertir en PDF
        pdf_filename = f'{used_by}_{cl_type}.pdf'
        pdf_path = os.path.join(output_dir, pdf_filename)
        pdf_path = get_unique_filename(pdf_path)

        if convert_docx_to_pdf(docx_path, pdf_path):
            # Supprimer le fichier DOCX après la conversion
=======
        # Convertir en .PDF
        result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path], capture_output=True, text=True)
        if result.returncode != 0:
            raise subprocess.SubprocessError(f"Erreur lors de la conversion en PDF : {result.stderr}")
        
        # Récupère le nom du fichier et ajoute .pdf
        pdf_generated_filename = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
        # Récupère le chemin vers le fichier .PDF généré
        pdf_generated_path = os.path.join(os.getcwd(), pdf_generated_filename)
        # Déplacer le .PDF à pdf_path
        if os.path.exists(pdf_generated_path):
            os.rename(pdf_generated_path, pdf_path)
        else:
            raise FileNotFoundError(f"Le fichier PDF généré n'existe pas :\n {pdf_generated_path}")
            
        # Effacer le .docx
        if os.path.isfile(docx_path):
>>>>>>> main
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

