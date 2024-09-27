import os
import logging
from docx import Document
from datetime import datetime
import subprocess
import json


# Définir le chemin du template
TEMPLATE_PATH_MOBILE_PHONE = './templates/template_recommandations_Mobile_Phone.docx'
TEMPLATE_PATH_LAPTOP = './templates/template_recommandations_Laptop.docx'
TEMPLATE_PATH_TABLET = './templates/template_recommandations_Tablet.docx'


    
# Renvoi un nom de fichier unique
def get_unique_filename(file_path):
    """ Génère un nom de fichier unique en ajoutant un numéro incrémental si nécessaire. """
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path
    while os.path.isfile(new_file_path):
        new_file_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_file_path
    
def format_date(date_str):
    """ Convertit une date en chaîne au format 'DD.MM.YYYY' ou retourne une valeur par défaut """
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b, %Y %H:%M GMT %z')
        return date_obj.strftime('%d.%m.%Y')
    except ValueError as e:
        logging.error(f"script.py :\n Erreur de formatage de la date : {e}", exc_info=True)
        return (datetime.now()).strftime("%d.%m.%Y")

def clean_data(data_string):
    try:
        cleaned_data = data_string.replace('\"', '"')
        logging.debug(f"script.py :\n Données nettoyées : {cleaned_data}")
        return cleaned_data
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors du nettoyage des données : {e}", exc_info=True)
        return None

def open_doc(doc_path):
    try:
        if not os.path.isfile(doc_path):
            raise FileNotFoundError(f"Le fichier template n'existe pas à l'emplacement : {doc_path}")
        doc = Document(doc_path)
        return doc
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors du chargement du document : {e}", exc_info=True)
        raise

def create_json(raw_data):
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError as e:
        logging.error(f"script.py :\n Erreur lors du parsing du JSON : {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors de l'obtention du JSON : {e}", exc_info=True)
        raise
    
    return data

def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors de la création du répertoire {path} : {e}", exc_info=True)
        raise
        
def definir_doc_path(cl_type):
    return (
            TEMPLATE_PATH_MOBILE_PHONE if cl_type == 'Mobile Phone' else
            TEMPLATE_PATH_LAPTOP if cl_type == 'Laptop' else
            TEMPLATE_PATH_TABLET if cl_type == 'Tablet' else
            ValueError('Le type d\'actif n\'est pas géré par ce script')
        )
        
def create_plaecholders(cl_type, data, custom_fields):
    
    logging.debug("""
        *********************************************************************************************************
                ********************************** Start script.py **********************************
        ********************************************************************************************************* """)
        
    if cl_type == 'Mobile Phone' :
        placeholders = {
            '{{Numéro_de_téléphone}}': '0' + str(
                custom_fields.get('numro_de_tlphone_50000227396', '..............................') or '..............................'),
            '{{Numéro_de_série}}': (
                custom_fields.get('serial_number_50000227369', '..............................') or '..............................'),
            '{{IMEI}}': (
                custom_fields.get('imei_number_50000227396', '..............................') or '..............................'),
            '{{PIN}}': (
                custom_fields.get('pin_code_50000227396', '..............................') or '..............................'),
            '{{PUK}}': (
                custom_fields.get('puk_code_50000227396', '..............................') or '..............................'),
            '{{Lock}}': (
                custom_fields.get('lock_code_50000227396', '..............................') or '..............................')
        }
    elif cl_type == 'Laptop' :
    # TODO gérer les données nécessaires pour la feuille de mat. intallé
        placeholders = {
            '{{Numéro_de_série}}': (
                custom_fields.get('serial_number_50000227369', '..............................') or '..............................')
        }
    elif cl_type == 'Tablet' :
    # TODO gérer les tablette
        placeholders = {
            '{{Numéro_de_série}}': (
                custom_fields.get('serial_number_50000227369', '..............................') or '..............................')
        }
    else :
        raise ValueError("le type d'actif reçu n'est pas géré par ce scritp")
        
    placeholders["{{Date}}"] = format_date(str(data.get('Date', 'date_is_None'))) or format_date(str(datetime.now()))
    placeholders["{{Nom}}"] = data.get('Used_by', 'user_is_None') or 'Aucun_utilisateur'
    placeholders["{{Appareil}}"] = data.get('Appareil', 'nom_appareil_is_None') or 'appareil ......'    
        
    return placeholders

