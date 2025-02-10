import rights_tests
import parameters_tests
import dblib
from  cipherlib import cipherlib

def proceed_all_tests(conn, methode):
    output_rights_tests = rights_tests.check_authentication_and_rights(conn, methode)
    if output_rights_tests['DATA'] is None:
        output = output_rights_tests
    else:
        output_parameters_tests = parameters_tests.check_parameters(conn, methode)
        if output_parameters_tests['DATA'] is None:
            output = output_parameters_tests
        elif methode == 'GET': 
            output = {
                'CODE': 'ALL_TESTS_OK',
                'TEXT': "Les tests se sont tous déroulés avec succès.",
                'DATA': {
                    'Login_Utilisateur': output_rights_tests['DATA']['Login_Utilisateur'],
                    'Mot_de_Passe': output_rights_tests['DATA']['Mot_de_Passe'],
                    'Login_Id_Utilisateur': output_rights_tests['DATA']['Login_Id_Utilisateur'],
                    'URI_Id_Utilisateur': output_parameters_tests['DATA']['URI_Id_Utilisateur'],
                    'INS': output_parameters_tests['DATA']['INS'],
                    'Categorie_Utilisateur': output_rights_tests['DATA']['Categorie_Utilisateur'],
                    'LOINC_Code': output_parameters_tests['DATA']['LOINC_Code']
                }
            }
        elif methode == 'POST':
            output = {
                'CODE': 'ALL_TESTS_OK',
                'TEXT': "Les tests se sont tous déroulés avec succès.",
                'DATA': {
                    'Login_Utilisateur': output_rights_tests['DATA']['Login_Utilisateur'],
                    'Mot_de_Passe': output_rights_tests['DATA']['Mot_de_Passe'],
                    'Login_Id_Utilisateur': output_rights_tests['DATA']['Login_Id_Utilisateur'],
                    'URI_Id_Utilisateur': output_parameters_tests['DATA']['URI_Id_Utilisateur'],
                    'INS': output_parameters_tests['DATA']['INS'],
                    'Categorie_Utilisateur': output_rights_tests['DATA']['Categorie_Utilisateur'],
                    'LOINC_Code': output_parameters_tests['DATA']['LOINC_Code'],
                    'Valeur': output_parameters_tests['DATA']['Valeur']
                }
            }
        elif methode == 'PUT':
            output = {
                'CODE': 'ALL_TESTS_OK',
                'TEXT': "Les tests se sont tous déroulés avec succès.",
                'DATA': {
                    'Login_Utilisateur': output_rights_tests['DATA']['Login_Utilisateur'],
                    'Mot_de_Passe': output_rights_tests['DATA']['Mot_de_Passe'],
                    'Login_Id_Utilisateur': output_rights_tests['DATA']['Login_Id_Utilisateur'],
                    'URI_Id_Utilisateur': output_parameters_tests['DATA']['URI_Id_Utilisateur'],
                    'INS': output_parameters_tests['DATA']['INS'],
                    'Categorie_Utilisateur': output_rights_tests['DATA']['Categorie_Utilisateur'],
                    'LOINC_Code': output_parameters_tests['DATA']['LOINC_Code'],
                    'Valeur_After_Update': output_parameters_tests['DATA']['Valeur_After_Update'],
                    'Valeur_Before_Update': output_parameters_tests['DATA']['Valeur_Before_Update']
                }
            }
        elif methode == 'DELETE':
            output = {
                'CODE': 'ALL_TESTS_OK',
                'TEXT': "Les tests se sont tous déroulés avec succès.",
                'DATA': {
                    'Login_Utilisateur': output_rights_tests['DATA']['Login_Utilisateur'],
                    'Mot_de_Passe': output_rights_tests['DATA']['Mot_de_Passe'],
                    'Login_Id_Utilisateur': output_rights_tests['DATA']['Login_Id_Utilisateur'],
                    'URI_Id_Utilisateur': output_parameters_tests['DATA']['URI_Id_Utilisateur'],
                    'INS': output_parameters_tests['DATA']['INS'],
                    'Categorie_Utilisateur': output_rights_tests['DATA']['Categorie_Utilisateur'],
                    'LOINC_Code': output_parameters_tests['DATA']['LOINC_Code'],
                    'Resultat_Examen_Before_Delete': output_parameters_tests['DATA']['Valeur_Before_Delete']
                }
            }
        else:
            output = {
                'CODE': 'UNAUTHORIZED_METHOD',
                'TEXT': "La méthode {} n'est pas autorisée. Seules les méthodes GET, POST, PUT et DELETE sont autorisées.".format(methode),
                'DATA': None
            }
    return output

def get_Categorie_Utilisateur_From_Login(conn, login):
    db_cursor = dblib.get_cursor(conn)
    output_get_cipher_specifications = cipherlib.get_cipher_specifications()
    if output_get_cipher_specifications['DATA'] is None:
                output = output_get_cipher_specifications
    else:
        cipher_specifications = output_get_cipher_specifications['DATA']
        requete = """SELECT `Utilisateur`.`Id_Utilisateur`, `Utilisateur`.`Login_Utilisateur`, `Categorie_Utilisateur`.`Libelle_Categorie_Utilisateur`
                    FROM `Utilisateur`
                    JOIN `Categorie_Utilisateur` ON `Utilisateur`.`Id_Categorie_Utilisateur`=`Categorie_Utilisateur`.`Id_Categorie_Utilisateur`
                    """
    db_cursor.execute(requete)
    resultat = db_cursor.fetchall()  
    dblib.cursor_close(db_cursor)
    trouve = False
    for ligne in resultat:
        login_BdD_dechiffre = cipherlib.fernet_cipher(ligne[1], "string", cipher_specifications["Utilisateur"]["cle"], "decrypt")
        if login == login_BdD_dechiffre:
            trouve = True
            categorie_utilisateur = cipherlib.fernet_cipher(ligne[2], "string", cipher_specifications["Categorie_Utilisateur"]["cle"], "decrypt")
            break

    if trouve == False:
        output = {
            'CODE': 'WRONG_PARAMETER_VALUE_Id_Utilisateur',
            'TEXT': "La valeur du paramètre Id_Utilisateur est inconnue de la base de données.",
            'DATA': None
        }
    else:
        output = {
            'CODE': 'SQL_QUERY_OK',
            'TEXT' : "La requête s'est exécutée correctement.",
            'DATA': {
                'Login_Id_Utilisateur': ligne[0],
                'Categorie_Utilisateur': categorie_utilisateur
            }
            
        }
    return output

