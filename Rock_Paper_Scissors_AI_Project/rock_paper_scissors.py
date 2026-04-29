import random
from collections import Counter
from colorama import init, Fore, Style

init(autoreset=True)

MOVES = ["rock", "paper", "scissors"]

print(Fore.CYAN + Style.BRIGHT + "=" * 38)
print("   Rock Paper Scissors - AI Edition  ")
print("=" * 38 + Style.RESET_ALL)

player_name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL).strip()
if player_name == "":
    player_name = "Player"

print(Fore.CYAN + "\nSelect AI difficulty / strategy:")
print(Fore.WHITE + "  1. Random (Easy)")
print(Fore.WHITE + "  2. Frequency Analysis (Medium)")
print(Fore.WHITE + "  3. Pattern Recognition (Hard)")

strategy_choice = ""
while strategy_choice not in ["1", "2", "3"]:
    strategy_choice = input(Fore.GREEN + "Enter 1, 2, or 3: " + Style.RESET_ALL).strip()

if strategy_choice == "1":
    strategy_name = "Random (Easy)"
elif strategy_choice == "2":
    strategy_name = "Frequency Analysis (Medium)"
else:
    strategy_name = "Pattern Recognition (Hard)"

print(Fore.CYAN + "\nAI strategy set to: " + strategy_name + "\n")

player_score = 0
ai_score = 0
ties = 0
player_history = []

playing = True

while playing:
    print(Fore.MAGENTA + "Score - " + player_name + ": " + str(player_score) + "  |  AI: " + str(ai_score) + "  |  Ties: " + str(ties))

    player_mv = ""
    while player_mv not in MOVES:
        raw = input(Fore.GREEN + "Your move (rock / paper / scissors): " + Style.RESET_ALL).strip().lower()
        if raw in MOVES:
            player_mv = raw
        else:
            print(Fore.RED + "Invalid input '" + raw + "'. Please type rock, paper, or scissors." + Style.RESET_ALL)

    if strategy_choice == "1":
        ai_mv = random.choice(MOVES)

    elif strategy_choice == "2":
        if len(player_history) == 0:
            ai_mv = random.choice(MOVES)
        else:
            counts = Counter(player_history)
            most_common = counts.most_common(1)[0][0]
            if most_common == "rock":
                ai_mv = "paper"
            elif most_common == "paper":
                ai_mv = "scissors"
            else:
                ai_mv = "rock"

    else:
        if len(player_history) < 3:
            if len(player_history) == 0:
                ai_mv = random.choice(MOVES)
            else:
                counts = Counter(player_history)
                most_common = counts.most_common(1)[0][0]
                if most_common == "rock":
                    ai_mv = "paper"
                elif most_common == "paper":
                    ai_mv = "scissors"
                else:
                    ai_mv = "rock"
        else:
            last_two = (player_history[-2], player_history[-1])
            sequence_table = {}
            for i in range(len(player_history) - 2):
                seq = (player_history[i], player_history[i + 1])
                following = player_history[i + 2]
                if seq not in sequence_table:
                    sequence_table[seq] = Counter()
                sequence_table[seq][following] += 1
            if last_two in sequence_table:
                predicted = sequence_table[last_two].most_common(1)[0][0]
                if predicted == "rock":
                    ai_mv = "paper"
                elif predicted == "paper":
                    ai_mv = "scissors"
                else:
                    ai_mv = "rock"
            else:
                if len(player_history) == 0:
                    ai_mv = random.choice(MOVES)
                else:
                    counts = Counter(player_history)
                    most_common = counts.most_common(1)[0][0]
                    if most_common == "rock":
                        ai_mv = "paper"
                    elif most_common == "paper":
                        ai_mv = "scissors"
                    else:
                        ai_mv = "rock"

    player_history.append(player_mv)

    print()
    print(Fore.YELLOW + "  " + player_name + "  : " + player_mv.capitalize())
    print(Fore.BLUE   + "  AI          : " + ai_mv.capitalize())
    print()

    if player_mv == ai_mv:
        outcome = "tie"
    elif (player_mv == "rock" and ai_mv == "scissors") or (player_mv == "scissors" and ai_mv == "paper") or (player_mv == "paper" and ai_mv == "rock"):
        outcome = "player"
    else:
        outcome = "ai"

    if outcome == "player":
        print(Fore.GREEN + Style.BRIGHT + "  You win! " + ai_mv.capitalize() + " loses to " + player_mv.capitalize() + ".")
        player_score = player_score + 1
    elif outcome == "ai":
        print(Fore.RED + Style.BRIGHT + "  AI wins! " + player_mv.capitalize() + " loses to " + ai_mv.capitalize() + ".")
        ai_score = ai_score + 1
    else:
        print(Fore.YELLOW + Style.BRIGHT + "  It's a tie!")
        ties = ties + 1

    print()

    again = input(Fore.CYAN + "Play another round? (yes / no): " + Style.RESET_ALL).strip().lower()
    if again != "yes":
        playing = False
    print()

print(Fore.CYAN + Style.BRIGHT + "\n--- Final Results ---")
print("  " + player_name + "  : " + str(player_score))
print("  AI            : " + str(ai_score))
print("  Ties          : " + str(ties))

total = player_score + ai_score + ties
if total > 0:
    win_rate = player_score / total * 100
    print("  Win rate      : " + str(round(win_rate, 1)) + "%")

if player_score > ai_score:
    print(Fore.GREEN + "\nWell played, " + player_name + "! You beat the AI!")
elif ai_score > player_score:
    print(Fore.RED + "\nThe AI wins overall. Give it another go!")
else:
    print(Fore.YELLOW + "\nOverall tie - great match!")

