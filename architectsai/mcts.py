from .game_state import GameMove, GameState, Outcome, OutcomeMap, PlayerName, outcome_map_to_str
import time
import numpy as np
from math import log2, sqrt
from random import choice
from typing import List, TypeVar
from copy import deepcopy

EXPLORE_CONST = 1.414  # sqrt(2) is the theoretical choice
TIME_BUDGET_S = 1 # How long to give the search to run, in seconds

T = TypeVar('T', bound='Node')

class Node():
  def __init__(self: T, state: GameState, player: PlayerName, move: GameMove = None, parent: T = None):
    self.state = deepcopy(state)
    self.player = player
    self.parent = parent
    self.move = move
    self.move_history = []
    if self.parent is not None:
      self.move_history = deepcopy(self.parent.move_history)
      self.move_history.append(move)
    self.children: List[T] = [] # List[Node]
    # dict of dicts. Maps PlayerName to Outcome to int
    self.outcomes = {p: {o: 0 for o in Outcome}
                     for p in state.get_players()}
    self.num_playouts = 0
    self.utility = 0

  def __str__(self):
    return f"move: {self.move} | " + \
      f"move history: {self.move_history} | " + \
      f"num children: {len(self.children)} | " + \
      f"outcomes: {outcome_map_to_str(self.outcomes)} | " + \
      f"num_playouts: {self.num_playouts} | " + \
      f"player: {self.player} | " + \
      f"parent: [{self.parent}]"

  def print_compact(self):
    print(f"{self.utility} (or {self.outcomes[self.player][Outcome.WIN]}) / {self.num_playouts} | {self.move_history}")
    for child in self.children:
      child.print_compact()

  def ucb1(self):
    if self.num_playouts == 0:
      return np.inf
    # outcomes = self.outcomes[self.player]
    print(f"In ucb1, to_move is: {self.state.to_move()}")
    # if self.player != self.state.to_move():
    #   utility = self.outcomes[self.state.to_move()][Outcome.WIN]
    # else:
    #   utility = -self.outcomes[self.state.other_player][Outcome.WIN]

    utility = self.utility
    # utility = self.outcomes[self.player][Outcome.WIN]
    if self.parent is None:
      raise ValueError("ucb1 called on parent node!")
      # print(f"In ucb1, self is: {self}")
      # return utility / self.num_playouts

    return utility / self.num_playouts \
      + EXPLORE_CONST * sqrt( log2(self.parent.num_playouts)/self.num_playouts )

def select(tree: Node):
  while len(tree.children) != 0:
    print(f"In select(), children's to_moves: {[c.state.to_move() for c in tree.children]}")
    max_ucb1_value = max([c.ucb1() for c in tree.children])
    
    # break ties randomly
    max_nodes = [n for n in tree.children if n.ucb1() == max_ucb1_value]
    selected_node = choice(max_nodes)

    tree = selected_node
  
  return tree


def expand(leaf):
  if leaf.state.is_terminal():
    print(f"At terminal node. Returning leaf from expand(): {leaf}")
    return leaf
  
  moves = leaf.state.get_moves()
  print(f"Received {len(moves)} moves from state: {moves}")
  children = [Node(deepcopy(leaf.state).play(move), leaf.player, move, leaf) for move in moves]
  leaf.children = children
  print(f"In expand(), leaf has {len(leaf.children)} children right now. leaf: {leaf}")
  expanded_node = choice(leaf.children)
  return expanded_node


def simulate(node: Node):
  state = deepcopy(node.state)
  # TODO: terminate playout early sometimes?
  while not state.is_terminal():
    move = choice(state.get_moves())
    state = state.play(move)
  
  return state.get_outcome()

def back_propogate(result: OutcomeMap, node: Node):
  reward = 1 if result[node.state.other_player][Outcome.WIN] == 1 else 0
  while node is not None:
    node.num_playouts += 1

    node.utility += reward
    reward = 0 if reward == 1 else 1
    for player_name in result:
      for outcome in result[player_name]:
        node.outcomes[player_name][outcome] += result[player_name][outcome]
    if node.parent is None:
      return node
    node = node.parent

def most_playouts_move(tree: Node) -> GameMove:
  # children_nodes = tree.children.values()
  max_playouts = max([c.num_playouts for c in tree.children])
  print(f"max_playouts: {max_playouts} | children's num_playouts: ",
    [c.num_playouts for c in tree.children])
  max_nodes = [n for n in tree.children if n.num_playouts == max_playouts]
  chosen_node = choice(max_nodes)
  return chosen_node.move
  
def mcts(state: GameState):
  start_time = time.time()
  player_name = state.to_move()
  tree = Node(state, player_name)
  print(f"initial tree: {tree}")
  count = 0
  while time.time() - start_time < TIME_BUDGET_S:
  # while count < 10:
    leaf = select(tree)
    print(f"leaf: {leaf}")
    child = expand(leaf)
    print(f"child: {child}")
    print(f"tree after expand(): {tree}")
    result = simulate(child)
    foo = back_propogate(result, child)
    print(f"tree after back_propogate: {tree}")
    for child in tree.children:
      print(f"move: {child.move} | num_playouts: {child.num_playouts} | utility: {child.utility} | player outcome wins: {child.outcomes[child.player][Outcome.WIN]}")
    count += 1
  print("AFTER LOOP")
  print(f"foo: {foo}")
  print(f"tree: {tree}")
  tree.print_compact()
  return most_playouts_move(tree)
  

