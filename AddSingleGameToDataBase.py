from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import os
import time
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def InitialConfiguration(initial_page): 
    print("Configurando driver...")
    
    chrome_options = Options()
    chrome_options.binary_location = "./chromeportable/App/Chrome-bin/chrome.exe" 
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=./chrome_user_data")  # Directorio temporal
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-minimized")
   
    
    service = Service(executable_path=resource_path('./driver/chromedriver.exe'))
   
    driver_setup = webdriver.Chrome(service=service,options=chrome_options)
    driver_setup.get(initial_page)
    
    return driver_setup

def SearchGame(game_name,driver):
    print("Buscando juego en https://boardgamegeek.com...")
    
    input_element = driver.find_element(By.NAME, "searchTerm")
    
    input_element.clear()
    input_element.send_keys(game_name)
    
    escape = True
    times_tried = 2
    while escape:
        times_tried = times_tried + 1
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID,"ngb-typeahead-0-0"))
            )
        except:
            input_element.clear()
            input_element.send_keys(game_name)
            if times_tried == 5:
                print("No se encontro el juego: "+game_name)
                return False
        else:
            game_link = driver.find_element(By.ID,"ngb-typeahead-0-0")
            
            game_link.click()
            full_credits = driver.find_element(By.PARTIAL_LINK_TEXT,"Full Credits")
            full_credits.click()
            return True

def ExtractInformation(driver):
    print("Extrayendo informacion del juego...")
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@itemprop, 'name')]"))
    )
    
    title_name = soup.find("span",{"itemprop": "name"})
    
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/boardgamemechanic/')]"))
        )
    except:
        mechanics = ''
        print("Mecanicas del juego "+title_name.text+" no encontradas")
    else:
        mechanics = driver.find_elements(By.XPATH, "//a[contains(@href, '/boardgamemechanic/')]")

#    mechanics = soup.findAll("a", href=re.compile(r"/boardgamemechanic/.2*"))
    mechanics = driver.find_elements(By.XPATH, "//a[contains(@href, '/boardgamemechanic/')]")
    
    game_entry = OrganizeInformation(mechanics,title_name)
    
    return game_entry

def OrganizeInformation(mechanics,title_name):
    print("Organizando informacion extraida...")
    
    game_entry = {}
    game_title = title_name.text.strip()
    game_entry[game_title] = {'Categorias': []}
    
    for mechanic in mechanics:
        mechanic_name = mechanic.text.strip()
        
        game_entry[game_title]['Categorias'].append(mechanic_name)
        
        
    return game_entry
    
def SaveGame(data_file_name,new_game_entry):
    print("Guardando juego...")
    
    existing_games = []
    existing_categories = []

    try:
        with open(data_file_name, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            existing_games = next(csv_reader, [])  
            existing_categories = next(csv_reader, [])  
    except FileNotFoundError:
        print("No se encontró el archivo")
        pass  # Si el archivo no existe, continuar sin cargar nada


    new_game_name = list(new_game_entry.keys())[0]
    
    if new_game_name in existing_games:
        print("El juego ya esta agregado al sistema")
        return

    # Agregar nuevas entradas de juegos y categorías
    with open(data_file_name, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        
        new_categories = [
            ';'.join(new_game_entry[new_game_name]['Categorias'])
        ]
        
        updated_games_row = existing_games + [new_game_name]
        updated_categories_row = existing_categories + new_categories

        # Reescribir el archivo completo con las filas actualizadas
        with open(data_file_name, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(updated_games_row)
            csv_writer.writerow(updated_categories_row)

    print(new_game_name+" agregado con exito")
    

def search_game_online(game_name):
    
    initial_page = "https://boardgamegeek.com"
    driver = InitialConfiguration(initial_page)
    driver.minimize_window()
    
    time.sleep(2)
    
    print("Activando driver...")
    
    game_entry = ""
    
    is_valid = SearchGame(game_name,driver)
    
    if not is_valid:
        
        driver.quit()
        
        return "fail"
    else:
        game_entry = ExtractInformation(driver)
    
        driver.quit()
        
        return game_entry

def main(game_name):
    initial_page = "https://boardgamegeek.com"
    driver = InitialConfiguration(initial_page)
    driver.minimize_window()
    
    if SearchGame(game_name,driver):
        game_entry = ExtractInformation(driver)
    
        SaveGame('test.csv',game_entry)
    
    driver.quit()
    

if __name__ == "__main__":
    main("jaipur")