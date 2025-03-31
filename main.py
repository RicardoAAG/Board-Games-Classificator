from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import csv
import keyboard
import sys

def SaveAndOrganizeInformation(mechanics,title_name):
    """
    for mechanic in mechanics:
        game_names.append(title_name.text)
        game_categories.append(mechanic.text)
    """
    game_title = title_name.text.strip()
    categories_by_games[game_title] = {'Categorias': []}
    
    for mechanic in mechanics:
        mechanic_name = mechanic.text.strip()
        
        categories_by_games[game_title]['Categorias'].append(mechanic_name)
        
        if mechanic_name not in games_by_categories:
            games_by_categories[mechanic_name] = []
    
    for mechanic in mechanics:
        mechanic_name = mechanic.text.strip()
        games_by_categories[mechanic_name].append(game_title)
    
#    for mechanic in        categories_by_games[game_title]['Categorias'].append(mechanic_name)
            
"""
def SearchFirstGame(game_name):
    input_element = driver.find_element(By.NAME, "searchTerm")
    input_element.clear()
    input_element.send_keys(game_name + Keys.ENTER)

    link = driver.find_element(By.PARTIAL_LINK_TEXT,game_name)
    link.click()
    
    link = driver.find_element(By.CLASS_NAME,"dropdown-toggle")
    link.click()
    link = driver.find_element(By.PARTIAL_LINK_TEXT,"Full Credits")
    link.click()
"""
    
def SearchGame(game_name,initial):
    if initial:
        input_element = driver.find_element(By.NAME, "searchTerm")
    else:
        input_element = driver.find_element(By.ID, "site-search")
    
    input_element.clear()
    input_element.send_keys(game_name)
    
    if initial:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID,"ngb-typeahead-0-0"))
        )
    
        game_link = driver.find_element(By.ID,"ngb-typeahead-0-0")
        
        game_link.click()
        full_credits = driver.find_element(By.PARTIAL_LINK_TEXT,"Full Credits")
        full_credits.click()
    else:
        escape = True
        tried = 2
        while escape == True:
            tried = tried + 1
            try:
                WebDriverWait(driver, tried).until(
                    EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'typeahead-') and contains(@id, 'option-0')]"))
                )
            except:
                input_element.clear()
                input_element.send_keys(game_name)
                if tried == 5:
                    print("No se encontro el juego: "+game_name)
                    escape = False
            else:
                game_link = driver.find_element(By.XPATH, "//*[starts-with(@id, 'typeahead-') and contains(@id, 'option-0')]")
                escape = False
                game_link.click()
                
                full_credits = driver.find_element(By.PARTIAL_LINK_TEXT,"Full Credits")
                full_credits.click()
    
def ExtractInformation():
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
    
    SaveAndOrganizeInformation(mechanics,title_name)
    
def InitialConfiguration(initial_page):
    service = Service(executable_path="chromedriver.exe")
    
    chrome_options = Options()
    
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
   
    driver_setup = webdriver.Chrome(service=service,options=chrome_options)
    driver_setup.get(initial_page)
    
    return driver_setup
   
def LoadCSV():
    output=[]
    
    csv_file_path = 'games_names.csv'
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:
                output.append(row[0])
    
    return output
    
def CreateCSV():
    existing_games = []
    existing_categories = []

    try:
        with open("games_information.csv", 'r', newline='') as file:
            csv_reader = csv.reader(file)
            existing_games = next(csv_reader, [])  
            existing_categories = next(csv_reader, [])  
    except FileNotFoundError:
        pass  # Si el archivo no existe, continuar sin cargar nada

    # Preparar nuevas entradas (solo juegos y categorías no guardados)
    games = list(categories_by_games.keys())
    new_games = [new_game for new_game in games if new_game not in existing_games]
    
    if len(new_games) == 0:
        print("No hay juegos nuevos para agregar.")
        return

    # Agregar nuevas entradas de juegos y categorías
    with open("games_information.csv", 'a', newline='') as file:
        csv_writer = csv.writer(file)

        # Crear lista de categorías para cada juego nuevo
        new_categories = [
            ';'.join(categories_by_games[game]['Categorias']) for game in new_games
        ]
        
        updated_games_row = existing_games + new_games
        updated_categories_row = existing_categories + new_categories

        # Reescribir el archivo completo con las filas actualizadas
        with open("games_information.csv", 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(updated_games_row)
            csv_writer.writerow(updated_categories_row)

    print("Juegos nuevos agregados exitosamente.")

games_to_search = LoadCSV()

initial_page = "https://boardgamegeek.com"
    
driver = InitialConfiguration(initial_page)
first_game = True

"""
game_names = []
game_categories = []
"""
games_by_categories = {}
categories_by_games = {}

while True:
    for game in games_to_search:
        if first_game:
            SearchGame(game,True)
            first_game = False
        else:
            SearchGame(game,False)
            
        ExtractInformation()
        CreateCSV()
        
        if keyboard.is_pressed("q"):
          break 

    #print(categories_by_games)
    
    time.sleep(1)
    CreateCSV()
    time.sleep(2)
    driver.quit()
    sys.exit(0)
    
    if keyboard.is_pressed("q"):
      break 


"""Waiting part, use when needed"""
"""
WebDriverWait(driver, 1).until(
    EC.presence_of_element_located((By.NAME, "searchTerm"))
)
"""