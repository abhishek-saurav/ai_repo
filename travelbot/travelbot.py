import re
import random
import json
import os
import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

destinations = {
    "beaches":   ["Bali", "Maldives", "Phuket", "Santorini", "Cancun"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas", "Patagonia", "Dolomites"],
    "cities":    ["Tokyo", "Paris", "New York", "Barcelona", "Singapore"],
    "deserts":   ["Sahara", "Wadi Rum", "Atacama", "Namib", "Sonoran"],
    "forests":   ["Amazon Rainforest", "Black Forest", "Daintree Rainforest", "Tongass", "Monteverde"],
}

jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because of all their hot spots!",
    "I told my suitcase there would be no vacation. Now I'm dealing with emotional baggage.",
    "Why did the map go to school? To improve its direction!",
]

weather_data = {
    "bali":       {"temp": "29°C", "condition": "Sunny with light breezes"},
    "maldives":   {"temp": "31°C", "condition": "Clear skies, perfect beach weather"},
    "phuket":     {"temp": "33°C", "condition": "Hot and humid"},
    "tokyo":      {"temp": "18°C", "condition": "Partly cloudy"},
    "paris":      {"temp": "14°C", "condition": "Light showers"},
    "new york":   {"temp": "10°C", "condition": "Overcast with wind"},
    "swiss alps": {"temp": "-2°C", "condition": "Heavy snowfall"},
    "himalayas":  {"temp": "-10°C", "condition": "Freezing, clear at high altitudes"},
    "barcelona":  {"temp": "22°C", "condition": "Sunny and warm"},
    "singapore":  {"temp": "30°C", "condition": "Tropical, expect afternoon showers"},
}

city_timezones = {
    "tokyo":     9,
    "paris":     1,
    "new york": -5,
    "barcelona": 1,
    "singapore": 8,
    "bali":      8,
    "london":    0,
    "dubai":     4,
    "sydney":   10,
}

travel_news = [
    "Visa-free travel expanded between 20 new country pairs this month.",
    "Tokyo named the safest city for solo travelers in 2026.",
    "Budget airlines launching new routes across Southeast Asia this summer.",
    "Maldives opens new eco-resort built from recycled materials.",
    "Singapore Changi Airport wins World Best Airport again.",
]

HISTORY_FILE = "conversation_history.json"

if os.path.exists(HISTORY_FILE):
    f = open(HISTORY_FILE, "r")
    history = json.load(f)
    f.close()
else:
    history = {}

print(Fore.WHITE + Back.BLUE + " TravelBot - Your AI Travel Companion " + Style.RESET_ALL)
print(Fore.CYAN + "TravelBot: Hello! I am TravelBot. Let me help plan your next adventure!")

name = input(Fore.YELLOW + "What is your name? ").strip()
if name == "":
    name = "Traveler"

if name in history and len(history[name]) > 1:
    print(Fore.GREEN + "TravelBot: Welcome back, " + name + "! Great to see you again.")
else:
    print(Fore.GREEN + "TravelBot: Nice to meet you, " + name + "!")

if name not in history:
    history[name] = []

print(Fore.WHITE + Back.BLUE + " What I Can Do " + Style.RESET_ALL)
print(Fore.GREEN + "  - recommend / suggest : Get a travel destination")
print(Fore.GREEN + "  - packing / pack      : Get a packing list")
print(Fore.GREEN + "  - weather             : Check weather at a destination")
print(Fore.GREEN + "  - time                : Find local time in a city")
print(Fore.GREEN + "  - news                : Read latest travel news")
print(Fore.GREEN + "  - joke                : Hear a travel joke")
print(Fore.GREEN + "  - history             : View chat history")
print(Fore.GREEN + "  - help                : Show this menu")
print(Fore.GREEN + "  - exit / bye          : End the conversation")
print()

running = True

