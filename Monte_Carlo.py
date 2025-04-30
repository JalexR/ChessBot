# Author: Andrew Gill
# Class: CSCI 4511W
# Assignment: Final Project
# Group: StockGopher
# Implements the framework for Monte Carlo tree search. Const

import time
import math
import random
import chess

PIECE_VALS = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


def get_successors(node):
    """
    Given a chess board, returns all legal moves and their resulting boards into a list.
    """
    moves = list(node.board.legal_moves)
    boards_moves = []
    for move in moves:
        new_board = node.board.copy()
        new_board.push(move)
        boards_moves.append((new_board, move))
    return boards_moves




class Tree_Node:
    """ 
    A structure for representing the Monte Carlo search tree. Each node keeps
    track of its game board, the move leading into it, the proportion of wins, and its children and parent.
    """

    def __init__(self, board = None, move = None):
        self.parent = None
        self.board = board
        self.move = move
        self.playouts = 0
        self.wins = 0
        self.children = []

    def add_child(self, board, move = None): #>>>> Need move associated with board for returning later
        """
        Adds a child with the given board.
        """
        new_child = Tree_Node(board, move)
        new_child.parent = self
        self.children.append(new_child)

    def child(self, n):
        """
        Returns the n-th child (0-indexed).
        """
        if n not in range(len(self.children)):
            return None
        return self.children[n]
    
    def is_leaf(self):
        """
        Returns true if and only if node has no children.
        """
        return self.children == []
    
    def add_playout(self, outcome):
        """
        Increments the node's playouts. If outcome == "win", also increments
        the node's wins.
        """
        self.playouts += 1
        if outcome == "win":
            self.wins += 1

    def propagate(self, outcome):
        """
        Records a playout for the current node and back propagates this data.
        Propagates a win if outcome == "win", and propagates a loss otherwise.
        """
        node = self
        while not node == None:
            node.add_playout(outcome)
            node = node.parent
            if outcome == "win":
                outcome = "loss"
            else:
                outcome = "win"

    def print(self, n=0):
        """
        Prints a visual representation of the tree for debugging.
        """
        print((n*"  ") + "(" + str(self.wins) + "/" + str(self.playouts) + ")")
        for succ in self.children:
            succ.print(n + 1)
        


class Playout_Policies:

    @staticmethod
    def Random(node):
        board = node.board.copy()
        while not board.is_game_over(): #Must playout board to end
            successors = list(board.legal_moves)
            move = random.choice(successors)
            board.push(move)

        return board.outcome() #Must return outcome
    
    @staticmethod
    def Offense(node):
        board = node.board.copy()
        while not board.is_game_over():
            legal_moves = list(board.legal_moves)
            best_moves = []
            max_value = -1
            for move in legal_moves:
                # checking if the move is captureing a piece
                if board.is_capture(move):
                    captured_square = move.to_square
                    captured_piece = board.piece_at(captured_square)
                    # checking if there was a captured piece
                    if captured_piece:
                        # value of captured peice
                        value = PIECE_VALS.get(captured_piece.piece_type, 0)
                        # checking if taking the piece is the best move so far
                        if value > max_value:
                            max_value = value
                            best_moves = [move]
                        elif value == max_value:
                            best_moves.append(move)
            # if moves that captured pieces were found
            if best_moves:
                chosen_move = random.choice(best_moves)
                # reseting bestmoves
                best_moves = []
            # if there were no moves that captured pieces
            else:
                chosen_move = random.choice(legal_moves)
            board.push(chosen_move)
        return board.outcome()
    
    @staticmethod
    def Defense(node):
        board = node.board.copy()    
        while not board.is_game_over():
            legal_moves = list(board.legal_moves)
            best_moves = []
            max_value = -1
            for move in legal_moves:
                # getting the piece that just moved
                moving_piece = board.piece_at(move.from_square)
                # if a piece was found
                if moving_piece and moving_piece.color == board.turn:
                    value = PIECE_VALS.get(moving_piece.piece_type, 0)
                    # checking if the last move was a good one
                    if value > max_value:
                        max_value = value
                        best_moves = [move]
                    elif value == max_value:
                        best_moves.append(move)
            # if a good move was found
            if best_moves:
                chosen_move = random.choice(best_moves)
            # if no move was found
            else:
                chosen_move = random.choice(legal_moves)
            board.push(chosen_move)
        return board.outcome()



class Agent:
    """
    An agent that can perform Monte Carlo Tree Search from a given Chess
    posiiton. The selection policy is UCB1, but the playout policy can be anything.
    """

    def __init__(self, playout_policy, duration):
        self.playout = playout_policy 
        self.duration = duration
        # Playout policy; Plays out from a board, 
        # returns "white" for white win, "black" for black win, "draw" for draw

    def add_playout(self, node):
        """
        Performs one playout from the given node and records the outcome in the
        tree.
        """
        outcome = self.playout(node) # 3: Perform a playout from that leaf node
        if outcome == node.board.turn: # 4: Back propagate
            node.propagate("win")
        else:
            node.propagate("loss")

    def selection_policy(self, node): # UCB1
        """
        Selects the proper child according to UCB1. Returns None if node is a
        leaf.
        """

        if node.is_leaf():
            return None

        # First, make sure each child has at least one playout
        for child in node.children:
            if child.playouts == 0:
                self.add_playout(child)

        curr_choice = node.children[0] 
        curr_score = 0
        for child in node.children:
            new_score = (child.wins / child.playouts) + 4 * math.sqrt(2 * math.log(node.playouts) / child.playouts)
            if new_score > curr_score:
                curr_choice = child
                curr_score = new_score
        
        return curr_choice

    def search(self, board): 
        """
        Given a board to play from, returns the board to which the current
        player should move.

        Arguments:
        board -- The board board to play from. Has board.player attribute
        duration -- The time, in seconds, to be spent searching.
        """

        if not board.outcome() == None:
            return None
        
        beginning = time.time()
        tree = Tree_Node(board)
        while time.time() - beginning < self.duration:
            curr = tree
            while True:
                selected = self.selection_policy(curr)
                if selected is None:
                    break
                curr = selected

            # Make sure the current board isn't checkmate
            if curr.board.is_game_over(): 
                continue
            else: # 2: Expand node and choose a child
                successors = get_successors(curr) 
                for succ in successors:
                    curr.add_child(succ[0], succ[1])
                curr = self.selection_policy(curr)  #>>>>>This is better than just picking the first child
                self.add_playout(curr) # 3, 4: Playout and back propagate

        # Return the child with the most playouts
        max_playouts = 0
        answer = tree.child(0)
        for option in tree.children:
            if option and option.playouts > max_playouts:
                max_playouts = option.playouts
                answer = option
        return answer.move if answer is not None else None

