import time
from time import sleep

import requests
from bs4 import BeautifulSoup, PageElement
import pandas as pd
import sys


def safe_extract_text(element: PageElement):
    if element is not None:
        return element.get_text(strip=True).replace('\n', '').replace('\t', '').strip()
    else:
        return ''

def extract_address(full_text):
    # Encuentra el guion que separa la descripción de la dirección
    start = full_text.find("-") + 1  # Encuentra el guion y el carácter siguiente

    address = full_text[start:].strip()  # Extrae y limpia la dirección
    return address


def extract_city(full_text):
    # Encuentra el inicio y el final de la ciudad
    start = full_text.find("en ") + 3  # Encuentra "en " y el carácter siguiente
    end = full_text.find(" (")  # Encuentra el primer paréntesis

    city = full_text[start:end].strip()  # Extrae y limpia la ciudad
    return city


def extract_province(full_text):
    # Encuentra el inicio y el final de la provincia entre paréntesis
    start = full_text.find("(") + 1  # Encuentra la apertura del paréntesis y el carácter siguiente
    end = full_text.find(")")  # Encuentra el cierre del paréntesis
    if start != -1 and end != -1 and start < end:
        province = full_text[start:end].strip()  # Extrae y limpia la provincia
        return province
    return None

def get_pc(province):
    provinces = {
        "Álava": "01001",
        "Albacete": "02001",
        "Alicante": "03001",
        "Almería": "04001",
        "Ávila": "05001",
        "Badajoz": "06001",
        "Islas Baleares": "07001",
        "Barcelona": "08001",
        "Burgos": "09001",
        "Cáceres": "10001",
        "Cádiz": "11001",
        "Castellón": "12001",
        "Ciudad Real": "13001",
        "Córdoba": "14001",
        "A Coruña": "15001",
        "Cuenca": "16001",
        "Girona": "17001",
        "Granada": "18001",
        "Guadalajara": "19001",
        "Guipúzcoa": "20001",
        "Huelva": "21001",
        "Huesca": "22001",
        "Jaén": "23001",
        "León": "24001",
        "Lleida": "25001",
        "La Rioja": "26001",
        "Lugo": "27001",
        "Madrid": "28001",
        "Málaga": "29001",
        "Murcia": "30001",
        "Navarra": "31001",
        "Ourense": "32001",
        "Asturias": "33001",
        "Palencia": "34001",
        "Las Palmas": "35001",
        "Pontevedra": "36001",
        "Salamanca": "37001",
        "Santa Cruz de Tenerife": "38001",
        "Cantabria": "39001",
        "Segovia": "40001",
        "Sevilla": "41001",
        "Soria": "42001",
        "Tarragona": "43001",
        "Teruel": "44001",
        "Toledo": "45001",
        "Valencia": "46001",
        "Valladolid": "47001",
        "Vizcaya": "48001",
        "Zamora": "49001",
        "Zaragoza": "50001",
        "Ceuta": "51001",
        "Melilla": "52001"
    }

    if province in provinces:
        #print("PC ->", provinces[province])
        return provinces[province]
    else:
        return None


categories = open("vu_categories.txt", "r")

if __name__ == '__main__':

    clas = "muebles"

    for category in categories:
        category = category.strip()  # Elimina cualquier espacio o salto de línea
        page = 1  # Inicializa la variable de página (si es necesario)
        
        while True:
            time_1 = time.process_time()
            # Realiza la solicitud
            response = requests.get(
                url=f"https://{clas}.vulka.es/{category}/{page}/",
                headers={'User-agent': 'Mozilla/5.0'}
            )
            
            html = response.content

        # Extract data
            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all("div", {"class": "normal"})
            parsed_items = []
            print(category, page)
            for item in items:

                parsed_items.append({
                    "name": safe_extract_text(item.find_next("h3").find("a")),###
                    "postal_code": get_pc(extract_province(safe_extract_text(item.find("span", class_="localizacion")))),  ###
                    "province": extract_province(safe_extract_text(item.find("span", class_="localizacion"))),###
                    "city": extract_city(safe_extract_text(item.find("span", class_="localizacion"))),###
                    "phone": safe_extract_text(item.find("div", class_="infoContacto")),###
                    "address": extract_address(safe_extract_text(item.find("span", class_="localizacion"))),###
                    "web": " " #
                })
                print(safe_extract_text(item.find_next("h3").find("a")))

                # Imprimir el array parsed_items

            time.sleep(7)
            # Write file
            pd.DataFrame.from_dict(parsed_items).to_csv(f"{category}.csv", mode='a', header=False, sep='#')
            time_2 = time.process_time()
            print(f"Page {page} scrapped (time: {time_2 - time_1})")
            page += 1
            if not items:
                print(f"No more items found for category {category} on page {page}.")
                break

