from typing import List, TypeVar
from collections import defaultdict
from .game_state import GameMove, GameState, Outcome, OutcomeMap, PlayerName

T = TypeVar('T', bound='GameState')

class TicTacToeState(GameState):
  def __init__(self, num_rows=3, num_cols=3, in_a_row=3):
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.in_a_row = in_a_row
    self.moves = [{'move': (r, c)} for r in range(num_rows)
                         for c in range(num_cols)]
    self._to_move = PlayerName('X')
    self.other_player = PlayerName('O')
    self.board = defaultdict(str)
    self.winning_player = None
    self.losing_player = None

  def get_players(self) -> List[PlayerName]:
    return [PlayerName('X'), PlayerName('O')]

  def get_moves(self) -> List[GameMove]:
    return self.moves

  def to_move(self) -> PlayerName:
    return self._to_move

  def is_terminal(self) -> bool:
    return self.winning_player is not None or len(self.moves) == 0

  def get_outcome(self) -> OutcomeMap:
    if self.winning_player is None:
      return {PlayerName('X'): {Outcome.TIE: 1, Outcome.WIN: 0, Outcome.LOSS: 0},
              PlayerName('O'): {Outcome.TIE: 1, Outcome.WIN: 0, Outcome.LOSS: 0}}
    return {self.winning_player: {Outcome.TIE: 0, Outcome.WIN: 1, Outcome.LOSS: 0},
            self.losing_player: {Outcome.TIE: 0, Outcome.WIN: 0, Outcome.LOSS: 1}}
  
  def k_in_row(self, move, delta_x_y):
    """Return true if there is a line through move on board for player."""
    (delta_x, delta_y) = delta_x_y
    x, y = move
    n = 0  # n is number of moves in row
    while self.board.get((x, y)) == self._to_move:
      n += 1
      x, y = x + delta_x, y + delta_y
    x, y = move
    while self.board.get((x, y)) == self._to_move:
      n += 1
      x, y = x - delta_x, y - delta_y
    n -= 1  # Because we counted move itself twice
    return n >= self.in_a_row

  def check_for_win(self, move):
    if (self.k_in_row(move, (0, 1)) or
          self.k_in_row(move, (1, 0)) or
          self.k_in_row(move, (1, -1)) or
          self.k_in_row(move, (1, 1))):
        self.winning_player = self._to_move
        self.losing_player = self.other_player
  
  def play(self: T, move: GameMove) -> T:
    print(f"received move: {move}. Available moves are: {self.moves}")
    if move not in self.moves:
      raise ValueError("Illegal move!")
    self.moves.remove(move)
    self.board[move['move']] = self._to_move

    self.check_for_win(move['move'])

    self._to_move, self.other_player = self.other_player, self._to_move
    return self
  
  def print_board(self):
    for row in range(self.num_rows):
      row_str = ""
      for col in range(self.num_cols):
        cell = self.board[(row, col)]
        if cell == '':
          cell = ' '
        row_str += cell + "|"
      row_str = row_str.rstrip("|")
      print(row_str)
      if row != self.num_rows - 1:
        print("-+-+-")

