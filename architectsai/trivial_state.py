from typing import List, TypeVar
from .game_state import GameMove, GameState, Outcome, OutcomeMap, PlayerName

T = TypeVar('T', bound='GameState')


class TrivialState(GameState):
  def __init__(self):
    self._to_move = PlayerName('X')
    self.other_player = PlayerName('O')
    self.moves = [{'win':True}, {'win':False}]
    self._is_terminal = False
    self.player_won = False
    self.turns_count = 0
  
  def get_players(self) -> List[PlayerName]:
    return [PlayerName('X'), PlayerName('O')]
  
  def get_moves(self):
    return self.moves
  
  def to_move(self) -> PlayerName:
    return self._to_move
  
  def is_terminal(self) -> bool:
    return self._is_terminal
  
  def get_outcome(self) -> OutcomeMap:
    if self.player_won:
      print("WIN!")
      return {PlayerName('X'): {Outcome.TIE: 0, Outcome.WIN: 1, Outcome.LOSS: 0},
              PlayerName('O'): {Outcome.TIE: 0, Outcome.WIN: 0, Outcome.LOSS: 1}}
    print("LOSS!")
    return {PlayerName('X'): {Outcome.TIE: 0, Outcome.WIN: 0, Outcome.LOSS: 1},
              PlayerName('O'): {Outcome.TIE: 0, Outcome.WIN: 1, Outcome.LOSS: 0}}
  
  def play(self: T, move: GameMove) -> T:
    if move not in self.moves:
      raise ValueError("Illegal move!")
    self.moves.remove(move)
    self.turns_count += 1
    if move['win']:
      self.player_won = True
    self._is_terminal = True
    self._to_move, self.other_player = self.other_player, self._to_move
    return self
