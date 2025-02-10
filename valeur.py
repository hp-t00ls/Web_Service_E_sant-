#!/usr/bin/env python3

print('Content-type: application/json\n')
output = {}  # Initialize output to avoid NameError
from cipherlib import cipherlib
import dblib
import tests
import db_interaction
import json
import os

output_get_cipher_specifications = cipherlib.get_cipher_specifications()
if output_get_cipher_specifications['DATA'] is None:
        output = output_get_cipher_specifications 
else:
    output_database_connection = dblib.db_connection()
    if output_database_connection['DATA'] is None:
        output = output_database_connection
    else:
        conn = output_database_connection['DATA']
        if os.environ['REQUEST_METHOD'] == 'GET':
            output_tests = tests.proceed_all_tests(conn, 'GET')
            if output_tests['DATA'] is None:
                output = output_tests
            else:
                Login_Utilisateur = output_tests['DATA']['Login_Utilisateur']
                Login_Id_Utilisateur = output_tests['DATA']['Login_Id_Utilisateur']
                LOINC_Code = output_tests['DATA']['LOINC_Code']
                INS = output_tests['DATA']['INS']
                output_Utilisateur_rights = tests.check_patient_rights(conn, Login_Utilisateur, INS)
                if output_Utilisateur_rights['DATA'] is None:
                    output = output_Utilisateur_rights
                else:
                    URI_Id_Utilisateur = output_tests['DATA']['URI_Id_Utilisateur']
                    output = db_interaction.get_Resultat_Examen(URI_Id_Utilisateur, LOINC_Code, conn)
        elif os.environ['REQUEST_METHOD'] == 'POST': 
            output_tests = tests.proceed_all_tests(conn, 'POST')
            if output_tests['DATA'] is None:
                output = output_tests
            else:
                Login_Id_Utilisateur = output_tests['DATA']['Login_Id_Utilisateur']
                URI_Id_Utilisateur = output_tests['DATA']['URI_Id_Utilisateur']
                LOINC_Code = output_tests['DATA']['LOINC_Code']
                Valeur = output_tests['DATA']['Valeur']
                output = db_interaction.post_Resultat_Examen(URI_Id_Utilisateur, LOINC_Code, Valeur, conn)
                
        elif os.environ['REQUEST_METHOD'] == 'PUT':
            output_tests = tests.proceed_all_tests(conn, 'PUT')
            if output_tests['DATA'] is None:
                output = output_tests
            else:
                Login_Id_Utilisateur = output_tests['DATA']['Login_Id_Utilisateur']
                URI_Id_Utilisateur = output_tests['DATA']['URI_Id_Utilisateur']
                LOINC_Code = output_tests['DATA']['LOINC_Code']
                Valeur_after_update = output_tests['DATA']['Valeur_After_Update']
                
                output = db_interaction.update_Resultat_Examen(URI_Id_Utilisateur, LOINC_Code, Valeur_after_update, conn)
        elif os.environ['REQUEST_METHOD'] == 'DELETE':
            output_tests = tests.proceed_all_tests(conn, 'DELETE')
            if output_tests['DATA'] is None:
                output = output_tests
            else:
                Login_Utilisateur= output_tests['DATA']['Login_Utilisateur']
                Login_Id_Utilisateur = output_tests['DATA']['Login_Id_Utilisateur']
                LOINC_Code = output_tests['DATA']['LOINC_Code']
                INS = output_tests['DATA']['INS']
                output_patients_rights = tests.check_patient_rights(conn, Login_Utilisateur, INS)
                if output_patients_rights['DATA'] is None:
                    output = output_patients_rights
                else:
                    URI_Id_Utilisateur = output_tests['DATA']['URI_Id_Utilisateur']
                    output = db_interaction.delete_Resultat_Examen(URI_Id_Utilisateur, LOINC_Code, conn)
        else:
            output = {
                'CODE': 'UNAUTHORIZED_METHOD',
                'TEXT': "Une méthode non autorisée a été utilisée. Seules les méthodes GET, POST, PUT et DELETE sont acceptées.",
                'DATA': None
            }
        dblib.db_close(conn)
print(json.dumps(output))