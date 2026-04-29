import random
from collections import Counter
from colorama import init, Fore, Style

init(autoreset=True)

MOVES = ["rock", "paper", "scissors"]

# What each move defeats
BEATS = {
    "rock":     "scissors",
    "scissors": "paper",
    "paper":    "rock",
}

EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

# ─── AI Strategies ────────────────────────────────────────────────────────────

def get_ai_move_random(_history):
    """Basic strategy: pick a completely random move."""
    return random.choice(MOVES)


def get_ai_move_frequency(history):
    """
    Frequency analysis: look at the player's most common move and counter it.
    Falls back to random when there is no history yet.
    """
    if not history:
        return get_ai_move_random(history)
    most_common_player_move = Counter(history).most_common(1)[0][0]
    # Return the move that beats the player's most frequent choice
    return next(m for m in MOVES if BEATS[m] == most_common_player_move)


def get_ai_move_pattern(history):
    """
    Pattern recognition: scan the player's move history for the last 2-move
    sequence and predict what they will play next, then counter it.
    Falls back to frequency analysis when not enough data.
    """
    if len(history) < 3:
        return get_ai_move_frequency(history)

    last_two = tuple(history[-2:])

    # Build a table: sequence -> Counter of what followed
    sequence_table = {}
    for i in range(len(history) - 2):
        seq = tuple(history[i:i + 2])
        following = history[i + 2]
        sequence_table.setdefault(seq, Counter())[following] += 1

    if last_two in sequence_table:
        predicted_player_move = sequence_table[last_two].most_common(1)[0][0]
        return next(m for m in MOVES if BEATS[m] == predicted_player_move)

    return get_ai_move_frequency(history)


AI_STRATEGIES = {
    "1": ("Random (Easy)",              get_ai_move_random),
    "2": ("Frequency Analysis (Medium)", get_ai_move_frequency),
    "3": ("Pattern Recognition (Hard)",  get_ai_move_pattern),
}

# ─── Player Input ─────────────────────────────────────────────────────────────

def get_player_move():
    """Prompt the player for a move and validate it."""
    while True:
        raw = input(Fore.GREEN + "Your move (rock / paper / scissors): " + Style.RESET_ALL).strip().lower()
        if raw in MOVES:
            return raw
        print(Fore.RED + f"  Invalid input '{raw}'. Please type rock, paper, or scissors." + Style.RESET_ALL)


# ─── Game Logic ───────────────────────────────────────────────────────────────

def determine_winner(player, ai):
    """Return 'player', 'ai', or 'tie'."""
    if player == ai:
        return "tie"
    return "player" if BEATS[player] == ai else "ai"


def display_round_result(player_move, ai_move, outcome, player_name):
    """Print the round moves and result with colour."""
    print()
    print(Fore.YELLOW + f"  {player_name:<14}: {EMOJI[player_move]}  {player_move.capitalize()}")
    print(Fore.BLUE   + f"  AI            : {EMOJI[ai_move]}  {ai_move.capitalize()}")
    print()
    if outcome == "player":
        print(Fore.GREEN + Style.BRIGHT + f"  ✅  You win! {ai_move.capitalize()} loses to {player_move.capitalize()}.")
    elif outcome == "ai":
        print(Fore.RED   + Style.BRIGHT + f"  ❌  AI wins! {player_move.capitalize()} loses to {ai_move.capitalize()}.")
    else:
        print(Fore.YELLOW + Style.BRIGHT + "  🤝  It's a tie!")
    print()


def choose_ai_strategy():
    """Let the player pick which AI strategy to face."""
    print(Fore.CYAN + "\nSelect AI difficulty / strategy:")
    for key, (name, _) in AI_STRATEGIES.items():
        print(Fore.WHITE + f"  {key}. {name}")
    choice = ""
    while choice not in AI_STRATEGIES:
        choice = input(Fore.GREEN + "Enter 1, 2, or 3: " + Style.RESET_ALL).strip()
    name, fn = AI_STRATEGIES[choice]
    print(Fore.CYAN + f"\nAI strategy set to: {name}\n")
    return fn


# ─── Main Game Loop ───────────────────────────────────────────────────────────

def play_game():
    print(Fore.CYAN + Style.BRIGHT + "=" * 38)
    print("   Rock Paper Scissors — AI Edition  ")
    print("=" * 38 + Style.RESET_ALL)

    player_name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL).strip() or "Player"
    ai_strategy = choose_ai_strategy()

    player_score = 0
    ai_score = 0
    ties = 0
    player_history = []   # full move history used by the AI strategies

    while True:
        print(Fore.MAGENTA + f"Score — {player_name}: {player_score}  |  AI: {ai_score}  |  Ties: {ties}" + Style.RESET_ALL)

        player_mv = get_player_move()
        ai_mv = ai_strategy(player_history)

        player_history.append(player_mv)

        outcome = determine_winner(player_mv, ai_mv)
        display_round_result(player_mv, ai_mv, outcome, player_name)

        if outcome == "player":
            player_score += 1
        elif outcome == "ai":
            ai_score += 1
        else:
            ties += 1

        again = input(Fore.CYAN + "Play another round? (yes / no): " + Style.RESET_ALL).strip().lower()
        if again != "yes":
            break
        print()

    # ── Final summary ──────────────────────────────────────────────────────────
    print(Fore.CYAN + Style.BRIGHT + "\n─── Final Results ───")
    print(f"  {player_name:<14}: {player_score}")
    print(f"  AI            : {ai_score}")
    print(f"  Ties          : {ties}")

    total = player_score + ai_score + ties
    if total > 0:
        print(f"  Win rate      : {player_score / total * 100:.1f}%")

    if player_score > ai_score:
        print(Fore.GREEN + f"\n🏆  Well played, {player_name}! You beat the AI!" + Style.RESET_ALL)
    elif ai_score > player_score:
        print(Fore.RED + "\n🤖  The AI wins overall. Give it another go!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "\n🤝  Overall tie — great match!" + Style.RESET_ALL)


if __name__ == "__main__":
    play_game()
