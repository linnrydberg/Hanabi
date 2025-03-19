import random
class Deck(): 
    def __init__(self):
        self.cards = []
        colors = ["red", "blue", "green", "yellow", "white"]
        numbers = [1,1,1,2,2,3,3,4,4,5]
        for color in colors: 
            for num in numbers: 
                self.cards.append((color, num))

        random.shuffle(self.cards)
    
    def pull(self): 
        return self.cards.pop(0)


        
