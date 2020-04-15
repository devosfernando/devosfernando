# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import date
import cv2
import json
import shutil
import requests
from bs4 import BeautifulSoup


# Manejo de la descarga binaria


# Descarga de imagenes
def descarga_imagen(imagen, nombre):
    # Optenemos datos del remoto
    resp = requests.get(imagen, stream=True)
    # Si la respuesta es correcta
    if resp.status_code == 200:
            # Descarga y escritura en disco
            print("Descargando la imagen; .\\badge\\" + str(nombre) + ".png")
            with open(".\\badge\\" + str(nombre) + ".png.tmp", 'wb') as f:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, f)
            # Validamos si la imagen existe previamente
            if os.path.isfile(".\\badge\\" + str(nombre) + ".png"):
                # Cargamos las dos imagenes para hacer las diferencias
                original = cv2.imread(".\\badge\\" + str(nombre) + ".png")
                image_to_compare = cv2.imread(".\\badge\\" + str(nombre) + ".png.tmp")
                # Calculamos la diferencia absoluta de las dos imagenes
                if original.shape == image_to_compare.shape:
                    # Si son iguales borramos la descarga actual
                    os.remove(".\\badge\\" + str(nombre) + ".png.tmp")
                else:
                    # Si son diferente respaldamos el binario y dejamos la actual
                    origen = (directorio + "\\badge\\" + str(nombre) + ".png")
                    destino = (directorio + "\\badge\\old\\" + str(nombre) + str(today) + ".png")
                    shutil.copy(origen, destino)
                    os.remove(".\\badge\\" + str(nombre) + ".png")
                    os.rename(".\\badge\\" + str(nombre) + ".png.tmp", ".\\badge\\" + str(nombre) + ".png")
            else:
                # Si no hay nada creamos la imagen
                os.rename(".\\badge\\" + str(nombre) + ".png.tmp", ".\\badge\\" + str(nombre) + ".png")


# Ciclo de descarga de imagenes
def ciclo_descarga_imagen(courses_json, flag, avatar, badge):
    print("Descargando Badge")
    descarga_imagen(avatar, "avatar")
    descarga_imagen(badge, "badge")
    descarga_imagen(flag, "flag")
    for dato in courses_json:
        descarga_imagen(dato["image"], dato["slug"])


# Recorte de variables
def filtrado(buscar, dato):
    inicio = dato.find(buscar)
    corte = dato[inicio:len(dato)]
    fin = corte.find("\n")
    corte2 = dato[inicio:inicio + fin - 1]
    valor = corte2.replace(buscar, "")
    resultado = corte2.replace(buscar, "")
    # Eliminamos comillas de string
    if valor[0:1] == "'":
        resultado = resultado[1:len(valor) - 1]
    print("Corte desde inicio: " + str(inicio) + " hasta " + str(fin) + " corte " + str(resultado))
    return (resultado)


# Variables de trabajo
directorio = os.path.dirname(os.path.realpath(__file__))
today = date.today()
courses_json = ""
username = ""
avatar = ""
badge = ""
flag = ""
#Creo directorios
try:
    os.makedirs(directorio + "\\badge\\old\\")
except:
    print("Directorio con historicos ya creado")
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
    contador = contador + 1
# Llamamos al ciclo de descargas
ciclo_descarga_imagen(courses_json, flag, avatar, badge)
