;(function () {
    let game = new Xiangqi()
    let $status = $('#status')
    let $fen = $('#fen')
    let $history = $('#history')
    let gamemode = 'vs_computer'

    let $player1 = $('#player1');
    let $player2 = $('#player2');
    let $loading1 = $('#loading1');
    let $loading2 = $('#loading2');
    let $grave1 = $("#grave1");
    let $grave2 = $("#grave2");
    let botMoveInfo = null;
    let player1MoveInfo = null;
    let player2MoveInfo = null;
    let graveUpdated = false;

    let grave1= {
        '兵':0 , //p
        '炮':0 , //c
        '車':0 , //r
        '馬':0 , //n
        '象':0 , //b
        '士':0 , //a
        '将':0 , //k
    };
    let grave2= {
        '兵':0 ,
        '炮':0 ,
        '車':0 ,
        '馬':0 ,
        '象':0 ,
        '士':0 ,
        '将':0 ,
    }

    function isTouchDevice () {
        return ('ontouchstart' in document.documentElement)
    }

    function onDragStart (source, piece, position, orientation) {
        // do not pick up pieces if the game is over
        if (game.game_over()) return false;
        if (gamemode === 'vs_computer') {
            if (piece.search(/^b/) !== -1) return false;
        } else if (gamemode === 'vs_human') {
            if ((game.turn() === 'r' && piece.search(/^b/) !== -1) ||
                (game.turn() === 'b' && piece.search(/^r/) !== -1)) {
                return false;
            }
        }
    }

    function makeRandomMove() {
        let possibleMoves = game.moves();

        if (possibleMoves.length === 0) return;

        let randomIdx = Math.floor(Math.random() * possibleMoves.length);
        game.move(possibleMoves[randomIdx]);
        board.position(game.fen());
        updateStatus()
    }

    function makeAIMove() {
        let possibleMoves = game.moves();
        let fen = game.fen();
        console.log(board.position())
        $.ajax({
            url: '/ai/move',
            type: 'POST',
            data: ({
                'fen': fen, 
                'possible_moves': possibleMoves
            }),
            success: function (response) {
                console.log(response)
                botMoveInfo = game.move(response.move);
                updateHistory(formattedHistory(botMoveInfo));
                board.position(game.fen());
                updateStatus();
            }
        })
    }

    function onDrop (source, target) {
        // see if the move is legal
        let move = game.move({
          from: source,
          to: target,
          promotion: 'q' // NOTE: always promote to a queen for example simplicity
        });
              
        // illegal move
        if (move === null) return 'snapback';
        
        // assign values to different fields when vs_human
        if (gamemode == 'vs_human'){
            if (move.color == 'r'){
                player1MoveInfo = move;
                updateHistory(formattedHistory(player1MoveInfo))
            }
            if (move.color == 'b'){
                player2MoveInfo = move;
                updateHistory(formattedHistory(player2MoveInfo))
            } 
        }
        
        updateStatus();

        // let AI make move after set delay
        if (gamemode === 'vs_computer') {
            player1MoveInfo = move;
            updateHistory(formattedHistory(player1MoveInfo));
            window.setTimeout(makeAIMove, 250);
        }

        graveUpdated = false;
        console.log('FEN String: ', game.fen())

    }

    // update the board position after the piece snap
    // for castling, en passant, pawn promotion
    function onSnapEnd () {
        board.position(game.fen());
    }

    function updateStatus () {
        let status = '';
      
        let moveColor = 'Red';
        if (game.turn() === 'b') {
          moveColor = 'Black';
        }
      
        // checkmate?
        if (game.in_checkmate()) {
          status = 'Game over, ' + moveColor + ' is in checkmate.';
        }
      
        // draw?
        else if (game.in_draw()) {
          status = 'Game over, drawn position';
        }
      
        // game still on
        else {
          status = moveColor + ' to move';

          //loading png shown
          if (moveColor == 'Red'){
            $loading2.show();
            $loading1.hide();
          }
          else{
            $loading1.show();
            $loading2.hide();
          }

          // Update graveyards
          if (botMoveInfo != null && graveUpdated == false){
            if  (botMoveInfo.flags == 'c' && botMoveInfo.color == 'b'){
                if (botMoveInfo.captured == 'p') {grave2['兵']++} else
                if (botMoveInfo.captured == 'c') {grave2['炮']++} else
                if (botMoveInfo.captured == 'r') {grave2['車']++} else
                if (botMoveInfo.captured == 'n') {grave2['馬']++} else
                if (botMoveInfo.captured == 'b') {grave2['象']++} else
                if (botMoveInfo.captured == 'a') {grave2['士']++} else
                if (botMoveInfo.captured == 'k') {grave2['将']++}
            }
          }

          if (player1MoveInfo != null && graveUpdated == false){
            if  (player1MoveInfo.flags == 'c' && player1MoveInfo.color == 'r' && moveColor == 'Black' ){
                if (player1MoveInfo.captured == 'p') {grave1['兵']++} else
                if (player1MoveInfo.captured == 'c') {grave1['炮']++} else
                if (player1MoveInfo.captured == 'r') {grave1['車']++} else
                if (player1MoveInfo.captured == 'n') {grave1['馬']++} else
                if (player1MoveInfo.captured == 'b') {grave1['象']++} else
                if (player1MoveInfo.captured == 'a') {grave1['士']++} else
                if (player1MoveInfo.captured == 'k') {grave1['将']++}
            }
          }

          if (player2MoveInfo != null && graveUpdated == false){
            if  (player2MoveInfo.flags == 'c' && player2MoveInfo.color == 'b' && moveColor == 'Red'){
                if (player2MoveInfo.captured == 'p') {grave2['兵']++} else
                if (player2MoveInfo.captured == 'c') {grave2['炮']++} else
                if (player2MoveInfo.captured == 'r') {grave2['車']++} else
                if (player2MoveInfo.captured == 'n') {grave2['馬']++} else
                if (player2MoveInfo.captured == 'b') {grave2['象']++} else
                if (player2MoveInfo.captured == 'a') {grave2['士']++} else
                if (player2MoveInfo.captured == 'k') {grave2['将']++}
            }
          }

          // ensure grave updated
          graveUpdated = true;

            // grave1=JSON.stringify(player1MoveInfo);
            // $grave1.html(grave1);

          $grave1.html(formattedGrave(grave1));
          $grave2.html(formattedGrave(grave2));
      
          // check?
          if (game.in_check()) {
            status += ', ' + moveColor + ' is in check';
          }
        }
      
        $status.html(status);
        $fen.html(game.fen()); 
    }

    function resetGame() {
        game.reset();
        resetGrave();
        resetMoveInfo();
        resetHistory();
        updateStatus();
        board.start();
    }
    function init () {
        let config = {
            draggable: true,
            position: 'start',
            onDragStart: onDragStart,
            onDrop: onDrop,
            onSnapEnd: onSnapEnd
          };
        board = Xiangqiboard('board', config);
        updateStatus();
        
        $('#startBtn').on('click', board.start)
        $('#clearBtn').on('click', board.clear)

        // prevent "browser drag" of the black king
        $('.hero-inner-556fe img').on('mousedown', function (evt) { evt.preventDefault() })
        // prevent hover problems on touch devices
        if (isTouchDevice()) {
            $('.navbar-a57cc').removeClass('hover-effect')
        }
        
        const gamemode_select = $('#gamemode_dialog');
        // gamemode_select.dialog();  

        $('#gamemode_btn').on('click', () => {
            gamemode_select.dialog();
        })
        $('#vs_computer_btn').on('click', () => {
            gamemode_select.dialog('close');
            resetGame();
            gamemode = 'vs_computer'
        })
        $('#vs_human_btn').on('click', () => {
            gamemode_select.dialog('close')
            resetGame();
            gamemode = 'vs_human'
        })
    }
    function updateHistory(text){
        $history.html($history.html()+ '<br/>' + text);
        let historyBox = document.getElementById("history");
        historyBox.scrollTop = historyBox.scrollHeight;
    }
    function formattedHistory(text){
        if (text['color'] == 'r'){
            if (text['flags'] == 'n'){
                return (
                    '<font color="red">' + 
                    ' Red move: ' + 
                    ' Piece ' + text['piece'] +
                    ' From ' + text['from'] +
                    ' To ' + text['to'] +
                    '</font>'
                );
            }
            else {
                return (
                    '<font color="red">' + 
                    ' Red move: ' + 
                    ' Piece ' + text['piece'] +
                    ' From ' + text['from'] +
                    ' To ' + text['to'] +
                    ' Catch ' + text['captured'] +
                    '</font>'
                );
            }
        }
        if (text['color'] == 'b'){
            if (text['flags'] == 'n'){
                return (
                    '<font color="black">' + 
                    ' Black move: ' + 
                    ' Piece ' + text['piece'] +
                    ' From ' + text['from'] +
                    ' To ' + text['to'] +
                    '</font>'
                );
            }
            else {
                return (
                    '<font color="black">' + 
                    ' Black move: ' + 
                    ' Piece ' + text['piece'] +
                    ' From ' + text['from'] +
                    ' To ' + text['to'] +
                    ' Catch ' + text['captured'] +
                    '</font>'
                );
            }
        }
    }
    function formattedGrave(text){
        return (
            '兵:' + text['兵'] + '<br/>' +
            '炮:' + text['炮'] + '<br/>' +
            '車:' + text['車'] + '<br/>' +
            '馬:' + text['馬'] + '<br/>' +
            '象:' + text['象'] + '<br/>' +
            '士:' + text['士'] + '<br/>' +
            '将:' + text['将'] + '<br/>' 
        );
    }
    function resetHistory(){
        $history.html("");
    }
    function resetGrave(){
        grave1['兵'] = 0;
        grave1['士'] = 0;
        grave1['将'] = 0;
        grave1['炮'] = 0;
        grave1['象'] = 0;
        grave1['車'] = 0;
        grave1['馬'] = 0;
        grave2['兵'] = 0;
        grave2['士'] = 0;
        grave2['将'] = 0;
        grave2['炮'] = 0;
        grave2['象'] = 0;
        grave2['車'] = 0;
        grave2['馬'] = 0;
    }
    function resetMoveInfo(){
        botMoveInfo=null;
        player1MoveInfo=null;
        player2MoveInfo=null;
    }
    $(document).ready(init)
})()

