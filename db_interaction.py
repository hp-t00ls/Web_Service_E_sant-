import dblib
from mysql.connector import Error
from cipherlib import cipherlib

def get_Resultat_Examen(Id_Patient, LOINC_Code, conn):
    db_cursor = dblib.get_cursor(conn)
    if Id_Patient == "all" and LOINC_Code == "all":
        where = ""
        params = None
    elif Id_Patient == "all":
        where = " WHERE `Resultat_Examen`.`LOINC_Code`=%s"
        params = (LOINC_Code,)
    elif LOINC_Code == "all":
        where = " WHERE `Resultat_Examen`.`Id_Utilisateur`=%s"
        params = (Id_Patient,)
    else:
        where = " WHERE `Resultat_Examen`.`Id_Utilisateur`=%s and `Resultat_Examen`.`LOINC_Code`=%s"
        params = (Id_Patient, LOINC_Code) 

    requete = """SELECT `Resultat_Examen`.`Id_Utilisateur`, 
                        `Resultat_Examen`.`LOINC_Code`, 
                        `Resultat_Examen`.`Valeur`, 
                        `Utilisateur`.`Nom_Utilisateur`, 
                        `Utilisateur`.`Login_Utilisateur`,
                        `Examen_Biologie`.`Libelle_Examen_Biologie`
                FROM `Resultat_Examen`
                JOIN `Utilisateur` ON `Utilisateur`.`Id_Utilisateur`=`Resultat_Examen`.`Id_Utilisateur`
                JOIN `Examen_Biologie` ON `Examen_Biologie`.`LOINC_Code`=`Resultat_Examen`.`LOINC_Code`
                {};""" . format(where)
    
    
    db_cursor.execute(requete, params)
    output_get_cipher_specifications = cipherlib.get_cipher_specifications()
    if output_get_cipher_specifications['DATA'] is None:
                output = output_get_cipher_specifications
    else:
        cipher_specifications = output_get_cipher_specifications['DATA']   
        all_resultats = []
        for Resultat_Examen in db_cursor:
            Id_Patient = Resultat_Examen[0]
            LOINC_Code = Resultat_Examen[1]
            Valeur = cipherlib.fernet_cipher(Resultat_Examen[2],"float", cipher_specifications["Resultat_Examen"]["cle"],"decrypt")
            Nom_Utilisateur = cipherlib.fernet_cipher(Resultat_Examen[3],"string", cipher_specifications["Utilisateur"]["cle"],"decrypt")
            Login_Utilisateur = Resultat_Examen[4]
            Libelle_Examen_Biologie = Resultat_Examen[5]
            all_resultats.append(
                {
                    'Id_Patient': Id_Patient,
                    'Nom_Utilisateur': Nom_Utilisateur,
                    'Login_Utilisateur': Login_Utilisateur,
                    'LOINC_Code': LOINC_Code,
                    'Libelle_Examen_Biologie': Libelle_Examen_Biologie,
                    'Valeur': Valeur
                }
            )
        if db_cursor.rowcount==0:
            output = {
                'CODE' : 'UNASSIGNED_RESULT',
                'TEXT': "Le résultat demandée n'a pas encore été affectée.",
                'DATA': None
            }
        else:
            output = {
                'CODE': 'QUERY_OK',
                'TEXT': "La requête est conforme et a pu être exécutée correctement.",
                'DATA' : all_resultats
            }  
        dblib.cursor_close(db_cursor)
    return output

def get_all_Resultat_Examen(conn):
    db_cursor = dblib.get_cursor(conn)
    requete = """SELECT `Resultat_Examen`.`Id_Utilisateur`, 
                        `Resultat_Examen`.`LOINC_Code`, 
                        `Resultat_Examen`.`Valeur`, 
                        `Utilisateur`.`Nom_Utilisateur`, 
                        `Utilisateur`.`Login_Utilisateur`,
                        `Examen_Biologie`.`Libelle_Examen_Biologie`
                FROM `Resultat_Examen`
                JOIN `Utilisateur` ON `Utilisateur`.`Id_Utilisateur`=`Resultat_Examen`.`Id_Utilisateur`
                JOIN `Examen_Biologie` ON `Examen_Biologie`.`LOINC_Code`=`Resultat_Examen`.`LOINC_Code`;"""
    db_cursor.execute(requete)
    output_get_cipher_specifications = cipherlib.get_cipher_specifications()
    if output_get_cipher_specifications['DATA'] is None:
                output = output_get_cipher_specifications
    else:
        cipher_specifications = output_get_cipher_specifications['DATA']   
        output = []
        for Resultat_Examen in db_cursor:
            Id_Patient = Resultat_Examen[0]
            LOINC_Code = Resultat_Examen[1]
            Valeur = cipherlib.fernet_cipher(Resultat_Examen[2],"float", cipher_specifications["Resultat_Examen"]["cle"],"decrypt")
            Nom_Utilisateur = cipherlib.fernet_cipher(Resultat_Examen[3],"string", cipher_specifications["Utilisateur"]["cle"],"decrypt")
            Login_Utilisateur = Resultat_Examen[4]
            Libelle_Examen_Biologie = Resultat_Examen[5]
            output.append(
                {
                    'Id_Patient': Id_Patient,
                    'Nom_Utilisateur': Nom_Utilisateur,
                    'Login_Utilisateur': Login_Utilisateur,
                    'LOINC_Code': LOINC_Code,
                    'Libelle_Examen_Biologie': Libelle_Examen_Biologie,
                    'Valeur': Valeur
                }
            )
            
        dblib.cursor_close(db_cursor)
        return output

