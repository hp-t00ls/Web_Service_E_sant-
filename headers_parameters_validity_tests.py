import os

def check_validity_content_type():
    if os.environ['CONTENT_TYPE'] == 'application/x-www-form-urlencoded':
        output = {
            'CODE': 'VALID_BODY_PARAMETER_VALUE_Content-Type',
            'TEXT': "Le paramètre de corps de requête Content-Type est valide.",
            'DATA': 'application/x-www-form-urlencoded'
        }
    else:
        output = {
            'CODE': 'INVALID_BODY_PARAMETER_VALUE_Content-Type',
            'TEXT': "Le paramètre de corps de requête Content-Type est invalide. La valeur attendue est 'application/x-www-form-urlencoded'",
            'DATA': None
        }
    return output
        
def check_validity_headers_parameters():
    output = check_validity_content_type()
    return output