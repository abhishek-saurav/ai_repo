import random
from collections import Counter
from colorama import init, Fore, Style

init(autoreset=True)

MOVES = ["rock", "paper", "scissors"]

# What each move beats
BEATS = {
    "rock":     "scissors",
    "scissors": "paper",
    "paper":    "rock",
}

EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

# ─── AI Strategies ────────────────────────────────────────────────────────────

def ai_random(_history):
    """Basic strategy: pick a random move."""
    return random.choice(MOVES)


def ai_frequency(history):
    """
    Frequency analysis: counter the player's most common move.
    Falls back to random if no history yet.
    """
    if not history:
        return ai_random(history)
    most_common = Counter(history).most_common(1)[0][0]
    # Play the move that beats the player's most common choice
    return next(m for m in MOVES if BEATS[m] == most_common)


def ai_pattern(history):
    """
    Pattern recognition: look for the last 2-move sequence in history
    and predict what the player will play next, then counter it.
    Falls back to frequency analysis if pattern not found.
    """
    if len(history) < 3:
        return ai_frequency(history)

    last_two = tuple(history[-2:])
    # Build a frequency table of what followed each 2-move sequence
    sequence_counts = {}
    for i in range(len(history) - 2):
        seq = tuple(history[i:i + 2])
        nxt = history[i + 2]
        sequence_counts.setdefault(seq, Counter())[nxt] += 1

    if last_two in sequence_counts:
        predicted = sequence_counts[last_two].most_common(1)[0][0]
        return next(m for m in MOVES if BEATS[m] == predicted)

    return ai_frequency(history)


AI_STRATEGIES = {
    "1": ("Random",              ai_random),
    "2": ("Frequency Analysis",  ai_frequency),
    "3": ("Pattern Recognition", ai_pattern),
}

# ─── Game Logic ───────────────────────────────────────────────────────────────

def get_player_move():
    """Prompt and validate the player's move."""
    while True:
        raw = input(Fore.GREEN + "Your move (rock / paper / scissors): " + Style.RESET_ALL).strip().lower()
        if raw in MOVES:
            return raw
        print(Fore.RED + f"Invalid input '{raw}'. Please type rock, paper, or scissors." + Style.RESET_ALL)


def determine_winner(player_move, ai_move_choice):
    """Return 'player', 'ai', or 'tie'."""
    if player_move == ai_move_choice:
        return "tie"
    if BEATS[player_move] == ai_move_choice:
        return "player"
    return "ai"


def display_result(player_move, ai_move_choice, outcome, player_name):
    """Print the round result with colors."""
    print()
    print(Fore.YELLOW + f"  {player_name:<12}: {EMOJI[player_move]}  {player_move.capitalize()}")
    print(Fore.BLUE   + f"  AI          : {EMOJI[ai_move_choice]}  {ai_move_choice.capitalize()}")
    print()
    if outcome == "player":
        print(Fore.GREEN + Style.BRIGHT + f"  ✅  You win this round! {BEATS[player_move].capitalize()} loses to {player_move.capitalize()}.")
    elif outcome == "ai":
        print(Fore.RED   + Style.BRIGHT + f"  ❌  AI wins this round! {BEATS[ai_move_choice].capitalize()} loses to {ai_move_choice.capitalize()}.")
    else:
        print(Fore.YELLOW + Style.BRIGHT + "  🤝  It's a tie!")
    print()


def choose_strategy():
    """Let the player pick the AI's difficulty/strategy."""
    print(Fore.CYAN + "\nChoose AI strategy:")
    for key, (name, _) in AI_STRATEGIES.items():
        print(Fore.WHITE + f"  {key}. {name}")
    choice = ""
    while choice not in AI_STRATEGIES:
        choice = input(Fore.GREEN + "Enter 1, 2, or 3: " + Style.RESET_ALL).strip()
    name, fn = AI_STRATEGIES[choice]
    print(Fore.CYAN + f"AI will use: {name}\n")
    return fn


# ─── Main Game Loop ───────────────────────────────────────────────────────────

def play_game():
    print(Fore.CYAN + Style.BRIGHT + "=" * 35)
    print("   Rock Paper Scissors — AI Edition")
    print("=" * 35 + Style.RESET_ALL)

    player_name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL).strip() or "Player"
    ai_strategy = choose_strategy()

    player_score = ai_score = ties = 0
    player_history = []   # tracks all moves the player has made

    while True:
        print(Fore.MAGENTA + f"Score — {player_name}: {player_score}  AI: {ai_score}  Ties: {ties}" + Style.RESET_ALL)

        player_mv = get_player_move()
        ai_mv = ai_strategy(player_history)

        player_history.append(player_mv)

        outcome = determine_winner(player_mv, ai_mv)
        display_result(player_mv, ai_mv, outcome, player_name)

        if outcome == "player":
            player_score += 1
        elif outcome == "ai":
            ai_score += 1
        else:
            ties += 1

        again = input(Fore.CYAN + "Play another round? (yes/no): " + Style.RESET_ALL).strip().lower()
        if again != "yes":
            break
        print()

    print(Fore.CYAN + Style.BRIGHT + "\n── Final Results ──")
    print(f"  {player_name}: {player_score}")
    print(f"  AI:           {ai_score}")
    print(f"  Ties:         {ties}")

    total = player_score + ai_score + ties
    if total > 0:
        win_rate = player_score / total * 100
        print(f"  Win rate:     {win_rate:.1f}%")

    if player_score > ai_score:
        print(Fore.GREEN + f"\n🏆  Well played, {player_name}! You beat the AI!" + Style.RESET_ALL)
    elif ai_score > player_score:
        print(Fore.RED + "\n🤖  The AI wins overall. Try again!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "\n🤝  Overall tie! Great match." + Style.RESET_ALL)


if __name__ == "__main__":
    play_game()
