import requests
import logging
from requests.auth import HTTPBasicAuth

# Clé API constante global
API_KEY = 'ouGa4QwnLWHsTWTk-uxy' # clé API freshdesk

def add_note_to_ticket(ticket_id, note_content):
    """ Cette fonction reçoit un identifiant de ticket Freshdesk et le contenu du message pour ajouter une note """
    # URL API note de ticket
    note_url = f'https://pro-geneve.freshservice.com/api/v2/tickets/{ticket_id}/notes'
    # Préparer les données de la note et le fichier
    files = {
        'body': (None, note_content),
        'private': (None, 'false')
    }
    # Créer la note avec attachement
    response = requests.post(note_url, files=files, auth=(API_KEY, 'X'))
    # Vérifier la réponse
    if response.status_code == 201:
        logging.info('Note ajoutée avec succès')
    else:
        logging.debug(f"add_note_to_ticket: ticket_id:{ticket_id};note_content:{note_content},\nfiles:{files}")
        logging.info("Erreur lors de l'ajout de la note")
        logging.error("Erreur lors de l'insertion la note : Status Code=%s, Message=%s", response.status_code, response.text)
    
def resquest_product_name(product_id):
    """ Reçoit l'ID d'un produit et renvoie le nom de celui-ci """
    # URL API produits
    freshdesk_url = f'https://pro-geneve.freshservice.com/api/v2/products/{product_id}'
    # Effectuer la requête GET
    response = requests.get(freshdesk_url, auth=HTTPBasicAuth(API_KEY, 'X'))
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
    # Séparer collaborateur_name en nom et prénom
    collaborateur_firstname = collaborateur_name.split(" ")[0]
    collaborateur_lastname = collaborateur_name.split(" ")[1]
    # URL API questionner la BDD des demandeur et demandeur agent
    freshdesk_url = f"https://pro-geneve.freshservice.com/api/v2/requesters?query=name%3A%27{collaborateur_firstname}%20{collaborateur_lastname}%27&active=true&include_agents=true"
    # Effectuer la requête GET
    response = requests.get(freshdesk_url, auth=HTTPBasicAuth(API_KEY, 'X'))
    logging.debug(f'valeur réponse collaborateurs api : {response}')
    # Vérifier si la requête est réussie
    if response.status_code == 200:
        collaborateur_info = response.json()
        logging.debug(f'valeur réponse api collaborateurs_info : {collaborateur_info}')
        return collaborateur_info
    else:
        raise ValueError(f"Erreur resquest_collaborateur_info: Impossible de récupérer les informations du collaborateur. Code d'état : {response.status_code}")
       
def add_attachment_to_ticket(ticket_id, file_path):
    """ Cette fonction reçoit un identifiant de ticket Freshdesk et le chemin vers le document remplit 
        puis, ajoute ce dernier en note dans le ticket                                                  """
    # URL API des notes du ticket
    note_url = f'https://pro-geneve.freshservice.com/api/v2/tickets/{ticket_id}/notes'
    note_content = "Voici le fichier d'attribution de matériel généré !"  # Contenu de la note
    # Préparer les données de la note et le fichier
    files = {
        'attachments[]': open(file_path, 'rb'),
        'body': (None, note_content),
        'private': (None, 'false')
    }
    # Créer la note avec attachement
    response = requests.post(note_url, files=files, auth=(API_KEY, 'X'))
    # Vérifier la réponse
    if response.status_code == 201:
        logging.debug('Fichier attaché avec succès')
    else:
        logging.debug("Erreur lors de l'attachement du fichier à la note :", response.status_code, response.text)
        
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

