from typing import Dict, List, NewType, TypeVar
from enum import Enum

class Outcome(Enum):
  LOSS = -1
  TIE = 0
  WIN = 1

GameMove = NewType('GameMove', dict)
PlayerName = NewType('PlayerName', str)

OutcomeMap = Dict[PlayerName, Outcome]

T = TypeVar('T', bound='GameState')

class GameState():
  def get_players(self) -> List[PlayerName]:
    pass
  def get_moves(self) -> List[GameMove]:
    pass
  def is_terminal(self) -> bool:
    pass
  def get_outcome(self) -> OutcomeMap:
    pass
  def to_move(self) -> PlayerName:
    pass
  def play(self: T, move: GameMove) -> T:
    pass
