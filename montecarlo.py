# Author: Andrew Gill
# Class: CSCI 4511W
# Assignment: Final Project
# Group: StockGopher
# Implements the framework for Monte Carlo tree search. Const

# NOTES:
# The two placeholder functions must be replaced with working functions!
#
# A game state is taken to mean a chess board along with the player to move.
# A state object is assumed to have state.player, either "white" or "black"

import time
import math

# ---------------------------------------------
# Chess functions (PLACEHOLDERS - REPLACE WITH REAL CODE!)
# ---------------------------------------------
def get_successors(state):
    """
    Given a chess state, returns all states that the player can move to as a list.
    """
    pass

def is_end(state): # Checks for checkmate; "white" for white win, "black" for black win, 0 else
    """
    Given a chess state, returns "white" or "black" if the state is a win for
    one player, and returns 0 if the game has not ended.
    """
    pass


# ---------------------------------------------
# Search Tree Class
# ---------------------------------------------
class Tree_Node:
    """ 
    A structure for representing the Monte Carlo search tree. Each node keeps
    track of its game state, the proportion of wins, and its children and parent.
    """

    def __init__(self, state = None):
        self.parent = None
        self.state = state
        self.playouts = 0
        self.wins = 0
        self.children = []

    def add_child(self, state):
        """
        Adds a child with the given state.
        """
        new_child = Tree_Node(state)
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
        

# ---------------------------------------------
# Search Agent Class
# ---------------------------------------------
class Monte_Carlo_Agent:
    """
    An agent that can perform Monte Carlo Tree Search from a given Chess
    posiiton. The selection policy is UCB1, but the playout policy can be anything.
    """

    def __init__(self, policy):
        self.playout = policy 
        # Playout policy; Plays out from a state, 
        # returns "white" for white win, "black" for black win, "draw" for draw

    def add_playout(self, node):
        """
        Performs one playout from the given node and records the outcome in the
        tree.
        """
        outcome = self.playout(node) # 3: Perform a playout from that leaf node
        if outcome == node.state.player: # 4: Back propagate
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
                self.add_playout(child, node)

        curr_choice = None
        curr_score = 0
        for child in node.children:
            new_score = (child.wins / child.playouts) + math.sqrt(2 * math.log(node.playouts) / child.playouts)
            if new_score > curr_score:
                curr_choice = child
                curr_score = new_score
        
        return curr_choice


    def search(self, state, duration = 1): 
        """
        Given a state to play from, returns the state to which the current
        player should move.

        Arguments:
        state -- The board state to play from. Has state.player attribute
        duration -- The time, in seconds, to be spent searching.
        """

        if not is_end(state) == 0:
            return None
        
        beginning = time.time()
        tree = Tree_Node(state)
        while time.time() - beginning < duration:
            curr = tree
            while not curr == None: # 1: Select until you get to a leaf node
                curr = self.selection_policy(curr)

            # Make sure the current state isn't checkmate
            game_ended = is_end(curr)
            if game_ended != 0: 
                outcome = game_ended
            else: # 2: Expand node and choose a child
                successors = get_successors(curr.state) 
                for succ in successors:
                    curr.add_child(succ)
                curr = curr.child(0)
                self.add_playout(curr) # 3, 4: Playout and back propagate

        # Return the child with the most playouts
        max_playouts = 0
        answer = tree.child(0)
        for option in tree.children:
            if (not option == None) and max_playouts < len(option.children):
                max_playouts = len(option.children)
                answer = option
        return answer
