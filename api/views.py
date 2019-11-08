from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
# Create your views here.

import requests

def fechas_faltantes(request):

    headers = {'Accept': 'application/json'}
    response = requests.get('http://localhost:8082/periodos/api', params=request.GET, headers=headers)
    content = json.loads(response.content)
    fecha_creacion = content["fechaCreacion"]
    fecha_fin = content["fechaFin"]
    list_fechas = content["fechas"]
    lista_fechas_faltantes= encontrar_fechas_faltantes(fecha_creacion, fecha_fin, list_fechas)
    response_data = {}
    response_data['id'] = content["id"]
    response_data['fechaCreacion'] = content["fechaCreacion"]
    response_data['fechaFin'] = content["fechaFin"]
    response_data['fechas'] = list_fechas
    response_data['fechasFaltantes'] = lista_fechas_faltantes

    if response.status_code == 200:
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
    return HttpResponse('No hubo conexión con la api GDD')

def encontrar_fechas_faltantes(fecha_inicio, fecha_fin, list_fechas):
    list_faltantes = []

    date_fecha_ini = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
    date_fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
    year_ini = date_fecha_ini.year

    while year_ini <= date_fecha_fin.year:
        for i in range(1, 12):
            date_nueva_fecha = datetime.datetime.strptime(str(year_ini) + "-" + str(i) + "-01", '%Y-%m-%d')
            existe = False

            for f in list_fechas:
                date_fecha_lista = datetime.datetime.strptime(f, '%Y-%m-%d')
                if date_nueva_fecha == date_fecha_lista:
                    existe = True
                    break

            if not existe:
                if date_nueva_fecha == date_fecha_ini or date_nueva_fecha == date_fecha_fin:
                    list_faltantes.append(str(date_nueva_fecha.date()))
                elif date_nueva_fecha > date_fecha_ini and date_nueva_fecha < date_fecha_fin:
                    list_faltantes.append(str(date_nueva_fecha.date()))

        year_ini = year_ini + 1

    return list_faltantes