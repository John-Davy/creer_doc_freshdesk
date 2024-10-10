import requests
import json

# URL de l'application Flask exécutée sur localhost
url = 'http://127.0.0.1:5000/webhook'

# Définir plusieurs jeux de données JSON à envoyer dans les requêtes POST
json_data_list = [
    {
   "custom_fields" : "{\"product_50000227369\":50000099041,\"vendor_50000227369\":50000757583,\"cost_50000227369\":\"514.12\",\"warranty_50000227369\":24,\"acquisition_date_50000227369\":\"2021-08-20T00:00:00+02:00\",\"warranty_expiry_date_50000227369\":\"2023-08-20T00:00:00+02:00\",\"domain_50000227369\":null,\"asset_state_50000227369\":1,\"serial_number_50000227369\":\"FFMG50GKPLK3\",\"last_audit_date_50000227369\":\"2021-09-01T00:00:00+02:00\",\"os_50000227396\":\"iOS 7\",\"numro_de_tlphone_50000227396\":765026881,\"os_version_50000227396\":\"14.8\",\"memory_50000227396\":\"128\",\"imei_number_50000227396\":\"35923040949668\",\"pin_code_50000227396\":4082,\"puk_code_50000227396\":123456,\"lock_code_50000227396\":1234}",

   "Asset_tag" : "iPhone SE",

   "Date" : "Mon, 7 Oct, 2024 15:46 GMT +0200",

   "Email_D" : "j-d.ferreira@pro-geneve.ch",

   "Cl_type" : "Mobile Phone",

   "Used_by" : "Sabrina VEZZA"

    },
    {
   "custom_fields" : "{\"product_50000227369\":50000126358,\"vendor_50000227369\":50001330537,\"cost_50000227369\":\"966.0\",\"warranty_50000227369\":36,\"acquisition_date_50000227369\":\"2023-03-06T00:00:00+01:00\",\"warranty_expiry_date_50000227369\":\"2026-03-06T00:00:00+01:00\",\"domain_50000227369\":50000007990,\"asset_state_50000227369\":1,\"serial_number_50000227369\":\"PF48YHSZ\",\"last_audit_date_50000227369\":\"2023-06-08T07:35:00+02:00\",\"os_50000227374\":\"Microsoft Windows 10 Professionnel\",\"os_version_50000227374\":\"10.0.19045\",\"os_service_pack_50000227374\":\"0.0\",\"memory_50000227374\":\"15.73\",\"disk_space_50000227374\":474,\"cpu_speed_50000227374\":\"2.8\",\"cpu_core_count_50000227374\":4,\"mac_address_50000227374\":\"AC:5A:FC:44:A6:4C\",\"uuid_50000227374\":\"45F81ACC-2787-11B2-A85C-954DA592D81F\",\"hostname_50000227374\":\"LAPTOP-EFVRGB\",\"computer_ip_address_50000227374\":\"172.16.50.136\",\"last_login_by_50000227374\":\"m.chalabi\"}",

   "Asset_tag" : "LAPTOP-EFVRGB",

   "Date" : "Thu, 26 Sep, 2024 15:41 GMT +0200",

   "Email_D" : "j-d.ferreira@pro-geneve.ch",

   "Cl_type" : "Laptop",

   "Used_by" : "Maxime CHALABI"

    },
    {
   "custom_fields" : "{\"product_50000227369\":50000140211,\"vendor_50000227369\":null,\"cost_50000227369\":\"92.9\",\"warranty_50000227369\":24,\"acquisition_date_50000227369\":\"2024-04-03T00:00:00+02:00\",\"warranty_expiry_date_50000227369\":\"2026-04-03T00:00:00+02:00\",\"domain_50000227369\":null,\"asset_state_50000227369\":1,\"serial_number_50000227369\":\"HGR2ZTQR\",\"last_audit_date_50000227369\":null,\"os_50000227397\":null,\"os_version_50000227397\":null,\"memory_50000227397\":null}",

   "Asset_tag" : "Lenovo Tab M8 G2",

   "Date" : "Thu, 26 Sep, 2024 15:54 GMT +0200",

   "Email_D" : "j-d.ferreira@pro-geneve.ch",

   "Cl_type" : "Tablet",

   "Used_by" : "J-D"

    },
    {
   "custom_fields" : "{\"product_50000227369\":null,\"vendor_50000227369\":null,\"cost_50000227369\":null,\"warranty_50000227369\":null,\"acquisition_date_50000227369\":null,\"warranty_expiry_date_50000227369\":null,\"domain_50000227369\":null,\"asset_state_50000227369\":4,\"serial_number_50000227369\":null,\"last_audit_date_50000227369\":null,\"os_50000227396\":null,\"numro_de_tlphone_50000227396\":null,\"os_version_50000227396\":null,\"memory_50000227396\":null,\"imei_number_50000227396\":null,\"pin_code_50000227396\":null,\"puk_code_50000227396\":null,\"lock_code_50000227396\":null}",
   "Asset_tag" : "test",
   "Used_by" : "test",
   "Date" : "",
   "Email_D" : "test",
   "Cl_type" : "Tablet"
    },
    {
   "custom_fields" : "{\"product_50000227369\":null,\"vendor_50000227369\":null,\"cost_50000227369\":null,\"warranty_50000227369\":null,\"acquisition_date_50000227369\":null,\"warranty_expiry_date_50000227369\":null,\"domain_50000227369\":null,\"asset_state_50000227369\":4,\"serial_number_50000227369\":null,\"last_audit_date_50000227369\":null,\"os_50000227396\":null,\"numro_de_tlphone_50000227396\":null,\"os_version_50000227396\":null,\"memory_50000227396\":null,\"imei_number_50000227396\":null,\"pin_code_50000227396\":null,\"puk_code_50000227396\":null,\"lock_code_50000227396\":null}",
   "Asset_tag" : "",
   "Used_by" : "test",
   "Date" : "Thu, 26 Sep, 2024 15:54 GMT +0200",
   "Email_D" : "test",
   "Cl_type" : "Tablet"
    },
    {
   "custom_fields" : "{\"product_50000227369\":null,\"vendor_50000227369\":null,\"cost_50000227369\":null,\"warranty_50000227369\":null,\"acquisition_date_50000227369\":null,\"warranty_expiry_date_50000227369\":null,\"domain_50000227369\":null,\"asset_state_50000227369\":4,\"serial_number_50000227369\":null,\"last_audit_date_50000227369\":null,\"os_50000227396\":null,\"numro_de_tlphone_50000227396\":null,\"os_version_50000227396\":null,\"memory_50000227396\":null,\"imei_number_50000227396\":null,\"pin_code_50000227396\":null,\"puk_code_50000227396\":null,\"lock_code_50000227396\":null}",
   "Asset_tag" : "test",
   "Used_by" : "",
   "Date" : "Thu, 26 Sep, 2024 15:54 GMT +0200",
   "Email_D" : "test",
   "Cl_type" : "Tablet"
    },
    {
   "custom_fields" : "{\"product_50000227369\":null,\"vendor_50000227369\":null,\"cost_50000227369\":null,\"warranty_50000227369\":null,\"acquisition_date_50000227369\":null,\"warranty_expiry_date_50000227369\":null,\"domain_50000227369\":null,\"asset_state_50000227369\":4,\"serial_number_50000227369\":null,\"last_audit_date_50000227369\":null,\"os_50000227396\":null,\"numro_de_tlphone_50000227396\":null,\"os_version_50000227396\":null,\"memory_50000227396\":null,\"imei_number_50000227396\":null,\"pin_code_50000227396\":null,\"puk_code_50000227396\":null,\"lock_code_50000227396\":null}",
   "Asset_tag" : "test",
   "Used_by" : "test",
   "Date" : "Thu, 26 Sep, 2024 15:54 GMT +0200",
   "Email_D" : "",
   "Cl_type" : "Tablet"
    },
    {
   "custom_fields" : "{\"product_50000227369\":null,\"vendor_50000227369\":null,\"cost_50000227369\":null,\"warranty_50000227369\":null,\"acquisition_date_50000227369\":null,\"warranty_expiry_date_50000227369\":null,\"domain_50000227369\":null,\"asset_state_50000227369\":4,\"serial_number_50000227369\":null,\"last_audit_date_50000227369\":null,\"os_50000227396\":null,\"numro_de_tlphone_50000227396\":null,\"os_version_50000227396\":null,\"memory_50000227396\":null,\"imei_number_50000227396\":null,\"pin_code_50000227396\":null,\"puk_code_50000227396\":null,\"lock_code_50000227396\":null}",
   "Asset_tag" : "test",
   "Used_by" : "test",
   "Date" : "Thu, 26 Sep, 2024 15:54 GMT +0200",
   "Email_D" : "test",
   "Cl_type" : "test"
    },
    {
   "custom_fields" : "{\"product_50000227369\":null,\"vendor_50000227369\":null,\"cost_50000227369\":null,\"warranty_50000227369\":null,\"acquisition_date_50000227369\":null,\"warranty_expiry_date_50000227369\":null,\"domain_50000227369\":null,\"asset_state_50000227369\":4,\"serial_number_50000227369\":null,\"last_audit_date_50000227369\":null,\"os_50000227396\":null,\"numro_de_tlphone_50000227396\":null,\"os_version_50000227396\":null,\"memory_50000227396\":null,\"imei_number_50000227396\":null,\"pin_code_50000227396\":null,\"puk_code_50000227396\":null,\"lock_code_50000227396\":null}",
   "Asset_tag" : "test",
   "Used_by" : "test",
   "Date" : "Thu, 26 Sep, 2024 15:54 GMT +0200",
   "Email_D" : "test",
   "Cl_type" : ""
    },
    {
   "custom_fields" : "{\"product_50000227369\":50000099041,\"vendor_50000227369\":50000757583,\"cost_50000227369\":\"514.12\",\"warranty_50000227369\":24,\"acquisition_date_50000227369\":\"2021-08-20T00:00:00+02:00\",\"warranty_expiry_date_50000227369\":\"2023-08-20T00:00:00+02:00\",\"domain_50000227369\":null,\"asset_state_50000227369\":1,\"serial_number_50000227369\":\"\",\"last_audit_date_50000227369\":\"2021-09-01T00:00:00+02:00\",\"os_50000227396\":\"iOS 7\",\"numro_de_tlphone_50000227396\":765026881,\"os_version_50000227396\":\"14.8\",\"memory_50000227396\":\"128\",\"imei_number_50000227396\":\"35923040949668\",\"pin_code_50000227396\":4082,\"puk_code_50000227396\":123456,\"lock_code_50000227396\":1234}",

   "Asset_tag" : "iPhone SE",

   "Date" : "Mon, 7 Oct, 2024 15:46 GMT +0200",

   "Email_D" : "j-d.ferreira@pro-geneve.ch",

   "Cl_type" : "Mobile Phone",

   "Used_by" : "Sabrina VEZZA"

    },
    {
   "custom_fields" : "{\"product_50000227369\":50000099041,\"vendor_50000227369\":50000757583,\"cost_50000227369\":\"514.12\",\"warranty_50000227369\":24,\"acquisition_date_50000227369\":\"2021-08-20T00:00:00+02:00\",\"warranty_expiry_date_50000227369\":\"2023-08-20T00:00:00+02:00\",\"domain_50000227369\":null,\"asset_state_50000227369\":1,\"serial_number_50000227369\":\"FFMG50GKPLK3\",\"last_audit_date_50000227369\":\"2021-09-01T00:00:00+02:00\",\"os_50000227396\":\"iOS 7\",\"numro_de_tlphone_50000227396\"null:,\"os_version_50000227396\":\"14.8\",\"memory_50000227396\":\"128\",\"imei_number_50000227396\":\"35923040949668\",\"pin_code_50000227396\":4082,\"puk_code_50000227396\":123456,\"lock_code_50000227396\":1234}",

   "Asset_tag" : "iPhone SE",

   "Date" : "Mon, 7 Oct, 2024 15:46 GMT +0200",

   "Email_D" : "j-d.ferreira@pro-geneve.ch",

   "Cl_type" : "Mobile Phone",

   "Used_by" : "Sabrina VEZZA"

    },
    {
   "custom_fields" : "{\"product_50000227369\":50000099041,\"vendor_50000227369\":50000757583,\"cost_50000227369\":\"514.12\",\"warranty_50000227369\":24,\"acquisition_date_50000227369\":\"2021-08-20T00:00:00+02:00\",\"warranty_expiry_date_50000227369\":\"2023-08-20T00:00:00+02:00\",\"domain_50000227369\":null,\"asset_state_50000227369\":1,\"serial_number_50000227369\":\"FFMG50GKPLK3\",\"last_audit_date_50000227369\":\"2021-09-01T00:00:00+02:00\",\"os_50000227396\":\"iOS 7\",\"numro_de_tlphone_50000227396\":765026881,\"os_version_50000227396\":\"14.8\",\"memory_50000227396\":\"128\",\"imei_number_50000227396\":\"\",\"pin_code_50000227396\":4082,\"puk_code_50000227396\":123456,\"lock_code_50000227396\":1234}",

   "Asset_tag" : "iPhone SE",

   "Date" : "Mon, 7 Oct, 2024 15:46 GMT +0200",

   "Email_D" : "j-d.ferreira@pro-geneve.ch",

   "Cl_type" : "Mobile Phone",

   "Used_by" : "Sabrina VEZZA"

    },
]

# Boucle pour envoyer chaque jeu de données via une requête POST
for data in json_data_list:
    # Convertir les données Python en JSON
    json_payload = json.dumps(data)

    # Envoyer la requête POST
    response = requests.post(url, data=json_payload, headers={"Content-Type": "application/json"})

    # Afficher la réponse
    print(f"Request sent with data: {json_payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    print("-" * 50)

