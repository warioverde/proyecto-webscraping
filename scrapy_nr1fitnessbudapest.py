"""
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 14 SEPTIEMBRE 2023
"""

#####
### ATENCION: OLX necesita que le demos permisos de geolocalizacion al navegador de selenium para que nos muestre los datos
### Esto lo haremos una unica vez en la primer corrida del programa. Este problema es mas comun en usuarios de MAC
#####
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv
import os
# Asi podemos setear el user-agent en selenium
chromedriver = "C:/Users/tatan/OneDrive/Documentos/proyecto-webscraping/chromedriver.exe"

option = webdriver.ChromeOptions()

option.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

s = Service(chromedriver)

driver = webdriver.Chrome(service=s, options=option)
# Voy a la pagina que quiero
driver.get('https://nr1fitnessbudapest.perfectgym.pl/ClientPortal2/#/Registration')
sleep(5)
# driver.refresh() # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página
# sleep(2) # Esperamos que cargue el boton

# Busco el boton para cargar mas informacion
boton_div = WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'col-xs-12')][3]"))
)
# boton_div = driver.find_element(By.XPATH, "//div[contains(@class,'col-xs-12')][3]")
boton_div.click()
boton_next = WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.XPATH, "//*[@icon='cp-button-right']"))
)
boton_next.click()
boton_next = WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='page-footer-lang']"))
)
sleep(5)
boton_next.click()
boton_next = WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.XPATH, "//a[@text='English']"))
)
boton_next.click()
sleep(3)
#divs_gym = driver.find_elements(By.XPATH, "//div[@class='tile-item-price']")

divs_gym = driver.find_elements(By.XPATH, "//div[contains(@class,'col-xs-12')]")
# precios_gym= driver.find_element(By.XPATH, "//div[@class='tile-item-price']//span[@class='tile-item-price-value']")
# periodos_gym= driver.find_element(By.XPATH, "//div[@class='tile-item-price']//span[@class='tile-item-price-interval']")
# divs_gym = driver.find_elements(By.XPATH, "//div[contains(@class,'row')]")
# print(str(len(divs_gym)))
contador = 0
templist = []
for div in divs_gym:
    # print("DIV--------------------"+str(contador))
    # print(div.get_attribute('innerHTML'))
    # print("DIV--------------------"+str(contador))
    precio_gym = div.find_element('xpath', ".//span[@class='tile-item-price-value']").text
    periodo_gym = div.find_element('xpath', ".//span[@class='tile-item-price-interval']").text
    print(precio_gym+"/"+periodo_gym)
    Table_dict = {
            'periodo': periodo_gym,
            'precio': precio_gym,
            'moneda': 'Florin',
            'gym': 'nr1fitnessbudapest'
        }
    templist.append(Table_dict)
    df = pd.DataFrame(templist)
    contador+=1

# Aquí haré que me lo deje en un archivo csv
ruta_del_archivo = 'output.csv'
if os.path.exists(ruta_del_archivo):
  print("El archivo ya existe, agregando resultados al final")
  df.to_csv('output.csv', mode='a', header=False, index=False)
else:
  print("El archivo no existe, creando archivo")
  df.to_csv('output.csv', mode='w', index=False)