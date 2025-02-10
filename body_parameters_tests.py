import body_parameters_compliance_tests
import body_parameters_validity_tests


def check_body_parameters(conn, httpData, methode):
    output_compliance_tests = body_parameters_compliance_tests.check_compliance_body_parameters(httpData)
    if output_compliance_tests['DATA'] is None:
        output = output_compliance_tests
    else:
        output_validity_tests = body_parameters_validity_tests.check_validity_body_parameters(conn, httpData, methode)
        if output_validity_tests['DATA'] is None:
            output = output_validity_tests
        else:
            output = {
                'CODE': 'BODY_PARAMETERS_OK',
                'TEXT': "Les paramètres de corps sont conformes.",
                'DATA': output_validity_tests['DATA']
            }
    return output