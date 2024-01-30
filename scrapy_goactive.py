"""
OBJETIVOS: 
    - Extraer los idiomas de la pagina principal de WIKIPEDIA
    - Aprender a utilizar requests para hacer requerimientos
    - Aprender a utilizar lxml para parsear el arbol HTML
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 14 ENERO 2024
"""
import requests # pip install requests
from lxml import html # pip install lxml
import sys
import pandas as pd
import os

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# URL SEMILLA
url = 'https://goactive.hu/en/membership/'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)
respuesta.encoding = 'utf-8' # Codificar correctamente caracteres extranos
# print(respuesta.content)
# PARSEO DEL ARBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
parser = html.fromstring(respuesta.content) # Uso .content para poder codificar los caracteres raros
# # EXTRACCION DE TODOS LOS MESES POR XPATH
meses = parser.xpath("//div[contains(@class,'vc_row')]//div[contains(@class,'wpb_column')]//div[contains(@class,'vc_column-inner')]//h3/text()")

# for mes in meses:
#   print(mes)
# EXTRACCION DE TODOS LOS PRECIOS POR XPATH
precios = parser.xpath("//div[contains(@class,'vc_row')]//div[contains(@class,'wpb_column')]//div[contains(@class,'vc_column-inner')]//h4/text()")

#precios = parser.xpath("//div[@class='vc_row']//div[@class='wpb_column']//div[@class='vc_column-inner']//h4/text()")
# print(precios)
for precio in precios:
  print(precio)

for mes in meses:
  print(mes)
if len(meses)-1 != len(precios):
  print("Error: meses y precios no coinciden en cantidad de registros")
  sys.exit(0)

templist = []
for i in range(len(precio)):
  Table_dict = {
            'periodo': meses[i+1],
            'precio': precios[i],
            'moneda': 'Euro',
            'gym': 'goactive'
        }
  templist.append(Table_dict)
  df = pd.DataFrame(templist)

# Aquí haré que me lo deje en un archivo csv

# Tengo que hacerme cargo de gestionar escribir csv
ruta_del_archivo = 'output.csv'
if os.path.exists(ruta_del_archivo):
  print("El archivo ya existe, agregando resultados al final")
  df.to_csv('output.csv', mode='a', header=False, index=False)
else:
  print("El archivo no existe, creando archivo")
  df.to_csv('output.csv', mode='w', index=False)
# si el archivo existe, hacer con appen, si no existe con w





