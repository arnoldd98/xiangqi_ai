;(function () {
    let game = new Xiangqi()
    let $status = $('#status')
    let $fen = $('#fen')
    let gamemode = 'vs_computer'

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
                game.move(response.move);
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
        
        updateStatus();

        // let AI make move after set delay
        if (gamemode === 'vs_computer') {
            window.setTimeout(makeAIMove, 250);
        }
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

    $(document).ready(init)
})()

