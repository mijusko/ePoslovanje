import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

# Pročitajte ime filma iz komandne linije
if len(sys.argv) != 2:
    print("Usage: python subtitles.py <film_name>")
    sys.exit(1)

film_name = sys.argv[1]

# Zamena razmaka sa donjom crtom
film_name_safe = film_name.replace(' ', '_')

# Putanja do vašeg WebDriver-a (zameni sa tačnom putanjom)
driver_path = "C:/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)

driver = webdriver.Chrome(service=service)

# Otvaranje OpenSubtitles sajta
driver.get('https://www.opensubtitles.org/sr/search/sublanguageid-scc')

# Pronalaženje polja za pretragu
search_box = driver.find_element(By.ID, 'search_text')

# Unos naziva filma
search_box.send_keys(film_name)

# Pronalaženje dugmeta za pretragu i klik na njega
submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
submit_button.click()

# Sačekajte da se rezultati učitaju
time.sleep(5)

# Klik na prvi rezultat sa klasom 'bnone' nakon submit-a
try:
    bnone_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'bnone'))
    )
    bnone_link.click()
except Exception as e:
    print(f"Greška prilikom klika na prvi rezultat sa klasom 'bnone': {e}")
    driver.quit()
    sys.exit(1)

# Sačekajte da se stranica sa titlovima učita
try:
    # Pronađi sve redove (tr) koji sadrže rezultate
    result_rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//tr[contains(@class, "change")]'))
    )

    # Prikupljanje informacija iz prvih 10 redova
    collected_data = []
    for row in result_rows[:10]:
        try:
            # Pokušaj da pronađeš span element sa atributom 'title'
            span_element = row.find_element(By.TAG_NAME, 'span')
            span_title = span_element.get_attribute('title')

            # Ako span nema title atribut, uzmi tekst između <br> tagova
            if not span_title:
                # Pronalaženje teksta između dva <br> taga
                br_elements = row.find_elements(By.TAG_NAME, 'br')
                if len(br_elements) > 1:
                    # Dobijanje teksta između dva <br> taga
                    span_title = br_elements[0].get_property(
                        'nextSibling').strip()
                else:
                    span_title = "Nema dostupnog naslova"
        except:
            span_title = film_name

        # Pronalaženje petog td elementa i svih a href linkova u njemu
        try:
            td_elements = row.find_elements(By.TAG_NAME, 'td')
            if len(td_elements) >= 5:  # Proveri da li ima barem 5 td elemenata
                fifth_td = td_elements[4]  # Peti td (indeks 4)
                a_elements = fifth_td.find_elements(By.TAG_NAME, 'a')
                links = [a.get_attribute('href') for a in a_elements]
            else:
                links = ["Nema dostupnih linkova"]

            link_texts = ', '.join(links)
        except:
            link_texts = "Nema dostupnih linkova"

        collected_data.append(f"Title: {span_title}, Links: {link_texts}")

except Exception as e:
    print(f"Greška prilikom preuzimanja podataka iz redova: {e}")

# Generisanje HTML datoteke sa prikupljenim podacima
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
html_content = f'<html><body><h1>Found Subtitles</h1><h6>Last update at {dt_string}</h6><ul>'
for data in collected_data:
    title, links = data.split(', Links: ')  # Razdvajanje naslova i linkova
    html_content += f"<li>{title} <a href='{link_texts}'\">Download</a></li>"
html_content += "</ul></body></html>"

# Zamenite sa željenim direktorijumom za čuvanje HTML datoteke
download_directory = "C:/Users/mihaj/source/Find_Movie/media/subtitles"

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Upisivanje u HTML datoteku koristeći UTF-8 enkodiranje
html_file_path = os.path.join(
    download_directory, f"{film_name_safe}_subtitles.html")

with open(html_file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"HTML datoteka generisana: {html_file_path}")

# Zatvaranje pretraživača
driver.quit()
