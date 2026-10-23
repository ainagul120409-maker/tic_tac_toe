import random

from django.shortcuts import redirect, render


WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def get_winner(board):
    for a, b, c in WINNING_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def available_moves(board):
    return [i for i, cell in enumerate(board) if not cell]


def choose_bot_move(board, difficulty):
    moves = available_moves(board)
    if difficulty == 'easy':
        return random.choice(moves)

    
    for mark in ('O', 'X'):
        for move in moves:
            board[move] = mark
            wins = get_winner(board) == mark
            board[move] = ''
            if wins:
                return move
    if difficulty == 'medium':
        return random.choice(moves)

    depth_limit = 3 if difficulty == 'hard' else len(moves)

    def score_position(position, depth, maximizing):
        winner = get_winner(position)
        if winner == 'O':
            return 10 + depth
        if winner == 'X':
            return -10 - depth
        if '' not in position:
            return 0
        if depth == 0:
            score = 0
            for a, b, c in WINNING_LINES:
                line = [position[a], position[b], position[c]]
                if 'X' not in line:
                    score += line.count('O')
                if 'O' not in line:
                    score -= line.count('X')
            return score

        scores = []
        mark = 'O' if maximizing else 'X'
        for move in available_moves(position):
            position[move] = mark
            scores.append(score_position(position, depth - 1, not maximizing))
            position[move] = ''
        return max(scores) if maximizing else min(scores)

    best_move = moves[0]
    best_score = float('-inf')
    for move in moves:
        board[move] = 'O'
        score = score_position(board, depth_limit - 1, False)
        board[move] = ''
        if score > best_score:
            best_move, best_score = move, score
    return best_move


def make_bot_move(request):
    board = request.session['board']
    if (request.session.get('mode') == 'bot' and
            request.session.get('turn') == 'O' and
            not get_winner(board) and '' in board):
        board[choose_bot_move(board, request.session.get('difficulty', 'medium'))] = 'O'
        request.session['board'] = board
        request.session['turn'] = 'X'


def index(request):
    if 'board' not in request.session:
        request.session['board'] = [''] * 9
        request.session['turn'] = 'X'
        request.session['mode'] = 'players'
        request.session['difficulty'] = 'medium'
        request.session['player1_mark'] = 'X'
        request.session['next_starter'] = 1
        request.session['starting_mark'] = 'X'

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'new_game':
            request.session['mode'] = 'bot' if request.POST.get('mode') == 'bot' else 'players'
            player1_mark = request.POST.get('player1_mark', 'X')
            request.session['player1_mark'] = player1_mark if player1_mark in {'X', 'O'} else 'X'
            difficulty = request.POST.get('difficulty', 'medium')
            request.session['difficulty'] = difficulty if difficulty in {'easy', 'medium', 'hard', 'hardcore'} else 'medium'
            request.session['board'] = [''] * 9
            if request.session['mode'] == 'players':
                first_mark = request.session['player1_mark'] if request.session.get('next_starter', 1) == 1 else ('O' if request.session['player1_mark'] == 'X' else 'X')
                request.session['starting_mark'] = first_mark
                request.session['turn'] = first_mark
                request.session['next_starter'] = 2 if request.session.get('next_starter', 1) == 1 else 1
            else:
                request.session['starting_mark'] = 'X'
                request.session['turn'] = 'X'
            return redirect('game')
        if action == 'restart':
            request.session['board'] = [''] * 9
            request.session['turn'] = request.session.get('starting_mark', request.session.get('player1_mark', 'X')) if request.session.get('mode') == 'players' else 'X'
            return redirect('game')

        try:
            cell = int(request.POST.get('cell', -1))
        except (TypeError, ValueError):
            cell = -1

        board = request.session['board']
        winner = get_winner(board)
        mode = request.session.get('mode', 'players')
        turn = request.session.get('turn', 'X')
        can_move = mode == 'players' or turn == 'X'
        if (0 <= cell < 9 and not board[cell] and not winner and '' in board
                and can_move):
            board[cell] = turn
            request.session['board'] = board
            request.session['turn'] = 'O' if turn == 'X' else 'X'
            make_bot_move(request)
            winner = get_winner(request.session['board'])
        return redirect('game')

    board = request.session['board']
    winner = get_winner(board)
    draw = not winner and '' not in board
    if winner:
        if request.session.get('mode') == 'bot':
            status = 'Бот победил!' if winner == 'O' else 'Вы победили!'
        else:
            status = f'Победили {winner}!'
    elif draw:
        status = 'Ничья!'
    elif request.session.get('mode') == 'bot':
        status = 'Ваш ход (X)' if request.session.get('turn') == 'X' else 'Бот думает…'
    else:
        current_player = 1 if request.session.get('turn') == request.session.get('player1_mark', 'X') else 2
        status = f'Ход игрока {current_player} ({request.session.get("turn", "X")})'

    return render(request, 'game/index.html', {
        'board': board,
        'status': status,
        'finished': bool(winner or draw),
        'winner': winner,
        'mode': request.session.get('mode', 'players'),
        'difficulty': request.session.get('difficulty', 'medium'),
        'player1_mark': request.session.get('player1_mark', 'X'),
        'player2_mark': 'O' if request.session.get('player1_mark', 'X') == 'X' else 'X',
    })
