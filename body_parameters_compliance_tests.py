import json

def check_compliance_data(httpData):
    if 'DATA' in httpData: 
        Valeur = json.loads(httpData['DATA'])['Valeur']
        output = {
            'CODE': 'PRESENT_BODY_PARAMETER_data',
            'TEXT': "Le paramètre 'DATA' est présent dans le corps de la requête.",
            'DATA': {
                    'Valeur': Valeur
            }
        }
    else:
        output = {
            'CODE': 'ABSENT_BODY_PARAMETER_data',
            'TEXT': "Le paramètre 'DATA' est absent du corps de la requête.",
            'DATA': None
        }
    return output
    
def check_compliance_body_parameters(httpData):
    return check_compliance_data(httpData) 