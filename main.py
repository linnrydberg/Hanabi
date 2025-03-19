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



