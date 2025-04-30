from event import DrawEvent, PlayEvent, ThrowEvent, ClueEvent

class Board:

    def __init__(self, log):
        self.log = log
        nbr_of_players = 0

        for log_event in self.log: 
            if log_event.player_idx > nbr_of_players: 
                nbr_of_players = log_event.player_idx + 1
        self.nbr_of_players = nbr_of_players

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
            elif isinstance(log_event,ThrowEvent) or (isinstance(log_event,PlayEvent) and log_event.card_played[1] == 5) :
                if clues_left < 8: 
                    clues_left += 1
        return clues_left

    def get_card(self, player_idx, card_idx): # card_idx == 0 is the newest card
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
        #hand.reverse()
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
    
    def player_index_of_me(self): 
        for i, log_event in enumerate(self.log):
            if isinstance(log_event, DrawEvent): 
                if log_event.card == (None, None):
                    return log_event.player_idx
        raise Exception("Log is not masked")

    def get_clues(self): 
        """
        dict: 
        keys: players 
        values: hand 
        
        hand = dictionary 
        keys: card_idx 
        values: clue
        """

        my_index = self.player_index_of_me()
        hands = [[] for _ in range(self.nbr_of_players)]

          
        for i, log_event in enumerate(self.log):
            if isinstance(log_event, DrawEvent):
                hands[log_event.player_idx].append((None, None))

            if isinstance(log_event, PlayEvent): 
                hands[log_event.player_idx].pop(log_event.card_idx)
                hands[log_event.player_idx].append((None, None))

            if isinstance(log_event, ThrowEvent): 
                hands[log_event.player_idx].pop(log_event.card_idx)
                hands[log_event.player_idx].append((None, None))

            if isinstance(log_event, ClueEvent):
                
                for i in range(len(log_event.clued_hand)):
                    # (R,C) == (R, None)
                    if (log_event.clued_hand[i][0] == log_event.clue[0]) and log_event.clue[0]:
                        hands[log_event.clued_player_idx][i] = (log_event.clue[0],hands[log_event.clued_player_idx][i][1])
                    if (log_event.clued_hand[i][1] == log_event.clue[1]) and log_event.clue[1]:
                        hands[log_event.clued_player_idx][i] = (hands[log_event.clued_player_idx][i][0],log_event.clue[1]) 
        return hands

    def get_discard(self):
        discard = []
        for log_event in self.log:
            if isinstance(log_event, ThrowEvent):
                discard.append(log_event.card_thrown)
        return discard

    def get_last_discarded_card(self):
        for i in range(len(self.log)-1,0,-1):
            log_event = self.log[i]
            if isinstance(log_event, ThrowEvent):
                return log_event.card_thrown
        return (None, None)






            


    
        
        

    
    


