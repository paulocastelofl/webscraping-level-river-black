
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pymongo import MongoClient

import json
import pandas as pd
import time

connection_string = "mongodb://localhost:27017/"
try:
    connect = MongoClient(connection_string)
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database
db = connect.levelBlackRiver
# creating or switching to demoCollection
collection = db.levels

options = Options()
options.add_argument("--headless")

browser = webdriver.Chrome(options=options)
browser.get('https://www.portodemanaus.com.br/?pagina=nivel-do-rio-negro-hoje')
time.sleep(0.5)
table_nivel_rio = browser.find_element(
    By.XPATH, "//table[2]/tbody/tr/td[7]/table[2]")
time.sleep(0.5)
htmlContent = table_nivel_rio.get_attribute("outerHTML")
time.sleep(0.5)
soup = BeautifulSoup(htmlContent, "html.parser")

months = ["jul", "ago", "set", "out", "nov", "dez"]
table_data = []
day = 1
for row in soup.find_all('tr')[2:]:
    columns = row.find_all('td')
    j = 0
    k = 1
    for number in range(6):
        query = {"_id": months[j]+"-"+str(day)}
        document = {
            "Dia": str(day),
            "Mes": months[j],
            "Cota": columns[k].text.strip(),
            "EncheuVazou": columns[(k+1)].text.strip()
        }
        # Inserting both document one by one
        collection.replace_one(query, document, upsert=True)
        k += 2
        j += 1
    day += 1
browser.quit()