def replace_placeholders(raw_data):
    
    try:
        # **********************************************************************************************************
        #            *************************** Initialisation des données *****************************
        # **********************************************************************************************************
        
        # création des JSON
        data = create_json(raw_data)
        custom_fields = create_json(data.get("custom_fields"))
            
        # récupère le type d'actif
        cl_type = data.get('Cl_type', 'Cl_type_is_None') or 'type_inconnu'
      
        # définir doc_path le chemin du fichier template à remplir
        doc_path = definir_doc_path(cl_type)
        
        # créer les champs à insérer dans le doc
        placeholders = create_plaecholders(cl_type, data, custom_fields)
        
        # **********************************************************************************************************
        #            *************************** Modification du document *****************************
        # **********************************************************************************************************
        
        # ouvrir doc template
        doc = open_doc(doc_path)
        
        # créer les dossiers de destination
        create_dir('./documents_finaux')
        create_dir(os.path.join('./documents_finaux', placeholders["{{Nom}}"]))
        dossier_nom = os.path.join('./documents_finaux', placeholders["{{Nom}}"])

        # TODO: vérifier si besoin des 2 path
        docx_path = get_unique_filename(os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Appareil}}"]}_{placeholders["{{Nom}}"]}.docx'))
        pdf_path = get_unique_filename(os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Appareil}}"]}_{placeholders["{{Nom}}"]}.pdf'))

        for paragraph in doc.paragraphs:
            for placeholder, value in placeholders.items():
                if placeholder in paragraph.text:
                    logging.debug(f"script.py :\n Remplacement de '{placeholder}' par '{value}'")
                    paragraph.text = paragraph.text.replace(placeholder, str(value))

        try:
            doc.save(docx_path)
            logging.debug(f'script.py :\n Sauvegarde du document Word modifié :\n {docx_path}')
        except Exception as e:
            logging.error(f"script.py :\n Erreur lors de la sauvegarde du document Word :\n {e}", exc_info=True)
            raise

        try:
            result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path], capture_output=True, text=True)
            if result.returncode != 0:
                raise subprocess.SubprocessError(f"Erreur lors de la conversion en PDF : {result.stderr}")
            pdf_generated_filename = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
            logging.debug(f"valeur de pdf_generated_filename :\n {pdf_generated_filename}")
            pdf_generated_path = os.path.join(os.getcwd(), pdf_generated_filename)
            logging.debug(f"valeur de pdf_generated_path :\n {pdf_generated_path}")
            logging.debug(f"valeur de pdf_path :\n {pdf_path}")
            if os.path.exists(pdf_generated_path):
                os.rename(pdf_generated_path, pdf_path)
                logging.debug(f'script.py :\n PDF sauvegardé à :\n {pdf_path}')
            else:
                raise FileNotFoundError(f"Le fichier PDF généré n'existe pas :\n {pdf_generated_path}")
        except Exception as e:
            logging.error(f"script.py :\n Erreur lors de la conversion du document Word en PDF : {e}", exc_info=True)
            

        try:
            if os.path.isfile(docx_path):
                os.remove(docx_path)
                logging.debug(f'script.py :\n Suppression du fichier DOCX : {docx_path}')
        except Exception as e:
            logging.error(f"script.py :\n Erreur lors de la suppression du fichier DOCX : {e}", exc_info=True)

    except Exception as e:
        logging.error(f"script.py :\n Erreur dans replace_placeholders : {e}", exc_info=True)
        

if __name__ == '__main__':
