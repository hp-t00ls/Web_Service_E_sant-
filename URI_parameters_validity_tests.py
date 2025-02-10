import dblib
from  cipherlib import cipherlib

def check_validity_INS(conn, INS):
    db_cursor = dblib.get_cursor(conn)
    if INS == 'all':
        output = {
            'CODE': 'VALID_URI_PARAMETER_VALUE_INS',
            'TEXT': "La valeur du paramètre d'URI INS est connue.",
            'DATA': {
                'INS': 'all',
                'URI_Id_Utilisateur': 'all'
            }
        }
    else:
        output_get_cipher_specifications = cipherlib.get_cipher_specifications()
        if output_get_cipher_specifications['DATA'] is None:
                    output = output_get_cipher_specifications
        else:
            cipher_specifications = output_get_cipher_specifications['DATA']
            request = """SELECT `Id_Utilisateur`, `INS`
        				FROM `Utilisateur`"""
            db_cursor.execute(request)
            resultat = db_cursor.fetchall()
            db_cursor.close()
            trouve = False
            for ligne in resultat:
                if not ligne[1] is None:
                    INS_BdD_dechiffre = cipherlib.fernet_cipher(ligne[1], "string", cipher_specifications["Utilisateur"]["cle"], "decrypt")
                    if INS == INS_BdD_dechiffre:
                        trouve = True
                        break
        if trouve == False:
            output = {
                'CODE': 'INVALID_URI_PARAMETER_VALUE_INS',
                'TEXT': "La valeur du paramètre d'URI INS est inconnue.",
                'DATA': None
            }
        else:
            URI_Id_Utilisateur = ligne[0]
            output = {
                'CODE': 'VALID_URI_PARAMETER_VALUE_INS',
                'TEXT': "La valeur du paramètre d'URI INS est connue.",
                'DATA': {
                    'INS': INS,
                    'URI_Id_Utilisateur': URI_Id_Utilisateur
                }
            }
    dblib.cursor_close(db_cursor)
    return output

def check_validity_LOINC_Code(conn, LOINC_Code, methode):
    db_cursor = dblib.get_cursor(conn)
    if LOINC_Code == 'all':
        if methode == 'GET':
            
            output = {
                'CODE': 'VALID_URI_PARAMETER_VALUE_LOINC_Code',
                'TEXT': "La valeur du paramètre d'URI LOINC_Code est connue.",
                'DATA': 'all'
            }
        else:
            output = {
                'CODE': 'INVALID_URI_PARAMETER_VALUE_LOINC_Code',
                'TEXT': "La valeur 'all' du paramètre d'URI LOINC_Code est réservée aux requêtes avec la méthode GET.",
                'DATA': None
            }
    else:
        request = """SELECT * 
                    FROM `Examen_Biologie`
                    WHERE `LOINC_Code`=%s"""
    
        params = (LOINC_Code,)
    
        db_cursor.execute(request, params)
        resultats = db_cursor.fetchone()
        if resultats is None:
            output = {
                'CODE': 'INVALID_URI_PARAMETER_VALUE_LOINC_Code',
                'TEXT': "La valeur du paramètre d'URI LOINC_Code est inconnue.",
                'DATA': None
            }
        else:
            output = {
                'CODE': 'VALID_URI_PARAMETER_VALUE_LOINC_Code',
                'TEXT': "La valeur du paramètre d'URI LOINC_Code est connue.",
                'DATA': LOINC_Code
            }
    dblib.cursor_close(db_cursor)
    return output

def check_validity_URI_parameters(conn, INS, LOINC_Code, methode):
    output_INS = check_validity_INS(conn, INS)
    if output_INS['DATA'] is None:
        output = output_INS
    else:
        URI_Id_Utilisateur = output_INS['DATA']['URI_Id_Utilisateur']
        output_LOINC_Code = check_validity_LOINC_Code(conn, LOINC_Code, methode)
        if output_LOINC_Code['DATA'] is None:
            output = output_LOINC_Code
        else:
            output = {
                'CODE': 'VALID_ALL_URI_PARAMETERS',
                'TEXT': "Les paramètres d'URI sont tous valides.",
                'DATA' : {
                    'URI_Id_Utilisateur': URI_Id_Utilisateur,
                    'INS': INS,
                    'LOINC_Code': LOINC_Code,
                }
            }
    return output