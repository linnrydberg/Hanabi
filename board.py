from event import DrawEvent, PlayEvent, ThrowEvent, ClueEvent

class Board:

    def __init__(self, log):
        self.log = log


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
        cards = []
        for log_event in self.log:
            if log_event.player_idx != player_idx:
                continue
            if isinstance(log_event,DrawEvent):
                cards.append(log_event.card)
            elif isinstance(log_event,PlayEvent) or isinstance(log_event,ThrowEvent):
                cards.append(log_event.card_pulled)
        return cards[-(card_idx+1)]
        

        
    


