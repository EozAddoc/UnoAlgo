def can_play (current_card, card):
    # vérifie si une carte peut être jouer:
    # si ils partagent la même colore, la même value, ou si la carte que l'on veut jouer est une carte wild
    # retourne True si peut jouer, False sinon
    if (card.color == current_card.color) or (card.value == current_card.value) or (card.color == "W"):
        return True
    else:
        return False

def get_playable_cards (hand:list, current_card: str)-> list:
    playable_cards = []
    
    # Itère sur chaque carte de la main et vérifie si elle peut être jouer,
    # Alors elle est ajouté à la liste 'playable_cards'
    for card in hand:
        if can_play(current_card,card):
            playable_cards.append(card)
    return playable_cards

def get_connections (hand:list) -> dict:
    # key: each card with a connnection, element: list of all cards connected to the key
    # Trouve toutes les connections des nombres entre les cartes
    connections = {}
    for card in hand:
        for card2 in hand:
            if card != card2 and (card.value==card2.value or card.color == "W" or card2.color == "W"):
                if card in connections:
                    connections[card].append(card2)
            else:
                connections[card] = [card2]
    
    return connections

def get_coloured_hands (hand:list) -> dict:
    # key: colour of the cards, element: list of all the cards of that colour
    coloured_cards = {}
    for card in hand:
        if card.color in coloured_cards:
            coloured_cards[card.color].append(card)
        else:
            coloured_cards[card.color] = [card]
    
    return coloured_cards

def get_scored_cards( connections, playable_cards, current_card) -> dict:
    # note chaque carte et l'ajoute dans un dictionnaire:
    # key: card , value: score
    # comment on calcule le score:
    avoid_scores = {}
    
    for card in playable_cards:
        score = 0
        # on -1 si c'est c'es la même couleur que la carte de la pioche
        if card.color == current_card.color:
            score -= 1
        # on ajoute au score le nombre de connection que la carte a
        score += len(connections[card])
        
        if card.value in [">>", "<>", "+2"]:
            score +=0.5
        
        # si la carte est un + on ajoute 1 au score
        if "+" in card.value:
            score += 1
        
        avoid_scores[card] = score
    
    return avoid_scores
# On peut ajouter d'autre règle, pour l'instant c'est juste ça


def make_decision(hand:list, is_attacked:bool, current_card:str):
    cards_in_hand = hand #récupère la main de l'IA
    print("in make decisions", cards_in_hand, is_attacked)
    #cards_in_hand.sort()
    
    # récupère les colors unique de la main
    first_character_of_hand = set()
    for card in cards_in_hand:
        first_character_of_hand.add(card.color)
    
    # récupère les cartes qui sont liées à chaque cartes par sa value (ou toutes si c'est une wild card)
    # c'est un dictionaire (key: carte, value: liste de carte connecté)
    connections = get_connections(cards_in_hand)
    # récupère les cartes qui peuvent être jouées, liste
    playable_cards = get_playable_cards(cards_in_hand, current_card)

    # récupère les cartes qui appartiennent à une certaine color
    # dictionaire: clef = colore, élément = liste de carte de la color
    coloured_cards = get_coloured_hands(cards_in_hand)

    # si aucune carte ne peut être jouer on pioche
    if len(playable_cards) == 0:
        return None
    # Si on est attacké, et que l'on a une carte +, on joue la carte +
    elif is_attacked and any( "+" in card.value for card in playable_cards):
        return next(card for card in playable_cards if "+" in card.value)
    # Si on ne peut jouer qu'une seule carte, on joue la carte
    elif len(playable_cards) == 1:
        return playable_cards[0]
    # Sinon calculer la value de chaque carte, et jouer celle qui a le moins de value
    else:
        attractiveness = get_scored_cards(connections, playable_cards, current_card)
        selected_card = min(attractiveness, key= attractiveness.get)
        return selected_card
    