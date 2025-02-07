import random
from IAm import make_decision, get_coloured_hands

# Card class
class Card:#4
    """
    Représente une carte du jeu avec une couleur et une valeur.
    """
    def __init__(self, color, value): #2
        """
        Initialise une carte avec sa couleur et sa valeur.

        Parameters:
        color (str): La couleur de la carte (R, B, G, Y, W).
        value (str): La valeur de la carte (par exemple: 0, 1, 2, +2, +4, etc.).
        """
        self.color = color
        self.value = value

    def __str__(self):#1
        """
        Retourne une chaîne de caractères représentant la carte.
        """
        return f"{self.color} {self.value}"

    def __repr__(self):#1
        """
        Utilisé pour la conversion de l'objet en chaîne de caractères pour les représentations en liste ou debug.
        """
        return self.__str__()

# Deck class
class Deck:#8 + 2n + 2n**2
    """
    Représente un jeu de cartes complet.
    """
    def __init__(self):#3
        """
        Initialise le jeu de cartes avec les couleurs et valeurs possibles et crée le deck.
        """
        self.colors = ["R", "B", "G", "Y"]  # Couleurs des cartes
        self.values = ["0"] + [str(i) for i in range(1, 10)] + [">>", "<>", "+2"]  # Valeurs des cartes
        self.cards = self._create_deck()  # Création du deck

    def _create_deck(self):#2n**2 + 2n +2
        """
        Crée le deck de cartes en fonction des couleurs et des valeurs définies.

        Returns:
        list: Liste contenant toutes les cartes du deck.
        """
        deck = []
        for color in self.colors:#2n**2
            for value in self.values:
                deck.append(Card(color, value))
                deck.append(Card(color, value))  # Chaque carte apparaît 2 fois
        for _ in range(4):#2n
            deck.append(Card("W", "W"))  # Cartes "Wild"
            deck.append(Card("W", "+4"))  # Cartes "Wild +4"
        return deck

    def shuffle(self):#1
        """
        Mélange le deck de cartes.
        """
        random.shuffle(self.cards)

    def draw(self):#2
        """
        Pioche une carte du deck.

        Returns:
        Card or None: Une carte piochée, ou None si le deck est vide.
        """
        return self.cards.pop() if self.cards else None

# DiscardPile class
class DiscardPile:#2n +7
    """
    Représente la pile de défausse, qui contient la carte du dessus.
    """
    def __init__(self, deck): # n+3
        """
        Initialise la pile de défausse avec une carte non spéciale tirée du deck.

        Parameters:
        deck (Deck): Le deck utilisé pour tirer la première carte.
        """
        self.top_card = self.draw_non_special_card(deck)
        self.pile = [self.top_card]  # La pile commence avec la carte du dessus

    def draw_non_special_card(self, deck):#n+2
        """
        Pioche une carte du deck jusqu'à ce que ce ne soit pas une carte spéciale.

        Parameters:
        deck (Deck): Le deck duquel tirer les cartes.

        Returns:
        Card: Une carte non spéciale.
        """
        card = deck.draw()
        while card.value in [">>", "<>", "+2", "W", "+4"]:
            card = deck.draw()
        return card

    def new_card(self, card):#2
        """
        Ajoute une nouvelle carte à la pile de défausse et met à jour la carte du dessus.

        Parameters:
        card (Card): La carte à ajouter à la pile de défausse.
        """
        self.pile.append(card)
        self.top_card = card

