import json
import dblib

def check_validity_Valeur(Valeur):
    try:
        # Conversion de la chaîne en float
        val = float(Valeur)
        # Vérification que la valeur est entre 0 et 20
        if 0 <= val and val <= 100:
            output = {
                'CODE': 'VALID_BODY_PARAMETER_VALUE_Valeur',
                'TEXT': "Le paramètre de corps de requête note est valide.",
                'DATA': Valeur
            }
        else:
            output = {
                'CODE': 'OUT_OF_RANGE_BODY_PARAMETER_Valeur',
                'TEXT': "Le paramètre de corps de requête Note est en dehors de l'intervalle autorisé. Seule une valeur numérique entre 0 et 20 est acceptée.",
                'DATA': None
            }
    except ValueError:
        # La conversion en float a échoué, donc ce n'est pas une valeur numérique
        output = {
            'CODE': 'WRONG_BODY_PARAMETER_TYPE_VALEUR_RESULTAT',
            'TEXT': "Le paramètre de corps de requête Valeur n'est pas un numérique. Seule une valeur numérique comprise entre 0 et 20 est acceptée.",
            'DATA': None
        }
    return output

def check_validity_Id_Utilisateur(conn, Id_Utilisateur):
    db_cursor = dblib.get_cursor(conn)
    if Id_Utilisateur=='all':
        output = {
            'CODE': 'VALID_URI_PARAMETER_VALUE_id_patient',
            'TEXT': "La valeur du paramètre d'URI id_patient est connue.",
            'DATA': 'all'
        }
    else:
        request = """SELECT *
                    FROM `Utilisateur`
                    WHERE `Id_Utilisateur` = %s"""

        params = (Id_Utilisateur,)
    
        db_cursor.execute(request, params)
        Result = db_cursor.fetchone()
        if Result is None:
            output = {
                'CODE': 'INVALID_URI_PARAMETER_VALUE_ID_UTILISATEUR',
                'TEXT': "La valeur du paramètre d'URI Id_Utilisateur est inconnue.",
                'DATA': None
            }
        else:
            output = {
                'CODE': 'VALID_URI_PARAMETER_VALUE_ID_UTILISATEUR',
                'TEXT': "La valeur du paramètre d'URI Id_Utilisateur est connue.",
                'DATA': {
                    'Id_Utilisateur': Id_Utilisateur
                }
            }
    dblib.cursor_close(db_cursor)
    return output

def check_validity_data(conn, data, methode):
    if not isinstance(data, str):
        output = {
            'CODE': 'WRONG_BODY_PARAMETER_TYPE_data',
            'TEXT': "Le paramètre data est du mauvais type de données. Seul une donnée de type chaîne de caractères est acceptée.",
            'DATA': None
        }
    else:   
        try:
            unserialized_data = json.loads(data)
            if not isinstance(unserialized_data, dict):
                output = {
                    'CODE': 'WRONG_BODY_PARAMETER_TYPE_data',
                    'TEXT': "Le paramètre data est du mauvais type de données. Seul un dictionnaire sérializé au format JSON est accepté.",
                    'DATA': None
                }
            else:
                if not 'Id_Utilisateur' in unserialized_data:
                        output = {
                            'CODE': "MISSING_PARAMETER_KEY_Id_Utilisateur",
                            'TEXT': "La clé Id_Utilisateur est manquante dans le dictionnaire data",
                            'DATA': None
                        }
                elif not 'Valeur' in unserialized_data and methode!='DELETE':
                    output = {
                     'CODE': 'MISSING_PARAMETER_KEY_Valeur',
                     'TEXT': "La clé Valeur est manquante dans le dictionnaire data",
                     'DATA': None
                    }
                else:
                    Valeur = unserialized_data['Valeur']
                    output_validity_Valeur = check_validity_Valeur(Valeur)

                    if output_validity_Valeur['DATA'] is None:
                        output = output_validity_Valeur
                    else:
                        Id_Utilisateur = unserialized_data['Id_Utilisateur']
                        output_validity_Id_Utilisateur = check_validity_Id_Utilisateur(conn, Id_Utilisateur)
                        if output_validity_Id_Utilisateur['DATA'] is None:
                            output = output_validity_Id_Utilisateur
                        else:
                            output = {
                                'CODE': 'VALID_BODY_DATA',
                                'TEXT': "Les données de corps de requête sont valides.",
                                'DATA': {
                                    'Id_Utilisateur': Id_Utilisateur,
                                    'Valeur': Valeur   
                                }
                            }
        except ValueError:
            output = {
                'CODE': 'WRONG_TYPE_BODY_PARAMETER_data',
                'TEXT': "Le paramètre data est du mauvais type de données. Seul une donnée de type chaîne de caractères de type JSON est acceptée.",
                'DATA': None
            }
        return output


def check_validity_body_parameters(conn, httpData, methode):
    data = httpData['DATA']
    output = check_validity_data(conn, data, methode)
    return output