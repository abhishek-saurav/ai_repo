import time
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore

init(autoreset=True)

try:
    df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "Error: The file 'imdb_top_1000.csv' was not found.")
    raise SystemExit

genres = sorted({g.strip() for xs in df["Genre"].dropna().str.split(", ") for g in xs})

print(Fore.BLUE + "Welcome to your Personal Movie Recommendation Assistant!\n")

name = input(Fore.YELLOW + "What's your name? ").strip()
if name == "":
    name = "Friend"

print(Fore.GREEN + "\nGreat to meet you, " + name + "!\n")
print(Fore.BLUE + "Let's find the perfect movie for you!\n")

print(Fore.GREEN + "\nAvailable Genres:")
genre_count = 1
for g in genres:
    print(Fore.CYAN + "  " + str(genre_count) + ". " + g)
    genre_count = genre_count + 1
print()

genre = None
while genre is None:
    x = input(Fore.YELLOW + "Enter genre number or name: ").strip()
    if x.isdigit() and 1 <= int(x) <= len(genres):
        genre = genres[int(x) - 1]
    else:
        x_titled = x.title()
        if x_titled in genres:
            genre = x_titled
        else:
            print(Fore.RED + "Invalid input. Try again.\n")

mood = input(Fore.YELLOW + "How do you feel today? (Describe your mood): ").strip()

print(Fore.BLUE + "\nAnalyzing mood", end="", flush=True)
print(Fore.YELLOW + ".", end="", flush=True)
time.sleep(0.5)
print(Fore.YELLOW + ".", end="", flush=True)
time.sleep(0.5)
print(Fore.YELLOW + ".", end="", flush=True)
time.sleep(0.5)

mp = TextBlob(mood).sentiment.polarity

if mp > 0:
    md = "positive"
elif mp < 0:
    md = "negative"
else:
    md = "neutral"

print(Fore.GREEN + "\nYour mood is " + md + " (Polarity: " + str(round(mp, 2)) + ").\n")

rating = None
rating_done = False
while not rating_done:
    x = input(Fore.YELLOW + "Enter minimum IMDB rating (7.6-9.3) or 'skip': ").strip()
    if x.lower() == "skip":
        rating_done = True
    else:
        try:
            r = float(x)
            if 7.6 <= r <= 9.3:
                rating = r
                rating_done = True
            else:
                print(Fore.RED + "Rating out of range. Try again.\n")
        except ValueError:
            print(Fore.RED + "Invalid input. Try again.\n")

print(Fore.BLUE + "\nFinding movies for " + name, end="", flush=True)
print(Fore.YELLOW + ".", end="", flush=True)
time.sleep(0.5)
print(Fore.YELLOW + ".", end="", flush=True)
time.sleep(0.5)
print(Fore.YELLOW + ".", end="", flush=True)
time.sleep(0.5)
print()

getting_recs = True

while getting_recs:
    d = df.copy()

    if genre:
        d = d[d["Genre"].str.contains(genre, case=False, na=False)]

    if rating is not None:
        d = d[d["IMDB_Rating"] >= rating]

    if d.empty:
        print(Fore.RED + "\nNo suitable movie recommendations found.\n")
    else:
        d = d.sample(frac=1).reset_index(drop=True)
        need_nonneg = bool(mood)
        recs = []

        for idx in range(len(d)):
            row = d.iloc[idx]
            ov = row.get("Overview")
            if pd.isna(ov):
                continue
            pol = TextBlob(ov).sentiment.polarity
            if (not need_nonneg) or pol >= 0:
                recs.append((row["Series_Title"], pol))
            if len(recs) == 5:
                break

        if len(recs) == 0:
            print(Fore.RED + "\nNo suitable movie recommendations found.\n")
        else:
            print(Fore.YELLOW + "\nAI-Analyzed Movie Recommendations for " + name + ":")
            i = 1
            for title, pol in recs:
                if pol > 0:
                    sentiment = "Positive"
                elif pol < 0:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"
                print(Fore.CYAN + str(i) + ". " + title + " (Polarity: " + str(round(pol, 2)) + ", " + sentiment + ")")
                i = i + 1

    a = input(Fore.YELLOW + "\nWould you like more recommendations? (yes/no): ").strip().lower()

    if a == "no":
        print(Fore.GREEN + "\nEnjoy your movie picks, " + name + "!\n")
        getting_recs = False
    elif a == "yes":
        print(Fore.BLUE + "\nFinding more movies", end="", flush=True)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.5)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.5)
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.5)
        print()
    else:
        print(Fore.RED + "Invalid choice. Try again.\n")

