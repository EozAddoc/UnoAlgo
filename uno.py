import random
from IAm import make_decision,get_coloured_hands
# Card class
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    def __str__(self):# Voir la carte en tant que string
         return f"{self.color} {self.value}"
    def __repr__(self):
        return self.__str__()#pour la convertion objet string
    #carte=Carte("Vert","3")
# Deck class
class Deck:
    def __init__(self):
        self.colors = ["R", "B", "G", "Y"]
        self.values = ["0"] + [str(i) for i in range(1, 10)] + [">>", "<>", "+2"]
        self.cards = self._create_deck()
    def _create_deck(self):
        deck = []
        for color in self.colors:
            for value in self.values:
                deck.append(Card(color, value))
                deck.append(Card(color, value)) 
        for _ in range(4):
            deck.append(Card("W", "W"))
            deck.append(Card("W", "+4"))
        return deck
    def shuffle(self):
        random.shuffle(self.cards)
    def draw(self):
        return self.cards.pop() if self.cards else None
# DiscardPile class
class DiscardPile:
    def __init__(self, deck):
        self.top_card = self.draw_non_special_card(deck)
        self.pile = [self.top_card]
    def draw_non_special_card(self, deck):
        card = deck.draw()
        # Keep drawing cards until we get a non-special card
        while card in [">>", "<>", "+2", "W", "+4"]:
            card = deck.draw()
        return card
    def new_card(self, card):
        self.pile.append(card)
        self.top_card = card
# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    def draw(self, deck, count=1):
        for _ in range(count):
            card = deck.draw()
            if card:
                self.hand.append(card)
                return card
    def play(self, card, discard_pile):
        if card in self.hand:
            self.hand.remove(card)
            discard_pile.new_card(card)
            return card
        return None
    def valid_moves(self, top_card):
        return [card for card in self.hand if self.is_valid_move(card, top_card)]
    def is_valid_move(self, card, top_card):
        return (
            card.color == top_card.color or
            card.value == top_card.value or
            card.color == "W"
        )
# AIPlayer class
class AIPlayer(Player):
    def __init__(self, name, difficulty="easy"):
        super().__init__(name)
        self.difficulty = difficulty  
        self.turn_counter = 0 
        self.is_attacked =0
    def decide_move(self, top_card, is_attacked):
        valid_moves = self.valid_moves(top_card)
        if self.difficulty == "easy":
            return random.choice(valid_moves)
        elif self.difficulty == "medium":
            self.turn_counter += 1
            if self.turn_counter % 2 == 1:
                return random.choice(valid_moves)
            else:
                best_move = None
                make_decision(self.hand, is_attacked, top_card)
                return best_move
        elif self.difficulty == "hard":
            best_move =make_decision(self.hand, is_attacked, top_card)
            return best_move
# Gameplay Functions
def display_game_state(players, discard_pile, current_player):
    print(f"\nTop card: {discard_pile.top_card}")
    if not isinstance(current_player, AIPlayer): 
        for player in players:
            if isinstance(player, AIPlayer):  
                print(f"{player.name} has {len(player.hand)} cards.")
# Gameplay Functions
def handle_turn(player, discard_pile, deck, players, current_player_index, reverse_order, stacked,ai):
    print(f"Active stack: {stacked} cards." if stacked > 0 else "")
    #ai
    if isinstance(player, AIPlayer):
        ai = True
        move = player.decide_move(discard_pile.top_card, (stacked > 0) )
        print(move)
        if move and (stacked == 0 or move.value in ["+2", "+4"]):
            print(f"{player.name} plays {move}.")
            
            player.play(move, discard_pile)
            current_player_index, reverse_order, stacked = handle_special_cards(
                move, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai
            )
        else:
            print(f"{player.name} draws cards due to stack!")
            if stacked == 0:
                drawn = player.draw(deck)
                valid_moves = player.valid_moves(discard_pile.top_card)
                if drawn in valid_moves:
                    print(f"AI drew a valid card: {drawn}. AI plays it.")
                    player.play(drawn, discard_pile)
                    current_player_index, reverse_order, stacked = handle_special_cards(
                        drawn, players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
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
            drawn = player.draw(deck)
            valid_moves = player.valid_moves(discard_pile.top_card)
            if drawn in valid_moves:
                print(f"Your drawn card {drawn} is valid! Would you like to play it? (y/n)")
                play_choice = input().lower()
                if play_choice == "y":
                    player.play(drawn, discard_pile)
                    current_player_index, reverse_order, stacked = handle_special_cards(
                    drawn, players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
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
def handle_special_cards(card, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai):
    if card.value == ">>":  # Skip
        print(f"{card} played 'Skip'. Skipping next player's turn.")
        step = -1 if reverse_order else 1
        current_player_index = (current_player_index + step) % len(players)
    elif card.value == "<>": 
        if len(players) == 2:
            print(f"{card} played 'Skip'. Skipping next player's turn.")
            step = -1 if reverse_order else 1
            current_player_index = (current_player_index + step) % len(players)
        else:
            reverse_order = not reverse_order
            print(f"{card} played 'Reverse'. Turn order reversed.")
    elif card.value == "+2": 
        next_player = players[(current_player_index + (1 if not reverse_order else -1)) % len(players)]
        print(f" played '+2'")
        stacked += 2
    elif card.value == "+4":  
        next_player = players[(current_player_index + (1 if not reverse_order else -1)) % len(players)]
        stacked += 4
        print(stacked)
        choose_color(card, discard_pile,ai, players[current_player_index])
    elif card.color == "W":  
        choose_color(card, discard_pile,ai, players[current_player_index] )
    return current_player_index, reverse_order, stacked
def choose_color(card, discard_pile,ai, current_player):
    if ai:
        coloured_cards = get_coloured_hands(current_player.hand)
        num_all_colours = len(coloured_cards)
        pair = list(coloured_cards.items())
        max_index = 0
        for i in range(num_all_colours):
            if len(pair[max_index][1]) < len(pair[i][1]):
                max_index = i
        new_color = pair[max_index][0]
    else:
        new_color = input("Choose a color (R, B, G, Y): ").upper()
        while new_color not in ["R", "B", "G", "Y"]:
            print("Invalid color. Choose from R, B, G, Y.")
            new_color = input("Choose a color: ").upper()
    card.color = new_color
    discard_pile.new_card(card)
    print(f"Color changed to {new_color}.")
    
def choose_number_of_players():
    # Ask the user how many players and what type
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
    players = []
    name = input("Enter your name: ")
    players.append(Player(name))  
    ai_difficulty = input("Choose difficulty for AI 1 (easy, medium, hard): ").lower()
    ai_counter = 1
    for player_type in player_types:
        if player_type == 'ai':
            players.append(AIPlayer(f"AI {ai_counter}",difficulty=ai_difficulty))
            ai_counter += 1
        else:
            human_name = input(f"Enter name for human player: ")
            players.append(Player(human_name))
    
    return players
# Main gameplay loop
def play_game():
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
    ai= False
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
        current_player_index, reverse_order, stacked = handle_turn(current_player, discard_pile, deck, players, current_player_index, reverse_order, stacked,ai)
        if len(current_player.hand) == 0:
            print(f"{current_player.name} wins!")
            break
        step = -1 if reverse_order else 1
        current_player_index = (current_player_index + step) % len(players)
# Start the game
if __name__ == "__main__":
    play_game()