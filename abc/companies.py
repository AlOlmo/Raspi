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
                    "name": safe_extract_text(item.find_next("span", {"itemprop": "name"})),#
                    "postal_code": safe_extract_text(item.find_next("span", {"itemprop": "postalCode"})),
                    "province": safe_extract_text(item.find_next("span", {"itemprop": "addressRegion"})),
                    "city": safe_extract_text(item.find_next("span", {"itemprop": "addressLocality"})),#
                    "phone": safe_extract_text(item.find_next("span", {"itemprop": "telephone"})),#
                    "address": safe_extract_text(item.find_next("span", {"itemprop": "streetAddress"})),#
                    "web": " " #
            })

        # Write file
        pd.DataFrame.from_dict(parsed_items).to_csv(f"{category}.csv", mode='a', header=False, sep='#')
        time_2 = time.process_time()
        print(f"Page {number} scrapped (time: {time_2 - time_1})")

#Adjust
        function getCity($div): ?string
    {
        $cityNodeList = $div->filter('span[itemprop="addressLocality"]');
        if (count($cityNodeList) > 0) {
            $address = $cityNodeList->text();
            preg_match('/\((.*?)\)\s*(.*?),/', $address, $matches);
            if (isset($matches[2])) {
                $city = trim($matches[2]);
                echo sprintf("Ciudad: %s %s", $city, PHP_EOL);
                return $city;
            }
        }
        return " ";
    }

    function getProvince($div): ?string
    {
        $cityNodeList = $div->filter('span[itemprop="addressLocality"]');
        if (count($cityNodeList) > 0) {
            $address = $cityNodeList->text();
            preg_match('/, (.*?)$/', $address, $matches);
            if (isset($matches[1])) {
                $province = trim($matches[1]);
                echo sprintf("Provincia: %s %s", $province, PHP_EOL);
                return $province;
            }
        }
        return null;
    }


    function getPc($div): ?string
    {
        $cityNodeList = $div->filter('span[itemprop="addressLocality"]');
        if (count($cityNodeList) > 0) {
            $address = $cityNodeList->text();
            preg_match('/\((.*?)\)/', $address, $matches);
            if (isset($matches[1])) {
                $postalCode = trim($matches[1]);
                echo sprintf("Código Postal: %s %s", $postalCode, PHP_EOL);
                return $postalCode;
            }
        }
        return null;
    }

