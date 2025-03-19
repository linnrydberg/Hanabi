from abc import ABC, abstractmethod
from action import PlayAction, ClueAction, ThrowAction

class Player(ABC): 
    
    @abstractmethod
    def make_move(self, log):
        pass


class PlayerPlayer(Player):

    def __init__(self):
        pass

    def make_move(self, log):
        return PlayAction(0)
        