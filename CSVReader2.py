import csv
from difflib import get_close_matches
import os
import time
from AddSingleGameToDataBase import search_game_online,SaveGame

save_file = 'games_information.csv'

class Game:
    def __init__(self, new_name, new_mechanics):
        self.name = new_name
        self.mechanics = new_mechanics
        
    def __repr__(self):
        output=self.name+"\n"
        for mechanic in self.mechanics:
            output = output + "►" + mechanic + "\n"
        return output
    
    def is_excluded(self,excluded_mechanics):
        return all(mechanic in excluded_mechanics for mechanic in self.mechanics)
    
    #def is_inside_catalog(self,catalog):
     #   if

    
class Catalog:
    def __init__(self):
        self.games = {}
    
    def add_game(self,new_game):
        self.games[new_game.name] = new_game
    
    def get_game(self,name_to_search):
        return self.games.get(name_to_search)
    
    def mechanic_names(self):
        output = []
        for game_name in self.games.keys():
            for mechanic in self.games[game_name].mechanics:
                if mechanic not in output:
                    output.append(mechanic)
        
        return output
       
    def count_games_per_mechanic(self,mechanic_to_count):
        output = 0
        for game_name in self.games.keys():
            if mechanic_to_count in self.games[game_name].mechanics:
                output = output + 1
                
        return output
    
    def count_mechanics_per_game(self,game_to_count):
        output = 0
        for mechanic in self.get_game(game_to_count).mechanics:
            output = output + 1
                
        return output
    
    def excluded_mechanics(self):
        output = []
        for game_name in self.games.keys():
            for mechanic in self.games[game_name].mechanics:
                if mechanic not in output:
                    ammount_of_games=self.count_games_per_mechanic(mechanic)
                    if ammount_of_games <= 5 or ammount_of_games > 40:
                        output.append(mechanic)
        
        return output
    
    def __repr__(self):
        return '\n'.join(str(new_game) for new_game in self.games.values())

class Categories:
    def __init__(self):
        self.all_categories = {}
        
    def add_category(self,category_name):
        if category_name not in self.all_categories:
            self.all_categories[category_name] = Catalog()
        else:
            print(f"La categoría {category_name} ya existe.")
    
    def erase_category(self,category_name):
        if category_name in self.all_categories:
            del self.all_categories[category_name]
        else:
            print(f"La categoría {category_name} no existe.")
        
    def add_game_in_category(self,category_name,games_list):
        for game in games_list:
            if category_name in self.all_categories:
                self.all_categories[category_name].add_game(game)
            else:
                print(f"La categoría {category_name} no existe. Añádela primero.")
                return
        
    def __repr__(self):
        output = "Categories Overview:\n"
        for category, catalog in self.all_categories.items():
            games_list = ', '.join(catalog.games.keys()) if catalog.games else "No games"
            output += f"- {category}: {games_list}\n"
        return output

def LoadCSV():
    output = Catalog()
    
    with open('games_information.csv', 'r') as file:
        csv_reader = csv.reader(file)       
        game_names = next(csv_reader)
        mechanics_for_each_game = next(csv_reader)
        
        for name, mechanics in zip(game_names,mechanics_for_each_game):
            if mechanics == '':
                mechanic_list = []
            else:
                mechanic_list = mechanics.split(';')
            new_game = Game(name,mechanic_list)
            
            output.add_game(new_game)
            
    return output

def ShowMechanics(catalog,categories=None):
    
    excluded_mechanics_list = catalog.excluded_mechanics()
    
    amount_of_excluded_mechanics = 0
    print("---------")
    for mechanic in catalog.mechanic_names():
        if mechanic not in excluded_mechanics_list:
            print("► "+mechanic)
            print("Contiene " + str(catalog.count_games_per_mechanic(mechanic))+" juegos \n")
        else:
            amount_of_excluded_mechanics = amount_of_excluded_mechanics + 1
            
    print("Se excluyeron "+str(amount_of_excluded_mechanics)+" mecanicas por contener menos de 10 juegos")
    print("---------")
    print("Los siguientes juegos no pertenecen a ninguna mecanica no excluida: ")
    for game_name in catalog.games:
        if catalog.get_game(game_name).is_excluded(excluded_mechanics_list):
            print(game_name)
    print("---------")
    
