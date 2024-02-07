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
driver.get('https://scramgym.com/member-portal/gym-registration/')
sleep(3)
# driver.refresh() # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página
# sleep(2) # Esperamos que cargue el boton
driver.execute_script("""window.scrollTo(0, 1000)""")
sleep(5)
# Busco el boton para cargar mas informacion
boton_div = WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'signup-box')]//a[@data-divisionid='15']"))
)
# boton_div = driver.find_element(By.XPATH, "//div[contains(@class,'col-xs-12')][3]")
boton_div.click()

divs_gym = driver.find_elements(By.XPATH, "//a[contains(@class,'btn-addmembership')]")
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
    precio_gym = div.find_element('xpath', "./span[contains(@class,'membership-price')]/h2").text
    periodo_gym = div.find_element('xpath', "./span[contains(@class,'membership-details')]/h4").text
    print(precio_gym+"/"+periodo_gym)
    Table_dict = {
            'periodo': periodo_gym,
            'precio': precio_gym,
            'moneda': 'Euro',
            'gym': 'scramgym'
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