import time
import random
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore, Style
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

init(autoreset=True)

try:
    df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "Error: 'imdb_top_1000.csv' not found. Place it in the same folder.")
    raise SystemExit

df = df.dropna(subset=["Genre", "Overview"]).reset_index(drop=True)

df["features"] = df["Genre"].fillna("") + " " + df["Overview"].fillna("")
tfidf = TfidfVectorizer(stop_words="english")
tfidf_mat = tfidf.fit_transform(df["features"])

genres = sorted({g.strip() for xs in df["Genre"].str.split(", ") for g in xs})

print(Fore.CYAN + Style.BRIGHT + "=" * 50)
print("   AI Movie Recommendation Assistant")
print("=" * 50 + Style.RESET_ALL)

player_name = input(Fore.YELLOW + "\nWhat's your name? ").strip()
if player_name == "":
    player_name = "Friend"

print(Fore.GREEN + "\nGreat to meet you, " + player_name + "! Let's find your next favourite film.\n")

running = True

while running:

    print(Fore.MAGENTA + "Choose recommendation type:")
    print(Fore.CYAN + "  1. AI-based recommendation")
    print(Fore.CYAN + "  2. Random recommendation")

    choice = ""
    while choice not in ["1", "2"]:
        choice = input(Fore.YELLOW + "Enter 1 or 2: ").strip()

    if choice == "2":
        print(Fore.BLUE + "\nPicking a random movie", end="", flush=True)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print()

        random_idx = random.randint(0, len(df) - 1)
        movie_row = df.iloc[random_idx]

        ov_text = str(movie_row.get("Overview", ""))
        pol = TextBlob(ov_text).sentiment.polarity

        if pol > 0:
            sentiment_label = "Positive"
        elif pol < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        print(Fore.YELLOW + "\nRandom Pick for " + player_name + ":\n")
        print(Fore.CYAN + "  Title       : " + Fore.WHITE + str(movie_row["Series_Title"]))
        print(Fore.GREEN + "  Genre       : " + Fore.WHITE + str(movie_row.get("Genre", "N/A")))
        print(Fore.GREEN + "  IMDB Rating : " + Fore.WHITE + str(movie_row.get("IMDB_Rating", "N/A")))
        print(Fore.GREEN + "  Sentiment   : " + Fore.WHITE + sentiment_label + " (Polarity: " + str(round(pol, 2)) + ")")
        overview_text = ov_text[:120] + "..." if len(ov_text) > 120 else ov_text
        print(Fore.GREEN + "  Overview    : " + Fore.WHITE + overview_text)
        print()

    else:
        print(Fore.GREEN + "\nAvailable Genres:")
        genre_count = 1
        for g in genres:
            print(Fore.CYAN + "  " + str(genre_count) + ". " + g)
            genre_count = genre_count + 1
        print()

        genre = None
        while genre is None:
            x = input(Fore.YELLOW + "Enter genre number or name (or 'any'): ").strip()
            if x.lower() == "any":
                genre = ""
            elif x.isdigit() and 1 <= int(x) <= len(genres):
                genre = genres[int(x) - 1]
            else:
                x_titled = x.title()
                if x_titled in genres:
                    genre = x_titled
                else:
                    print(Fore.RED + "Invalid. Try again or type 'any' to skip.\n")

        mood = input(Fore.YELLOW + "Describe your mood: ").strip()

        print(Fore.BLUE + "\nAnalyzing mood", end="", flush=True)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print()

        if mood:
            mp = TextBlob(mood).sentiment.polarity
        else:
            mp = 0

        if mp > 0:
            md = "positive"
        elif mp < 0:
            md = "negative"
        else:
            md = "neutral"

        print(Fore.GREEN + "Mood detected: " + md + " (Polarity: " + str(round(mp, 2)) + ")\n")

        rating = None
        rating_done = False
        while not rating_done:
            x = input(Fore.YELLOW + "Minimum IMDB rating (7.6-9.3) or 'skip': ").strip()
            if x.lower() == "skip":
                rating_done = True
            else:
                try:
                    r = float(x)
                    if 7.6 <= r <= 9.3:
                        rating = r
                        rating_done = True
                    else:
                        print(Fore.RED + "Out of range (7.6-9.3). Try again.\n")
                except ValueError:
                    print(Fore.RED + "Not a valid number. Try again.\n")

        print(Fore.BLUE + "\nFinding best matches for " + player_name, end="", flush=True)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)
        print()

        pool = df.copy()

        if genre:
            pool = pool[pool["Genre"].str.contains(genre, case=False, na=False)]

        if rating is not None:
            pool = pool[pool["IMDB_Rating"] >= rating]

        if pool.empty:
            print(Fore.RED + "\nNo movies found with those filters. Try relaxing genre or rating.\n")
        else:
            query_doc = genre + " " + mood
            query_vec = tfidf.transform([query_doc])

            candidate_indices = pool.index.tolist()
            candidate_matrix = tfidf_mat[candidate_indices]
            sims = cosine_similarity(query_vec, candidate_matrix).flatten()

            sorted_local_indices = sims.argsort()[::-1]
            top_local = sorted_local_indices[:25]

            results = []
            need_pos = bool(mood)

            for local_idx in top_local:
                row = pool.iloc[local_idx]
                ov_text = str(row.get("Overview", ""))
                pol = TextBlob(ov_text).sentiment.polarity
                if need_pos and pol < 0:
                    continue
                results.append(row)
                if len(results) == 5:
                    break

            if len(results) == 0:
                print(Fore.RED + "\nNo suitable movies found. Try different filters.\n")
            else:
                print(Fore.YELLOW + "\nAI Recommendations for " + player_name + ":\n")
                i = 1
                for row in results:
                    ov_text = str(row.get("Overview", ""))
                    pol = TextBlob(ov_text).sentiment.polarity
                    if pol > 0:
                        sentiment_label = "Positive"
                    elif pol < 0:
                        sentiment_label = "Negative"
                    else:
                        sentiment_label = "Neutral"
                    print(Fore.CYAN + str(i) + ". " + Fore.YELLOW + str(row["Series_Title"]))
                    print("     " + Fore.GREEN + "Genre       : " + Fore.WHITE + str(row.get("Genre", "N/A")))
                    print("     " + Fore.GREEN + "IMDB Rating : " + Fore.WHITE + str(row.get("IMDB_Rating", "N/A")))
                    print("     " + Fore.GREEN + "Sentiment   : " + Fore.WHITE + sentiment_label + " (Polarity: " + str(round(pol, 2)) + ")")
                    overview_text = ov_text[:120] + "..." if len(ov_text) > 120 else ov_text
                    print("     " + Fore.GREEN + "Overview    : " + Fore.WHITE + overview_text)
                    print()
                    i = i + 1

    again = input(Fore.YELLOW + "Would you like another recommendation? (yes/no): ").strip().lower()
    if again != "yes":
        print(Fore.GREEN + "\nEnjoy your movie, " + player_name + "!\n")
        running = False
    print()

