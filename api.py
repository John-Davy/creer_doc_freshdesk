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
        raise ValueError(f"Erreur resquest_product_name: Impossible de récupérer les informations du produit. Code d'état : {response.status_code}")
            

def resquest_collaborateur_info (collaborateur_name):
    """ reçoit le nom d'un collaborateur, questionne l'API et renvoie la réponse au format Json"""
    """ champs recherchés 'department_names' 'address' : voir bas de page pour réponse Json complet"""
    # Détails d'authentification
    collaborateur_firstname = collaborateur_name.split(" ")[0]
    collaborateur_lastname = collaborateur_name.split(" ")[1]
    api_key = 'ouGa4QwnLWHsTWTk-uxy'
    freshdesk_url = f"https://pro-geneve.freshservice.com/api/v2/requesters?query=name%3A%27{collaborateur_firstname}%20{collaborateur_lastname}%27&active=true&include_agents=true"

    # Effectuer la requête GET
    response = requests.get(freshdesk_url, auth=HTTPBasicAuth(api_key, 'X'))
    logging.debug(f'valeur réponse collaborateurs api : {response}')

    # Vérifier si la requête est réussie
    if response.status_code == 200:
        collaborateur_info = response.json()
        logging.debug(f'valeur réponse api collaborateurs_info : {collaborateur_info}')
        return collaborateur_info
    else:
        raise ValueError(f"Erreur resquest_collaborateur_info: Impossible de récupérer les informations du collaborateur. Code d'état : {response.status_code}")
       
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

# recherche par prénom et nom concaténés    
    curl -u ouGa4QwnLWHsTWTk-uxy:X -X GET "https://pro-geneve.freshservice.com/api/v2/requesters?query=name:%27john-davy%20ferreira%27&include_agents=true"
leur réponse collaborateurs api : <Response [400]>
# requete avec filtre compte actif = vrai 
curl -u ouGa4QwnLWHsTWTk-uxy:X -X GET "https://pro-geneve.freshservice.com/api/v2/requesters?query=name:%27{collaborateur_firstname}%20{collaborateur_lastname}%27&active=true&include_agents=true"

curl -u ouGa4QwnLWHsTWTk-uxy:X -X GET "https://pro-geneve.freshservice.com/api/v2/requesters?query=name%3A%27john-davy%20ferreira%27&active=true&include_agents=true"


JSon =
     requesters:
     first_name
     last_name
     department_names
     address
     job_title
     
     primary_email
     
     
     {"requesters":[{
     "active":true,
     "address":"Direction Générale",
     "background_information":null,
     "can_see_all_changes_from_associated_departments":false,
     "can_see_all_tickets_from_associated_departments":false,
     "created_at":"2024-04-24T12:38:41Z",
     "custom_fields":{},
     "department_ids":[50004086875],
     "department_names":["Informatique et technologies"],
     "external_id":"49e1e33d-f9e1-4b83-ba1e-0614a64b8c50",
     "first_name":"John-Davy",
     "has_logged_in":true,
     "id":50005475925,
     "is_agent":true,
     "job_title":"Collaborateur"
     ,"language":"fr",
     "last_name":"FERREIRA",
     "location_id":50000123667,
     "location_name":"Genève Tourbillon",
     "mobile_phone_number":null,"
"""

