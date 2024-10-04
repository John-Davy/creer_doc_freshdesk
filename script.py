import os
import logging
from docx import Document
from datetime import datetime
import subprocess
import json
from logging.handlers import RotatingFileHandler

# Chemins vers les différents templates en fonction du type d'actif
try:
    TEMPLATES = {
        'Mobile Phone': './templates/template_recommandations_Mobile_Phone.docx',
        'Laptop': './templates/template_recommandations_Laptop.docx',
        'Tablet': './templates/template_recommandations_Tablet.docx'
    }
except ValueError as e:
    logging.error(f"Le type d'actif envoyé n'est pas pris en charge !")
    
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
        logging.error(f"script.py : Mauvais format de date !")
        return (datetime.now()).strftime("%d.%m.%Y")

def open_doc(doc_path):
    """ Crée une instance du template et la renvoie """
    if not os.path.isfile(doc_path):
        raise FileNotFoundError(f"Le fichier template n'existe pas à l'emplacement : {doc_path}")
    doc = Document(doc_path)
    return doc

def create_json(raw_data):
    """ Converti la chaine de caractère et renvoie un object JSON """
    data = json.loads(str(raw_data))
    return data
        
def create_dir(path):
    """ Crée de répertoire si inexistant """
    if not os.path.exists(path):
        os.makedirs(path)
        
        
def create_plaecholders(cl_type, data, custom_fields):
    """ Crée le dictionnaire avec les bonnes clés et valeurs pour remplir le doc """
    logging.debug("""********************************** Start script.py **********************************""")
    
    if cl_type == 'Mobile Phone' :
        placeholders = {
            '{{Numéro_de_téléphone}}': '0' + str(
                custom_fields.get('numro_de_tlphone_50000227396') or '..............................'),
            '{{Numéro_de_série}}': (
                custom_fields.get('serial_number_50000227369') or '..............................'),
            '{{IMEI}}': (
                custom_fields.get('imei_number_50000227396') or '..............................'),
            '{{PIN}}': (
                custom_fields.get('pin_code_50000227396') or '..............................'),
            '{{PUK}}': (
                custom_fields.get('puk_code_50000227396') or '..............................'),
            '{{Lock}}': (
                custom_fields.get('lock_code_50000227396') or '..............................')
        }
    elif cl_type == 'Laptop' or 'Tablet' :
        placeholders = {
            '{{Numéro_de_série}}': (
                custom_fields.get('serial_number_50000227369') or '..............................')
        }
    else :
        raise ValueError("le type d'actif reçu n'est pas géré par ce scritp")
        
    placeholders["{{Date}}"] = format_date(str(data.get('Date'))) or format_date(str(datetime.now()))
    placeholders["{{Appareil}}"] = data.get('Appareil') or '.............................'    
    
    if data.get('Used_by') not in [None, ""]:
        placeholders["{{Nom}}"] = data.get('Used_by')
    else:
        raise ValueError("l'actif n'est pas attribué à une utilisateur !")
        
    return placeholders

def replace_placeholders(raw_data):
    """ Remplace les données dans le document template, modifie son nom, et l'enregistre au bon endroit """
    # création des JSON
    data = create_json(raw_data)
    custom_fields = create_json(data.get("custom_fields"))
        
    # récupère le type d'actif
    cl_type = data.get('Cl_type', 'Cl_type_is_None') or 'type_inconnu'
    if cl_type not in ["Tablet", "Laptop", "Mobile Phone"]:
        return "Type d'actif n'est pas pris en charge", 500
  
    # définir le template a utiliser
    doc_path = TEMPLATES[cl_type]
    doc = open_doc(doc_path)
    
    # créer les champs à insérer dans le doc
    placeholders = create_plaecholders(cl_type, data, custom_fields)
    
    # créer les dossiers de destination
    create_dir('./documents_finaux')
    dossier_nom = os.path.join('./documents_finaux', placeholders["{{Nom}}"])
    create_dir(dossier_nom)

    # Défini nom fichier unique
    docx_path = os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Appareil}}"]}_{placeholders["{{Nom}}"]}.docx')
    pdf_path = get_unique_filename(os.path.join(dossier_nom, f'Attribuer_{cl_type}_{placeholders["{{Appareil}}"]}_{placeholders["{{Nom}}"]}.pdf'))

    # **********************************************************************************************************
    #            *************************** Modification du document *****************************
    # **********************************************************************************************************
    
    # Remplacer les placeholders dans le document
    for paragraph in doc.paragraphs:
        for placeholder, value in placeholders.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, str(value))
                logging.debug(f"script.py : placeholder: {placeholder} est remplacé par {str(value)} !")

    doc.save(docx_path)

    # Convertir en PDF
    result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path], capture_output=True, text=True)
    
    # Définir le chemin final du .pdf
    pdf_generated_filename = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
    pdf_generated_path = os.path.join(os.getcwd(), pdf_generated_filename)
    
    # Effacer le .docx temporaire
    if os.path.isfile(docx_path):
        os.remove(docx_path)
        
    # Déplacer le fichier .pdf
    if os.path.exists(pdf_generated_path):
            os.rename(pdf_generated_path, pdf_path)
            return True
    else:
        raise FileNotFoundError(f"Le fichier PDF généré n'existe pas : {pdf_generated_path}")

if __name__ == '__main__':
    logging.debug("************** MAIN START ****************")
