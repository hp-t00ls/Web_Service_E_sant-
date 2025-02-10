'''
# Example usage
response = execute_request('1111111111', '718-7', 'admin', 'password4', valeur=17.4, id_utilisateur=1, date_examen='2024-02-01', http_method='PUT')
print(response)
'''

import requests
import json
import base64
import tkinter as tk
from tkinter import messagebox

def execute_request(INS, LOINC_Code, login_utilisateur, mot_de_passe, valeur=None, id_utilisateur=None, http_method='GET'):
    url = f"https://www.gaalactic.fr/~user_SEV5206E/ws/Web_Service_E-SANTE/valeur.py?INS={INS}&LOINC_Code={LOINC_Code}"
    login_et_mot_de_passe = f"{login_utilisateur}:{mot_de_passe}"
    base64_login_et_mot_de_passe = base64.b64encode(bytes(login_et_mot_de_passe, 'utf-8')).decode('utf-8')
    
    customHeaders = {
        'Authorization': f'Basic {base64_login_et_mot_de_passe}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'Id_Utilisateur': id_utilisateur,
        'Valeur': valeur
    }
    
    if http_method == 'GET':
        response = requests.get(url, headers=customHeaders, params=data)
    elif http_method == 'POST':
        response = requests.post(url, headers=customHeaders, data={'DATA': json.dumps(data)})
    elif http_method == 'PUT':
        response = requests.put(url, headers=customHeaders, data={'DATA': json.dumps(data)})
    elif http_method == 'DELETE':
        response = requests.delete(url, headers=customHeaders, data={'DATA': json.dumps(data)})
    else:
        raise ValueError("Invalid HTTP method")

    return response.text

def execute_request_tk():
    INS = entry_INS.get()
    Id_Utilisateur = entry_id_user.get() or None
    LOINC_Code = entry_LOINC.get()
    login_utilisateur = entry_login.get()
    mot_de_passe = entry_password.get()
    valeur = entry_valeur.get() or None
    http_method = method_var.get()

    response_text = execute_request(INS, LOINC_Code, login_utilisateur, mot_de_passe, valeur, Id_Utilisateur, http_method)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, response_text)

# Interface Tkinter
root = tk.Tk()
root.title("WS E-Santé - Hippolyte PASCAL - E5 BIO 2025")

# Create frames for better organization
frame_inputs = tk.Frame(root, padx=10, pady=10)
frame_inputs.grid(row=0, column=0, sticky="ew")

frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.grid(row=1, column=0, sticky="ew")

frame_results = tk.Frame(root, padx=10, pady=10)
frame_results.grid(row=2, column=0, sticky="ew")

# Input fields
tk.Label(frame_inputs, text="INS:").grid(row=0, column=0, sticky="w")
entry_INS = tk.Entry(frame_inputs)
entry_INS.grid(row=0, column=1, sticky="ew")

tk.Label(frame_inputs, text="LOINC Code:").grid(row=1, column=0, sticky="w")
entry_LOINC = tk.Entry(frame_inputs)
entry_LOINC.grid(row=1, column=1, sticky="ew")

tk.Label(frame_inputs, text="Login Utilisateur:").grid(row=2, column=0, sticky="w")
entry_login = tk.Entry(frame_inputs)
entry_login.grid(row=2, column=1, sticky="ew")

tk.Label(frame_inputs, text="Mot de passe:").grid(row=3, column=0, sticky="w")
entry_password = tk.Entry(frame_inputs, show="*")
entry_password.grid(row=3, column=1, sticky="ew")

tk.Label(frame_inputs, text="Valeur (optionnel):").grid(row=4, column=0, sticky="w")
entry_valeur = tk.Entry(frame_inputs)
entry_valeur.grid(row=4, column=1, sticky="ew")

tk.Label(frame_inputs, text="Id Utilisateur (optionnel):").grid(row=5, column=0, sticky="w")
entry_id_user = tk.Entry(frame_inputs)
entry_id_user.grid(row=5, column=1, sticky="ew")

tk.Label(frame_inputs, text="Méthode HTTP:").grid(row=7, column=0, sticky="w")
method_var = tk.StringVar(value="GET")
tk.OptionMenu(frame_inputs, method_var, "GET", "POST", "PUT", "DELETE").grid(row=7, column=1, sticky="ew")

# Execute button
btn_execute = tk.Button(frame_buttons, text="Envoyer", command=execute_request_tk)
btn_execute.grid(row=0, column=0, sticky="ew")

# Result display
tk.Label(frame_results, text="Résultat:").grid(row=0, column=0, sticky="w")
result_text = tk.Text(frame_results, wrap="word", height=10, width=50)
result_text.grid(row=1, column=0, sticky="ew")

# Configure column weights for better resizing
frame_inputs.columnconfigure(1, weight=1)
frame_buttons.columnconfigure(0, weight=1)
frame_results.columnconfigure(0, weight=1)

root.mainloop()