def get_Id_Utilisateur_From_INS(conn, INS):
    if INS == "all":
        output = {
            'CODE': 'FOUND_ID_UTILISATEUR',
            'TEXT': "La valeur du paramètre Id_Utilisateur a été trouvée à partir de l'INS",
            'DATA': {
                'INS': INS,
                'Id_Utilisateur': 'all'
            }
        }
    else:
        output_get_cipher_specifications = cipherlib.get_cipher_specifications()
        if output_get_cipher_specifications['DATA'] is None:
                    output = output_get_cipher_specifications
        else:
            cipher_specifications = output_get_cipher_specifications['DATA']
        
        db_cursor = dblib.get_cursor(conn)            
        requete = """SELECT `Utilisateur`.`Id_Utilisateur`, `Categorie_Utilisateur`.`Libelle_Categorie_Utilisateur`, `Utilisateur`.`INS` 
                    FROM `Utilisateur`
                    JOIN `Categorie_Utilisateur` ON `Utilisateur`.`Id_Categorie_Utilisateur`=`Categorie_Utilisateur`.`Id_Categorie_Utilisateur`
                    """
        db_cursor.execute(requete)
        resultat = db_cursor.fetchall()
        dblib.cursor_close(db_cursor)

        trouve = False
        for liste in resultat:
                INS_BdD_dechiffre = cipherlib.fernet_cipher(liste[2], "string", cipher_specifications["Utilisateur"]["cle"], "decrypt")
                if INS == INS_BdD_dechiffre:
                    categorie_utilisateur = cipherlib.fernet_cipher(liste[1], "string", cipher_specifications["Categorie_Utilisateur"]["cle"], "decrypt")
                    trouve = True
                    break

        if trouve == False:
            output = {
                'CODE': 'WRONG_PARAMETER_VALUE_INS',
                'TEXT': "La valeur du paramètre INS est inconnue de la base de données.",
                'DATA': None
                }
        else:
            output = {
                'CODE': 'SQL_QUERY_OK',
                'TEXT': "La requête s'est exécutée correctement.",
                'DATA':{
                        'INS': INS,
                        'Id_Utilisateur': liste[0],
                        'Categorie_Utilisateur': categorie_utilisateur
                    }
                }       
    return output

def check_patient_rights(conn, Login_Utilisateur, INS):
    output_categorie_utilisateur = get_Categorie_Utilisateur_From_Login(conn, Login_Utilisateur)
    if output_categorie_utilisateur['DATA'] is None:
        output = output_categorie_utilisateur
    else:
        Login_Id_Utilisateur = output_categorie_utilisateur['DATA']['Login_Id_Utilisateur']
        Categorie_Utilisateur = output_categorie_utilisateur['DATA']['Categorie_Utilisateur']
        output_URI_Id_Utilisateur = get_Id_Utilisateur_From_INS(conn, INS)
        if output_URI_Id_Utilisateur['DATA'] is None:
            output = output_URI_Id_Utilisateur
        else:
            URI_Id_Utilisateur = output_URI_Id_Utilisateur['DATA']['Id_Utilisateur']
        
            if Categorie_Utilisateur != 'Patient':
                output = {
                    'CODE': 'AUTHORIZED_OPERATION',
                    'TEXT': "L'opération demandée est autorisée pour cet utilisateur.",
                    'DATA': {
                        'Login_Id_Utilisateur': Login_Id_Utilisateur,
                        'URI_Id_Utilisateur': URI_Id_Utilisateur,
                        'Categorie_Utilisateur': Categorie_Utilisateur
                    }
                }
                
            else:
                # L'utilisateur est un patient
                if INS == "all":
                    output = {
                        'CODE': 'UNAUTHORIZED_OPERATION',
                        'TEXT': "L'opération demandée est interdite. Un étudiant ne peut avoir accès aux notes de l'ensemble des étudiants.",
                        'DATA': None
                    }
                elif int(Login_Id_Utilisateur) != int(URI_Id_Utilisateur):
                    output = {
                        'CODE': 'UNAUTHORIZED_OPERATION',
                        'TEXT': "L'opération demandée est interdite. Un étudiant ne peut avoir accès aux notes d'un autre étudiant.",
                        'DATA': None
                    }
                else:
                    output = {
                        'CODE': 'AUTHORIZED_OPERATION',
                        'TEXT': "L'opération demandée est autorisée pour cet utilisateur.",
                        'DATA': {
                            'Login_Id_Utilisateur': Login_Id_Utilisateur,
                            'URI_Id_Utilisateur': URI_Id_Utilisateur,
                            'Categorie_Utilisateur': Categorie_Utilisateur
                        }
                    }
    return output