# Player class
class Player:
    """
    Représente un joueur humain dans le jeu.
    """
    def __init__(self, name):#2
        """
        Initialise un joueur avec un nom et une main vide.

        Parameters:
        name (str): Le nom du joueur.
        """
        self.name = name
        self.hand = []  # La main du joueur

    def draw(self, deck, count=1):#3n
        """
        Pioche une ou plusieurs cartes du deck et les ajoute à la main du joueur.

        Parameters:
        deck (Deck): Le deck duquel piocher.
        count (int): Le nombre de cartes à piocher.
        """
        for _ in range(count):
            card = deck.draw()
            if card:
                self.hand.append(card)

    def play(self, card, discard_pile):#5
        """
        Permet au joueur de jouer une carte depuis sa main.

        Parameters:
        card (Card): La carte à jouer.
        discard_pile (DiscardPile): La pile de défausse où la carte sera ajoutée.

        Returns:
        Card or None: La carte jouée si elle est valide, sinon None.
        """
        if card in self.hand:
            self.hand.remove(card)
            discard_pile.new_card(card)
            return card
        return None

    def valid_moves(self, top_card):#n +1
        """
        Retourne une liste des cartes valides que le joueur peut jouer.

        Parameters:
        top_card (Card): La carte du dessus de la pile de défausse.

        Returns:
        list: Liste des cartes valides que le joueur peut jouer.
        """
        return [card for card in self.hand if self.is_valid_move(card, top_card)]

    def is_valid_move(self, card, top_card):#2
        """
        Vérifie si une carte peut être jouée sur la carte du dessus de la pile de défausse.

        Parameters:
        card (Card): La carte à tester.
        top_card (Card): La carte du dessus de la pile de défausse.

        Returns:
        bool: True si la carte est valide, sinon False.
        """
        return (
            card.color == top_card.color or
            card.value == top_card.value or
            card.color == "W"
        )

# AIPlayer class
class AIPlayer(Player):
    """
    Représente un joueur contrôlé par l'IA.
    """
    def __init__(self, name, difficulty="easy"):#4
        """
        Initialise un joueur IA avec un nom, une main et une difficulté.

        Parameters:
        name (str): Le nom de l'IA.
        difficulty (str): La difficulté de l'IA ("easy", "medium", "hard").
        """
        super().__init__(name)
        self.difficulty = difficulty
        self.turn_counter = 0
        self.is_attacked = 0

    def decide_move(self, top_card, is_attacked):#15 + n
        """
        Permet à l'IA de décider quelle carte jouer.

        Parameters:
        top_card (Card): La carte du dessus de la pile de défausse.
        is_attacked (bool): Si l'IA a été attaquée par une carte spéciale.

        Returns:
        Card or None: La carte choisie par l'IA, ou None si elle doit piocher.
        """
        valid_moves = self.valid_moves(top_card) #n+1
        if not valid_moves:
            return None
        if self.difficulty == "easy":
            return random.choice(valid_moves)
        elif self.difficulty == "medium":
            self.turn_counter += 1
            if self.turn_counter % 2 == 1:
                return random.choice(valid_moves)
            else:
                return make_decision(self.hand, is_attacked, top_card)
        elif self.difficulty == "hard":
            print("in hard mode")
            return make_decision(self.hand, is_attacked, top_card)
        return None

# Gameplay Functions
def display_game_state(players, discard_pile, current_player):
    """
    Affiche l'état actuel du jeu, y compris la carte du dessus de la pile de défausse et les mains des joueurs.

    Parameters:
    players (list): Liste des joueurs.
    discard_pile (DiscardPile): La pile de défausse.
    current_player (Player): Le joueur dont c'est le tour.
    """
    print(f"\nTop card: {discard_pile.top_card}")
    if not isinstance(current_player, AIPlayer): 
        for player in players:
            if isinstance(player, AIPlayer):  
                print(f"{player.name} has {len(player.hand)} cards.")