def post_Resultat_Examen(Id_Utilisateur, LOINC_Code, Valeur, conn):
    db_cursor = dblib.get_cursor(conn)

    output_get_cipher_specifications = cipherlib.get_cipher_specifications()
    if output_get_cipher_specifications['DATA'] is None:
                output = output_get_cipher_specifications
    else:
        cipher_specifications = output_get_cipher_specifications['DATA']
        Valeur = cipherlib.fernet_cipher(Valeur, "float", cipher_specifications["Resultat_Examen"]["cle"], "encrypt")
        requete = """INSERT INTO `Resultat_Examen`(`Id_Utilisateur`, `LOINC_Code`, `Valeur`)
                    VALUES ({}, "{}", '{}');""" . format(Id_Utilisateur, LOINC_Code, Valeur);
        db_cursor.execute(requete) 
        if db_cursor.rowcount==1:
            conn.commit()
            output = {
                'CODE': 'QUERY_OK',
                'TEXT': "La requête est conforme et a pu être exécutée correctement.",
                'DATA' : get_all_Resultat_Examen(conn)
            }
        else:
            output = {
                'CODE' : 'DATABASE_ERROR',
                'TEXT': "Une erreur est survenue lors de l'exécution de la requête sur la base de données.",
                'DATA': None
            }
            dblib.cursor_close(db_cursor)
        return output

def update_Resultat_Examen(Id_Utilisateur, LOINC_Code, Valeur, conn):
    db_cursor = dblib.get_cursor(conn)
            
    output_get_cipher_specifications = cipherlib.get_cipher_specifications()
    if output_get_cipher_specifications['DATA'] is None:
                output = output_get_cipher_specifications
    else:
        cipher_specifications = output_get_cipher_specifications['DATA']
        Valeur_chiffree = cipherlib.fernet_cipher(Valeur, "float", cipher_specifications["Resultat_Examen"]["cle"], "encrypt")
        requete = """UPDATE `Resultat_Examen`
                    SET `Valeur`=%s
                    WHERE `Id_Utilisateur`=%s AND `LOINC_Code`=%s"""
        params = (Valeur_chiffree, Id_Utilisateur, LOINC_Code)

        db_cursor.execute(requete, params)
        try:
            if db_cursor.rowcount==1:
                conn.commit()
                output = {
                    'CODE': 'QUERY_OK',
                    'TEXT': "La requête est conforme et a pu être exécutée correctement.",
                    'DATA' : get_all_Resultat_Examen(conn)
                }
            else:
                output = {
                    'CODE' : 'QUERY_OK',
                    'TEXT': "Le nouveau résulat étant identique au précédent, la base de données n'a pas été modifiée.",
                    'DATA': None
                }
        except Error as err:
            output = {
                'CODE' : 'DATABASE_ERROR',
                'TEXT': str(err),
                'DATA': None
            }
        dblib.cursor_close(db_cursor)
    return output

def delete_Resultat_Examen(Id_Patient, LOINC_Code, conn):
    db_cursor = dblib.get_cursor(conn)

    requete = """DELETE FROM `Resultat_Examen`
                WHERE `Id_Utilisateur`=%s AND `LOINC_Code`=%s"""
    params = (Id_Patient, LOINC_Code)
        
    db_cursor.execute(requete, params)
    if db_cursor.rowcount==1:
        conn.commit()
        output = {
            'CODE': 'QUERY_OK',
            'TEXT': "La requête est conforme et a pu être exécutée correctement.",
            'DATA' : get_all_Resultat_Examen(conn)
        }
    else:
        output = {
            'CODE' : 'DATABASE_ERROR',
            'TEXT': "Une erreur est survenue lors de l'exécution de la requête sur la base de données.",
            'DATA': None
        }
    
    dblib.cursor_close(db_cursor)
    return output