
// Setup  --------------------------------------
socket = io();

// Helper  --------------------------------------
const pastelColors = {
    red: "#FFB3BA",
    red_clued: "#FF6675",
    blue: "#B3D1FF",
    blue_clued: "#66A3FF",
    green: "#BAFFC9",
    green_clued: "#66FF87",
    yellow: "#FFFFBA",
    yellow_clued: "#FFFF66",
    white: "#F5F5F5",
    white_clued: "#FFFFFF",
    unknown: "#757575",
    unclued_text: "#111",
    clued_text: "#111",
};

function createCard(colorName, value, empty=false) {
    const card = document.createElement("div");
    card.classList.add("card");
    if (empty){
        card.classList.add("empty-cardpile");
        card.style.borderColor = pastelColors[colorName.toLowerCase()];
    } else {
        card.style.backgroundColor = pastelColors[colorName.toLowerCase()];
        if (["yellow", "white"].includes(colorName.toLowerCase())) {
            card.style.color = "#111";
        } else {
            card.style.color = "#111";
        }
    }

    const valueDisplay = document.createElement("div");
    valueDisplay.classList.add("card-value");
    valueDisplay.textContent = value;

    card.appendChild(valueDisplay);

    return card
}

function create_card_play_discard_buttons(){
    const playBtn = document.createElement("button");
    playBtn.classList.add("play-btn")
    playBtn.textContent = "Play";
    playBtn.onclick = (e) => {
        e.stopPropagation();

        // find index in hand this is
        var index_in_hand = -1;
        for (var i = 0;i < playBtn.parentElement.parentElement.childNodes.length; i++){
            if (playBtn.parentElement.parentElement.childNodes[i] === playBtn.parentElement){
                index_in_hand = i;
            }
        }
        socket.emit('send move',{"move_type": "play", "index_in_hand":index_in_hand});
    };

    const discardBtn = document.createElement("button");
    discardBtn.textContent = "Discard";
    discardBtn.classList.add("discard-btn")
    discardBtn.onclick = (e) => {
        e.stopPropagation();
        // find index in hand this is
        var index_in_hand = -1;
        for (var i = 0;i < playBtn.parentElement.parentElement.childNodes.length; i++){
            if (playBtn.parentElement.parentElement.childNodes[i] === playBtn.parentElement){
                index_in_hand = i;
            }
        }
        socket.emit('send move',{"move_type": "discard", "index_in_hand":index_in_hand});
    };
    return {playBtn, discardBtn} 
}

function rgbToHex(rgb) {
    const match = rgb.match(/\d+/g);
    if (!match || match.length < 3) return null;
    return (
      "#" +
      match.slice(0, 3).map(x =>
        parseInt(x).toString(16).padStart(2, "0")
      ).join("").toUpperCase()
    );
  }

function create_card_clue_buttons(){
    const colorClueBtn = document.createElement("button");
    colorClueBtn.textContent = "Color";
    colorClueBtn.classList.add("color-clue-btn")
    colorClueBtn.onclick = (e) => {
        e.stopPropagation();
        //alert("Clue Color clicked on card: " + colorClueBtn.parentElement.childNodes[1].textContent);
        // find which hand this is and which color this card has
        const hc = document.getElementsByClassName("hand-container")[0];
        const index_of_hand = (Array.from(hc.childNodes).findIndex(child => child.contains(e.currentTarget))); // my hand is ignored, so 0 is the first other players hand
        
        //const clue = (e.currentTarget.parentElement.childNodes[1].textContent)
        //const clue = console.log(getComputedStyle(e.currentTarget.parentElement).backgroundColor)
        const elementHex = rgbToHex(getComputedStyle(e.currentTarget.parentElement).backgroundColor);

        let matchedColor = null;

        for (const [name, hex] of Object.entries(pastelColors)) {
            if (hex.toUpperCase() === elementHex) {
                matchedColor = name;
                break;
            }
        }
        socket.emit('send move',{"move_type": "clue", "hand_index": index_of_hand, "clue_type":"color", clue:matchedColor});
    };

    const valueClueBtn = document.createElement("button");
    valueClueBtn.textContent = "Value";
    valueClueBtn.classList.add("value-clue-btn")
    valueClueBtn.onclick = (e) => {
        e.stopPropagation();
        const hc = document.getElementsByClassName("hand-container")[0];
        const index_of_hand = (Array.from(hc.childNodes).findIndex(child => child.contains(e.currentTarget))); // my hand is ignored, so 0 is the first other players hand
        const value = (e.currentTarget.parentElement.childNodes[1].textContent)
        socket.emit('send move',{"move_type": "clue", "hand_index": index_of_hand, "clue_type":"value", clue:value});

    };
    return {colorClueBtn, valueClueBtn} 
}

