import URI_parameters_tests
import headers_parameters_tests
import body_parameters_tests
import wslib 
from  cipherlib import cipherlib
import dblib

def check_match_between_Id_Utilisateur_and_INS(conn, INS, Id_Utilisateur):
    db_cursor = dblib.get_cursor(conn)
    requete = """SELECT `INS`, `Id_Utilisateur`
                FROM `Utilisateur`
                """
    db_cursor.execute(requete)
    resultat = db_cursor.fetchall()
    output_get_cipher_specifications = cipherlib.get_cipher_specifications()
    if output_get_cipher_specifications['DATA'] is None:
                output = output_get_cipher_specifications
    else:
        cipher_specifications = output_get_cipher_specifications['DATA']
        couple_INS_Id_Utilisateur = [INS, int(Id_Utilisateur)]
        trouve = False
        for Tuple in resultat:
            ligne = list(Tuple)
            if ligne[0] is not None:
                decrypted_INS = cipherlib.fernet_cipher(ligne[0], "string", cipher_specifications["Utilisateur"]["cle"], "decrypt")
                ligne[0] = decrypted_INS
                if couple_INS_Id_Utilisateur == ligne:
                    trouve = True
                    break
    
        if trouve == False:
            output = {
                'CODE': 'NO_MATCH_BETWEEN_Id_Utilisateur_AND_INS',
                'TEXT': "L'INS fourni et l'Id_Utilisateur ne correspondent pas.",
                'DATA': None
            }
        else:
            output = {
                'CODE': 'MATCH_BETWEEN_Id_Utilisateur_AND_INS',
                'TEXT': "L'INS fourni et l'Id_Utilisateur correspondent.",
                'DATA': {
                    'Id_Utilisateur': Id_Utilisateur,
                    'INS': INS
                }
            }
        dblib.cursor_close(db_cursor)
    return output

def check_parameters(conn, methode):
    httpData = wslib.returnHttpData()
    output_URI_parameters = URI_parameters_tests.check_URI_parameters(methode, httpData, conn)
    if output_URI_parameters['DATA'] is None:
        output = output_URI_parameters
    else:
        output_headers_parameters = headers_parameters_tests.check_headers_parameters()
        if output_headers_parameters['DATA'] is None:
            output = output_headers_parameters
        else:
            if methode == 'POST':
                output_body_parameters = body_parameters_tests.check_body_parameters(conn, httpData, 'POST')
                if output_body_parameters['DATA'] is None:
                    output = output_body_parameters
                else:
                    INS = output_URI_parameters['DATA']['INS']
                    Body_Id_Utilisateur = output_body_parameters['DATA']['Id_Utilisateur']
                    output_match_between_Id_Utilisateur_and_INS = check_match_between_Id_Utilisateur_and_INS(conn, INS, Body_Id_Utilisateur)
                    if output_match_between_Id_Utilisateur_and_INS['DATA'] is None:
                        output = output_match_between_Id_Utilisateur_and_INS
                    else:
                        output = {
                            'CODE': 'PARAMETERS_OK',
                            'TEXT': "Les paramètres sont tous conformes.",
                            'DATA': {
                                'INS': output_URI_parameters['DATA']['INS'],
                                'URI_Id_Utilisateur': output_URI_parameters['DATA']['URI_Id_Utilisateur'],
                                'Body_Id_Utilisateur': Body_Id_Utilisateur,
                                'LOINC_Code': output_URI_parameters['DATA']['LOINC_Code'],
                                'Content-Type': output_headers_parameters['DATA']['Content-Type'],
                                'Valeur': output_body_parameters['DATA']['Valeur']
                            }
                        }

            elif methode == 'PUT':
                output_body_parameters = body_parameters_tests.check_body_parameters(conn, httpData, 'PUT')
                if output_body_parameters['DATA'] is None:
                    output = output_body_parameters
                else:
                    INS = output_URI_parameters['DATA']['INS']
                    Body_Id_Utilisateur = output_body_parameters['DATA']['Id_Utilisateur']
                    output_match_between_Id_Utilisateur_and_INS = check_match_between_Id_Utilisateur_and_INS(conn, INS, Body_Id_Utilisateur)
                    if output_match_between_Id_Utilisateur_and_INS['DATA'] is None:
                        output = output_match_between_Id_Utilisateur_and_INS
                    else:
                        output = {
                            'CODE': 'PARAMETERS_OK',
                            'TEXT': "Les paramètres sont tous conformes.",
                            'DATA': {
                                'INS': output_URI_parameters['DATA']['INS'],
                                'URI_Id_Utilisateur': output_URI_parameters['DATA']['URI_Id_Utilisateur'],
                                'Body_Id_Utilisateur': Body_Id_Utilisateur,
                                'LOINC_Code': output_URI_parameters['DATA']['LOINC_Code'],
                                'Content-Type': output_headers_parameters['DATA']['Content-Type'],
                                'Valeur_After_Update': output_body_parameters['DATA']['Valeur'],
                                'Valeur_Before_Update': output_URI_parameters['DATA']['Valeur']
                            }
                        }
            elif methode == 'DELETE':
                output_body_parameters = body_parameters_tests.check_body_parameters(conn, httpData, 'DELETE')
                if output_body_parameters['DATA'] is None:
                    output = output_body_parameters
                else:
                    INS = output_URI_parameters['DATA']['INS']
                    Body_Id_Utilisateur = output_body_parameters['DATA']['Id_Utilisateur']
                    output_match_between_Id_Utilisateur_and_INS = check_match_between_Id_Utilisateur_and_INS(conn, INS, Body_Id_Utilisateur)
                    if output_match_between_Id_Utilisateur_and_INS['DATA'] is None:
                        output = output_match_between_Id_Utilisateur_and_INS
                    else:
                        output = {
                            'CODE': 'PARAMETERS_OK',
                            'TEXT': "Les paramètres sont tous conformes.",
                            'DATA': {
                                'INS': output_URI_parameters['DATA']['INS'],
                                'URI_Id_Utilisateur': output_URI_parameters['DATA']['URI_Id_Utilisateur'],
                                'Body_Id_Utilisateur': Body_Id_Utilisateur,
                                'LOINC_Code': output_URI_parameters['DATA']['LOINC_Code'],
                                'Content-Type': output_headers_parameters['DATA']['Content-Type'],
                                'Valeur_Before_Delete': output_URI_parameters['DATA']['Valeur']
                            }
                        }
            elif methode == 'GET':
                output = output_URI_parameters
            else:
                output = {
                    'CODE': 'UNAUTHORIZED_METHOD',
                    'TEXT': "La méthode {} n'est pas autorisée. Seules les méthodes GET, POST, PUT et DELETE sont autorisées.".format(methode),
                    'DATA': None
                }
    return output