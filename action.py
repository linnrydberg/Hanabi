class Action(): 
    pass

class ClueAction(Action):
    def __init__(self, player_idx, clue):
        super().__init__()
        self.player_idx = player_idx
        self.clue = clue 
    

class PlayAction(Action): 
    def __init__(self, card_idx):
        super().__init__()
        self.card_idx = card_idx
    

class ThrowAction(Action): 
    def __init__(self, card_idx):
        super().__init__()
        self.card_idx = card_idx

    
