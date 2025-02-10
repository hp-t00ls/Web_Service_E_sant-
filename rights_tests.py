#!/usr/bin/env python3
import os
import base64
import dblib
from cipherlib import cipherlib

def check_authentication(conn):
    if 'HTTP_AUTHORIZATION' not in os.environ:
        output = {
            'CODE': 'MISSING_HEADER_PARAMETER_Authorization',
            'TEXT': "Le paramètre d'en-tête Authorization est manquant. Ce web service n'est accessible que sur authentification",
            'DATA': None
        }
    else:
        authorization = os.environ['HTTP_AUTHORIZATION']
        if not authorization.startswith("Basic "):
            output = {
                'CODE': 'MISSING_BASIC_PREFIX_IN_AUTHORIZATION_HEADER',
                'TEXT': "The 'Basic' prefix is missing in Authorization prefix",
                'DATA': None
            }
            
        else:
            output_get_cipher_specifications = cipherlib.get_cipher_specifications()
            if output_get_cipher_specifications['DATA'] is None:
                        output = output_get_cipher_specifications
            else:
                cipher_specifications = output_get_cipher_specifications['DATA']
                cleaned_authorization = authorization.replace("Basic ", "", 1)
                decoded_bytes = base64.b64decode(cleaned_authorization)
                decoded_authorization = decoded_bytes.decode('utf-8')
                decoded_authorization_split = decoded_authorization.split(':')
                Login_Utilisateur = decoded_authorization_split[0]
                Mot_de_Passe = decoded_authorization_split[1]  

                db_cursor = dblib.get_cursor(conn)
                
                requete = """SELECT PASSWORD(%s)"""
                params=(Mot_de_Passe,)
                db_cursor.execute(requete, params)
                resultat = db_cursor.fetchone()
                Mot_de_Passe_BdD_hash = resultat[0]
                
                requete = """SELECT `Login_Utilisateur`, `Mot_de_Passe`, `Id_Utilisateur`
                            FROM  `Utilisateur`"""
                db_cursor.execute(requete)
                resultat = db_cursor.fetchall()
                trouve = False
                couple_Login_Utilisateur_Mot_de_Passe_BdD_hash = [Login_Utilisateur, Mot_de_Passe_BdD_hash]
                for Tuple in resultat:
                    ligne = list(Tuple)
                    ligne[0] = cipherlib.fernet_cipher(ligne[0], "string", cipher_specifications["Utilisateur"]["cle"], "decrypt")
                    if couple_Login_Utilisateur_Mot_de_Passe_BdD_hash == ligne[:2]:
                        trouve = True
                        break
                if trouve == False:
                    output = {
                        'CODE': 'WRONG_AUTHENTICATION_DATA',
                        'TEXT': "Les données d'authentification sont erronnées. Elles ne correspondent à aucun utilisateur.",
                        'DATA': None
                    }
                else:
                    output = {
                        'CODE': 'AUTHENTICATION_OK',
                        'TEXT': "Les données d'authentification sont valide.",
                        'DATA': {
                            'Login_Utilisateur': Login_Utilisateur,
                            'Mot_de_Passe': Mot_de_Passe,
                            'Id_Utilisateur': ligne[2]
                        }
                    }
                dblib.cursor_close(db_cursor)
    return output


def check_user_rights(conn, login, methode):
    output_get_cipher_specifications = cipherlib.get_cipher_specifications()
    if output_get_cipher_specifications['DATA'] is None:
                output = output_get_cipher_specifications
    else:
        cipher_specifications = output_get_cipher_specifications['DATA']
        
        db_cursor = dblib.get_cursor(conn)
        requete = """SELECT `Utilisateur`.`Login_Utilisateur`, `Droit_Utilisateur`.`Methode_HTTP`,`Utilisateur`.`Id_Utilisateur`, `Categorie_Utilisateur`.`Libelle_Categorie_Utilisateur`
                    FROM `Utilisateur`
                    JOIN `Categorie_Utilisateur` ON `Utilisateur`.`Id_Categorie_Utilisateur`=`Categorie_Utilisateur`.`Id_Categorie_Utilisateur`
                    JOIN `Droit_Categorie_Utilisateur` ON `Categorie_Utilisateur`.`Id_Categorie_Utilisateur`=`Droit_Categorie_Utilisateur`.`Id_Categorie_Utilisateur`
                    JOIN `Droit_Utilisateur` ON `Droit_Categorie_Utilisateur`.`Id_Droit`=`Droit_Utilisateur`.`Id_Droit`
                    """
        db_cursor.execute(requete)
        resultat = db_cursor.fetchall()
        dblib.cursor_close(db_cursor)
        operation_autorisee = False
        for Tuple in resultat:
            ligne = list(Tuple)
            ligne[0] = cipherlib.fernet_cipher(ligne[0], "string", cipher_specifications["Utilisateur"]["cle"], "decrypt")
            if login == ligne[0]:
                methode_HTTP_autorisee = ligne[1]
                Id_Utilisateur = ligne[2]
                categorie_utilisateur_chiffre = ligne[3]
                if methode == methode_HTTP_autorisee:
                    operation_autorisee = True
      
        if operation_autorisee == False:
            output = {
                'CODE': 'UNAUTHORIZED_OPERATION_{}' . format(methode),
                'TEXT': "La méthode {} n'est pas autorisée pour cet utilisateur." . format(methode),
                'DATA': None
            }
        else:
            Categorie_Utilisateur = cipherlib.fernet_cipher(categorie_utilisateur_chiffre, "string", cipher_specifications["Categorie_Utilisateur"]["cle"], "decrypt")
            output = {
                'CODE': 'AUTHORIZED_OPERATION_{}' . format(methode),
                'TEXT': "La méthode {} est autorisée pour cet utilisateur." . format(methode),
                'DATA': {
                    'Id_Utilisateur': Id_Utilisateur,
                    'Categorie_Utilisateur': Categorie_Utilisateur
                }
            }
    return output

def check_authentication_and_rights(conn, methode):
    output_authentication = check_authentication(conn)
    if output_authentication['DATA'] is None:
        output = output_authentication
    else:
        Login_Utilisateur = output_authentication['DATA']['Login_Utilisateur']
        output_user_rights = check_user_rights(conn, Login_Utilisateur, methode)
        if output_user_rights['DATA'] is None:
            output = output_user_rights
        else:
            output = {
                'CODE': 'SUCCESSFUL_AUTHENTICATION',
                'TEXT': "L'autentification s'est déroulée avec succès.",
                'DATA' : {
                    'Login_Utilisateur': Login_Utilisateur,
                    'Mot_de_Passe': output_authentication['DATA']['Mot_de_Passe'],
                    'Login_Id_Utilisateur' :  output_authentication['DATA']['Id_Utilisateur'] ,
                    'Categorie_Utilisateur': output_user_rights['DATA']['Categorie_Utilisateur']
                }
            }   
    return output
        
            
