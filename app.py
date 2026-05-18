# app.py

def print_board(board):
    """Prints the current state of the board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_win(board, player):
    """Checks if the specified player has won the game."""
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Vertical
        (0, 4, 8), (2, 4, 6)             # Diagonal
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def is_board_full(board):
    """Checks if the board is completely full (a draw)."""
    return " " not in board

def play_game():
    """Main game loop."""
    # Initialize a blank board with 9 spaces
    board = [" " for _ in range(9)]
    current_player = "X"
    game_running = True

    print("Welcome to Tic-Tac-Toe!")
    print("Positions are numbered 0-8, starting from the top-left to bottom-right.")

    while game_running:
        print_board(board)
        
        # 1. Get valid input from the user
        while True:
            try:
                move = int(input(f"Player {current_player}, choose a spot (0-8): "))
                if move < 0 or move > 8:
                    print("Invalid number. Please choose a number between 0 and 8.")
                elif board[move] != " ":
                    print("That spot is already taken! Try again.")
                else:
                    break # Valid move, exit the input loop
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # 2. Apply the move
        board[move] = current_player

        # 3. Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            game_running = False
            continue

        # 4. Check for a draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            game_running = False
            continue

        # 5. Switch players for the next turn
        current_player = "O" if current_player == "X" else "X"

# This ensures the game only runs when you execute this script directly
if __name__ == "__main__":
    play_game()