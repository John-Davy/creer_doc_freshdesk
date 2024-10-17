import requests
import logging
from requests.auth import HTTPBasicAuth

def resquest_product_name(product_id):
    # Détails d'authentification
    api_key = 'ouGa4QwnLWHsTWTk-uxy'
    freshdesk_url = f'https://pro-geneve.freshservice.com/api/v2/products/{product_id}'

    # Effectuer la requête GET
    response = requests.get(freshdesk_url, auth=HTTPBasicAuth(api_key, 'X'))
    logging.debug(f'valeur réponse produits api : {response}')

    # Vérifier si la requête est réussie
    if response.status_code == 200:
        product_info = response.json()
        logging.debug(f'valeur réponse api product_info : {product_info}')
        product_name = product_info['product']['name'] or 'non_trouvé'
        return (product_name)
    else:
        raise ValueError(f"Erreur : Impossible de récupérer les informations du produit. Code d'état : {response.status_code}")
            

def resquest_collaborateur_service (collaborateur_id):
    # Détails d'authentification
    api_key = 'ouGa4QwnLWHsTWTk-uxy'
    freshdesk_url = f'https://pro-geneve.freshservice.com/api/v2/collaborateurs/{collaborateur_id}'

    # Effectuer la requête GET
    response = requests.get(freshdesk_url, auth=HTTPBasicAuth(api_key, 'X'))
    logging.debug(f'valeur réponse collaborateurs api : {response}')

    # Vérifier si la requête est réussie
    if response.status_code == 200:
        collaborateur_info = response.json()
        logging.debug(f'valeur réponse api collaborateurs_info : {collaborateur_info}')
        collaborateur_service = product_info['collaborateur']['service'] or 'non_trouvé'
        return (collaborateur_service)
    else:
        raise ValueError(f"Erreur : Impossible de récupérer les informations du produit. Code d'état : {response.status_code}")
            
def add_attachment_to_ticket(ticket_id, file_path):
    """ 
    Cette fonction reçoit un identifiant de ticket Freshdesk et le chemin vers le document remplit 
    puis, ajoute ce dernier en note dans le ticket 
    """
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
        
""" 
ici la requete CURL qui fonctionne :

    curl -v -u ouGa4QwnLWHsTWTk-uxy:X \
-F 'attachments[]=@/home/john/Projets/creer_doc_freshdesk/documents_finaux/John-Davy FERREIRA/Attribuer_Mobile Phone_ASSET-1060_John-Davy FERREIRA.pdf' \
-F 'body=Test ok avec pièce jointe' \
-F 'private=false' \
-X POST 'https://pro-geneve.freshservice.com/api/v2/tickets/9873/notes'
"""