def handle_turn(player, discard_pile, deck, players, current_player_index, reverse_order, stacked, ai):
    """
    Gère le tour d'un joueur, en fonction de si c'est un joueur humain ou IA.

    Parameters:
    player (Player): Le joueur dont c'est le tour.
    discard_pile (DiscardPile): La pile de défausse.
    deck (Deck): Le deck de cartes.
    players (list): Liste des joueurs.
    current_player_index (int): L'index du joueur actuel dans la liste.
    reverse_order (bool): Indique si l'ordre des tours est inversé.
    stacked (int): Le nombre de cartes empilées à jouer.
    ai (bool): Si le joueur actuel est une IA.

    Returns:
    tuple: L'index du prochain joueur, l'état de l'ordre des tours, et le nombre de cartes empilées.
    """
   
    print(f"Active stack: {stacked} cards." if stacked > 0 else "")
    #ai
    if isinstance(player, AIPlayer):
        ai = True
        move = player.decide_move(discard_pile.top_card, (stacked > 0) )
        if move and (stacked == 0 or move.value in ["+2", "+4"]):
            print(f"{player.name} plays {move}.")
            
            player.play(move, discard_pile)
            current_player_index, reverse_order, stacked = handle_special_cards(
                move, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai
            )
        else:
            print(f"{player.name} draws cards due to stack!")
            if stacked == 0:
                player.draw(deck)
                valid_moves = player.valid_moves(discard_pile.top_card)
                if player.hand[-1] in valid_moves:
                    print(f"AI drew a valid card: {player.hand[-1]}. AI plays it.")
                    player.play(player.hand[-1], discard_pile)
                    current_player_index, reverse_order, stacked = handle_special_cards(
                        player.hand[-1], players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
                    )
            for _ in range(stacked):
                player.draw(deck)
            stacked = 0 
     #human       
    else:
        if stacked > 0:
            print(f"A stack of {stacked} cards must be resolved.")
            print("Your options: Play another +2 or +4 to add to the stack, or type 'draw'.")
        
        print(f"Your hand: {', '.join(str(card) for card in player.hand)}")
        valid_moves = player.valid_moves(discard_pile.top_card)
        print("Valid moves: " + ", ".join(str(card) for card in valid_moves) + " or 'draw'.")
        choice = input("Choose a card or type 'draw': ")
        parts = choice.split()
        parts.append("")
        
        if stacked > 0 and parts[1] not in ["+2", "+4"]:
            print(f"You draw {stacked} cards due to the stack!")
            for _ in range(stacked):
                player.draw(deck)
            stacked = 0  
        elif choice == "draw":
            player.draw(deck)
            valid_moves = player.valid_moves(discard_pile.top_card)
            if player.hand[-1] in valid_moves:
                print(f"Your drawn card {player.hand[-1]} is valid! Would you like to play it? (y/n)")
                play_choice = input().lower()
                if play_choice == "y":
                    player.play(player.hand[-1], discard_pile)
                    current_player_index, reverse_order, stacked = handle_special_cards(
                    player.hand[-1], players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
                )
                    print(stacked, "after drawn")
                else:
                    print("You chose not to play the drawn card.")
        else:
            card = next((card for card in valid_moves if str(card) == choice), None)
            if card:
                player.play(card, discard_pile)
                current_player_index, reverse_order, stacked = handle_special_cards(
                    card, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai
                )
            else:
                print("Invalid choice. Try again.")
                current_player_index, reverse_order, stacked = handle_turn(player, discard_pile, deck, players, current_player_index, reverse_order, stacked,ai)
    return current_player_index, reverse_order, stacked


def handle_special_cards(card, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai): #54 +8n
    if card.value == ">>":  # Skip
        print(f"{ players[current_player_index].name} played 'Skip'. Skipping next player's turn.")
        step = -1 if reverse_order else 1
        current_player_index = (current_player_index + step) % len(players)
    elif card.value == "<>": 
        if len(players) == 2:
            print(f"{players[current_player_index].name} played 'Skip'. Skipping next player's turn.")
            step = -1 if reverse_order else 1
            current_player_index = (current_player_index + step) % len(players)
        else:
            reverse_order = not reverse_order
            print(f"{players[current_player_index].name} played 'Reverse'. Turn order reversed.")
    elif card.value == "+2": 
        next_player = players[(current_player_index + (1 if not reverse_order else -1)) % len(players)]
        print(f" {players[current_player_index].name} played '+2'")
        stacked += 2
    elif card.value == "+4":  
        next_player = players[(current_player_index + (1 if not reverse_order else -1)) % len(players)]
        print(f" {players[current_player_index].name} played '+4'")
        stacked += 4
        print(stacked)
        choose_color(card, discard_pile,ai, players[current_player_index])
    elif card.color == "W":  
        print("played W")
        choose_color(card, discard_pile,ai, players[current_player_index] )
    return current_player_index, reverse_order, stacked