while running:
    user_input = input(Fore.YELLOW + "\n" + name + ": ").strip()

    if user_input == "":
        continue

    user_input_clean = re.sub(r"\s+", " ", user_input.strip().lower())

    history[name].append({"role": "user", "text": user_input_clean})

    if re.search(r"recommend|suggest|destination", user_input_clean):
        print(Fore.CYAN + "TravelBot: Beaches, mountains, cities, deserts, or forests?")
        getting_rec = True
        while getting_rec:
            pref_raw = input(Fore.YELLOW + "You: ")
            pref = re.sub(r"\s+", " ", pref_raw.strip().lower())
            if pref in destinations:
                suggestion = random.choice(destinations[pref])
                print(Fore.GREEN + "TravelBot: How about " + suggestion + "?")
                print(Fore.CYAN + "TravelBot: Do you like it? (yes / no)")
                ans_raw = input(Fore.YELLOW + "You: ")
                answer = re.sub(r"\s+", " ", ans_raw.strip().lower())
                if re.search(r"\byes\b", answer):
                    print(Fore.GREEN + "TravelBot: Awesome! Enjoy your trip to " + suggestion + "!")
                    getting_rec = False
                else:
                    print(Fore.RED + "TravelBot: Let's try another one.")
            else:
                print(Fore.RED + "TravelBot: Sorry, I don't have that type. Try: beaches, mountains, cities, deserts, forests.")
                getting_rec = False

    elif re.search(r"pack|packing|luggage|suitcase", user_input_clean):
        print(Fore.CYAN + "TravelBot: What type of trip? (beach / mountain / city / desert / forest)")
        trip_type_raw = input(Fore.YELLOW + "You: ")
        trip_type = re.sub(r"\s+", " ", trip_type_raw.strip().lower())
        print(Fore.CYAN + "TravelBot: Where are you headed?")
        location_raw = input(Fore.YELLOW + "You: ")
        location = re.sub(r"\s+", " ", location_raw.strip().lower())
        print(Fore.CYAN + "TravelBot: How many days?")
        days = input(Fore.YELLOW + "You: ").strip()
        print(Fore.GREEN + "TravelBot: Packing list for " + days + " days in " + location.title() + ":")
        if "beach" in trip_type:
            print(Fore.GREEN + "  - Sunscreen SPF 50+")
            print(Fore.GREEN + "  - Swimwear")
            print(Fore.GREEN + "  - Flip-flops")
            print(Fore.GREEN + "  - Beach towel")
            print(Fore.GREEN + "  - Sunglasses")
        elif "mountain" in trip_type:
            print(Fore.GREEN + "  - Thermal layers")
            print(Fore.GREEN + "  - Waterproof jacket")
            print(Fore.GREEN + "  - Hiking boots")
            print(Fore.GREEN + "  - Gloves and beanie")
            print(Fore.GREEN + "  - First-aid kit")
        elif "city" in trip_type:
            print(Fore.GREEN + "  - Comfortable walking shoes")
            print(Fore.GREEN + "  - Smart casual clothes")
            print(Fore.GREEN + "  - Day backpack")
            print(Fore.GREEN + "  - Portable charger")
        elif "desert" in trip_type:
            print(Fore.GREEN + "  - High SPF sunscreen")
            print(Fore.GREEN + "  - Wide brim hat")
            print(Fore.GREEN + "  - Light breathable clothing")
            print(Fore.GREEN + "  - Plenty of water bottles")
        elif "forest" in trip_type:
            print(Fore.GREEN + "  - Insect repellent")
            print(Fore.GREEN + "  - Waterproof boots")
            print(Fore.GREEN + "  - Rain poncho")
            print(Fore.GREEN + "  - Torch and headlamp")
        else:
            print(Fore.GREEN + "  - Pack versatile clothes")
            print(Fore.GREEN + "  - Bring chargers and adapters")
            print(Fore.GREEN + "  - Check the weather forecast")
            print(Fore.GREEN + "  - Carry a copy of your documents")

    elif re.search(r"weather|climate|temperature|forecast", user_input_clean):
        print(Fore.CYAN + "TravelBot: Which destination do you want weather for?")
        city_raw = input(Fore.YELLOW + "You: ")
        city = re.sub(r"\s+", " ", city_raw.strip().lower())
        if city in weather_data:
            w = weather_data[city]
            print(Fore.GREEN + "TravelBot: Weather in " + city.title() + ":")
            print(Fore.GREEN + "  Temperature : " + w["temp"])
            print(Fore.GREEN + "  Condition   : " + w["condition"])
        else:
            print(Fore.RED + "TravelBot: No weather data for " + city.title() + ". Try: Bali, Tokyo, Paris, etc.")

    elif re.search(r"time|local time|timezone", user_input_clean):
        print(Fore.CYAN + "TravelBot: Which city local time do you want?")
        city_raw = input(Fore.YELLOW + "You: ")
        city = re.sub(r"\s+", " ", city_raw.strip().lower())
        if city in city_timezones:
            offset = city_timezones[city]
            utc_now = datetime.datetime.utcnow()
            total_minutes = int(utc_now.hour * 60 + utc_now.minute + offset * 60)
            local_hour = (total_minutes // 60) % 24
            local_min = total_minutes % 60
            if offset >= 0:
                sign = "+"
            else:
                sign = ""
            print(Fore.GREEN + "TravelBot: Local time in " + city.title() + ": " + str(local_hour).zfill(2) + ":" + str(local_min).zfill(2) + " (UTC" + sign + str(offset) + ")")
        else:
            print(Fore.RED + "TravelBot: No timezone data for " + city.title() + ". Try: Tokyo, Paris, New York, London, Dubai.")

    elif re.search(r"news|latest|update|headline", user_input_clean):
        print(Fore.WHITE + Back.BLUE + " Latest Travel News " + Style.RESET_ALL)
        headlines = random.sample(travel_news, min(4, len(travel_news)))
        count = 1
        for headline in headlines:
            print(Fore.CYAN + "  " + str(count) + ". " + headline)
            count = count + 1

    elif re.search(r"joke|funny|laugh|humor", user_input_clean):
        joke = random.choice(jokes)
        print(Fore.YELLOW + "TravelBot: " + joke)

    elif re.search(r"history|previous|past chat", user_input_clean):
        user_hist = history.get(name, [])
        if len(user_hist) == 0:
            print(Fore.RED + "TravelBot: No chat history yet.")
        else:
            print(Fore.WHITE + Back.BLUE + " Chat History - " + name + " " + Style.RESET_ALL)
            start = len(user_hist) - 20
            if start < 0:
                start = 0
            for i in range(start, len(user_hist)):
                entry = user_hist[i]
                if entry["role"] == "user":
                    print(Fore.GREEN + "  You       : " + Fore.WHITE + entry["text"])
                else:
                    print(Fore.CYAN + "  TravelBot : " + Fore.WHITE + entry["text"])

    elif re.search(r"help|what can you do|commands", user_input_clean):
        print(Fore.WHITE + Back.BLUE + " What I Can Do " + Style.RESET_ALL)
        print(Fore.GREEN + "  - recommend / suggest : Get a travel destination")
        print(Fore.GREEN + "  - packing / pack      : Get a packing list")
        print(Fore.GREEN + "  - weather             : Check weather at a destination")
        print(Fore.GREEN + "  - time                : Find local time in a city")
        print(Fore.GREEN + "  - news                : Read latest travel news")
        print(Fore.GREEN + "  - joke                : Hear a travel joke")
        print(Fore.GREEN + "  - history             : View chat history")
        print(Fore.GREEN + "  - exit / bye          : End the conversation")

    elif re.search(r"exit|bye|goodbye|quit", user_input_clean):
        history[name].append({"role": "bot", "text": "Goodbye!"})
        f = open(HISTORY_FILE, "w")
        json.dump(history, f, indent=2)
        f.close()
        print(Fore.CYAN + "TravelBot: Safe travels, " + name + "! Come back anytime. Goodbye!")
        running = False

    else:
        print(Fore.RED + "TravelBot: I did not quite catch that. Could you rephrase? Type help to see what I can do.")

    f = open(HISTORY_FILE, "w")
    json.dump(history, f, indent=2)
    f.close()
