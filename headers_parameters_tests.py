import headers_parameters_compliance_tests
import headers_parameters_validity_tests

def check_headers_parameters():
    output_compliance_tests = headers_parameters_compliance_tests.check_compliance_headers_parameters()
    if output_compliance_tests['DATA'] is None:
        output = output_compliance_tests
    else:
        output_validity_tests = headers_parameters_validity_tests.check_validity_headers_parameters()
        if output_validity_tests['DATA'] is None:
            output = output_validity_tests
        else:
            output = {
                'CODE': 'HEADERS_PARAMETERS_OK',
                'TEXT': "Les paramètres d'en-tête sont conformes.",
                'DATA': {
                    'Content-Type': output_validity_tests['DATA']
                }
            }
    return output