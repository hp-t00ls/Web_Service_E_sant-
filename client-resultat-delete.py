#!/usr/bin/env python3

import requests
import json
import base64

#POST
uri = "https://www.gaalactic.fr/~user_SEV5206E/ws/Web_Service_E-SANTE/valeur.py?INS=1111111111&LOINC_Code=EX001"

login = 'jdupont'
mot_de_passe = '*668425423DB5193AF921380129F465A6425216D0'
login_et_mot_de_passe = '{}:{}' . format(login, mot_de_passe)
base64_login_et_mot_de_passe = base64.b64encode(bytes(login_et_mot_de_passe, 'utf-8')).decode('utf-8')
basic_authentication = 'Basic {}' . format(base64_login_et_mot_de_passe)

customHeaders = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Authorization': basic_authentication
}

httpReturn = requests.delete(uri, headers=customHeaders)
httpReturnText = httpReturn.text
structuredHttpReturn = json.loads(httpReturnText)
print(structuredHttpReturn)