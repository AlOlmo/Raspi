import time
from time import sleep
import json

import requests
from bs4 import BeautifulSoup, PageElement
import pandas as pd
import sys


def safe_extract_text(element: PageElement):
    if element is not None:
        return element.text
    else:
        return ''


def get_phone(element):
    if element is not None:
        text = element.text
        # Eliminar espacios en blanco entre dígitos
        text = text.replace(" ", "")
        # Eliminar el prefijo "+34"
        text = text.replace("+34", "")
        return text
    else:
        return ""


class ProvinceFinder:
    def __init__(self):
        self.provinces = {
            "02": "Albacete",
            "03": "Alicante/Alacant",
            "04": "Almería",
            "01": "Araba/Álava",
            "33": "Asturias",
            "05": "Ávila",
            "06": "Badajoz",
            "07": "Illes Balears",
            "08": "Barcelona",
            "48": "Bizkaia",
            "09": "Burgos",
            "10": "Cáceres",
            "11": "Cádiz",
            "39": "Cantabria",
            "12": "Castellón/Castelló",
            "13": "Ciudad Real",
            "14": "Córdoba",
            "15": "Coruña, A",
            "16": "Cuenca",
            "20": "Gipuzkoa",
            "17": "Girona",
            "18": "Granada",
            "19": "Guadalajara",
            "21": "Huelva",
            "22": "Huesca",
            "23": "Jaén",
            "24": "León",
            "25": "Lleida",
            "27": "Lugo",
            "28": "Madrid",
            "29": "Málaga",
            "30": "Murcia",
            "31": "Navarra",
            "32": "Ourense",
            "34": "Palencia",
            "35": "Las Palmas",
            "36": "Pontevedra",
            "26": "Rioja, La",
            "37": "Salamanca",
            "38": "Tenerife",
            "40": "Segovia",
            "41": "Sevilla",
            "42": "Soria",
            "43": "Tarragona",
            "44": "Teruel",
            "45": "Toledo",
            "46": "Valencia/València",
            "47": "Valladolid",
            "49": "Zamora",
            "50": "Zaragoza",
            "51": "Ceuta",
            "52": "Melilla"
        }

    def get_province(self, pc: str) -> str:
        if pc and pc[:2] in self.provinces:
            province = self.provinces[pc[:2]]
            #print(f"Provincia: {province}")
            return province
        return None



finder = ProvinceFinder()

categories = open("cy_categories.txt", "r")
pcs = open("cy_pcs.txt", "r")

if __name__ == '__main__':

    for category in categories:
        category = category.strip()  # Elimina cualquier espacio o salto de línea

        for line in pcs:
            varPC_list = json.loads(line.strip())

            for varPC in varPC_list:
                page = 1  # Inicializa la variable de página (si es necesario)
                
                while True:
                    time_1 = time.process_time()
                    # Realiza la solicitud
                    response = requests.get(
                        url=f"https://www.cylex.es/s?q={category}&c=&z={varPC}&p={page}",
                        headers={'User-agent': 'Mozilla/5.0'}
                    )
                    
                    html = response.content

                # Extract data
                    soup = BeautifulSoup(html, "html.parser")
                    items = soup.find_all("div", {"class": "lm-item"})
                    #print(items)
                    parsed_items = []
                    print(category, page)
                    for item in items:
                
                        parsed_items.append({
                            "name": safe_extract_text(item.find("div", class_="h4 bold my-2").find("a")),###
                            "postal_code": varPC,###
                            "province": finder.get_province(varPC),###
                            "city": safe_extract_text(item.find("p", class_="m-0").find("strong")),###
                            "phone": get_phone(item.find("p", class_="lm-adr-ln4")),###
                            "address": safe_extract_text(item.find("p", class_="lm-adr-ln2")),###
                            "web": " " 
                        })

                        print(safe_extract_text(item.find("div", class_="h4 bold my-2").find("a")))
                    page += 1
                    time.sleep(7)
            # Write file TODO cambiar el nombre de cada ciudad a peinar
                    pd.DataFrame.from_dict(parsed_items).to_csv(f"Cylex.csv", mode='a', header=False, sep='#')
                    time_2 = time.process_time()
                    print(f"Page https://www.cylex.es/s?q={category}&c=&z={varPC}&p={page} scrapped (time: {time_2 - time_1})")
                    