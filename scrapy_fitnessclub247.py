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

if len(meses) != len(precio):
  print("Error: meses y precios no coinciden en cantidad de registros")
  sys.exit(0)

templist = []
for i in range(len(precio)):
  Table_dict = {
            'periodo': meses[i],
            'precio': precios[i],
            'moneda': 'Euro',
            'gym': 'fitnessclub247'
        }
  templist.append(Table_dict)
  df = pd.DataFrame(templist)

# Aquí haré que me lo deje en un archivo csv
df.to_csv('output.csv')

# Tengo que hacerme cargo de gestionar escribir csv




