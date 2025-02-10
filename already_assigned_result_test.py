import dblib
from cipherlib import cipherlib

def has_result_already_been_assigned(Id_Patient, LOINC_Code, conn):
    db_cursor = dblib.get_cursor(conn)
    params = (Id_Patient, LOINC_Code)
        
    requete = """SELECT `Valeur`
                FROM `Resultat_Examen`
                WHERE `Id_Utilisateur`=%s AND `LOINC_Code`=%s;""" 
    
    db_cursor.execute(requete, params)
    Result = db_cursor.fetchone()
    dblib.cursor_close(db_cursor)

    already_assigned_result = Result is not None
    
    if already_assigned_result:        
        output_get_cipher_specifications = cipherlib.get_cipher_specifications()
        if output_get_cipher_specifications['DATA'] is None:
                    output = output_get_cipher_specifications
        else:
            cipher_specifications = output_get_cipher_specifications['DATA']
            Valeur = cipherlib.fernet_cipher(Result[0], "float", cipher_specifications["Resultat_Examen"]["cle"], "decrypt")
            output = {
            'CODE': 'ALREADY_ASSIGNED_RESULT',
            'TEXT': "Le patient {} a déjà reçu le résultat {} pour l'examen {}.". format(Id_Patient, Valeur, LOINC_Code),
            'DATA': {
                'Id_Patient': Id_Patient,
                'LOINC_Code': LOINC_Code,
                'Valeur': Valeur
            }
        }
    else:
        output = {
            'CODE': 'UNASSIGNED_RESULT',
            'TEXT': "Le résultat du patient {} pour l'examen {} n'a pas encore été affecté.". format(Id_Patient, LOINC_Code),
            'DATA': None
        }
    
    return output
