"""
This file will provide the means to evalute the chess board and get the chess bot's move.
It will implement the minimax algorithm with alpha-beta pruning, which will be explained.
The Python chess library will also be utilized for move generation and basic chess logic.
"""

# ----- Imports ----- #
import chess as ch


# ----- Class ----- #
class Engine:

    # ----- Class Constructor ----- #
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color


    # ----- Core Functionality ----- #
    """
    The core functionality of the Chess Engine. Computers play chess by searching game states, and picking
    the best one. This implementation uses the Minimax algorithm, combined with Alpha-Beta Pruning to
    significantly improve runtime

    High Level Explanation:
    The algorithm creates a tree representation of the game states, branching from original poisition that the
    bot is in when the algorithm is called. Children nodes represent legal moves from a parent game state.

    The bot attempts to maximize the score it can receive, while at the same time minimizing the score the human
    can get. If there are no legal moves or the max depth parameter has been hit, the bot is at a leaf node, and
    evaluates the game state to a number

    Above the leaf nodes, the game states are evaluated based on their favorability to the bot. The bot will pick
    the largest number when it is the bot's turn, and pick the smallest number on the human's turn. Alpha-Beta
    Pruning is also used. Essentially, if the bot can guarantee a more favorable game state than the branch it is
    searching, it will stop searching the branch.
    """
    def minimax(self, depth, alpha = float("-inf"), beta = float("inf"), bot_turn = True):
        if (depth == 0) or (self.board.legal_moves.count() == 0):
            return self.evaluate_board(), None
        best_move = None
        if (bot_turn):
            max_value = float("-inf")
            moves = list(self.board.legal_moves)
            for move in moves:
                self.board.push(move)
                score = self.minimax(depth - 1, alpha, beta, False)[0]
                self.board.pop()
                if (score > max_value):
                    max_value = score
                    best_move = move
                alpha = max(alpha, score)
                if (alpha >= beta):
                    break
            return max_value, best_move
        else:
            min_value = float("inf")
            moves = list(self.board.legal_moves)
            for move in moves:
                self.board.push(move)
                score = self.minimax(depth - 1, alpha, beta, True)[0]
                self.board.pop()
                if (score < min_value):
                    min_value = score
                    best_move = move
                beta = min(beta, score)
                if (alpha >= beta):
                    break
            return min_value, best_move


    # ----- Auxilary Functions ----- #
    """
    Function to evaluate board, returning a value representing
    desirability of that game state
    """
    def evaluate_board(self):
        rv = 0
        for square in self.board.piece_map():
            rv += self.square_score(square)
        rv += self.mate()
        return rv

    """
    Function to determine if a checkmate or stalemate is possible
    """
    def mate(self):
        # if there are no more moves to play, must be in a check/stalemate
        if (self.board.legal_moves.count() == 0):
            # if the bot is the one in mate, avoid this possibility by
            # assigning a score to avoid it. Alternatively, if the player
            # is in the mate, assign a score to assure this outcome
            if (self.board.turn == self.color):
                return -9999
            else:
                return 9999
        # if no mate opportunity, do not impact board evaluation
        return 0

    """
    Function to evaluate a given square. Uses a slightly modified version of
    Bobby Fischer's evaluation method, since check/stalemate should still 
    have greater priority
    """
    def square_score(self, square):
        rv = 0
        if (self.board.piece_type_at(square) == ch.PAWN):
            rv = 1
        elif (self.board.piece_type_at(square) == ch.KNIGHT):
            rv = 3
        elif (self.board.piece_type_at(square) == ch.BISHOP):
            rv = 3.25
        elif (self.board.piece_type_at(square) == ch.ROOK):
            rv = 5
        elif (self.board.piece_type_at(square) == ch.QUEEN):
            rv = 9
        # Value of the king is arbitrary since mates are handled seperately
        # Used 20, however this value is not indicative of anything
        elif (self.board.piece_type_at(square) == ch.KING):
            rv = 20
        # if piece color is not the bot's, assign a negative value
        if (self.board.color_at(square) != self.color):
            return -1 * rv
        return rv


    # ----- Unused Functions ----- #
    # deprecated, DO NOT USE
    def old_minimax(self, candidate, depth):
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evaluate_board()
        else:
            moves = list(self.board.legal_moves)
            newCandidate = None
            if (depth % 2 == 0):
                newCandidate = float("inf")
            else:
                newCandidate = float("-inf")
            for move in moves:
                self.board.push(move)
                value = self.minimax(newCandidate, depth + 1)
                bot_turn = depth % 2 != 0
                if (value > newCandidate) and (bot_turn):
                    if (depth == 1):
                        best_move = move
                    newCandidate = value
                elif (value < newCandidate) and (not bot_turn):
                    newCandidate = value
                if (candidate is not None) and (value < candidate) and (not bot_turn):
                    self.board.pop()
                    break
                elif (candidate is not None) and (value > candidate) and (bot_turn):
                    self.board.pop()
                    break
                self.board.pop()
            if (depth > 1):
                return newCandidate
            return best_move
    
    # unused function, used to understand minimax as a whole
    def maximize(self, depth):
        if (depth == 0):
            return self.evaluate_board()
        max = float("-inf")
        moves = list(self.board.legal_moves)
        for move in moves:
            self.board.push(move)
            score = self.minimize(depth - 1)
            if score > max:
                max = score
            self.board.pop()
        return max
    
    # unused function, used to understand minimax as a whole
    def minimize(self, depth):
        if (depth == 0):
            return self.evaluate_board()
        min = float("inf")
        moves = list(self.board.legal_moves)
        for move in moves:
            self.board.push(move)
            score = self.maximize(depth - 1)
            if score < min:
                min = score
            self.board.pop()
        return min
    
