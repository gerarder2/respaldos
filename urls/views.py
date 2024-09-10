from django.http import HttpResponse
from django.shortcuts import render
import requests
from requests.auth import HTTPBasicAuth
import json
from django.http import HttpResponse
import zipfile
import os
from django.conf import settings


def home(request):
    if request.method == "POST":
        try:
            ruta_temp = os.path.join(settings.MEDIA_ROOT, "respaldo.zip")
            os.remove(ruta_temp)
        except:
            print("No existe el respaldo")
        
        try:
            jobId = request.POST['jobId']
            generarArchivo1(jobId)
            generarArchivo2()
            generarArchivo3()
            response = crear_zip()
            os.remove("urls/urls/data/jobStatusId.json")
            os.remove("urls/urls/data/jobStatusId.txt")
            os.remove("urls/urls/data/size.json")
            os.remove("urls/urls/data/size.txt")
            os.remove("urls/urls/data/totalDocs.json")
            os.remove("urls/urls/data/totalDocs.txt")
            return response
        except:
            print("Error al generar archivos.")
    else:
         return render(request, 'urls/home.html')

def generarArchivo1(jobId):
    # Datos de autenticación
    user = "spiuser"
    password = "Coppel12"

    # URL de la API a la que queremos hacer la petición
    url = 'https://search-prodauth.coppel.com/search/admin/resources/index/build/status?jobStatusId='+jobId


    # Realizamos la petición POST con autenticación
    response = requests.get(url, auth=HTTPBasicAuth(user, password))

    # Verificamos el estado de la respuesta
    if response.status_code == 200:
        print("informacion obtenida correctamente \n", json.loads(response.text))
        
        data = response.json()
        with open("urls/urls/data/jobStatusId.json", "w") as json_file:
            json.dump(data, json_file , indent=4)

        with open("urls/urls/data/jobStatusId.txt", "w") as txt_file:
            json.dump(data, txt_file , indent=4)

    else:
        print("Error:", response.status_code)

def generarArchivo2():
    # Datos de autenticación
    user = "spiuser"
    password = "Coppel12"

    # URL de la API a la que queremos hacer la petición
    url = "https://search-prodauth.coppel.com/solr/MC_10001_CatalogEntry_es_ES/dataimport?command=status"


    # Realizamos la petición POST con autenticación
    response = requests.get(url, auth=HTTPBasicAuth(user, password))

    # Verificamos el estado de la respuesta
    if response.status_code == 200:
        print("informacion obtenida correctamente \n", json.loads(response.text))
        
        data = response.json()
        with open("urls/urls/data/totalDocs.json", "w") as json_file:
            json.dump(data, json_file , indent=4)

        with open("urls/urls/data/totalDocs.txt", "w") as txt_file:
            json.dump(data, txt_file , indent=4)
    else:
        print("Error:", response.status_code)

def generarArchivo3():
    # Datos de autenticación
    user = "spiuser"
    password = "Coppel12"

    # URL de la API a la que queremos hacer la petición
    url = "https://search-prodauth.coppel.com/solr/admin/cores?core=MC_10001_CatalogEntry_es_ES&action=status"


    # Realizamos la petición POST con autenticación
    response = requests.get(url, auth=HTTPBasicAuth(user, password))

    # Verificamos el estado de la respuesta
    if response.status_code == 200:
        print("informacion obtenida correctamente \n", json.loads(response.text))
        
        data = response.json()
        with open("urls/urls/data/size.json", "w") as json_file:
            json.dump(data, json_file , indent=4)

        with open("urls/urls/data/size.txt", "w") as txt_file:
            json.dump(data, txt_file , indent=4)
    else:
        print(":", response.status_code)



def crear_zip():
    ruta1 = 'urls/urls/data/jobStatusId.txt'
    ruta2 = 'urls/urls/data/size.txt'
    ruta3 = 'urls/urls/data/totalDocs.txt'
    nombre_zip = 'respaldo.zip'

    ruta_temp = os.path.join(settings.MEDIA_ROOT, nombre_zip)

    with zipfile.ZipFile(ruta_temp, 'w') as zip_file:
        for ruta_archivo in [ruta1, ruta2, ruta3]:
            zip_file.write(ruta_archivo, os.path.basename(ruta_archivo))
    
  # Descargar el archivo ZIP
    with open(ruta_temp, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(nombre_zip) 
        return response
