#create game (deck, antal spelare)
#reset game 
from player import PlayerPlayer
from deck import Deck
import event

nbr_of_players = 4 

hand_sizes = {
    2 : 5, 
    3: 5,  
    4:4, 
    5: 4
}
hand_size = hand_sizes[nbr_of_players]

players = []
for _ in range(nbr_of_players): 
    player  = PlayerPlayer()
    players.append(player)

deck = Deck()


# Draw initial cards
log = []
for _ in range(hand_size):
    for player_idx in range(nbr_of_players):
        log.append(event.DrawEvent(player_idx, deck.pull()))


game_on = True
active_player_idx = 0 
while game_on:
    action = players[active_player_idx].make_move()
    active_player_idx = (active_player_idx +1)%nbr_of_players
    

print(log)

def mask_log(log, player_idx):
    re_log = []
    for log_event in log:
        if isinstance(log_event, event.Event) and not isinstance(log_event, event.ClueEvent) and log_event.player_idx == player_idx:
            if isinstance(log_event,event.PlayEvent):
                re_log.append(event.PlayEvent(log_event.player_idx,log_event.card_idx,log_event.card_played,(None, None)))
            elif isinstance(log_event,event.ThrowEvent):
                re_log.append(event.ThrowEvent(log_event.player_idx,log_event.card_idx,log_event.card_thrown,(None, None)))
            elif isinstance(log_event,event.DrawEvent):
                re_log.append(event.DrawEvent(log_event.player_idx,(None,None)))
            else:
                raise Exception("Found weird log_event!")            
        else:
            re_log.append(log_event)
    return re_log


        


