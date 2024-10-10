import pytest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from script import replace_placeholders

# Définir les cas de test
def test_replace_placeholders():
    data = {
            "data1" : {"custom_fields": "{\"product_50000227369\":50000126358,\"vendor_50000227369\":50001330537,\"cost_50000227369\":\"966.0\",\"warranty_50000227369\":36,\"acquisition_date_50000227369\":\"2023-03-06T00:00:00+01:00\",\"warranty_expiry_date_50000227369\":\"2026-03-06T00:00:00+01:00\",\"domain_50000227369\":50000007990,\"asset_state_50000227369\":1,\"serial_number_50000227369\":\"PF48YHSZ\",\"last_audit_date_50000227369\":\"2023-06-08T07:35:00+02:00\",\"os_50000227374\":\"Microsoft Windows 10 Professionnel\",\"os_version_50000227374\":\"10.0.19045\",\"os_service_pack_50000227374\":\"0.0\",\"memory_50000227374\":\"15.73\",\"disk_space_50000227374\":474,\"cpu_speed_50000227374\":\"2.8\",\"cpu_core_count_50000227374\":4,\"mac_address_50000227374\":\"AC:5A:FC:44:A6:4C\",\"uuid_50000227374\":\"45F81ACC-2787-11B2-A85C-954DA592D81F\",\"hostname_50000227374\":\"LAPTOP-EFVRGB\",\"computer_ip_address_50000227374\":\"172.16.50.136\",\"last_login_by_50000227374\":\"m.chalabi\"}",
                   "Asset_tag": "LAPTOP-EFVRGB",
                   "Date": "Tue, 24 Sep, 2024 14:41 GMT +0200",
                   "Email_D": "j-d.ferreira@pro-geneve.ch",
                   "Cl_type": "Laptop",
                   "Used_by": "Maxime CHALABI"
            },
            "data2" : {"custom_fields": "{\"product_50000227369\":null,\"vendor_50000227369\":null,\"cost_50000227369\":null,\"warranty_50000227369\":null,\"acquisition_date_50000227369\":null,\"warranty_expiry_date_50000227369\":null,\"domain_50000227369\":null,\"asset_state_50000227369\":null,\"serial_number_50000227369\":null,\"last_audit_date_50000227369\":null,\"os_50000227396\":null,\"numro_de_tlphone_50000227396\":null,\"os_version_50000227396\":null,\"memory_50000227396\":null,\"imei_number_50000227396\":null,\"pin_code_50000227396\":null,\"puk_code_50000227396\":null,\"lock_code_50000227396\":null}",
       "Asset_tag": "test 123",
       "Date": "",
       "Email_D": "",
       "Cl_type": "Mobile Phone",
       "Used_by": "test"  
            }
    }

    
    
    for key, value in data.items():
        # Appeler la fonction avec des données de test
        result = replace_placeholders(json.dumps(value))
        assert result is False  # Assurez-vous qu'une sortie est générée

