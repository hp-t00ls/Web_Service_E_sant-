
def check_compliance(parametre, httpData):
    if parametre in httpData:
        output = {
            'CODE': 'PRESENT_URI_PARAMETER_{}'.format(parametre),
            'TEXT': "Le paramètre d'URI {} est présent.".format(parametre),
            'DATA': httpData[parametre]
        }
    else:
        output = {
            'CODE': 'ABSENT_URI_PARAMETER_{}'.format(parametre),
            'TEXT': "Le paramètre d'URI {} est absent.".format(parametre),
            'DATA': None
        }
    return output
        
def check_compliance_URI_parameters(httpData):
    output_INS = check_compliance('INS', httpData)
    if output_INS['DATA'] is None:
        output = output_INS
    else:
        output_LOINC_Code = check_compliance('LOINC_Code', httpData)
        if output_LOINC_Code['DATA'] is None:
            output = output_LOINC_Code
        else:
            output = {
                'CODE': 'PRESENT_URI_PARAMETERS',
                'TEXT': "Les paramètres d'URI sont tous présents.",
                'DATA': {
                    'INS': httpData['INS'],
                    'LOINC_Code': httpData['LOINC_Code'],
                }
            }

    return output