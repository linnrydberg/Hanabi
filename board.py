from event import DrawEvent, PlayEvent, ThrowEvent, ClueEvent

class Board:

    def __init__(self, log):
        self.log = log
        nbr_of_players = 0

        for log_event in self.log: 
            if log_event.player_idx > nbr_of_players: 
                nbr_of_players = log_event.player_idx


        hand_sizes = {
                2 : 5,
                3: 5,  
                4:4, 
                5: 4
            }
        self.hand_size = hand_sizes[nbr_of_players]


    def add_event_to_log(self,event):
        self.log.append(event)

    def get_clues_left(self):
        clues_left = 8
        for i, log_event in enumerate(self.log):
            if isinstance(log_event,ClueEvent):
                clues_left -= 1
            elif isinstance(log_event,ThrowEvent) or (isinstance(log_event,PlayEvent) and log_event.card_played[1] == 5):
                clues_left += 1
        return clues_left

    def get_card(self, player_idx, card_idx):
        return self.get_hand(player_idx)[card_idx]

         
    def get_hand(self, player_idx):
        cards = []
        for log_event in self.log:
            if log_event.player_idx != player_idx:
                continue
            if isinstance(log_event,DrawEvent):
                cards.append(log_event.card)
            elif isinstance(log_event,PlayEvent) or isinstance(log_event,ThrowEvent):
                cards.append(log_event.card_pulled)

        hand = cards[-self.hand_size:]
        hand.reverse()
        return hand 
    

    def get_highest_cards(self): 
        highest_cards = {"red" : 0 , "blue": 0, "green":0, "yellow":0, "white":0}
        for i, log_event in enumerate(self.log):
            if isinstance(log_event, PlayEvent): 
                col, num =log_event.card_played
                if highest_cards[col] +1 == num:
                    highest_cards[col] = num
        return highest_cards

    def get_lives_left(self):
        lives_left = 3
        highest_cards = {"red" : 0 , "blue": 0, "green":0, "yellow":0, "white":0}
        for i, log_event in enumerate(self.log):
            if isinstance(log_event, PlayEvent): 
                col, num =log_event.card_played
                if highest_cards[col] +1 == num:
                    highest_cards[col] = num
                else:
                    lives_left -=1
        return lives_left
    
        
        

    
    


