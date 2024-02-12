import requests
import pandas as pd
import os

headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

response = requests.get('https://scramgym.gymmasteronline.com/portal/getcompanymemberships?session=eyJjb250ZXh0X2NvbXBhbnlpZCI6MiwibGFuZ3VhZ2UiOiJlbl9HQiIsImlwX2FkZHIiOiI3Ny43MS4yNTAuMjAifQ.Zcaqyg.Af4XZObgwacDCAU4qYQJaxsSO4k&companyid=2&divisionids=%5B%5D&renew_ref=&discount_list=&discount_code=&company_group=None', headers=headers)
# print(response)

# Parseo la respuesta en formato JSON. Requests automaticamente lo convierte en un diccionario de Python
data = response.json()
# print(data)

gyms_totales = []

gyms = data["memberships"]
for gym in gyms:
    if gym['divisionid'] == 15:
        gyms_totales.append ({
            'periodo':  gym['name'],
            "precio": gym['price'],
            'moneda': 'Euro',
            'gym': 'scramgym'
        })
df = pd.DataFrame(gyms_totales)
# print (df)
ruta_del_archivo = 'output.csv'
if os.path.exists(ruta_del_archivo):
  print("El archivo ya existe, agregando resultados al final")
  df.to_csv('output.csv', mode='a', header=False, index=False)
else:
  print("El archivo no existe, creando archivo")
  df.to_csv('output.csv', mode='w', index=False)
# si el archivo existe, hacer con appen, si no existe con w