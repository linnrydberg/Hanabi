#create game (deck, antal spelare)
#reset game 
from player import PlayerPlayer, NaivePlayer
from deck import Deck
import event
from action import PlayAction, ClueAction, ThrowAction
from board import Board
from matplotlib import pyplot as plt

#SETTINGS
players = [NaivePlayer() for i in range(4)]


def nice_print(log): 
    for log_event in log:
        print(log_event)

def mask_log(log, player_idx):
    re_log = []
    for log_event in log:
        if isinstance(log_event,event.PlayEvent) and log_event.player_idx == player_idx:
            re_log.append(event.PlayEvent(log_event.player_idx,log_event.card_idx,log_event.card_played,(None, None)))
        elif isinstance(log_event,event.ThrowEvent) and log_event.player_idx == player_idx:
            re_log.append(event.ThrowEvent(log_event.player_idx,log_event.card_idx,log_event.card_thrown,(None, None)))
        elif isinstance(log_event,event.DrawEvent) and log_event.player_idx == player_idx:
            re_log.append(event.DrawEvent(log_event.player_idx,(None,None)))
        
        elif isinstance(log_event,event.ClueEvent) and log_event.clued_player_idx == player_idx:
            clued_hand = log_event.clued_hand
            clue = log_event.clue
            masked_hand = []
            for card in clued_hand: 
                (col, num) = card 
                if col == clue[0]: 
                    masked_hand.append((col,None))
                elif num == clue[1]: 
                    masked_hand.append((None, num))
                else: 
                    masked_hand.append((None, None))
            re_log.append(event.ClueEvent(log_event.player_idx, log_event.clued_player_idx, log_event.clue, masked_hand))
        else:
            re_log.append(log_event)
    return re_log


nbr_of_players = len(players) 

hand_sizes = {
    2 : 5, 
    3: 5,  
    4:4, 
    5: 4
}
hand_size = hand_sizes[nbr_of_players]


print_out = False
results = []

for _ in range(1000): 
    deck = Deck()
    log = []
    # Draw initial cards
    for _ in range(hand_size):
        for player_idx in range(nbr_of_players):
            log.append(event.DrawEvent(player_idx, deck.pull()))
            #board.add_event_to_log(log[-1])

    board = Board(log)
    game_on = True
    active_player_idx = 0 
    rounds_left = -1
    while game_on and rounds_left != 0 and board.get_lives_left() > 0:
        action = players[active_player_idx].make_move(mask_log(log, active_player_idx))
        if rounds_left > 0: 
            rounds_left = rounds_left -1 
            
        if isinstance(action, ClueAction):
            if board.get_clues_left() <= 0: 
                raise Exception("Invalid clue")
            
            else: 
                clued_player = action.player_idx
                clued_hand = board.get_hand(clued_player)
                log.append(event.ClueEvent(active_player_idx, clued_player, action.clue, clued_hand))  

        elif isinstance(action, PlayAction): 
            log.append(event.PlayEvent(active_player_idx, action.card_idx, board.get_card(active_player_idx, action.card_idx), deck.pull()))
        
        
        elif isinstance(action, ThrowAction): 
            log.append(event.ThrowEvent(active_player_idx, action.card_idx, board.get_card(active_player_idx, action.card_idx), deck.pull()))

        if deck.size() == 0 and rounds_left == -1: 
            rounds_left = nbr_of_players

        #board.add_event_to_log(log[-1])
        active_player_idx = (active_player_idx +1)%nbr_of_players

    if print_out: 
        nice_print(log)
        print("__________________________")
        print("Game over!")
        print(board.get_highest_cards())
        print(f"Clues left: {board.get_clues_left()}")
        print(f"Lives left: {board.get_lives_left()}" )
        print(f"Decksize : {deck.size()}" )
    
    sum = 0
    for key in board.get_highest_cards(): 
        sum += board.get_highest_cards()[key]
    results.append(sum)

tot = 0 
for item in results:
    tot += item

print(tot/len(results))
plt.hist(results)
    

    




        


