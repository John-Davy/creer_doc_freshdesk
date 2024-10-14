import requests

        
""" 
ici la requete CURL qui fonctionne :

    curl -v -u ouGa4QwnLWHsTWTk-uxy:X \
-F 'attachments[]=@/home/john/Projets/creer_doc_freshdesk/documents_finaux/John-Davy FERREIRA/Attribuer_Mobile Phone_ASSET-1060_John-Davy FERREIRA.pdf' \
-F 'body=Test ok avec pièce jointe' \
-F 'private=false' \
-X POST 'https://pro-geneve.freshservice.com/api/v2/tickets/9873/notes'

"""

def add_attachment_to_ticket(ticket_id, file_path):
""" Cette fonction reçoit un identifiant de ticker Freshdesk et le chemin vers un fichier et ajoute ce dernier en note dans le ticket """
    api_key = 'ouGa4QwnLWHsTWTk-uxy'  # Remplacez par votre clé API
    ticket_id = ticket_id.split('-')[1]  # Filtrer pour n'avoir que les chiffres du ticket ID
    note_url = f'https://pro-geneve.freshservice.com/api/v2/tickets/{ticket_id}/notes'
    note_content = "Voici le fichier d'attribution de matériel généré !"  # Contenu de la note

    # Préparer les données de la note et le fichier
    files = {
        'attachments[]': open(file_path, 'rb'),
        'body': (None, note_content),
        'private': (None, 'false')
    }

    # Créer la note avec attachement
    response = requests.post(note_url, files=files, auth=(api_key, 'X'))

    # Vérifier la réponse
    if response.status_code == 201:
        print('Fichier attaché avec succès')
    else:
        print('Erreur:', response.status_code, response.text)
