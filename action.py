class Action(): 
    pass

class ClueAction(Action):
    def __init__(self, player_idx, clue):
        super().__init__()
        self.player_idx = player_idx
        self.clue = clue 
    

class PlayAction(Action): 
    
    def __init__(self, player_idx, card_idx, card_played, card_pulled):
        super().__init__()
        self.player_idx = player_idx
        self.card_idx = card_idx
        self.card_played = card_played
        self.card_pulled = card_pulled
