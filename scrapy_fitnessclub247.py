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
url = 'https://fitnessclub247.com/'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)
respuesta.encoding = 'utf-8' # Codificar correctamente caracteres extranos

# PARSEO DEL ARBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
parser = html.fromstring(respuesta.content) # Uso .content para poder codificar los caracteres raros

# EXTRACCION DE TODOS LOS MESES POR XPATH
meses = parser.xpath("//div[contains(@class,'ttbase-pricing-table')]//h4/text()")

for mes in meses:
  print(mes)
# EXTRACCION DE TODOS LOS PRECIOS POR XPATH
precios = parser.xpath("//div[contains(@class,'ttbase-pricing-table')]//span[contains(@class,'price')]/text()")
for precio in precios:
  print(precio)

if len(meses) != len(precios):
  print("Error: meses y precios no coinciden en cantidad de registros")
  sys.exit(0)

templist = []
for i in range(len(precio)):
  Table_dict = {
            'periodo': meses[i],
            'precio': precios[i],
            'moneda': 'Florin',
            'gym': 'fitnessclub247'
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





