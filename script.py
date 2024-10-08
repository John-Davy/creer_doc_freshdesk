import os
import logging
from docx import Document
from datetime import datetime
import subprocess
import json

# Définir le chemin du template
TEMPLATE = {"Mobile Phone" : './templates/template_recommandations_Mobile_Phone.docx',
            "Laptop" : './templates/template_recommandations_Laptop.docx',
            "Tablet" : './templates/template_recommandations_Tablet.docx',
}
            
# Initialisation de l'indicateur d'erreur
ERRORS_OCCURED = False            

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
        logging.error(f"script.py : Erreur de formatage de la date : {e}", exc_info=True)
        ERRORS_OCCURED = True
        return str(datetime.now().strftime('%d.%m.%Y'))

def open_doc(doc_path):
    """ Crée une instance du template et la renvoie """
    try:
        if not os.path.isfile(doc_path):
            raise FileNotFoundError(f"Le fichier template n'existe pas à l'emplacement : {doc_path}")
        doc = Document(doc_path)
        return doc
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors du chargement du document : {e}", exc_info=True)
        ERRORS_OCCURED = True
        raise # Propager l'exception pour app.py

def create_json(raw_data):
    """ Converti la chaine de caractère et renvoie un object JSON """
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError as e:
        logging.error(f"script.py :\n Erreur lors du parsing du JSON : {e}", exc_info=True)
        ERRORS_OCCURED = True
        raise # Propager l'exception pour app.py
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors de l'obtention du JSON : {e}", exc_info=True)
        ERRORS_OCCURED = True
        raise # Propager l'exception pour app.py
    return data
    
def create_dir(path):
    """ Crée de répertoire si inexistant """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        logging.error(f"script.py :\n Erreur lors de la création du répertoire {path} : {e}", exc_info=True)
        ERRORS_OCCURED = True
        raise # Propager l'exception pour app.py
        
def init_palceholders(data, custom_fields):
    placeholders = {}
    
    # gestion dela date
    date = str(data.get('Date'))
    date = format_date(date)
    placeholders["{{Date}}"] = date
    
    # valeurs obligatoires
    requiered_values = {
        "{{Used_by}}" : data.get("Used_by"),
        "{{Asset_tag}}" : data.get("Asset_tag"), 
        "{{Numéro_de_série}}" : custom_fields.get("serial_number_50000227369")
    }
    
    for key, value in requiered_values.items():
        if value not in [ None, ""] :
            placeholders[key] = value
        else :
            ERRORS_OCCURED = True
            raise ValueError(f"La variable {key} n'a pas de valeur = {key} = {value} !")
            
    return placeholders

def create_placeholders(cl_type, data, custom_fields):
    """ Crée le dictionnaire avec les bonnes clefs et valeurs pour remplir le doc """
    placeholders = init_palceholders(data, custom_fields)
    
    # gerer les champs spécifiques si l'actif est un Mobile Phone
    if cl_type == 'Mobile Phone' :
        dic = {
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
        for key, value in dic.items():
            placeholders[key] = value
    elif cl_type not in ['Tablet', 'Laptop']:
        ERRORS_OCCURED = True
        raise ValueError("Le type d'actif reçu n'est pas géré par ce script")        
    return placeholders

def replace_placeholders(raw_data):
    """ Remplace les données dans le document template, modifie son nom, et l'enregistre au bon endroit """
    logging.debug("""
    *********************************************************************************************************
               ********************************** Start script.py **********************************
    *********************************************************************************************************""")
    ERRORS_OCCURED = False
    try:
        # création des JSON
        data = create_json(raw_data)
        custom_fields = create_json(data.get("custom_fields"))
        
        # récupère le type d'actif
        cl_type = data.get('Cl_type')
        
        # Choisi le template en fonction du type d'actif
        doc_path = TEMPLATE[cl_type]
          
        # créer les champs à insérer dans le doc
        placeholders = create_placeholders(cl_type, data, custom_fields)
        logging.debug(f"Afficher palceholders : {placeholders}")

        # ouvrir doc template pour pouvoir le modifier
        doc = open_doc(doc_path)
        
        # créer les dossiers de destination du fichier rempli
        create_dir('./documents_finaux')
        create_dir(os.path.join('./documents_finaux', placeholders["{{Used_by}}"]))
        dossier_nom = os.path.join('./documents_finaux', placeholders["{{Used_by}}"])

        docx_path = get_unique_filename(os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Asset_tag}}"]}_{placeholders["{{Used_by}}"]}.docx'))
        pdf_path = get_unique_filename(os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Asset_tag}}"]}_{placeholders["{{Used_by}}"]}.pdf'))

        for paragraph in doc.paragraphs:
            for placeholder, value in placeholders.items():
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, str(value))
                    logging.debug(f"remplacement :\t {placeholder} ................ {str(value)}")

        doc.save(docx_path)

        # Convertir en .PDF
        result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path], capture_output=True, text=True)
        if result.returncode != 0:
            ERRORS_OCCURED = True
            raise subprocess.SubprocessError(f"Erreur lors de la conversion en PDF : {result.stderr}")
        
        # Récupère le nom du fichier et ajoute .pdf
        pdf_generated_filename = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
        # Récupère le chemin vers le fichier .PDF généré
        pdf_generated_path = os.path.join(os.getcwd(), pdf_generated_filename)
        # Déplacer le .PDF à pdf_path
        if os.path.exists(pdf_generated_path):
            os.rename(pdf_generated_path, pdf_path)
        else:
            ERRORS_OCCURED = True
            raise FileNotFoundError(f"Le fichier PDF généré n'existe pas :\n {pdf_generated_path}")
            
        # Effacer le .docx
        if os.path.isfile(docx_path):
            os.remove(docx_path)
            
        return ERRORS_OCCURED

    except Exception as e:
        logging.error(f"script.py :\n Erreur dans replace_placeholders : {e}", exc_info=True)
        ERRORS_OCCURED = True
        raise # Propager l'exception pour app.py
        
if __name__ == '__main__':
    logging.info("************** MAIN START ****************")
