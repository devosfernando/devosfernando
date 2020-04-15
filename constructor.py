#Requeridos pip install beautifulsoup4
import re
import json
import requests
from bs4 import BeautifulSoup


def filtrado(buscar, dato):
    inicio = dato.find(buscar)
    corte = dato[inicio:len(dato)]
    fin = corte.find("\n")
    corte2 = dato[inicio:inicio+fin-1]
    valor = corte2.replace(buscar, "")
    resultado = corte2.replace(buscar, "")
    if valor[0:1] == "'":
        resultado =resultado[1:len(valor)-1]
    print("Corte desde inicio: " + str(inicio) + " hasta " + str(fin) + " corte " + str(resultado))
    return (resultado)


# Estraemos un consumo Html del portal de platzi
req = requests.get('https://platzi.com/@devosfernando/')
# Pasamor el Html por el BeautifulSoup para obtener solo los script
soup = BeautifulSoup(req.content, "html.parser")
scripts = soup.select('script')
# Pasamos el resultado a un arreglo
scripts = [scripts for script in scripts]
# Iniciamos el proceso de recorrido del arreglo para poder consultear los datos necesarios
contador = 0
for script in scripts:
    # Creamos nuestra variable de trabajo para la cadena en string del script
    script_evaluar = []
    # Recorremos el objeto para convertirlo a string dentro de un arreglo en script_evaluar
    for cadena in script[contador]:
        script_evaluar.append(str(cadena))
    # Recorremos los datos del arreglo, ya que podemos tener nulos
    for script_evaluar_sub in script_evaluar:
        # Validamos si el dato tiene nuestra palabra de referencia username
        if int(script_evaluar_sub.find("window.data")) != -1:
            username = filtrado("username: ", script_evaluar_sub)
            courses_test = filtrado("courses: ", script_evaluar_sub)
            avatar = filtrado("avatar: ", script_evaluar_sub)
            badge = filtrado("badge: ", script_evaluar_sub)
            flag = filtrado("flag: ", script_evaluar_sub)
            courses_json = json.loads(courses_test)
            print(courses_json[0]["title"])
    contador = contador + 1

