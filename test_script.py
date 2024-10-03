import pytest
from script import replace_placeholders, TEMPLATES

# Données de test
mobile_phone_data = {
    "custom_fields": "{\"serial_number_50000227369\":\"FFMG50GKPLK3\"}",
    "Appareil": "Iphone SE",
    "Date": "Tue, 24 Sep, 2024 14:41 GMT +0200",
    "Email_D": "j-d.ferreira@pro-geneve.ch",
    "Cl_type": "Mobile Phone",
    "Used_by": "Sabrina VEZZA"
}

tablet_data = {
    "custom_fields": "{\"serial_number_50000227369\":\"HGR2ZTQR\"}",
    "Appareil": "Lenovo Tab M8 G2",
    "Date": "Thu, 26 Sep, 2024 15:54 GMT +0200",
    "Email_D": "j-d.ferreira@pro-geneve.ch",
    "Cl_type": "Tablet",
    "Used_by": "J-D"
}

laptop_data = {
    "custom_fields": "{\"serial_number_50000227369\":\"PF48YHSZ\"}",
    "Appareil": "LAPTOP-EFVRGB",
    "Date": "Thu, 26 Sep, 2024 15:41 GMT +0200",
    "Email_D": "j-d.ferreira@pro-geneve.ch",
    "Cl_type": "Laptop",
    "Used_by": "Maxime CHALABI"
}

# Test de la fonction replace_placeholders
@pytest.mark.parametrize("data, expected_template", [
    (mobile_phone_data, 'Mobile Phone'),
    (tablet_data, 'Tablet'),
    (laptop_data, 'Laptop'),
])
def test_replace_placeholders(data, expected_template):
    template_path = TEMPLATES[expected_template]
    pdf_path = replace_placeholders(expected_template, template_path, data)
    assert pdf_path is not None

