import random
from colorama import init, Fore, Style

init(autoreset=True)

win_conditions = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

print(Fore.CYAN + Style.BRIGHT + "=" * 30)
print("   Welcome to Tic-Tac-Toe!")
print("=" * 30 + Style.RESET_ALL)

player_name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL).strip()
if player_name == "":
    player_name = "Player"

wins = 0
losses = 0
ties = 0

play_again = "yes"

while play_again == "yes":

    board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    symbol = ""
    while symbol not in ["X", "O"]:
        symbol = input(Fore.GREEN + "Do you want to be X or O? " + Style.RESET_ALL).strip().upper()

    if symbol == "X":
        player_symbol = "X"
        ai_symbol = "O"
    else:
        player_symbol = "O"
        ai_symbol = "X"

    turn = "Player"
    game_on = True

    while game_on:

        print()
        if board[0] == "X":
            c0 = Fore.RED + board[0] + Style.RESET_ALL
        elif board[0] == "O":
            c0 = Fore.BLUE + board[0] + Style.RESET_ALL
        else:
            c0 = Fore.YELLOW + board[0] + Style.RESET_ALL

        if board[1] == "X":
            c1 = Fore.RED + board[1] + Style.RESET_ALL
        elif board[1] == "O":
            c1 = Fore.BLUE + board[1] + Style.RESET_ALL
        else:
            c1 = Fore.YELLOW + board[1] + Style.RESET_ALL

        if board[2] == "X":
            c2 = Fore.RED + board[2] + Style.RESET_ALL
        elif board[2] == "O":
            c2 = Fore.BLUE + board[2] + Style.RESET_ALL
        else:
            c2 = Fore.YELLOW + board[2] + Style.RESET_ALL

        if board[3] == "X":
            c3 = Fore.RED + board[3] + Style.RESET_ALL
        elif board[3] == "O":
            c3 = Fore.BLUE + board[3] + Style.RESET_ALL
        else:
            c3 = Fore.YELLOW + board[3] + Style.RESET_ALL

        if board[4] == "X":
            c4 = Fore.RED + board[4] + Style.RESET_ALL
        elif board[4] == "O":
            c4 = Fore.BLUE + board[4] + Style.RESET_ALL
        else:
            c4 = Fore.YELLOW + board[4] + Style.RESET_ALL

        if board[5] == "X":
            c5 = Fore.RED + board[5] + Style.RESET_ALL
        elif board[5] == "O":
            c5 = Fore.BLUE + board[5] + Style.RESET_ALL
        else:
            c5 = Fore.YELLOW + board[5] + Style.RESET_ALL

        if board[6] == "X":
            c6 = Fore.RED + board[6] + Style.RESET_ALL
        elif board[6] == "O":
            c6 = Fore.BLUE + board[6] + Style.RESET_ALL
        else:
            c6 = Fore.YELLOW + board[6] + Style.RESET_ALL

        if board[7] == "X":
            c7 = Fore.RED + board[7] + Style.RESET_ALL
        elif board[7] == "O":
            c7 = Fore.BLUE + board[7] + Style.RESET_ALL
        else:
            c7 = Fore.YELLOW + board[7] + Style.RESET_ALL

        if board[8] == "X":
            c8 = Fore.RED + board[8] + Style.RESET_ALL
        elif board[8] == "O":
            c8 = Fore.BLUE + board[8] + Style.RESET_ALL
        else:
            c8 = Fore.YELLOW + board[8] + Style.RESET_ALL

        print(" " + c0 + " | " + c1 + " | " + c2)
        print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
        print(" " + c3 + " | " + c4 + " | " + c5)
        print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
        print(" " + c6 + " | " + c7 + " | " + c8)
        print()

        if turn == "Player":
            move = -1
            valid_move = False
            while not valid_move:
                try:
                    move = int(input(Fore.GREEN + "Enter your move (1-9): " + Style.RESET_ALL))
                    if move in range(1, 10) and board[move - 1].isdigit():
                        valid_move = True
                    else:
                        print(Fore.RED + "Invalid move. Please try again." + Style.RESET_ALL)
                except ValueError:
                    print(Fore.RED + "Please enter a number between 1 and 9." + Style.RESET_ALL)

            board[move - 1] = player_symbol

            player_won = False
            for a, b, c in win_conditions:
                if board[a] == board[b] == board[c] == player_symbol:
                    player_won = True

            if player_won:
                print()
                if board[0] == "X":
                    d0 = Fore.RED + board[0] + Style.RESET_ALL
                elif board[0] == "O":
                    d0 = Fore.BLUE + board[0] + Style.RESET_ALL
                else:
                    d0 = Fore.YELLOW + board[0] + Style.RESET_ALL
                if board[1] == "X":
                    d1 = Fore.RED + board[1] + Style.RESET_ALL
                elif board[1] == "O":
                    d1 = Fore.BLUE + board[1] + Style.RESET_ALL
                else:
                    d1 = Fore.YELLOW + board[1] + Style.RESET_ALL
                if board[2] == "X":
                    d2 = Fore.RED + board[2] + Style.RESET_ALL
                elif board[2] == "O":
                    d2 = Fore.BLUE + board[2] + Style.RESET_ALL
                else:
                    d2 = Fore.YELLOW + board[2] + Style.RESET_ALL
                if board[3] == "X":
                    d3 = Fore.RED + board[3] + Style.RESET_ALL
                elif board[3] == "O":
                    d3 = Fore.BLUE + board[3] + Style.RESET_ALL
                else:
                    d3 = Fore.YELLOW + board[3] + Style.RESET_ALL
                if board[4] == "X":
                    d4 = Fore.RED + board[4] + Style.RESET_ALL
                elif board[4] == "O":
                    d4 = Fore.BLUE + board[4] + Style.RESET_ALL
                else:
                    d4 = Fore.YELLOW + board[4] + Style.RESET_ALL
                if board[5] == "X":
                    d5 = Fore.RED + board[5] + Style.RESET_ALL
                elif board[5] == "O":
                    d5 = Fore.BLUE + board[5] + Style.RESET_ALL
                else:
                    d5 = Fore.YELLOW + board[5] + Style.RESET_ALL
                if board[6] == "X":
                    d6 = Fore.RED + board[6] + Style.RESET_ALL
                elif board[6] == "O":
                    d6 = Fore.BLUE + board[6] + Style.RESET_ALL
                else:
                    d6 = Fore.YELLOW + board[6] + Style.RESET_ALL
                if board[7] == "X":
                    d7 = Fore.RED + board[7] + Style.RESET_ALL
                elif board[7] == "O":
                    d7 = Fore.BLUE + board[7] + Style.RESET_ALL
                else:
                    d7 = Fore.YELLOW + board[7] + Style.RESET_ALL
                if board[8] == "X":
                    d8 = Fore.RED + board[8] + Style.RESET_ALL
                elif board[8] == "O":
                    d8 = Fore.BLUE + board[8] + Style.RESET_ALL
                else:
                    d8 = Fore.YELLOW + board[8] + Style.RESET_ALL
                print(" " + d0 + " | " + d1 + " | " + d2)
                print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
                print(" " + d3 + " | " + d4 + " | " + d5)
                print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
                print(" " + d6 + " | " + d7 + " | " + d8)
                print()
                print(Fore.GREEN + Style.BRIGHT + "Congratulations, " + player_name + "! You won!")
                wins = wins + 1
                game_on = False
            else:
                board_full = True
                for spot in board:
                    if spot.isdigit():
                        board_full = False
                if board_full:
                    print(Fore.YELLOW + "It's a tie!")
                    ties = ties + 1
                    game_on = False
                else:
                    turn = "AI"

        else:
            print(Fore.BLUE + "AI is thinking...")

            ai_placed = False

            for i in range(9):
                if board[i].isdigit() and not ai_placed:
                    board_copy = list(board)
                    board_copy[i] = ai_symbol
                    win_found = False
                    for a, b, c in win_conditions:
                        if board_copy[a] == board_copy[b] == board_copy[c] == ai_symbol:
                            win_found = True
                    if win_found:
                        board[i] = ai_symbol
                        ai_placed = True

            if not ai_placed:
                for i in range(9):
                    if board[i].isdigit() and not ai_placed:
                        board_copy = list(board)
                        board_copy[i] = player_symbol
                        win_found = False
                        for a, b, c in win_conditions:
                            if board_copy[a] == board_copy[b] == board_copy[c] == player_symbol:
                                win_found = True
                        if win_found:
                            board[i] = ai_symbol
                            ai_placed = True

            if not ai_placed:
                if board[4].isdigit():
                    board[4] = ai_symbol
                    ai_placed = True

            if not ai_placed:
                corners = []
                for i in [0, 2, 6, 8]:
                    if board[i].isdigit():
                        corners.append(i)
                if len(corners) > 0:
                    board[random.choice(corners)] = ai_symbol
                    ai_placed = True

            if not ai_placed:
                possible_moves = []
                for i in range(9):
                    if board[i].isdigit():
                        possible_moves.append(i)
                board[random.choice(possible_moves)] = ai_symbol

            ai_won = False
            for a, b, c in win_conditions:
                if board[a] == board[b] == board[c] == ai_symbol:
                    ai_won = True

            if ai_won:
                print()
                if board[0] == "X":
                    e0 = Fore.RED + board[0] + Style.RESET_ALL
                elif board[0] == "O":
                    e0 = Fore.BLUE + board[0] + Style.RESET_ALL
                else:
                    e0 = Fore.YELLOW + board[0] + Style.RESET_ALL
                if board[1] == "X":
                    e1 = Fore.RED + board[1] + Style.RESET_ALL
                elif board[1] == "O":
                    e1 = Fore.BLUE + board[1] + Style.RESET_ALL
                else:
                    e1 = Fore.YELLOW + board[1] + Style.RESET_ALL
                if board[2] == "X":
                    e2 = Fore.RED + board[2] + Style.RESET_ALL
                elif board[2] == "O":
                    e2 = Fore.BLUE + board[2] + Style.RESET_ALL
                else:
                    e2 = Fore.YELLOW + board[2] + Style.RESET_ALL
                if board[3] == "X":
                    e3 = Fore.RED + board[3] + Style.RESET_ALL
                elif board[3] == "O":
                    e3 = Fore.BLUE + board[3] + Style.RESET_ALL
                else:
                    e3 = Fore.YELLOW + board[3] + Style.RESET_ALL
                if board[4] == "X":
                    e4 = Fore.RED + board[4] + Style.RESET_ALL
                elif board[4] == "O":
                    e4 = Fore.BLUE + board[4] + Style.RESET_ALL
                else:
                    e4 = Fore.YELLOW + board[4] + Style.RESET_ALL
                if board[5] == "X":
                    e5 = Fore.RED + board[5] + Style.RESET_ALL
                elif board[5] == "O":
                    e5 = Fore.BLUE + board[5] + Style.RESET_ALL
                else:
                    e5 = Fore.YELLOW + board[5] + Style.RESET_ALL
                if board[6] == "X":
                    e6 = Fore.RED + board[6] + Style.RESET_ALL
                elif board[6] == "O":
                    e6 = Fore.BLUE + board[6] + Style.RESET_ALL
                else:
                    e6 = Fore.YELLOW + board[6] + Style.RESET_ALL
                if board[7] == "X":
                    e7 = Fore.RED + board[7] + Style.RESET_ALL
                elif board[7] == "O":
                    e7 = Fore.BLUE + board[7] + Style.RESET_ALL
                else:
                    e7 = Fore.YELLOW + board[7] + Style.RESET_ALL
                if board[8] == "X":
                    e8 = Fore.RED + board[8] + Style.RESET_ALL
                elif board[8] == "O":
                    e8 = Fore.BLUE + board[8] + Style.RESET_ALL
                else:
                    e8 = Fore.YELLOW + board[8] + Style.RESET_ALL
                print(" " + e0 + " | " + e1 + " | " + e2)
                print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
                print(" " + e3 + " | " + e4 + " | " + e5)
                print(Fore.CYAN + "---+---+---" + Style.RESET_ALL)
                print(" " + e6 + " | " + e7 + " | " + e8)
                print()
                print(Fore.RED + "AI has won the game! Better luck next time.")
                losses = losses + 1
                game_on = False
            else:
                board_full = True
                for spot in board:
                    if spot.isdigit():
                        board_full = False
                if board_full:
                    print(Fore.YELLOW + "It's a tie!")
                    ties = ties + 1
                    game_on = False
                else:
                    turn = "Player"

    print(Fore.MAGENTA + "\nScore - " + player_name + ": " + str(wins) + "  AI: " + str(losses) + "  Ties: " + str(ties))

    play_again = input(Fore.CYAN + "Play again? (yes/no): " + Style.RESET_ALL).strip().lower()

print(Fore.CYAN + "Thanks for playing, " + player_name + "! Final - Wins: " + str(wins) + ", Losses: " + str(losses) + ", Ties: " + str(ties))

