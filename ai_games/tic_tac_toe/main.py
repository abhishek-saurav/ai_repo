import random
from colorama import init, Fore, Style

init(autoreset=True)

# =========================================
# CONSTANTS
# =========================================
win_conditions = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
    (0, 4, 8), (2, 4, 6),              # Diagonal
]


def display_board(board):
    """Prints the Tic-Tac-Toe board in color."""
    print()

    def colored(cell):
        if cell == "X":
            return Fore.RED + cell + Style.RESET_ALL
        elif cell == "O":
            return Fore.BLUE + cell + Style.RESET_ALL
        else:
            return Fore.YELLOW + cell + Style.RESET_ALL

    print(" " + colored(board[0]) + " | " + colored(board[1]) + " | " + colored(board[2]))
    print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
    print(" " + colored(board[3]) + " | " + colored(board[4]) + " | " + colored(board[5]))
    print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
    print(" " + colored(board[6]) + " | " + colored(board[7]) + " | " + colored(board[8]))
    print()


def player_choice():
    """Asks player to choose X or O and returns (player_symbol, ai_symbol)."""
    symbol = ""
    while symbol not in ["X", "O"]:
        symbol = input(Fore.GREEN + "Do you want to be X or O? " + Style.RESET_ALL).strip().upper()
    return ("X", "O") if symbol == "X" else ("O", "X")


def player_move(board, symbol):
    """Asks for a move (1-9), validates the spot is empty, then places the symbol."""
    move = -1
    while move not in range(1, 10) or not board[move - 1].isdigit():
        try:
            move = int(input(Fore.GREEN + "Enter your move (1-9): " + Style.RESET_ALL))
            if move not in range(1, 10) or not board[move - 1].isdigit():
                print(Fore.RED + "Invalid move. Please try again." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Please enter a number between 1 and 9." + Style.RESET_ALL)
    board[move - 1] = symbol


def ai_move(board, ai_symbol, player_symbol):
    """AI strategy: win if possible, block player, else pick randomly."""
    # Try to win in 1 move
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = ai_symbol
            if check_win(board_copy, ai_symbol):
                board[i] = ai_symbol
                return

    # Block player's winning move
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = player_symbol
            if check_win(board_copy, player_symbol):
                board[i] = ai_symbol
                return

    # Prefer center
    if board[4].isdigit():
        board[4] = ai_symbol
        return

    # Prefer corners
    corners = [i for i in [0, 2, 6, 8] if board[i].isdigit()]
    if corners:
        board[random.choice(corners)] = ai_symbol
        return

    # Random remaining spot
    possible_moves = [i for i in range(9) if board[i].isdigit()]
    board[random.choice(possible_moves)] = ai_symbol


def check_win(board, symbol):
    """Returns True if the given symbol has a winning combination."""
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] == symbol:
            return True
    return False


def check_full(board):
    """Returns True if no empty spots remain on the board."""
    return all(not spot.isdigit() for spot in board)


def tic_tac_toe():
    print(Fore.CYAN + Style.BRIGHT + "=" * 30)
    print("   Welcome to Tic-Tac-Toe!")
    print("=" * 30 + Style.RESET_ALL)

    player_name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL).strip() or "Player"

    wins = losses = ties = 0

    while True:
        board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        player_symbol, ai_symbol = player_choice()
        turn = "Player"
        game_on = True

        while game_on:
            display_board(board)

            if turn == "Player":
                player_move(board, player_symbol)
                if check_win(board, player_symbol):
                    display_board(board)
                    print(Fore.GREEN + Style.BRIGHT + f"Congratulations, {player_name}! You won! 🎉" + Style.RESET_ALL)
                    wins += 1
                    game_on = False
                elif check_full(board):
                    display_board(board)
                    print(Fore.YELLOW + "It's a tie!" + Style.RESET_ALL)
                    ties += 1
                    game_on = False
                else:
                    turn = "AI"
            else:
                print(Fore.BLUE + "AI is thinking..." + Style.RESET_ALL)
                ai_move(board, ai_symbol, player_symbol)
                if check_win(board, ai_symbol):
                    display_board(board)
                    print(Fore.RED + "AI has won the game! Better luck next time." + Style.RESET_ALL)
                    losses += 1
                    game_on = False
                elif check_full(board):
                    display_board(board)
                    print(Fore.YELLOW + "It's a tie!" + Style.RESET_ALL)
                    ties += 1
                    game_on = False
                else:
                    turn = "Player"

        print(Fore.MAGENTA + f"\nScore — {player_name}: {wins}  AI: {losses}  Ties: {ties}" + Style.RESET_ALL)

        play_again = input(Fore.CYAN + "Play again? (yes/no): " + Style.RESET_ALL).strip().lower()
        if play_again != "yes":
            print(Fore.CYAN + f"Thanks for playing, {player_name}! Final score — Wins: {wins}, Losses: {losses}, Ties: {ties}" + Style.RESET_ALL)
            break


if __name__ == "__main__":
    tic_tac_toe()
