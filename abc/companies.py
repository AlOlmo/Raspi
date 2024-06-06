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

def extract_city(full_address):
    # Elimina el código postal entre paréntesis
    start = full_address.find(")") + 2  # Encuentra el cierre del paréntesis y el espacio posterior
    end = full_address.find(",")  # Encuentra la coma que separa la ciudad del estado/provincia
    if start != -1 and end != -1:
        city = full_address[start:end].strip()  # Extrae y limpia la ciudad
        return city
    return None

def extract_postal_code(full_address):
    # Encuentra el inicio y el final del código postal entre paréntesis
    start = full_address.find("(") + 1  # Encuentra la apertura del paréntesis y el carácter siguiente
    end = full_address.find(")")  # Encuentra el cierre del paréntesis
    if start != -1 and end != -1 and start < end:
        postal_code = full_address[start:end].strip()  # Extrae y limpia el código postal
        return postal_code
    return None

def extract_province(full_address):
    # Encuentra la coma que separa la ciudad de la provincia
    start = full_address.find(",") + 1  # Encuentra la coma y el carácter siguiente
    if start != -1:
        province = full_address[start:].strip()  # Extrae y limpia la provincia
        return province
    return None

categories = open("abc_categories.txt", "r")

if __name__ == '__main__':

    for category in categories:
        category = category.strip()  # Elimina cualquier espacio o salto de línea
        page = 1  # Inicializa la variable de página (si es necesario)
        
        while True:
            time_1 = time.process_time()
            # Realiza la solicitud
            response = requests.get(
                url=f"https://www.abctelefonos.com{category}/espana/pag_{page}",
                headers={'User-agent': 'Mozilla/5.0'}
            )

            html = response.content

        # Extract data
            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all("div", {"class": "resultItem"})
            parsed_items = []
            for item in items:
        
                parsed_items.append({
                    "name": safe_extract_text(item.find_next("span", {"itemprop": "name"})),###
                    "postal_code": extract_postal_code(safe_extract_text(item.find_next("span", {"itemprop": "addressLocality"}))),###
                    "province": extract_province(safe_extract_text(item.find_next("span", {"itemprop": "addressLocality"}))),###
                    "city": extract_city(safe_extract_text(item.find_next("span", {"itemprop": "addressLocality"}))),###
                    "phone": safe_extract_text(item.find_next("span", {"itemprop": "telephone"})),###
                    "address": safe_extract_text(item.find_next("span", {"itemprop": "streetAddress"})),###
                    "web": " " #
            })

        # Write file
            pd.DataFrame.from_dict(parsed_items).to_csv(f"{category}.csv", mode='a', header=False, sep='#')
            time_2 = time.process_time()
            print(f"Page {category} scrapped (time: {time_2 - time_1})")

