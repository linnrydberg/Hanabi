from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time, flask, random
from threading import Thread
from hanabi_game import HanabiGame
import player, board
from action import PlayAction, ClueAction, ThrowAction

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
client_data = {}


def random_hand():
    return [(["red", "blue", "green", "yellow", "white"][random.randint(0,4)], random.randint(1,5)) for _ in range(4)]

@app.route('/')
def index():
    return render_template('index.html')  # will load our client code

@socketio.on('start')
def get_game_state(data):
    client_data[request.sid] = {} 
    client_data[request.sid]["me"]  = player.HumanPlayer()
    client_data[request.sid]["game"] = HanabiGame([client_data[request.sid]["me"] if i==0 else player.NaivePlayer() for i in range(4)])
    game_thread = Thread(target=client_data[request.sid]["game"].run)
    game_thread.start()


@socketio.on('get hand')
def get_hand(data):
    print("get_hand")
    emit('hand update', {'hand' : random_hand()})
    
@socketio.on('get game state')
def get_game_state(data):
    print("get_game_state")
    b = board.Board(client_data[request.sid]["me"].last_log)
    emit('game state update', 
        {'my_hand' : [("unknown","?") for _ in range(4)],
        'hands' : {"Player " +str(i) : b.get_hand(i+1) for i in range(3)},
        "board": b.get_highest_cards(), 
        "lives":b.get_lives_left(), 
        "clues":b.get_clues_left(), 
        "last_discarded":("unknown","") if not b.get_last_discarded_card()[0] else b.get_last_discarded_card(),
        "clued_cards_my_hand":b.get_clues()[0],
        "clued_cards_hands":b.get_clues()[1:],
        })

@socketio.on('send move')
def send_move(data):
    if data["move_type"] == 'play':
        action = PlayAction(data['index_in_hand'])
    elif data["move_type"] == 'discard':
        action = ThrowAction(data['index_in_hand'])
    elif data["move_type"] == 'clue':
        action = ClueAction(data["hand_index"],(data["clue"], None) if data["clue_type"] == "color" else (None, int(data["clue"])))
    else: 
        Exception("data did not contain a valid move_type")
    client_data[request.sid]["me"].q.put(action)

@socketio.on('get discard')
def get_discard(data):
    b = board.Board(client_data[request.sid]["me"].last_log)
    discard = b.get_discard()
    re_discard = {color:{value:0 for value in range(1,6)} for color in ["red", "blue", "green", "yellow", "white"]}
    for color,value in discard:
        re_discard[color][value] += 1
    emit('send discard', re_discard)



if __name__ == '__main__':
    socketio.run(app, debug=True)