function create_my_card(colorName, value){
    const card = createCard(colorName, value);
    
    const {playBtn, discardBtn} = create_card_play_discard_buttons();
    card.prepend(playBtn);
    card.appendChild(discardBtn);
    return card
}

function create_clueable_card(colorName, value){
    const card = createCard(colorName, value);
    
    const {colorClueBtn, valueClueBtn} = create_card_clue_buttons();
    card.prepend(colorClueBtn);
    card.appendChild(valueClueBtn);
    return card
}

function create_clues_lives_left_container(clues_left_value, lives_left_value){
    const clue_life_container = document.createElement("div");
    clue_life_container.classList.add("clue-life-container");

    const clues_left = document.createElement("div");
    clues_left.classList.add("clue-life-tracker");
    const clue_title = document.createElement("div");
    clue_title.classList.add("clue-life-tracker-title");
    clue_title.textContent = "Clues";
    clues_left.appendChild(clue_title);
    const clue_value = document.createElement("div");
    clue_value.classList.add("clue-life-tracker-value");
    clue_value.textContent = clues_left_value;
    clues_left.appendChild(clue_value);
    clue_life_container.appendChild(clues_left)

    const lives_left = document.createElement("div");
    lives_left.classList.add("clue-life-tracker");
    const life_title = document.createElement("div");
    life_title.classList.add("clue-life-tracker-title");
    life_title.textContent = "Lives";
    lives_left.appendChild(life_title);
    const life_value = document.createElement("div");
    life_value.classList.add("clue-life-tracker-value");
    life_value.textContent = lives_left_value;
    lives_left.appendChild(life_value);
    clue_life_container.appendChild(lives_left)
    
    return clue_life_container
}

function create_hand(cards, owner_name, create_card_function){
    const hand = document.createElement("div")
    hand.classList.add("hand");

    const hand_owner = document.createElement("div")
    hand_owner.classList.add("hand-owner");
    hand_owner.textContent = owner_name;
    hand.appendChild(hand_owner)

    const card_container = document.createElement("div")
    card_container.classList.add("card-container");
    hand.appendChild(card_container)
    
    for (const card of cards){
        const card_element = create_card_function(card[0],card[1])
        card_container.appendChild(card_element)
    }
    return hand

}

function display_discard(){
    socket.emit('get discard',{data: 'I want discard'});
} 

