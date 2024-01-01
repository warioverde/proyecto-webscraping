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
sleep(2)
boton_next = driver.find_element(By.XPATH, "//*[@icon='cp-button-right']")
boton_next.click()
sleep(5)
#divs_gym = driver.find_elements(By.XPATH, "//div[@class='tile-item-price']")

divs_gym = driver.find_elements(By.XPATH, "//div[contains(@class,'col-xs-12')]")
# precios_gym= driver.find_element(By.XPATH, "//div[@class='tile-item-price']//span[@class='tile-item-price-value']")
# periodos_gym= driver.find_element(By.XPATH, "//div[@class='tile-item-price']//span[@class='tile-item-price-interval']")

contador = 0
for gym in divs_gym: # Voy a darle click en cargar mas 3 veces
    print("contador de gym "+ str(contador))
    precio_gym = driver.find_element(By.XPATH, "//span[@class='tile-item-price-value']").text
    periodo_gym = driver.find_element(By.XPATH, "//span[@class='tile-item-price-interval']").text
    print(precio_gym)
    print(periodo_gym)
    contador = contador+1
# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
# autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')


# # Recorro cada uno de los anuncios que he encontrado
# for auto in autos:
#     try:
#         # Por cada anuncio hallo el precio
#         precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
#         print (precio)
#         # Por cada anuncio hallo la descripcion
#         descripcion = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text
#         print (descripcion)
#     except Exception as e:
#         print ('Anuncio carece de precio o descripcion')