import os
import logging
from docx import Document
from datetime import datetime
import subprocess
import json
import re

# Configurer le module de logging
try:
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
except Exception as e:
    logging.error(f"script.py : Erreur lors de la création du directory './logs' : {e}")
    raise
    
logging.basicConfig(filename='./logs/log_createDoc.txt',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

TEMPLATE_PATH = './templates/template_sortie_materiel.docx'

def get_unique_filename(file_path):
    """ Génère un nom de fichier unique en ajoutant un numéro incrémental si nécessaire. """
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path
    while os.path.isfile(new_file_path):
        new_file_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_file_path
    
# Fonction de formatage de la date
def format_date(date_str):
    """ Convertit une date en chaîne au format 'DD.MM.YYYY' ou retourne une valeur par défaut """
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b, %Y %H:%M GMT %z')  # Format que vous recevez
        return date_obj.strftime('%d.%m.%Y')  # Format désiré pour le document
    except ValueError as e:
        logging.error(f"script.py : Erreur de formatage de la date : {e}")
        return '..............................'  # Valeur par défaut si la conversion échoue

# Fonction pour convertir les données en JSON
def clean_data(data_string):
    try:
        # Nettoyage de la chaîne JSON brute
        cleaned_data = data_string.replace('\\"', '"')  # Remplacer les guillemets échappés
        logging.debug(f"script.py : Données nettoyées : {cleaned_data}")
    except Exception as e:
        logging.error(f"script.py : Erreur lors de la conversion des données en JSON : {e}")
        return None
    return cleaned_data
    
def open_doc(doc_path):
    # Charger le document Word
    if not os.path.isfile(doc_path):
        logging.error(f"script.py : Le fichier template n'existe pas à l'emplacement : {doc_path}")
        return

    try:
        doc = Document(doc_path)
    except Exception as e:
        logging.error(f"script.py : Erreur lors du chargement du document : {e}")
        raise

    return doc
    
def create_json(raw_data, key):
    data = json.loads(raw_data)
    try:
        value = data.get(key)
        logging.debug(f"script.py : valeur de {key} du str en Json : {value}")    
    except Exception as e:
        logging.error(f"script.py : Erreur lors de la lecture {key} comme valeur Json : {e}")
        raise
        
    # Créer dossier si inexistant
def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        logging.error(f"script.py : Erreur lors de la création du directory {path} : {e}")
        raise


def replace_placeholders(doc_path, raw_data):
    logging.debug("********************************** Start script.py **********************************")
    logging.debug(f"script.py : Chemin du fichier template : {doc_path}")    
    
    # Ouvre le document template
    doc = open_doc(doc_path)
        
    # logger de la chaîne brute
    logging.debug(f"script.py : données brutes reçues : {raw_data}")
    
    # création des données Json
    # try :
    create_json(raw_data, "custom_fields")
    data = json.loads(raw_data)
    custom_fields_str = data.get("custom_fields")
    create_json(custom_fields_str, "serial_number_50000227369")
    custom_fields = json.loads(custom_fields_str)
    #except Exception as e:
    #    logging.error(f"script.py : Erreur lors de la création des données Json : {e}")
    #    raise

    # Récupérer les données custom_fields
    num_tel = custom_fields.get('numro_de_tlphone_50000227396', '..............................') or '..............................'
    num_serie = custom_fields.get('serial_number_50000227369', '..............................') or '..............................'
    imei = custom_fields.get('imei_number_50000227396', '..............................') or '..............................'
    pin = custom_fields.get('pin_code_50000227396', '..............................') or '..............................'
    puk = custom_fields.get('puk_code_50000227396', '..............................') or '..............................'
    lock_code = custom_fields.get('lock_code_50000227396', '..............................') or '..............................'
    
    # Récupérer les données data
    nom = data.get('Used_by', '..............................')
    appareil = data.get('Appareil', '..............................')
    date = format_date(data.get('Date', '..............................'))
    cl_type = data.get('Cl_type', 'Inconnu')  
    
    # définir nom de dossier
    nom_dossier = str(nom)

    # Charger et remplacer les placeholders dans le document Word
    placeholders = {
        '{{Numéro_de_téléphone}}': '0' + str(num_tel),
        '{{Numéro_de_série}}': num_serie,
        '{{IMEI}}': imei,
        '{{PIN}}': pin,
        '{{PUK}}': puk,
        '{{Lock}}': lock_code,
        '{{Date}}': date,
        '{{Nom}}': nom,
        '{{Appareil}}': appareil
    }

    # Créer dossier documents finaux si inexistant
    final_dir = './document_finaux'
    create_dir(final_dir)

    # Créer dossier collaborateur si inexistant
    dossier_nom = os.path.join(final_dir, nom_dossier)
    create_dir(dossier_nom)

    # Construire les noms de fichiers en utilisant les valeurs obtenues
    docx_path = os.path.join(dossier_nom, f'Reglement_sortie_{cl_type}_{appareil}_{nom_dossier}.docx')
    docx_path = get_unique_filename(docx_path)
    pdf_path = os.path.join(dossier_nom, f'Reglement_sortie_{cl_type}_{appareil}_{nom_dossier}.pdf')
    pdf_path = get_unique_filename(pdf_path)
    
    # Remplacement des placeholders dans le document Word
    for paragraph in doc.paragraphs:
        for placeholder, value in placeholders.items():
            if placeholder in paragraph.text:
                logging.debug(f"script.py : Remplacement de '{placeholder}' par '{value}'")
                paragraph.text = paragraph.text.replace(placeholder, str(value))

    # Sauvegarder le document modifié en .docx
    try:
        doc.save(docx_path)
        logging.debug(f'script.py : Sauvegarde du document Word modifié : {docx_path}')
    except Exception as e:
        logging.error(f"script.py : Erreur lors de la sauvegarde du document Word : {e}")
        raise

    # Convertir le document Word modifié en PDF avec LibreOffice
    try:
        # Convertir le fichier DOCX en PDF
        result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path],
                                capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"script.py : Erreur lors de la conversion du document Word en PDF : {result.stderr}")
            return

        # Déplacer le fichier PDF généré au bon endroit
        pdf_generated_filename = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
        pdf_generated_path = os.path.join(os.getcwd(), pdf_generated_filename)
        if os.path.exists(pdf_generated_path):
            os.rename(pdf_generated_path, pdf_path)
            logging.debug(f'script.py : Sauvegarde du PDF : {pdf_path}')
        else:
            logging.error(f"script.py : Le fichier PDF généré n'existe pas : {pdf_generated_path}")

    except Exception as e:
        logging.error(f"script.py : Erreur lors de la conversion du document Word en PDF : {e}")
        raise

    # Supprimer le fichier DOCX modifié après la conversion en PDF
    try:
        if os.path.isfile(docx_path):
            os.remove(docx_path)
            logging.debug(f'script.py : Suppression du fichier DOCX modifié : {docx_path}')
    except Exception as e:
        logging.error(f"script.py : Erreur lors de la suppression du fichier DOCX : {e}")
        raise

    return pdf_path

# Code de test placé sous la condition __main__
if __name__ == '__main__':

    #pdf_path = replace_placeholders(TEMPLATE_PATH, data)
    print(f"script.py : PDF généré à l'emplacement {pdf_path}")

