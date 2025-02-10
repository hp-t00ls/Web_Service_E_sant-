#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de chiffrement pour le domaine médical
Version améliorée de tuto9 basée sur tuto8

Auteur: lacombea
"""

print("Content-Type: text/plain\n")
try:
    import os
    import json
    import dblib
    import cgi
    import cgitb
    cgitb.enable()
    import re
    import pwd
    import grp
    import stat
    import subprocess
    from mysql.connector import Error
    from pathlib import Path
    import base64
    from cryptography.fernet import Fernet
    
    a_chiffrer = {
                            "Utilisateur" : ["INS","Nom_Utilisateur", "Login_Utilisateur"], 
                            "Categorie_Utilisateur" : ["Libelle_Categorie_Utilisateur"], 
                            "Resultat_Examen" : ["Valeur"]
    }
   
    # Récupération du login et de l'id UNIX
    uri_requete = os.environ.get("REQUEST_URI", "")
    match = re.search(r"/~([^/]+)/", uri_requete)
    login = match.group(1)
    id_UNIX_personne = pwd.getpwnam(login).pw_uid
    
    chemin_fichier_specifications_chiffrement = "./.wsdata/.cipher.spec"

    if Path(chemin_fichier_specifications_chiffrement).exists():
        print("Un fichier .cipher.spec a été trouvé, le chiffrement a déjà été réalisé.")
    else:
        print("\n---------------------------------DEBUT DU PROCESSUS DE CHIFFREMENT DE LA BASE DE DONNEES")
        # Génération des clés AES en représentation HEXA
        print("\n---------------------------------Génération des clés de chiffrement...")
        specifications_chiffrement = {}
        for table, attributs in a_chiffrer.items():
            cle = Fernet.generate_key()
            cle_BASE64 = base64.b64encode(cle).decode('utf-8')
            specifications_chiffrement[table] = {"cle": cle_BASE64, "attributs_chiffres": attributs}
        

        specifications_chiffrement_JSON = json.dumps(specifications_chiffrement)
        
        print("""\n---------------------------------Enregistrement des spécifications de chiffrement dans le fichier "./.wsdata/.cipher.spec" au format JSON""")
        with open(chemin_fichier_specifications_chiffrement, "w") as fichier:
            fichier.write(specifications_chiffrement_JSON)
            os.chmod(chemin_fichier_specifications_chiffrement, 0o740)
            subprocess.run(["sudo", "chown", login, chemin_fichier_specifications_chiffrement], check=True)
            
            infos = os.stat(chemin_fichier_specifications_chiffrement) # Obtention et affichage des droits d'accès du propriétaire du fichier
            mode = infos.st_mode  
            droits = stat.filemode(mode) # Convertir des permissions en format lisible (identique à ls -l)
            uid = infos.st_uid  # User ID
            gid = infos.st_gid  # Group ID
            proprietaire = pwd.getpwuid(uid).pw_name
            groupe = grp.getgrgid(gid).gr_name

            print("\n---------------------------------Protection du fichier .cipher.spec")
            print("Droits : {}".format(droits))
            print("Propriétaire -> UID : {} - nom : {}".format(uid, proprietaire))
            print("Groupe -> GID : {} - nom : {}\n".format(gid, groupe))

        # Réouverture du fichier contenant les spécifications pour s'assurer qu'il est bien accessible
        with open(chemin_fichier_specifications_chiffrement, "r") as fichier:
            specifications_chiffrement_JSON = fichier.read()
            specifications_chiffrement = json.loads(specifications_chiffrement_JSON)
                
        # Exécution des requêtes de chiffrement des tables
        try:
            connexion = dblib.db_connection()["DATA"]
            curseur = dblib.get_cursor(connexion)
            connexion.autocommit = False
            print("\n---------------------------------Exécution des requêtes de mise à jour")
            for table in specifications_chiffrement:
                cle_BASE64 = specifications_chiffrement[table]["cle"]
                cle = base64.b64decode(cle_BASE64)
                chiffreur_fernet = Fernet(cle) # Création d'une ressource de chiffrement Fernet utilisant la clé "cle"
                attributs = specifications_chiffrement[table]["attributs_chiffres"]
                print(attributs)
                 # Création des colonnes temporaires dans chacune des tables (suffixes _aes) et insertion
                # des valeurs chiffrées
                for attribut in attributs:                
                    sql = "ALTER TABLE {} ADD COLUMN {}_aes TEXT;".format(table, attribut)
                    print(sql)
                    curseur.execute(sql)
                    sql = "SELECT {} FROM {}".format(attribut, table)
                    print(sql)
                    curseur.execute(sql)
                    resultat = curseur.fetchall()
                    for ligne in resultat:
                        print(ligne[0])
                        if ligne[0]:
                            valeur_attribut_chiffre_BIN = chiffreur_fernet.encrypt(str(ligne[0]).encode())
                            valeur_attribut_chiffre_BASE64 = base64.b64encode(valeur_attribut_chiffre_BIN).decode()
                            print(valeur_attribut_chiffre_BASE64)
                            sql = "UPDATE {} SET {}_aes = '{}' WHERE {} = '{}'".format(table, attribut, valeur_attribut_chiffre_BASE64, attribut, ligne[0])
                            print(sql)
                            curseur.execute(sql)
                            
            # Remplacement des colonnes d'origine par les colonnes temporaires renommées contenant les données chiffrées
            for table in specifications_chiffrement:
                attributs = specifications_chiffrement[table]["attributs_chiffres"]
                for attribut in attributs:            
                    sql = "ALTER TABLE {} DROP COLUMN {}".format(table, attribut)
                    print(sql)
                    curseur.execute(sql)
                    sql = "ALTER TABLE {} RENAME COLUMN {}_aes TO {}".format(table, attribut, attribut);
                    print("{}".format(sql))
                    curseur.execute(sql)
                print("\n---------------------------------BASE DE DONNEES CHIFFREE AVEC SUCCES")
        except Error as erreur_transaction:
            # Annulation de la transaction et suppression du fichier de clés en cas d'erreur d'exécution des requêtes
            connexion.rollback()
            Path(chemin_fichier_specifications_chiffrement).unlink()
            curseur.close() 
            dblib.db_close(connexion) 
            print("\n---------------------------------LA BASE DE DONNEES N'A PAS PU ETRE MISE A JOUR : {}".format(erreur_transaction))
            
        print("\n---------------------------------TEST D'ACCES AUX DONNEES APRES CHIFFREMENT")
        for table in specifications_chiffrement:
            cle_BASE64 = specifications_chiffrement[table]["cle"]
            cle = base64.b64decode(cle_BASE64)
            chiffreur_fernet = Fernet(cle) # Création d'une ressource de chiffrement Fernet utilisant la clé "cle"
            attributs = specifications_chiffrement[table]["attributs_chiffres"]
            print("\nRécupération et déchiffrement des données depuis la table {}".format(table))
            nb_specification = len(attributs)
            index = 0
            sql = "SELECT"
            for attribut in attributs:
                if index < nb_specification -1 and not nb_specification == 1:
                    sql += " {},".format(attribut)
                else:
                    sql += " {}".format(attribut)
                index += 1
            sql += " FROM {};".format(table)
            curseur.execute(sql)
            resultat = curseur.fetchall()
            donnees_dechiffrees = []
            for ligne in resultat:
                ligne_dechiffree = []
                for valeur_attribut_BASE64 in ligne:
                    if valeur_attribut_BASE64:
                        valeur_attribut_BIN = base64.b64decode(valeur_attribut_BASE64)
                        if table == "Resultat_Examen":
                            valeur_attribut = float(chiffreur_fernet.decrypt(valeur_attribut_BIN).decode())
                        else:
                            valeur_attribut = chiffreur_fernet.decrypt(valeur_attribut_BIN).decode()
                        ligne_dechiffree.append(valeur_attribut)
                    else:
                        ligne_dechiffree.append(None)
                donnees_dechiffrees.append(ligne_dechiffree)
            print(donnees_dechiffrees)
        print("\n---------------------------------DONNEES DECHIFFREES ET RECUPEREES AVEC SUCCES")
    
        curseur.close() 
        dblib.db_close(connexion)

except Exception as e:
    print(str(e))
