#!/usr/bin/env python3
import requests
import json
import base64

# DELETE request to delete Resultat_Examen
uri = "https://www.gaalactic.fr/~user_SEV5206E/ws/Web_Service_E-SANTE/chiffrement_init.py?"

login = 'admin'
mot_de_passe = 'password4'

login_et_mot_de_passe = '{}:{}'.format(login, mot_de_passe)
base64_login_et_mot_de_passe = base64.b64encode(bytes(login_et_mot_de_passe, 'utf-8')).decode('utf-8')
basic_authentication = 'Basic {}'.format(base64_login_et_mot_de_passe)

customHeaders = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Authorization': basic_authentication
}

httpReturn = requests.delete(uri, headers=customHeaders)
httpReturnText = httpReturn.text

# Print the raw response text for debugging
print("Raw response text:", httpReturnText)

# Attempt to parse the response as JSON
try:
    structuredHttpReturn = json.loads(httpReturnText)
    print(structuredHttpReturn)
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)