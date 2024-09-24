import json
import os
from flask import Flask, request, send_file
from docx import Document
from pypdf import PdfWriter
from datetime import datetime

app = Flask(__name__)

# Chemin vers le dossier des templates et logs
TEMPLATE_PATH = '/home/john/projets/creer_doc_freshdesk/log_et_templates/template.docx'
LOG_PATH = '/home/john/projets/creer_doc_freshdesk/log_et_templates/logs.txt'

def log_to_file(message):
    with open(LOG_PATH, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def format_date_from_system(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date.strftime("%d.%m.%Y")

def fill_placeholders(data):
    # Ouvrir le document Word modèle
    doc = Document(TEMPLATE_PATH)
    
    # Remplacer les placeholders par les valeurs
    phone_number = data['custom_fields'].get('numro_de_tlphone_50000227396', '')
    if phone_number:
        phone_number = '0' + phone_number
    else:
        phone_number = '..............................'

    placeholders = {
        '{{Num_Tel}}': phone_number,
        '{{Appareil}}': data.get('Appareil', '..............................'),
        '{{Num_serie}}': data['custom_fields'].get('serial_number_50000227369', '..............................'),
        '{{IMEI}}': data['custom_fields'].get('imei_number_50000227396', '..............................'),
        '{{PIN}}': data['custom_fields'].get('pin_code_50000227396', '..............................'),
        '{{PUK}}': data['custom_fields'].get('pin_code_50000227396', '..............................'),
        '{{Lock}}': data['custom_fields'].get('lock_code_50000227396', '..............................'),
        '{{Date}}': format_date_from_system(data.get('Date', '..............................')),
        '{{Nom}}': data.get('Nom', '..............................')
    }

    # Remplacement des placeholders dans le document Word
    for paragraph in doc.paragraphs:
        for placeholder, value in placeholders.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, value)

    # Enregistrer le document rempli en PDF
    output_docx = '/home/john/projets/creer_doc_freshdesk/log_et_templates/output_document.docx'
    output_pdf = '/home/john/projets/creer_doc_freshdesk/log_et_templates/output_document.pdf'
    doc.save(output_docx)

    # Convertir le fichier DOCX en PDF
    pdf_writer = PdfWriter()
    pdf_writer.add_document(output_docx)
    with open(output_pdf, 'wb') as f:
        pdf_writer.write(f)

    return output_pdf

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        log_to_file("Received POST request")

        if not request.data:
            log_to_file('No data received or postData is empty')
            return 'No data received', 400

        json_data = request.get_json()
        log_to_file(f"Data received: {json.dumps(json_data)}")

        pdf_path = fill_placeholders(json_data)

        log_to_file("PDF created successfully")

        # Envoyer le fichier PDF en réponse ou par email (selon votre choix)
        return send_file(pdf_path, as_attachment=True, download_name='output_document.pdf')

    except Exception as e:
        log_to_file(f"Error: {str(e)}")
        return f"Internal Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

