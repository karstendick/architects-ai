from .game_state import GameMove, GameState, Outcome, OutcomeMap
import time
import numpy as np
from math import log2, sqrt
from random import choice
from typing import TypeVar

EXPLORE_CONST = 1.414  # sqrt(2) is the theoretical choice
TIME_BUDGET_S = 10 # How long to give the search to run, in seconds

T = TypeVar('T', bound='Node')

class Node():
  def __init__(self: T, state: GameState, move: GameMove = None, parent: T = None):
    self.state = state
    self.parent = None
    self.move = move
    self.children = {}  # dict of GameMove to Node?
    # dict of dicts. Maps PlayerName to Outcome to int

    self.outcomes = {p: {o: 0 for o in Outcome}
                     for p in state.get_players()}
    self.num_playouts = 0

  def ucb1(self):
    if self.num_playouts == 0:
      return np.inf
    outcomes = self.outcomes[self.state.to_move()]
    utility = outcomes[Outcome.WIN]
    return utility / self.num_playouts \
      + EXPLORE_CONST * sqrt( log2(self.parent.num_playouts)/self.num_playouts )

def select(tree: Node):
  while len(tree.children) != 0:
    children_nodes = tree.children.values()
    max_ucb1_value = max([c.ucb1() for c in children_nodes])
    
    # break ties randomly
    max_nodes = [n for n in tree.children if n.ucb1() == max_ucb1_value]
    selected_node = choice(max_nodes)

    tree = selected_node
  
  return tree


def expand(leaf):
  if leaf.state.is_terminal():
    return leaf
  
  moves = leaf.state.get_moves()
  children = {move: Node(leaf.state.play(move), move, leaf) for move in moves}
  leaf.children = children
  expanded_node = choice(leaf.children.values())
  return expanded_node


def simulate(node: Node):
  state = node.state
  # TODO: terminate playout early sometimes?
  while not state.is_terminal():
    move = choice(state.get_moves())
    state = state.play(move)
  
  return node.state.get_outcome()

def back_propogate(result: OutcomeMap, node: Node):
  while node is not None:
    for player_name in result:
      for outcome in result[player_name]:
        node.outcomes[player_name][outcome] += result[player_name][outcome]
    node = node.parent

def most_playouts_move(tree: Node) -> GameMove:
  children_nodes = tree.children.values()
  max_playouts = [c.num_playouts for c in children_nodes]
  max_nodes = [n for n in children_nodes if n.num_playouts == max_playouts]
  chosen_node = choice(max_nodes)
  return chosen_node.move

def mcts(state: GameState):
  start_time = time.time()

  tree = Node(state)

  while time.time() - start_time < TIME_BUDGET_S:
    leaf = select(tree)
    child = expand(leaf)
    result = simulate(child)
    back_propogate(result, child)
  
  return most_playouts_move(tree)
  

