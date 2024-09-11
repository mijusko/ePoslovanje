import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

# Pročitajte ime filma iz komandne linije
if len(sys.argv) != 2:
    print("Usage: python torrent.py <film_name>")
    sys.exit(1)

film_name = sys.argv[1]

# Zamena razmaka sa donjom crtom
film_name_safe = film_name.replace(' ', '_')

# Putanja do vašeg WebDriver-a (zameni sa tačnom putanjom)
driver_path = "C:/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)

driver = webdriver.Chrome(service=service)

# Otvaranje TPB sajta
driver.get('https://tpb.party/')

# Pronalaženje pretrage
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'https_form'))
    )
    # Unos pretrage za film
    search_box.send_keys(film_name)

    # Pronalaženje dugmeta za pretragu i klik
    search_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
    search_button.click()

    # Sačekajte da se rezultati učitaju
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'main-content'))
    )

    # Pronalaženje tabele sa rezultatima u divu 'main-content'
    main_content = driver.find_element(By.ID, 'main-content')
    rows = main_content.find_elements(By.XPATH, './/table//tr')

    # Prikupljanje podataka za prvih 5 redova (isključujući header red)
    div_contents = []
    for row in rows[1:6]:  # Preskačemo header red
        row_html = row.get_attribute('outerHTML')
        div_contents.append(f'<div class="row">{row_html}</div>')

except Exception as e:
    print(f"Greška prilikom preuzimanja podataka: {e}")

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# Generisanje HTML datoteke sa prikupljenim podacima
html_content = f"""
<html>
<head>
    <style>
        .row {{
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h1>Found Torrents</h1>
    <h6>Last update at {dt_string}</h6>
"""

for div_content in div_contents:
    html_content += div_content

html_content += "</body></html>"

# Zamenite sa željenim direktorijumom za čuvanje HTML datoteke
download_directory = "C:/Users/mihaj/source/Find_Movie/media/torrents"

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Upisivanje u HTML datoteku koristeći UTF-8 enkodiranje
html_file_path = os.path.join(
    download_directory, f"{film_name_safe}_torrents.html")

with open(html_file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"HTML datoteka generisana: {html_file_path}")

# Zatvaranje pretraživača
driver.quit()
