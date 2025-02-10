import os

def check_compliance_content_type():
    if 'CONTENT_TYPE' in os.environ:
        output = {
            'CODE': 'PRESENT_BODY_PARAMETER_Content-Type',
            'TEXT': "Le paramètre de corps de requête Content-Type est présent.",
            'DATA': os.environ['CONTENT_TYPE']
        }
    else:
        output = {
            'CODE': 'ABSENT_BODY_PARAMETER_Content-Type',
            'TEXT': "Le paramètre de corps de requête Content-Type est absent.",
            'DATA': None
        }
    return output
        
def check_compliance_headers_parameters():
    output = check_compliance_content_type()
    return output