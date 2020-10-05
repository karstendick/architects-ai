from .tictactoe_state import TicTacToeState
from .game_state import PlayerName
from .mcts import mcts
from .trivial_state import TrivialState

def tictactoe_2_human_players():
  print("Hello, architects!")

  state = TicTacToeState()
  while not state.is_terminal():
    moves = state.get_moves()
    to_move = state.to_move
    print("Board: ")
    state.print_board()
    print(f"It's {to_move}'s turn.")
    print("Available moves: ", moves)
    row = input("Input the row of your move: ")
    col = input("Input the col of your move: ")
    state = state.play({'move': (int(row), int(col))})
    
  print("Game over. Outcome: ", state.get_outcome())
  print("Goodbye!")

def tictactoe_against_mcts():
  state = TicTacToeState()
  while not state.is_terminal():
    to_move = state.to_move()
    print("Board: ")
    state.print_board()
    print(f"It's {to_move}'s turn.")
    if to_move == PlayerName('X'):
      moves = state.get_moves()
      print("Available moves: ", moves)
      row = input("Input the row of your move: ")
      col = input("Input the col of your move: ")
      state = state.play({'move': (int(row), int(col))})
    else:
      move = mcts(state)
      print(f"MCTS decided to play move: {move}")
      state = state.play(move)

  print("Board: ")
  state.print_board()
  print("Game over. Outcome: ", state.get_outcome())
  print("Goodbye!")

def trivial_against_mcts():
  state = TrivialState()
  while not state.is_terminal():
    to_move = state.to_move()
    print(f"It's {to_move}'s turn.")
    moves = state.get_moves()
    print("Available moves: ", moves)

    move = mcts(state)
    print(f"MCTS decided to play move: {move}")
    state = state.play(move)
      

  print("Game over. Outcome: ", state.get_outcome())
  print("Goodbye!")

def main():
  tictactoe_against_mcts()

if __name__ == "__main__":
  main()