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
    Prio 2: Clue a playable card (not already clued, and clue not touching other things)
    Prio 3: Discard oldest card 
    """
    def __init__(self):
        super().__init__()
        pass

    def make_move(self, log): 
        #kolla om det det finns ett clue:at kort på handen
        colors = ["red", "blue", "green", "yellow", "white"]
        board = Board(log)
       
        my_index = board.player_index_of_me()
        tutti_clues = board.get_clues()
        my_clues = tutti_clues[my_index]
        
        for i,clue in enumerate(my_clues):
            if clue[0] or clue[1]:
                return PlayAction(i)
        
        if board.get_clues_left() > 0 : 
            max_playable = 0
            max_clue = (None, None)
            max_player = None
            for i in range(board.nbr_of_players): 
                for col in colors: 
                    current_hand = board.get_hand(i)
                    nbr_of_playable_cards = 0
                    for j, card in enumerate(current_hand): 
                        if col == card[0]: 
                            card_col = card[0]
                            card_num = card[1]
                            if board.get_highest_cards()[card_col] +1 == card_num: 
                                if not tutti_clues[i][j][0] and not tutti_clues[i][j][1]: 
                                    nbr_of_playable_cards +=1

                            else:
                                nbr_of_playable_cards = 0
                                break
                    
                    if nbr_of_playable_cards > max_playable: 
                        max_playable = nbr_of_playable_cards
                        max_player = i
                        max_clue = (col, None)
                    
                
                for num in range(1,6): 
                    current_hand = board.get_hand(i)
                    nbr_of_playable_cards = 0
                    for card in current_hand: 
                        if num == card[1]: 
                            card_col = card[0]
                            card_num = card[1]
                            if board.get_highest_cards()[card_col] +1 == card_num: 
                                if not tutti_clues[i][j][0] and not tutti_clues[i][j][1]: 
                                    nbr_of_playable_cards +=1
                            else:
                                nbr_of_playable_cards = 0
                                break

                    if nbr_of_playable_cards > max_playable: 
                        max_playable = nbr_of_playable_cards
                        max_player = i
                        max_clue = (None, num)
            
            if max_player: 
                return ClueAction(max_player, max_clue)
        return ThrowAction(0)
        
    

        


        