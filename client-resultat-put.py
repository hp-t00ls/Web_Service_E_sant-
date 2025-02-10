#!/usr/bin/env python3

import requests
import json
import base64

#POST
uri = "https://www.gaalactic.fr/~user_SEV5206E/ws/Web_Service_E-SANTE/valeur.py?INS=1111111111&LOINC_Code=718-7"

login = 'admin'
mot_de_passe = 'password4'
login_et_mot_de_passe = '{}:{}' . format(login, mot_de_passe)
base64_login_et_mot_de_passe = base64.b64encode(bytes(login_et_mot_de_passe, 'utf-8')).decode('utf-8')
basic_authentication = 'Basic {}' . format(base64_login_et_mot_de_passe)

customHeaders = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Authorization': basic_authentication
}

data = {
        'Id_Utilisateur':1,
        'Valeur':10.4
}
httpReturn = requests.put(uri, headers=customHeaders, data={'DATA':json.dumps(data)})
httpReturnText = httpReturn.text
structuredHttpReturn = json.loads(httpReturnText)
print(structuredHttpReturn)
