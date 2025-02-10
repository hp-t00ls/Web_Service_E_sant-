#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:28:32 2025

@author: lacombea
"""

import json
import base64
from cryptography.fernet import Fernet

def get_cipher_specifications():
    fichier_specifications_chiffrement = './.wsdata/.cipher.spec'
    try:
        fichier = open(fichier_specifications_chiffrement, "r")
        specifications_chiffrement_JSON = fichier.read()
        try:
            specifications_chiffrement = json.loads(specifications_chiffrement_JSON)
            output = {
                'CODE': 'CIPHER_SPECIFICATION_FILE_OK',
                'TEXT': 'Les spécifications de chiffrement de la base de données ont bien été trouvées',
                'DATA' : specifications_chiffrement
            }
        except json.JSONDecodeError as err:
            output = {
                'CODE': 'CIPHER_SPECIFICATION_FILE_NOT_JSON_CONTENT',
                'TEXT': str(err),
                'DATA' : None
            }
    except FileNotFoundError as err:
        output = {
            'CODE': 'CIPHER_SPECIFICATION_FILE_NOT_FOUND',
            'TEXT': str(err),
            'DATA' : None
        } 
    except PermissionError as err:
        output = {
            'CODE': 'CIPHER_SPECIFICATION_FILE_NOT_READABLE',
            'TEXT': str(err),
            'DATA' : None
        }
    return output    


class cipherlib:

    _cipher_specifications = get_cipher_specifications()
    
    @classmethod
    def get_cipher_specifications(cls):
        return cls._cipher_specifications       
   
    @classmethod
    def fernet_cipher(cls, donnee, type_donnee, cle_BASE64, operation):
        cle = base64.b64decode(cle_BASE64)
        chiffreur_fernet = Fernet(cle)
        if operation == "encrypt":
            if type_donnee == "float":
                donnee_STR = str(donnee)
            elif type_donnee == "string":
                donnee_STR = donnee
            donnee_chiffree_BIN = chiffreur_fernet.encrypt(donnee_STR.encode())
            retour = base64.b64encode(donnee_chiffree_BIN).decode()
        elif operation == "decrypt":
            donnee_chiffree_BIN = base64.b64decode(donnee)
            donnee_dechiffree = chiffreur_fernet.decrypt(donnee_chiffree_BIN).decode()
            
            if type_donnee == "float":
                retour = float(donnee_dechiffree)
            else:
                retour = donnee_dechiffree
                     
        return retour
    



