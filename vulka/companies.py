import time
from time import sleep

import requests
from bs4 import BeautifulSoup, PageElement
import pandas as pd


def safe_extract_text(element: PageElement):
    if element is not None:
        return element.text
    else:
        return ''

def extract_address(full_text):
    # Encuentra el guion que separa la descripción de la dirección
    start = full_text.find("-") + 1  # Encuentra el guion y el carácter siguiente
    if start != -1:
        address = full_text[start:].strip()  # Extrae y limpia la dirección
        return address
    return None

def extract_city(full_text):
    # Encuentra el inicio y el final de la ciudad
    start = full_text.find("en ") + 3  # Encuentra "en " y el carácter siguiente
    end = full_text.find(" (")  # Encuentra el primer paréntesis
    if start != -1 and end != -1 and start < end:
        city = full_text[start:end].strip()  # Extrae y limpia la ciudad
        return city
    return None

def extract_province(full_text):
    # Encuentra el inicio y el final de la provincia entre paréntesis
    start = full_text.find("(") + 1  # Encuentra la apertura del paréntesis y el carácter siguiente
    end = full_text.find(")")  # Encuentra el cierre del paréntesis
    if start != -1 and end != -1 and start < end:
        province = full_text[start:end].strip()  # Extrae y limpia la provincia
        return province
    return None


categories = open("vu_categories.txt", "r")

if __name__ == '__main__':

    clas = "moda"

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
            for item in items:
        
                parsed_items.append({
                    "name": safe_extract_text(item.find_next("h3").find("a")),###
                    "postal_code": safe_extract_text(item.find_next("span", {"itemprop": "postalCode"})),
                    "province": extract_province(safe_extract_text(item.find_next("span", {"itemprop": "localizacion"}))),###
                    "city": extract_city(safe_extract_text(item.find_next("span", {"itemprop": "localizacion"}))),###
                    "phone": safe_extract_text(item.find("div", class_="infoContacto")),###
                    "address": extract_address(safe_extract_text(item.find("span", class_="localizacion"))),###
                    "web": " " #
            })

        # Write file
        pd.DataFrame.from_dict(parsed_items).to_csv(f"{category}.csv", mode='a', header=False, sep='#')
        time_2 = time.process_time()
        print(f"Page {number} scrapped (time: {time_2 - time_1})")