def ShowGames(catalog,categories=None):
    print("---------")
    for game_name in catalog.games.keys():
        print("► "+game_name)
        print("Contiene " + str(catalog.count_mechanics_per_game(game_name))+" mecanicas \n")
    print("---------")
    
def ShowCategories(catalog,categories):
    print("---------")
    for category in categories.all_categories.keys():
        print(category)
    

def ShowExcludedMechanics(catalog):
    print("---------")
    for mechanic in catalog.excluded_mechanics():
        print(mechanic)
    print("---------")
    return True, "mechanics"

def ShowStart(catalog = None,categories=None):
    os.system('cls')
    time.sleep(1)
    print("""\

          
 ██████╗ █████╗ ██████╗  █████╗ ██╗   ██╗ █████╗ ███╗   ██╗ █████╗ 
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔══██╗
██║     ███████║██████╔╝███████║██║   ██║███████║██╔██╗ ██║███████║
██║     ██╔══██║██╔══██╗██╔══██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██╔══██║
╚██████╗██║  ██║██║  ██║██║  ██║ ╚████╔╝ ██║  ██║██║ ╚████║██║  ██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝                                                                   
          """)
    
#Menu Handlers

def handle_exit(catalog=None,categories=None):
    return False, ""

def handle_switch_to_games(catalog=None):
    return True, "games"

def handle_switch_to_mechanics(catalog=None):
    return True, "mechanics"

def handle_switch_to_categories(catalog=None):
    return True, "categories"

def handle_switch_to_main_menu(catalog=None,categories=None):
    return True, "menu"

#


def generic_menu(catalog, categories,prompt, options, select):  
    print(prompt)
    for key, value in options.items():
        print(f"► Ingrese {key} para {value['desc']}")
    while True:
        selection = input()
        
        if selection in options.keys():
            action = options[selection]['func']
            if categories!= None:
                result = action(catalog,categories)
            else:
                result = action(catalog)
            input("Presione ENTER para continuar...")
            print("---------")
            return result
        elif selection == "":
            continue
        else:
            input("Presione ENTER para continuar...")
            print("---------")
            result = select(catalog,selection)
            input("Presione ENTER para continuar...")
            print("---------")
            return result
            

def MechanicMenu(catalog,categories=None):
    options = {
        "0": {"desc": "salir", "func": handle_exit},
        "1": {"desc": "volver al menu principal", "func": handle_switch_to_main_menu},
        "2": {"desc": "ver mecanicas excluidas", "func": lambda catalog: ShowExcludedMechanics(catalog)},
    }
    return generic_menu(catalog, None, "Qué mecanica quieres ver? Ingresa el nombre de la mecanica", options, lambda catalog,mechanic_to_search: SelectMechanicWithTheirGames(catalog,mechanic_to_search))

def GameMenu(catalog,categories=None):    
    options = {
        "0": {"desc": "salir", "func": handle_exit},
        "1": {"desc": "volver al menu principal", "func": handle_switch_to_main_menu},
    }
    
    return generic_menu(catalog, None, "Qué juego quieres ver? Ingresa el nombre del juego", options, lambda catalog,game_to_search: SelectGameWithTheirMechanics(catalog,game_to_search))

def Menu(catalog=None,categories=None):
    options = {
        "0": {"desc": "salir", "func": handle_exit},
        "1": {"desc": "TODO (ver inventario de categorias creadas)", "func": handle_switch_to_categories},
        "2": {"desc": "cambiar a juegos", "func": handle_switch_to_games},
        "3": {"desc": "cambiar a ver mecanicas", "func": handle_switch_to_mechanics},
        "4": {"desc": "agregar nuevo juego al sistema", "func": AddGameToFullDataBase},
    }
    return generic_menu(None, None, "Bienvenido al sistema de inventario de juegos, selecciona a donde quieres ir", options, select = None)

