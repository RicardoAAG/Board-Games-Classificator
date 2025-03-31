import csv
import copy

def LoadCSV():
    output = {}
    
    with open('games_information.csv', 'r') as file:
        csv_reader = csv.reader(file)
        
        csv_reader
        
        games = next(csv_reader)
        categories = next(csv_reader)
        
        for game, category in zip(games,categories):
            if category == '':
                category_list = []
            else:
                category_list = category.split(';')
            output[game] = {'Categorias': category_list}
            
    return output

def ExtractCategories():
    output = []
    
    for game in categories_by_games.keys():
        for category in categories_by_games[game]['Categorias']:
            if category not in output:
                output.append(category)
    
    return output

def ShowMorePerSelected(mode,selected,excluded):
    if mode == "categories":
        for game in categories_by_games.keys():
            if selected_category in categories_by_games[game]['Categorias']:
                print(game)
    if mode == "games":
        for category in categories_by_games[selected]['Categorias']:
            if category in excluded:
                print("EXCLUIDA "+category)
            else:
                print(category)
        
def ShowAllAndCountPerSelected(mode,excluded_categories):
    
    if mode == "categories":
        small_categories = []
        small_categorie_count = 0
        total_games = 0
        
        for category in categories:
            total_games = 0
            for game in categories_by_games.keys():
                if category in categories_by_games[game]['Categorias']:
                    total_games=total_games+1
            
            small_categories,small_categorie_count = DefineExcludedCategories(total_games,category,small_categories,small_categorie_count)
        
        CountExcludedGames(small_categories)
        print("Se excluyeron "+str(small_categorie_count)+" categorias por contener menos de 5 juegos \n")
        return small_categories
            
            
    if mode == "games":
        total_categories = 0
        
        for game in categories_by_games.keys():
            total_categories = 0
            for category in categories_by_games[game]['Categorias']:
                total_categories=total_categories+1
                
            print("► "+game)
            print("Contiene "+str(total_categories)+" categorias \n")
   
def DefineExcludedCategories(games_per_category, category_being_checked, list_of_excluded_categories, count):
    if games_per_category > 15:
        print("► "+category_being_checked)
        print("Contiene "+str(games_per_category)+" juegos \n")
    else:
        list_of_excluded_categories.append(category_being_checked)
        count = count + 1
        
    return list_of_excluded_categories, count

def CountExcludedGames(excluded_categories):
    
    check_copy = copy.deepcopy(categories_by_games)
    
    print("Estos juegos no se encuentran en ninguna categoria no excluida: ")
    for game in categories_by_games.keys():
        for excluded in excluded_categories:
            if excluded in categories_by_games[game]['Categorias']:
                check_copy[game]['Categorias'].remove(excluded)
        if len(check_copy[game]['Categorias']) == 0:
            print("► "+game)

categories_by_games = LoadCSV()
categories = ExtractCategories()
run=True
mode="categories"

while(run):
    while(mode=="categories"):
        
        small_categories = ShowAllAndCountPerSelected(mode,[])
        
        print("Que categoria quieres ver? Ingresa el nombre de la categoria")
        print("► Ingrese 0 para salir")
        print("► Ingresa 1 para cambiar a ver los juegos")
        print("► Ingresa 2 para ver las categorias excluidas")
        selected_category=input()
        print("---------")
        
        if selected_category=="2":
            for category in small_categories:
                print(category)
        if selected_category == "0":
            run=False
            break
        if selected_category == "1":
            mode="games"
        elif selected_category != "":
            ShowMorePerSelected(mode,selected_category,[])
        
        input("Presione ENTER para continuar...")
        print("---------")
    while(mode=="games"):
        
        ShowAllAndCountPerSelected(mode,small_categories)
        
        print("Que juego quieres ver? Ingresa el nombre del juego")
        print("► Ingrese 0 para salir")
        print("► Ingresa 1 para cambiar a ver categorias")
        selected_game=input()
        print("---------")
        
        if selected_game == "0":
            run=False
            break
        if selected_game == "1":
            mode="categories"
        elif selected_game != "" and selected_game in categories_by_games.keys():
            ShowMorePerSelected(mode,selected_game,small_categories)
        
        input("Presione ENTER para continuar...")
        print("---------")  