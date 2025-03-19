from abc import ABC, abstractmethod

class Player(ABC): 
    
    @abstractmethod
    def make_move(self, log):
        pass




class PlayerPlayer(Player):

    def __init__(self):
        pass

    def make_move(self, log):
        return 0 # TODO: what is format of action