def CategoryMenu(catalog,categories):
    options = {
        "0": {"desc": "salir", "func": handle_exit},
        "1": {"desc": "volver al menu principal", "func": handle_switch_to_main_menu},
        "2": {"desc": "crear categoria", "func": lambda catalog,categories: CreateNewCategory(catalog,categories)},
    }
    return generic_menu(catalog,categories, "Qué categoría quieres ver? Ingresa el nombre de la categoría", options, select = None)

def AddGameToFullDataBase(catalog):
    input("Presione ENTER para continuar...")
    print("---------")
    
    print("Ingrese el nombre del juego que quiere agregar")
    new_game = input()
    #print("Extrayendo informacion de BGG...")
    
    if new_game == "":
        print("Ingresa un nombre valido")
    else:
        new_game_entry = search_game_online(new_game)
        if new_game_entry == "fail":
            print("Juego no encontrado")
        else:
            print("---------")
            print("Seguro que quieres agregar el juego: "+list(new_game_entry.keys())[0]+"?")
            print("Categorias:")
            print(new_game_entry[list(new_game_entry.keys())[0]]['Categorias'])
            print("1 para guardarlo")
            print("2 para continuar sin hacer cambios")
            is_save = input()
            
            if is_save == "1":
                SaveGame(save_file,new_game_entry)
            else:
                return True, "menu"
    
    return True, "menu"

def CreateNewCategory(catalog,categories):
    
    print("Cual seria el nombre de la categoria?")
    new_category_name = input()
    
    categories.add_category(new_category_name)
    
    #Continuar el proceso siempre y cuando el usuario quiera seguir agregando juegos      
        #Preguntar que juego quiere agregar
        #Revisar si el juego esta en el catlogo de juegos
        #Confirmar si ese es el juego que el usuario quiere agregar
        #Agregarlo al nuevo catalogo
        #Preguntar si quiere agregar mas juegos
    #Salir si el usuario ya no quiere agregar mas juegos
    #Agregar nombre y catalogo a la nueva categoria
    
    return True, "categories"

def SelectMechanicWithTheirGames(catalog,mechanic_to_search):
    
    close_match = get_close_matches(mechanic_to_search,catalog.mechanic_names())
    
    if len(close_match) >= 1:
        print(close_match[0])
        
        for game_name in catalog.games.keys():
            if close_match[0] in catalog.games[game_name].mechanics:
                print("► "+game_name)
            
    else:
        print("No se pudo encontrar la mecanica, revisar mayusculas y que se esta ingresando el nombre completo")
    
    return True, "mechanics"

            
def SelectGameWithTheirMechanics(catalog,game_to_search):
    excluded_mechanics_list = catalog.excluded_mechanics()
    
    close_match = get_close_matches(game_to_search,list(catalog.games.keys()))

    if len(close_match) >= 1:
        game = catalog.get_game(close_match[0])
        print(game.name)
        for mechanic in game.mechanics:
            if mechanic in excluded_mechanics_list:
                print("► EXCLUIDA "+mechanic)
            else:
                print("► "+ mechanic)
    else:
        print("No se pudo encontrar el juego, revisar mayusculas y que se esta ingresando el nombre completo")
    
    return True, "games"
            
def main():
    catalog = LoadCSV()  
    categories = Categories()
    mode = "menu"

    menu_functions = {
        "mechanics": MechanicMenu,
        "games": GameMenu,
        "menu": Menu,
        "categories": CategoryMenu
    }

    while True:
        catalog = LoadCSV()
        if mode == "menu":
            show_function = ShowStart
        if mode == "categories":
            show_function = ShowCategories
        elif mode == "mechanics":
            show_function = ShowMechanics
        elif mode == "games":
            show_function = ShowGames
        
        show_function(catalog,categories)
        continue_running, new_mode = menu_functions[mode](catalog,categories) 

        if not continue_running:
            break
        mode = new_mode

if __name__ == "__main__":
    main()