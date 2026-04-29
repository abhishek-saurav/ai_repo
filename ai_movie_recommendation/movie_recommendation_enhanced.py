import time
import random
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore, Style
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

init(autoreset=True)

# ── Load dataset ───────────────────────────────────────────────────────────────
try:
    df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "Error: 'imdb_top_1000.csv' not found. Place it in the same folder.")
    raise SystemExit

# Keep only rows that have both Genre and Overview
df = df.dropna(subset=["Genre", "Overview"]).reset_index(drop=True)

# ── TF-IDF on combined Genre + Overview ───────────────────────────────────────
df["features"] = df["Genre"].fillna("") + " " + df["Overview"].fillna("")
tfidf     = TfidfVectorizer(stop_words="english")
tfidf_mat = tfidf.fit_transform(df["features"])

# ── Genre list ─────────────────────────────────────────────────────────────────
genres = sorted({g.strip() for xs in df["Genre"].str.split(", ") for g in xs})


# ── Helpers ───────────────────────────────────────────────────────────────────
def dots(label="Processing"):
    print(Fore.BLUE + f"\n{label}", end="", flush=True)
    for _ in range(3):
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
    print()


def senti(p):
    return "Positive 😊" if p > 0 else "Negative 😞" if p < 0 else "Neutral 😐"


def display_movie(row, index=None):
    """Print full details for one movie."""
    pol  = TextBlob(str(row.get("Overview", ""))).sentiment.polarity
    prefix = f"{Fore.CYAN}{index}. " if index else f"{Fore.CYAN}  "
    print(prefix + Fore.YELLOW + Style.BRIGHT + f"🎥 {row['Series_Title']}")
    print(f"     {Fore.GREEN}Genre       : {row.get('Genre', 'N/A')}")
    print(f"     {Fore.GREEN}IMDB Rating : {row.get('IMDB_Rating', 'N/A')}")
    print(f"     {Fore.GREEN}Sentiment   : {senti(pol)} (Polarity: {pol:.2f})")
    overview = str(row.get("Overview", ""))
    if len(overview) > 120:
        overview = overview[:120] + "…"
    print(f"     {Fore.WHITE}Overview    : {overview}")
    print()


# ── Input helpers ─────────────────────────────────────────────────────────────
def get_genre():
    print(Fore.GREEN + "\nAvailable Genres:")
    for i, g in enumerate(genres, 1):
        print(f"  {Fore.CYAN}{i:>2}. {g}")
    print()
    while True:
        x = input(Fore.YELLOW + "Enter genre number or name (or 'any'): ").strip()
        if x.lower() == "any":
            return None
        if x.isdigit() and 1 <= int(x) <= len(genres):
            return genres[int(x) - 1]
        x = x.title()
        if x in genres:
            return x
        print(Fore.RED + "Invalid. Try again or type 'any' to skip.\n")


def get_rating():
    while True:
        x = input(Fore.YELLOW + "Minimum IMDB rating (7.6–9.3) or 'skip': ").strip()
        if x.lower() == "skip":
            return None
        try:
            r = float(x)
            if 7.6 <= r <= 9.3:
                return r
            print(Fore.RED + "Out of range (7.6–9.3). Try again.\n")
        except ValueError:
            print(Fore.RED + "Not a valid number. Try again.\n")


# ── AI Recommendation (TF-IDF + cosine similarity) ────────────────────────────
def ai_recommend(genre, mood, rating, n=5):
    """
    Build a query vector from the user's genre + mood and find the most
    similar movies using cosine similarity, then filter by genre/rating.
    """
    # Filter candidate pool
    pool = df.copy()
    if genre:
        pool = pool[pool["Genre"].str.contains(genre, case=False, na=False)]
    if rating is not None:
        pool = pool[pool["IMDB_Rating"] >= rating]
    if pool.empty:
        return []

    # Build a query document from genre + mood and score it against the full matrix
    query_doc = f"{genre or ''} {mood or ''}"
    query_vec = tfidf.transform([query_doc])

    # Compute cosine similarity only for the candidate rows
    candidate_indices = pool.index.tolist()
    candidate_matrix  = tfidf_mat[candidate_indices]
    sims = cosine_similarity(query_vec, candidate_matrix).flatten()

    # Sort by similarity descending and return top-n rows
    top_local = sims.argsort()[::-1][:n * 3]           # oversample to allow mood filter
    results   = []
    need_pos  = bool(mood)
    for local_idx in top_local:
        row = pool.iloc[local_idx]
        pol = TextBlob(str(row.get("Overview", ""))).sentiment.polarity
        if need_pos and pol < 0:
            continue
        results.append(row)
        if len(results) == n:
            break

    return results


# ── Random Recommendation ─────────────────────────────────────────────────────
def random_recommend():
    """Return one completely random movie from the dataset."""
    return df.sample(1).iloc[0]


# ── Main program ──────────────────────────────────────────────────────────────
def main():
    print(Fore.BLUE + Style.BRIGHT + "=" * 50)
    print("   🎬 AI Movie Recommendation Assistant 🎬")
    print("=" * 50 + Style.RESET_ALL)

    name = input(Fore.YELLOW + "\nWhat's your name? ").strip() or "Friend"
    print(f"\n{Fore.GREEN}Great to meet you, {name}! Let's find your next favourite film.\n")

    while True:
        # ── Choose mode ───────────────────────────────────────────────────────
        print(Fore.MAGENTA + "Choose recommendation type:")
        print(f"  {Fore.CYAN}1. 🤖 AI-based recommendation")
        print(f"  {Fore.CYAN}2. 🎲 Random recommendation")
        choice = ""
        while choice not in ("1", "2"):
            choice = input(Fore.YELLOW + "Enter 1 or 2: ").strip()

        if choice == "2":
            # ── Random mode ───────────────────────────────────────────────────
            dots("Picking a random movie")
            movie = random_recommend()
            print(Fore.YELLOW + f"\n🍿 Random Pick for {name}:\n")
            display_movie(movie)

        else:
            # ── AI mode ───────────────────────────────────────────────────────
            genre  = get_genre()
            mood   = input(Fore.YELLOW + "Describe your mood: ").strip()
            dots("Analyzing mood")
            mp = TextBlob(mood).sentiment.polarity if mood else 0
            md = "positive 😊" if mp > 0 else "negative 😞" if mp < 0 else "neutral 😐"
            print(f"{Fore.GREEN}Mood detected: {md} (Polarity: {mp:.2f})\n")

            rating = get_rating()
            dots(f"Finding best matches for {name}")

            results = ai_recommend(genre=genre, mood=mood, rating=rating, n=5)
            if not results:
                print(Fore.RED + "\nNo movies found with those filters. Try relaxing genre or rating.\n")
            else:
                print(Fore.YELLOW + f"\n🍿 AI Recommendations for {name}:\n")
                for i, row in enumerate(results, 1):
                    display_movie(row, index=i)

        # ── Continue? ─────────────────────────────────────────────────────────
        again = input(Fore.YELLOW + "Would you like another recommendation? (yes/no): ").strip().lower()
        if again != "yes":
            print(Fore.GREEN + f"\nEnjoy your movie, {name}! 🎬🍿\n")
            break
        print()


if __name__ == "__main__":
    main()
