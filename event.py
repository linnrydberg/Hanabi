class Event(): 
    pass

class DrawEvent(Event): 
    def __init__(self, player_idx, card):
        super().__init__()
        self.player_idx = player_idx
        self.card = card

    def __str__(self):
        return "Player: " + str(self.player_idx) + " drew " + str(self.card)
    
    def __repr__(self):
        return self.__str__()

class PlayEvent(Event): 
    def __init__(self, player_idx, card_idx, card_played, card_pulled):
        super().__init__()
        self.player_idx = player_idx
        self.card_idx = card_idx
        self.card_played = card_played
        self.card_pulled = card_pulled

class ThrowEvent(Event): 
    def __init__(self, player_idx, card_idx, card_thrown, card_pulled):
        super().__init__()
        self.player_idx = player_idx
        self.card_idx = card_idx
        self.card_thrown = card_thrown
        self.card_pulled = card_pulled

class ClueEvent(Event): 
    def __init__(self, clueing_player_idx, clued_player_idx, clue):
        super().__init__()
        self.clueing_player_idx = clueing_player_idx
        self.clued_player_idx = clued_player_idx
        self.clue = clue 







