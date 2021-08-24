# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 08:21:19 2020
Last modified on Fri Nov 27 17:24:30 2020

@author: pirio
"""
from time import time
start_time = time()

# 0. Import modules: "requests", to get the web code from different pages,
# bs4, for parsing HTML if available, and "re", to use regular expressions, and 

import requests
import bs4
import re

# 0. Open the current Comunitat Valenciana data file and check out the last available date for data:

csv_file = open ('../../data/original/valencia/valencia.csv', 'r')

lineas = csv_file.readlines()
num = len(lineas)-1

ultima = lineas[num]
# print (ultima)

find_fec = re.findall('(.*?),', ultima)
fecha_cur = find_fec[0]
print ('Última fecha disponible: ', fecha_cur)

# 1. Set the list page of COVID-19 news in Comunitat Valenciana

url_list = 'https://www.gva.es/es/inicio/area_de_prensa/ap_notas_prensa?zona=21&idioma=ES&tipoContenido=26&busquedadescripcion=Coronavirus%7Ccovid19%7Ccovid-19&busquedacategoria=0&busquedaorganismo=3.07&busquedafechaini=&busquedafechafin=&botonBuscar=Buscar'

    
# 2. Get the list of links webpage
res1 = requests.get(url_list)
# Test if the connection is OK. If so, nothing happens. Otherwises, an error message appears.
res1.status_code == requests.codes.ok

# 3. Parse HTML
gethtml = bs4.BeautifulSoup(res1.text, 'html.parser')

noticias = gethtml.select('div.noticia')


# 4. Find the most current news report
for i in noticias:
    texto = i.text
    # print (texto)
    # input ('¿Sigo?')
    
    datos_covid = re.compile('\d* (nuevos casos|casos nuevos) de coronavirus')
    gettit = datos_covid.search(texto)
    if gettit == None:
        continue
    else:
        # Extraer la fecha y ponerla en formato
        date_re = re.compile(r'(\d\d)/(\d\d)/(\d\d\d\d)')
        getfecha = date_re.search(texto)
        fecha = getfecha.group(3) + '-' + getfecha.group(2) + '-' + getfecha.group(1)
        print ("Date: " , fecha)
        
        enlace_dia = i.select('[href]')[0].get('href')
        print (enlace_dia)
        break 

# 5. Test if this report is not updated in the final CSV yet
    
if fecha > fecha_cur:
    
    print ('Nueva noticia')
    
    url_report = 'https://www.gva.es/es' + enlace_dia + '&languageId=es_ES'
           
    # Get the list of links webpage
    res2 = requests.get(url_report)
    # Test if the connection is OK. If so, nothing happens. Otherwises, an error message appears.
    res2.status_code == requests.codes.ok
    
    # Parse HTML
    gethtml2 = bs4.BeautifulSoup(res2.text, 'html.parser')
    
    csv_file.close()

# 5b. Get all the text from all the paragraphs.
        # So, if data where at a different paragraph than in previous reports,
        # they will be located more likely, anyway.
        
    parrafos = gethtml2.select('p')
    texto = ''
    for i in parrafos:
        texto = texto + i.text

#    casos_re = re.compile('por prueba PCR(.*? )en total\)\.|por prueba PCR.*?Por provincias(.*?)\.')
#    casos_re = re.compile('Por provincias, la distribución de nuevos positivos(.*?\))\.')
#    casos_re = re.compile('por prueba PCR(.*? )en total\)\.|por prueba PCR.*?Por provincias(.*?)\.')
#    casos_re = re.compile('por prueba PCR.*?Por provincias(.*?)\.')
    casos_re = re.compile('por prueba PCR.*?Por provincias(.*?) total de casos no asignados')
#    casos_re = re.compile('por prueba PCR.*?Por provincias(.*?)\. El total de casos no asignados')
    
    
    

    try:
        getcasos = casos_re.search(texto)
        casos = getcasos.group(1).replace('.', '')
    except:
        casos = ""    
                
    print(casos)    
    
    casos_split = re.findall('(\d+?) ', casos)
    print (casos_split)

    if len(casos_split) == 5:
        casos_split_val = re.findall('(\d+)\)', casos)
        casos_split.append(casos_split_val[0])
    
    print (casos_split)
    # input('?')
   
    # cast_acti_pcr = casos_split[0]
    # cast_accu_pcr = casos_split[1]
    # alic_acti_pcr = casos_split[2]
    # alic_accu_pcr = casos_split[3]
    # vale_acti_pcr = casos_split[4]
    # vale_accu_pcr = casos_split[5]

    try:
        cast_acti_pcr = casos_split[0]
    except:
        cast_acti_pcr = ""
        
    try:
        cast_accu_pcr = casos_split[1]
    except:
        cast_accu_pcr = ""
        
    try:
        alic_acti_pcr = casos_split[2]
    except:
        alic_acti_pcr = ""

    try:
        alic_accu_pcr = casos_split[3]
    except:
        alic_accu_pcr = ""

    try:
        vale_acti_pcr = casos_split[4]
    except:
        vale_acti_pcr = ""

    try:
        vale_accu_pcr = casos_split[5]       
    except:
        vale_accu_pcr = ""       
        
   
    print ('Castellón, activos: ', cast_acti_pcr)
    print ('Castellón, acumulados: ', cast_accu_pcr)
    print ('Alicante, activos: ', alic_acti_pcr)
    print ('Alicante, acumulados: ', alic_accu_pcr)
    print ('Valencia, activos: ', vale_acti_pcr)
    print ('Valencia, acumulados: ', vale_accu_pcr)
    
#    input('?')
    
# 5d. Get the number of recovered, for each province
    rec_re = re.compile('superado la enfermedad.*?:(.*? Valencia)')

    try:

        getrec = rec_re.search(texto)
        recovs = getrec.group(1).replace('.','')
        # print (recovs)
    
        rec_prov = re.findall('\d+',recovs)
     
        cast_recov = rec_prov[0]
        alic_recov = rec_prov[1]
        vale_recov = rec_prov[2]
 
    
    except:
        cast_recov = ""
        alic_recov = ""
        vale_recov = ""
           
    print ('Castellón, recuperados: ', cast_recov)
    print ('Alicante, recuperados: ', alic_recov)
    print ('Valencia, recuperados: ', vale_recov)
    
# 5e. Get the number of hospitalized, for each province
    
    # Extract the  strings from Castellón, Valencia y Alicante
    
    try:
        hosp_re = re.compile('personas ingresadas.*?:(.*? UCI)\.')
        
        gethosp = hosp_re.search(texto)
        hosps = gethosp.group(1).replace('.','')
        
        datos_hosps = re.findall('\d+', hosps)

        uci_cast = int(datos_hosps[1])
        print ("UCI Castellón: ", uci_cast)
        hospi_cast = int(datos_hosps[0])
        hospi_cast = str(hospi_cast - uci_cast)
        uci_cast = str(uci_cast)
        print ('Hospi Cast', hospi_cast)

        uci_alic = int(datos_hosps[3])
        print ("UCI Alicante: ", uci_alic)
        hospi_alic = int(datos_hosps[2])
        hospi_alic = str(hospi_alic - uci_alic)
        uci_alic = str(uci_alic)
        print ('Hospi Alicante', hospi_alic)

        uci_vale = int(datos_hosps[5])
        print ("UCI Valencia: ", uci_vale)
        hospi_vale = int(datos_hosps[4])
        hospi_vale = str(hospi_vale - uci_vale)
        uci_vale = str(uci_vale)
        print ('Hospi Valencia', hospi_vale)
        
    except:
        
        hospi_cast = ""
        uci_cast = ""
        hospi_alic = ""
        uci_alic = ""
        hospi_vale = ""
        uci_vale = ""
        
    
    
# 5f. Get the number of deceased (death), for each province
#    dece_re = re.compile('han registrado .*? fallecimientos por coronavirus.*?: (.*?) en la provincia de Castellón, (.*?) en la de Alicante y (.*?) en la de Valencia.')
#    dece_re = re.compile('han registrado .*? fallecimientos.*?: (.*?) en la provincia de Castellón, (.*?) en la de Alicante y (.*?) en la de Valencia.')
    dece_re = re.compile('han registrado .*? fallecimientos.*?: (.*?) en la provincia de Castellón, (.*?) en la de Alicante y (.*?) en la de Valencia.')

    getdece = dece_re.search(texto)
 
    try:
        cast_dece = getdece.group(1).replace('.', '')
        alic_dece = getdece.group(2).replace('.', '')
        vale_dece = getdece.group(3).replace('.', '')
 
    
    except:
        cast_dece = ""
        alic_dece = ""
        vale_dece = ""

           
    print ('Castellón, acum. fallecidos: ', cast_dece)
    print ('Alicante, acum. fallecidos: ', alic_dece)
    print ('Valencia, acum. fallecidos: ', vale_dece)   
    
#    input('?')
    
    
# # 5g. Append a new line for EACH province, to the current CSV data file.
    
    # Close the CSV as a read file
    csv_file.close()
    
    # Open it as an append file.
    
    csv_file = open ('../../data/original/valencia/valencia.csv', 'a', encoding = "utf-8")   
    new_line_alic = '\n' + fecha + ',' + 'Alicante/Alacant' + ',' + 'Comunitat Valenciana' + ',' + alic_acti_pcr + ',' + ',' + ',' + ',' + hospi_alic + ',,,' + uci_alic + ',' + alic_dece  + ',' + alic_accu_pcr + ',' + ',' + alic_recov + ',Sanidad Generalitat Valenciana,' + url_report
    csv_file.write(new_line_alic)
    print (new_line_alic)
    
    new_line_cast = '\n' + fecha + ',' + 'Castellón/Castelló' + ',' + 'Comunitat Valenciana' + ',' + cast_acti_pcr + ',' + ',' + ',' + ',' + hospi_cast + ',,,' + uci_cast + ',' + cast_dece + ',' + cast_accu_pcr + ',' + ',' + cast_recov + ',Sanidad Generalitat Valenciana,' + url_report
    csv_file.write(new_line_cast)
    print (new_line_cast)

    new_line_vale = '\n' + fecha + ',' + 'Valencia/València' + ',' + 'Comunitat Valenciana' + ',' + vale_acti_pcr + ',' + ',' + ',' + ',' + hospi_vale + ',,,' + uci_vale + ',' + vale_dece  + ',' + vale_accu_pcr + ',' + ',' + vale_recov + ',Sanidad Generalitat Valenciana,' + url_report
    csv_file.write(new_line_vale)
    print (new_line_vale)
         
    csv_file.close()
     
    
# # 6. ELSE: if data are already included into the file (for example, there is
# # no udpate on weekends) 

else:
    
    print ('Ya está actualizado')

    
    csv_file.close()
    
duration = time() - start_time
duration = round(duration, 2)

print ("Ha tardado ", duration, "segundos")
