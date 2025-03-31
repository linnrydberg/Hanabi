from abc import ABC, abstractmethod
from action import PlayAction, ClueAction, ThrowAction
from board import Board

class Player(ABC): 
    
    @abstractmethod
    def make_move(self, log):
        pass


class PlayerPlayer(Player):

    def __init__(self):
        pass

    def make_move(self, log):
        return PlayAction(0)

class NaivePlayer(Player):
    """ 
    Prio 1: Play clued cards 
    Prio 2: Clue a playable card 
    Prio 3: Discard oldest card 
    """
    def __init__(self):
        super().__init__()
        pass

    def make_move(self, log): 
        #kolla om det det finns ett clue:at kort på handen
        board = Board(log)
        
        return "hi "

        


        