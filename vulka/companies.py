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
                    "province": safe_extract_text(item.find_next("span", {"itemprop": "addressRegion"})),
                    "city": safe_extract_text(item.find_next("span", {"itemprop": "addressLocality"})),#
                    "phone": safe_extract_text(item.find("div", class_="infoContacto")),###
                    "address": safe_extract_text(item.find("span", class_="localizacion")),#
                    "web": " " #
            })

        # Write file
        pd.DataFrame.from_dict(parsed_items).to_csv(f"{category}.csv", mode='a', header=False, sep='#')
        time_2 = time.process_time()
        print(f"Page {number} scrapped (time: {time_2 - time_1})")