function update_interface_from_game_state(game_state){
    console.log(game_state);
    const game_window = document.getElementById("game-window");
    game_window.classList.add("game-window");

    while (game_window.firstChild) {
        game_window.removeChild(game_window.lastChild);
    }

    const hand_container = document.createElement("div");
    hand_container.classList.add("hand-container");
    game_window.appendChild(hand_container)
    
    const my_hand = create_hand(game_state["my_hand"], "Me", create_my_card)
    hand_container.appendChild(my_hand)
    for (const [hand_owner, hand] of Object.entries(game_state["hands"])) {
        hand_container.appendChild(create_hand(game_state["hands"][hand_owner], hand_owner, create_clueable_card))
    }

    const board_container = document.createElement("div");
    board_container.classList.add("board-container");
    game_window.appendChild(board_container);

    
    board_container.appendChild(create_clues_lives_left_container(game_state["clues"],game_state["lives"]))

    const board_cards_container = document.createElement("div");
    board_cards_container.classList.add("board-cards-container");
    board_container.appendChild(board_cards_container);
    for (const [color, value] of Object.entries(game_state["board"])) {
        board_cards_container.appendChild(createCard(color, value, empty=(value==0)));
    }

    const discard_pile = document.createElement("div");
    discard_pile.classList.add("discard-pile");
    board_container.appendChild(discard_pile);
    discard_pile.appendChild(createCard(game_state["last_discarded"][0],game_state["last_discarded"][1],empty=game_state["last_discarded"][1]==0));
    const discard_pile_title = document.createElement("div");
    discard_pile_title.classList.add("discard-pile-title");
    discard_pile_title.textContent = "Discard"
    discard_pile.appendChild(discard_pile_title)
    discard_pile.addEventListener("click", display_discard)

    // Change color of text and background on clued cards
    const hands = document.getElementById("game-window").getElementsByClassName("hand-container")[0];
    var clued_hands = [game_state["clued_cards_my_hand"]];
    for (var hand of game_state["clued_cards_hands"]){
        clued_hands.push(hand);
    }
    clued_hands.forEach((clued_hand,hand_i) => {
        clued_hand.forEach((clued_card, card_i) => {
            const card = hands.childNodes[hand_i].getElementsByClassName("card-container")[0].childNodes[card_i];
            if (clued_card[0] !== null){
                console.log(clued_card[0] + "_clued");
                //card.style.backgroundColor = pastelColors[clued_card[0] + "_clued"];
                //card.style.background = 'linear-gradient(135deg,' + pastelColors[clued_card[0]] + ', #000000)';
                card.style.background = 'linear-gradient(to bottom right,' + pastelColors[clued_card[0]] + ' 0%,'+pastelColors[clued_card[0]]+' 80%, #000000 100%)';
            }
            if (clued_card[1] !== null){
                card.style.color = pastelColors["clued_text"];
                card.style.textDecoration = 'underline';
                if (hand_i == 0){
                    card.childNodes[1].textContent = clued_card[1];
                }

            }
        });
    });




}

function change_to_discard_interface(discard){
    console.log("Got discard!")
    console.log(discard)

    const game_window = document.getElementById("game-window");
    // remove what is in window
    while (game_window.firstChild) {
        game_window.removeChild(game_window.lastChild);
    }

    // display discarded cards in a matrix
    discard_matrix = document.createElement("div")
    discard_matrix.classList.add("discard-matrix")
    game_window.appendChild(discard_matrix)
    for (let color in discard){
        discard_column = document.createElement("div")
        discard_column.classList.add("discard-column")
        discard_matrix.appendChild(discard_column)
        for (let value in discard[color]){
            discard_element = document.createElement("div")
            discard_element.classList.add("discard-element")
            discard_column.appendChild(discard_element)
            card = createCard(color, value, empty=discard[color][value]==0)
            discard_element.appendChild(card)
            for (let i = 1; i < discard[color][value]; i++){
                card = createCard(color, value, empty=discard[color][value]==0)
                card.style.top = `${i * -6}px`; // adjust offset as needed
                card.style.left = `${i * -6}px`; // adjust offset as needed
                card.style.zIndex = -i;

                discard_element.appendChild(card)
            }
        }
    }
}

// Requests  --------------------------------------

function get_game_state(){
    socket.emit('get game state',{data: 'I want gamestate'});
}

function start(){
    socket.emit('start',{data: 'I want start'});
}


// Responses  --------------------------------------
socket.on('game state update', update_interface_from_game_state);

socket.on('send discard', change_to_discard_interface);