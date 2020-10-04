from .tictactoe_state import TicTacToeState

def main():
  print("Hello, architects!")

  state = TicTacToeState()
  while not state.is_terminal():
    # moves = [v for k, v in state.get_moves()]
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

if __name__ == "__main__":
  main()