def choose_color(card, discard_pile, ai, current_player):#16 + 4n 
    """
    Permet de choisir la couleur d'une carte 'Wild' ou '+4'. Si c'est un joueur IA, la couleur sera choisie automatiquement.

    Parameters:
    card (Card): La carte 'Wild' ou '+4' qui nécessite un changement de couleur.
    discard_pile (DiscardPile): La pile de défausse à mettre à jour avec la nouvelle couleur.
    ai (bool): Indique si le joueur actuel est une IA.
    current_player (Player): Le joueur qui joue la carte et doit choisir la couleur.
    
    Returns:
    None: Modifie directement l'objet `card` en fonction de la couleur choisie et met à jour la pile de défausse.
    """
    print("in choose color",current_player.name)
    new_color="Y"
    if isinstance(current_player, AIPlayer):
        if(current_player.difficulty =="hard"):
            coloured_cards = get_coloured_hands(current_player.hand)
            num_all_colours = len(coloured_cards)
            pair = list(coloured_cards.items())
            max_index = 0
            for i in range(num_all_colours):#2n
                if len(pair[max_index][1]) < len(pair[i][1]):
                    max_index = i
            new_color = pair[max_index][0]
            print("AI chose", new_color)
    else:
        new_color = input("Choose a color (R, B, G, Y): ").upper()
        while new_color not in ["R", "B", "G", "Y"]:#2n
            print("Invalid color. Choose from R, B, G, Y.")
            new_color = input("Choose a color: ").upper()
    if new_color not in ["R", "B", "G", "Y"]:
        new_color="Y"
    card.color = new_color
    discard_pile.new_card(card)
    print(f"{current_player.name} Color changed to {new_color}.")

    
def choose_number_of_players():
    """
    Demande à l'utilisateur combien de joueurs participeront à la partie, et quel type de joueur (humain ou IA) pour chaque joueur.

    Returns:
    list: Liste contenant les types des joueurs (ex: ['human', 'ai', 'human', 'ai']).
    """
    while True:
        try:
            num_players = int(input("How many players do you want to play with (1-4)? "))
            if 1 <= num_players <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    player_types = []
    for i in range(num_players):
        while True:
            player_type = input(f"Player {i+1}: Do you want this player to be 'human' or 'ai'? ").lower()
            if player_type in ['human', 'ai']:
                player_types.append(player_type)
                break
            else:
                print("Invalid choice. Please choose 'human' or 'ai'.")
    
    return player_types

def create_players(player_types):
    """
    Crée la liste des joueurs, en demandant à l'utilisateur de nommer les joueurs humains et de définir la difficulté des IA.

    Parameters:
    player_types (list): Liste des types de joueurs ('human' ou 'ai').

    Returns:
    list: Liste d'objets `Player` et `AIPlayer` pour représenter tous les joueurs dans la partie.
    """
    players = []
    name = input("Enter your name: ")
    players.append(Player(name))  
    ai_difficulty = input("Choose difficulty for AI 1 (easy, medium, hard): ").lower()
    ai_counter = 1
    for player_type in player_types:
        if player_type == 'ai':
            players.append(AIPlayer(f"AI {ai_counter}", difficulty=ai_difficulty))
            ai_counter += 1
        else:
            human_name = input(f"Enter name for human player: ")
            players.append(Player(human_name))
    
    return players


# Main gameplay loop
def play_game():
    """
    Démarre et gère la boucle principale du jeu.
    """
    player_types = choose_number_of_players()
    players = create_players(player_types)
    deck = Deck()
    deck.shuffle()
    discard_pile = DiscardPile(deck)

    for _ in range(7):
        for player in players:
            player.draw(deck)

    current_player_index = 0
    reverse_order = False
    stacked = 0
    ai = False

    while True:
        current_player = players[current_player_index]
        display_game_state(players, discard_pile, current_player)
        if len(current_player.hand) == 1:  
            if isinstance(current_player, AIPlayer):
                print(f"{current_player.name} calls UNO.")
            else:
                uno = input("You have one card left! Type 'UNO' to call it: ").lower()
                if uno != 'uno':
                    print(f"{current_player.name} didn't call 'UNO'! You draw 2 penalty cards.")
                    current_player.draw(deck, 2)  

        # Vérification si un joueur a gagné
        if len(current_player.hand) == 0:
            print(f"{current_player.name} wins!")
            break

        # Gestion du tour du joueur actuel
        current_player_index, reverse_order, stacked = handle_turn(
            current_player, discard_pile, deck, players, current_player_index, reverse_order, stacked, ai
        )
        
        # Passage au joueur suivant en fonction de l'ordre
        step = -1 if reverse_order else 1
        current_player_index = (current_player_index + step) % len(players)

# Start the game
if __name__ == "__main__":
    play_game()
