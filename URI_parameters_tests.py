import URI_parameters_compliance_tests
import URI_parameters_validity_tests
import already_assigned_result_test

def check_URI_parameters(methode, httpData, conn):
    output_compliance_tests = URI_parameters_compliance_tests.check_compliance_URI_parameters(httpData)
    if output_compliance_tests['DATA'] is None:
        output = output_compliance_tests
    else:
        INS = output_compliance_tests['DATA']['INS']
        LOINC_Code = output_compliance_tests['DATA']['LOINC_Code']
        # Valeur = output_compliance_tests['DATA']['Valeur']
        output_validity_tests = URI_parameters_validity_tests.check_validity_URI_parameters(conn, INS, LOINC_Code, methode)
        if output_validity_tests['DATA'] is None:
            output = output_validity_tests
        else:
            URI_Id_Utilisateur = output_validity_tests['DATA']['URI_Id_Utilisateur']
            if methode == 'POST':
                output_already_assigned_result = already_assigned_result_test.has_result_already_been_assigned(URI_Id_Utilisateur, LOINC_Code, conn)
                if output_already_assigned_result['DATA'] is None:
                    output = {
                        'CODE': 'URI_PARAMETERS_OK',
                        'TEXT': "Les paramètres d'URI sont conformes.",
                        'DATA': {
                            'URI_Id_Utilisateur': URI_Id_Utilisateur,
                            'INS': INS,
                            'LOINC_Code': LOINC_Code
                        }
                    }
                else:
                    output = {
                        'CODE': 'ALREADY_ASSIGNED_GRADE',
                        'TEXT': "Le patient {} a déjà une valeur dans l'examen {}".format(INS, LOINC_Code),
                        'DATA': None
                    }
                    
            elif methode == 'PUT' or methode == 'DELETE':
                output_already_assigned_result = already_assigned_result_test.has_result_already_been_assigned(URI_Id_Utilisateur, LOINC_Code, conn)
                if output_already_assigned_result['DATA'] is None:
                    output = output_already_assigned_result
                else:
                    output = {
                        'CODE': 'URI_PARAMETERS_OK',
                        'TEXT': "Les paramètres d'URI sont conformes.",
                        'DATA': {
                            'URI_Id_Utilisateur': URI_Id_Utilisateur,
                            'INS': INS,
                            'LOINC_Code': LOINC_Code,
                            'Valeur': output_already_assigned_result['DATA']['Valeur']
                        }
                    }
            elif methode == 'GET':
                output = {
                    'CODE': 'URI_PARAMETERS_OK',
                    'TEXT': "Les paramètres d'URI sont conformes.",
                    'DATA': {
                        'URI_Id_Utilisateur': URI_Id_Utilisateur,
                        'INS': INS,
                        'LOINC_Code': LOINC_Code
                    }
                }
            else:
                output = {
                    'CODE': 'UNAUTHORIZED_METHOD',
                    'TEXT': "La méthode {} n'est pas autorisée. Seules les méthodes GET, POST, PUT et DELETE sont autorisées.".format(methode),
                    'DATA': None
                }
    return output