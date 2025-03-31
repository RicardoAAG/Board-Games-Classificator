import csv

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


catalog = LoadCSV()

juegos_por_categoria = {
    "Estrategia de Guerra y Militar": [

    ],
    "Gestión de Recursos, Mercado y Economía": [

    ],
    "Optimización y Simulación": [

    ],
    "Patrones y Reconocimiento": [

    ],
    "Conflicto Directo y Competitivos": [

    ],
    "Control del Azar": [

    ],
    "Manipulación, Engaño y Comunicación": [

    ],
    "Expansión y Desarrollo de Civilizaciones": [

    ]
}


mecanicas_por_categoria = {
    "Estrategia de Guerra y Militar": [
        ("Action Points", 0.7),
        ("Area Majority / Influence", 1),
        ("Player Elimination", 0.9),
        ("Action Queue", 0.8),
        ("Zone of Control", 1),
        ("Secret Unit Deployment", 0.9),
        ("Hidden Movement", 0.8),
        ("Conflict Resolution (Card Play, Dice Rolling)", 0.9),
        ("Tech Trees / Tech Tracks", 0.7),
        ("Campaign / Battle Card Driven", 1),
        ("Area Movement", 0.9),
        ("Command Cards", 0.9),
        ("Turn Order: Stat-Based", 0.7),
        ("Turn Order: Progressive", 0.7),
        ("Modular Board", 0.7),
        ("Variable Player Powers", 0.7),
        ("Pick-up and Deliver", 0.7),
        ("Rondel", 0.7)
    ],
    "Gestión de Recursos, Mercado y Economía": [
        ("Worker Placement", 1),
        ("Auction/Bidding", 0.9),
        ("Contracts", 1),
        ("Trading", 1),
        ("Income", 0.8),
        ("Deck, Bag, and Pool Building", 0.7),
        ("Set Collection", 0.8),
        ("Commodity Speculation", 1),
        ("Investment", 0.9),
        ("Loans", 0.7),
        ("Resource to Move", 0.8),
        ("Market", 1),
        ("Hidden Roles", 0.6),
        ("Variable Set-up", 0.7),
        ("Tech Trees / Tech Tracks", 0.7),
        ("Modular Board", 0.7),
        ("Auction: Dutch", 0.8),
        ("Auction: English", 0.8),
        ("Auction: Sealed Bid", 0.8),
        ("Bingo", 0.6)
    ],
    "Optimización y Simulación": [
        ("Action Points", 0.9),
        ("Modular Board", 0.8),
        ("Tile Placement", 1),
        ("Grid Movement", 0.8),
        ("Simulation", 1),
        ("Tech Trees / Tech Tracks", 1),
        ("Automatic Resource Growth", 0.8),
        ("Variable Set-up", 0.7),
        ("Scenario / Mission / Campaign Game", 0.8),
        ("Pattern Building", 0.8),
        ("Action Timer", 0.7),
        ("Worker Placement, Different Worker Types", 0.8),
        ("Pick-up and Deliver", 0.7),
        ("Network and Route Building", 0.7),
        ("Victory Points as a Resource", 0.8),
        ("Track Movement", 0.8),
        ("Turn Order: Time Track", 0.7)
    ],
    "Patrones y Reconocimiento": [
        ("Pattern Recognition", 1),
        ("Pattern Building", 1),
        ("Tile Placement", 0.8),
        ("Set Collection", 0.7),
        ("Grid Movement", 0.8),
        ("Melding and Splaying", 0.8),
        ("Matching", 0.9),
        ("Pattern Movement", 1),
        ("Hexagon Grid", 0.9),
        ("Memory", 0.7),
        ("Line Drawing", 0.9),
        ("Speed Matching", 0.9),
        ("Pattern Recognition", 1)
    ],
    "Conflicto Directo y Competitivos": [
        ("Player Elimination", 1),
        ("Take That", 1),
        ("Action Points", 0.7),
        ("Auction/Bidding", 0.7),
        ("Betting and Bluffing", 0.9),
        ("Programmed Movement", 0.8),
        ("Role Playing", 0.7),
        ("Conflict Resolution (Card Play, Dice Rolling)", 1),
        ("King of the Hill", 1),
        ("Kill Steal", 0.9),
        ("Race", 0.8),
        ("Trick-taking", 0.7),
        ("Rondel", 0.6),
        ("Negotiation", 0.7),
        ("Turn Order: Auction", 0.8),
        ("Bribery", 0.8)
    ],
    "Control del Azar": [
        ("Dice Rolling", 1),
        ("Push Your Luck", 1),
        ("Re-rolling and Locking", 1),
        ("Random Production", 0.9),
        ("Victory Points as a Resource", 0.7),
        ("Hot Potato", 0.9),
        ("Roll / Spin and Move", 1),
        ("Predictive Bid", 0.8),
        ("Take That", 0.7),
        ("Catch the Leader", 0.9),
        ("Bingo", 0.8),
        ("Layering", 0.6),
        ("Die Icon Resolution", 0.9)
    ],
    "Manipulación, Engaño y Comunicación": [
        ("Hidden Roles", 1),
        ("Betting and Bluffing", 1),
        ("Traitor Game", 1),
        ("Roles with Asymmetric Information", 1),
        ("Bribery", 0.9),
        ("Negotiation", 1),
        ("Voting", 0.8),
        ("Player Judge", 1),
        ("Simultaneous Action Selection", 0.9),
        ("Alliances", 0.8),
        ("Semi-Cooperative Game", 0.9),
        ("Deduction", 0.9),
        ("Targeted Clues", 0.8),
        ("Tug of War", 0.6),
        ("Communication Limits", 0.9),
        ("Simultaneous Action Selection", 0.9),
        ("Follow", 0.8),
        ("Hidden Movement", 0.8)
    ],
    "Expansión y Desarrollo de Civilizaciones": [
        ("Worker Placement", 1),
        ("Tech Trees / Tech Tracks", 1),
        ("Tile Placement", 0.8),
        ("Area Majority / Influence", 0.9),
        ("Deck, Bag, and Pool Building", 0.9),
        ("Resource to Move", 0.9),
        ("Pick-up and Deliver", 0.7),
        ("Variable Set-up", 0.8),
        ("Income", 0.9),
        ("Automatic Resource Growth", 1),
        ("Modular Board", 0.7),
        ("Map Addition", 0.8),
        ("Contracts", 0.8),
        ("Auction/Bidding", 0.7),
        ("Victory Points as a Resource", 0.7),
        ("Market", 0.9)
    ]
}



for game in catalog.games.values():  
    for category in mecanicas_por_categoria.keys():
        peso_total = 0  

        for game_mechanic in game.mechanics:
            for category_mechanic, valor in mecanicas_por_categoria[category]:
                if game_mechanic == category_mechanic:
                    peso_total += valor

        if peso_total > 0:
            juegos_por_categoria[category].append((game.name, peso_total))
            
with open('prueba_de_pesos.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Categoría", "Juego", "Peso"])
    
    for category, games in juegos_por_categoria.items():
        for game, peso in games:
            writer.writerow([category, game, peso])
                