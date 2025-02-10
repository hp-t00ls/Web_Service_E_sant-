import cgi
import cgitb

cgitb.enable()

# Fonction retournant le dictionnaire qui contient les données http
def returnHttpData():
    formData = cgi.FieldStorage()
    httpData = {}
    try:
        httpDataKeys = list(formData)
    except Exception:
        httpDataKeys = []
    for key in httpDataKeys:
        httpData[key] = (formData[key].value)
    return httpData

