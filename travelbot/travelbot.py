import re
import random
import json
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

# ─── Data ────────────────────────────────────────────────────────────────────

destinations = {
    "beaches": ["Bali", "Maldives", "Phuket", "Santorini", "Cancun"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas", "Patagonia", "Dolomites"],
    "cities": ["Tokyo", "Paris", "New York", "Barcelona", "Singapore"],
    "deserts": ["Sahara", "Wadi Rum", "Atacama", "Namib", "Sonoran"],
    "forests": ["Amazon Rainforest", "Black Forest", "Daintree Rainforest", "Tongass", "Monteverde"],
}

jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because of all their hot spots!",
    "I told my suitcase there would be no vacation this year. Now I'm dealing with emotional baggage.",
    "Why did the map go to school? To improve its direction!",
]

# Simulated weather data per destination
weather_data = {
    "bali":        {"temp": "29°C", "condition": "Sunny with light breezes"},
    "maldives":    {"temp": "31°C", "condition": "Clear skies, perfect beach weather"},
    "phuket":      {"temp": "33°C", "condition": "Hot and humid"},
    "tokyo":       {"temp": "18°C", "condition": "Partly cloudy"},
    "paris":       {"temp": "14°C", "condition": "Light showers"},
    "new york":    {"temp": "10°C", "condition": "Overcast with wind"},
    "swiss alps":  {"temp": "-2°C", "condition": "Heavy snowfall"},
    "himalayas":   {"temp": "-10°C", "condition": "Freezing, clear at high altitudes"},
    "barcelona":   {"temp": "22°C", "condition": "Sunny and warm"},
    "singapore":   {"temp": "30°C", "condition": "Tropical, expect afternoon showers"},
    "santorini":   {"temp": "25°C", "condition": "Sunny Mediterranean weather"},
    "cancun":      {"temp": "34°C", "condition": "Hot with occasional thunderstorms"},
    "patagonia":   {"temp": "8°C", "condition": "Windy and unpredictable"},
    "amazon rainforest": {"temp": "27°C", "condition": "Rainy and very humid"},
}

# Local time offsets from UTC (in hours)
city_timezones = {
    "tokyo":         9,
    "paris":         1,
    "new york":     -5,
    "barcelona":     1,
    "singapore":     8,
    "bali":          8,
    "maldives":      5,
    "phuket":        7,
    "london":        0,
    "dubai":         4,
    "sydney":       10,
    "los angeles": -8,
    "mumbai":      5.5,
    "cairo":         2,
    "toronto":      -5,
}

# Simulated travel news
travel_news = [
    "Visa-free travel expanded between 20 new country pairs this month.",
    "Tokyo named the safest city in the world for solo travelers in 2026.",
    "Budget airlines launching new routes across Southeast Asia this summer.",
    "Maldives opens new eco-resort built entirely from recycled materials.",
    "Swiss Alps introduce night skiing season extended by two weeks this year.",
    "Barcelona implements new short-term rental restrictions in city center.",
    "Singapore's Changi Airport wins World's Best Airport for the 12th time.",
    "Paris gears up for its biggest travel season following stadium renovations.",
]

# Packing lists by trip type
packing_lists = {
    "beach":    ["Sunscreen (SPF 50+)", "Swimwear", "Flip-flops", "Beach towel", "Sunglasses", "Light linen clothes"],
    "mountain": ["Thermal layers", "Waterproof jacket", "Hiking boots", "Gloves & beanie", "Trekking poles", "First-aid kit"],
    "city":     ["Comfortable walking shoes", "Smart casual clothes", "Day backpack", "City map / offline maps", "Portable charger"],
    "desert":   ["High-SPF sunscreen", "Wide-brim hat", "Light breathable clothing", "Plenty of water bottles", "Goggles for sandstorms"],
    "forest":   ["Insect repellent", "Waterproof boots", "Rain poncho", "Long-sleeve shirts", "Binoculars", "Torch/headlamp"],
}

HISTORY_FILE = "conversation_history.json"

# ─── Memory & History ─────────────────────────────────────────────────────────

conversation_memory = {}  # stores per-user session data


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_history(history: dict):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def record_message(history: dict, name: str, role: str, text: str):
    history.setdefault(name, []).append(
        {"role": role, "text": text, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )


# ─── Helpers ──────────────────────────────────────────────────────────────────

def normalize_input(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def bot_say(msg: str, color=Fore.CYAN):
    print(color + f"TravelBot: {msg}")


def user_ask(prompt: str) -> str:
    return input(Fore.YELLOW + f"You: ")


def section_header(title: str):
    print(Fore.WHITE + Back.BLUE + f" {title} " + Style.RESET_ALL)


# ─── Features ─────────────────────────────────────────────────────────────────

def show_help():
    section_header("What I Can Do")
    commands = [
        ("recommend / suggest",   "Get a travel destination suggestion"),
        ("packing / pack",        "Get a smart packing list"),
        ("weather",               "Check simulated weather at a destination"),
        ("time / local time",     "Find local time in a city"),
        ("news",                  "Read latest travel news"),
        ("joke / funny",          "Hear a travel joke"),
        ("history",               "View our chat history"),
        ("help",                  "Show this menu"),
        ("exit / bye",            "End the conversation"),
    ]
    for cmd, desc in commands:
        print(Fore.GREEN + f"  • {cmd:<22}" + Fore.WHITE + desc)
    print()


def recommend(name: str, history: dict):
    bot_say("Beaches, mountains, cities, deserts, or forests?")
    preference = normalize_input(user_ask("You: "))
    record_message(history, name, "user", preference)

    if preference in destinations:
        suggestion = random.choice(destinations[preference])
        bot_say(f"How about {suggestion}?", Fore.GREEN)
        bot_say("Do you like it? (yes / no)", Fore.CYAN)
        answer = normalize_input(user_ask("You: "))
        record_message(history, name, "user", answer)

        if re.search(r"\byes\b", answer):
            bot_say(f"Awesome! Enjoy your trip to {suggestion}! ✈", Fore.GREEN)
            conversation_memory.setdefault(name, {})["last_destination"] = suggestion
        elif re.search(r"\bno\b", answer):
            bot_say("Let's try another one.", Fore.RED)
            recommend(name, history)
        else:
            bot_say("I'll take that as a maybe — let me suggest again.", Fore.RED)
            recommend(name, history)
    else:
        bot_say(f"Sorry, I don't have '{preference}' destinations yet. Try: beaches, mountains, cities, deserts, forests.", Fore.RED)

    save_history(history)
    show_help()


def packing_tips(name: str, history: dict):
    bot_say("What type of trip? (beach / mountain / city / desert / forest)")
    trip_type = normalize_input(user_ask("You: "))
    record_message(history, name, "user", trip_type)

    bot_say("Where are you headed?")
    location = normalize_input(user_ask("You: "))
    record_message(history, name, "user", location)

    bot_say("How many days?")
    days = user_ask("You: ").strip()
    record_message(history, name, "user", days)

    matched_list = None
    for key in packing_lists:
        if re.search(key, trip_type):
            matched_list = packing_lists[key]
            break

    if matched_list:
        bot_say(f"Smart packing list for {days} days in {location.title()}:", Fore.GREEN)
        for item in matched_list:
            print(Fore.GREEN + f"  ✓ {item}")
    else:
        bot_say(f"General packing tips for {days} days in {location.title()}:", Fore.GREEN)
        for item in ["Pack versatile clothes", "Bring chargers/adapters", "Check the weather forecast",
                     "Carry a copy of your documents", "Pack a small first-aid kit"]:
            print(Fore.GREEN + f"  ✓ {item}")

    save_history(history)


def check_weather(name: str, history: dict):
    bot_say("Which destination do you want the weather for?")
    city = normalize_input(user_ask("You: "))
    record_message(history, name, "user", city)

    if city in weather_data:
        w = weather_data[city]
        bot_say(f"Weather in {city.title()}:", Fore.GREEN)
        print(Fore.GREEN + f"  🌡  Temperature : {w['temp']}")
        print(Fore.GREEN + f"  🌤  Condition   : {w['condition']}")
    else:
        bot_say(
            f"I don't have weather data for '{city.title()}' yet. "
            "Try: Bali, Tokyo, Paris, Swiss Alps, Himalayas, etc.",
            Fore.RED,
        )

    save_history(history)


def local_time(name: str, history: dict):
    bot_say("Which city's local time do you want to know?")
    city = normalize_input(user_ask("You: "))
    record_message(history, name, "user", city)

    if city in city_timezones:
        offset = city_timezones[city]
        utc_now = datetime.utcnow()
        # Apply offset (handle half-hour zones like Mumbai)
        total_minutes = int(utc_now.hour * 60 + utc_now.minute + offset * 60)
        local_hour = (total_minutes // 60) % 24
        local_min = total_minutes % 60
        local_time_str = f"{local_hour:02d}:{local_min:02d}"
        sign = "+" if offset >= 0 else ""
        bot_say(f"Current local time in {city.title()}: {local_time_str} (UTC{sign}{offset})", Fore.GREEN)
    else:
        bot_say(
            f"I don't have timezone data for '{city.title()}' yet. "
            "Try: Tokyo, Paris, New York, London, Dubai, Singapore, etc.",
            Fore.RED,
        )

    save_history(history)


def show_news():
    section_header("Latest Travel News")
    headlines = random.sample(travel_news, min(4, len(travel_news)))
    for i, headline in enumerate(headlines, 1):
        print(Fore.CYAN + f"  {i}. {headline}")
    print()


def tell_joke():
    bot_say(random.choice(jokes), Fore.YELLOW)


def show_chat_history(name: str, history: dict):
    user_history = history.get(name, [])
    if not user_history:
        bot_say("No chat history yet for this session.", Fore.RED)
        return
    section_header(f"Chat History — {name}")
    for entry in user_history[-20:]:  # show last 20 messages
        role_label = Fore.GREEN + "You        " if entry["role"] == "user" else Fore.CYAN + "TravelBot  "
        print(f"  {role_label}" + Fore.WHITE + f"[{entry['time']}]  {entry['text']}")
    print()


# ─── Main Chat Loop ───────────────────────────────────────────────────────────

def chat():
    history = load_history()

    section_header("TravelBot — Your AI Travel Companion")
    bot_say("Hello! I'm TravelBot. I'm here to help you plan your next adventure!")

    name = input(Fore.YELLOW + "What's your name? ").strip() or "Traveler"
    record_message(history, name, "bot", f"Hello {name}!")

    # Greet returning users
    if name in history and len(history[name]) > 1:
        bot_say(f"Welcome back, {name}! Great to see you again.", Fore.GREEN)
        last_dest = conversation_memory.get(name, {}).get("last_destination")
        if last_dest:
            bot_say(f"Last time we talked about {last_dest}. Ready for a new adventure?", Fore.GREEN)
    else:
        bot_say(f"Nice to meet you, {name}! Let's plan your next adventure.", Fore.GREEN)

    show_help()

    # Intent patterns
    patterns = [
        (r"recommend|suggest|destination|where (should|can) i go", "recommend"),
        (r"pack|packing|luggage|suitcase|what (to|should i) bring", "packing"),
        (r"weather|climate|temperature|forecast",                    "weather"),
        (r"time|local time|what time is it|timezone",                "time"),
        (r"news|latest|update|headline",                             "news"),
        (r"joke|funny|laugh|humor|lol",                              "joke"),
        (r"history|previous|past (chat|conversation)",               "history"),
        (r"help|\?|what can you do|commands",                        "help"),
        (r"exit|bye|goodbye|quit|see you|later",                     "exit"),
    ]

    while True:
        user_input = input(Fore.YELLOW + f"\n{name}: ").strip()
        if not user_input:
            continue
        normalized = normalize_input(user_input)
        record_message(history, name, "user", normalized)
        save_history(history)

        matched_intent = None
        for pattern, intent in patterns:
            if re.search(pattern, normalized):
                matched_intent = intent
                break

        if matched_intent == "recommend":
            recommend(name, history)
        elif matched_intent == "packing":
            packing_tips(name, history)
        elif matched_intent == "weather":
            check_weather(name, history)
        elif matched_intent == "time":
            local_time(name, history)
        elif matched_intent == "news":
            show_news()
        elif matched_intent == "joke":
            tell_joke()
        elif matched_intent == "history":
            show_chat_history(name, history)
        elif matched_intent == "help":
            show_help()
        elif matched_intent == "exit":
            record_message(history, name, "bot", "Goodbye!")
            save_history(history)
            bot_say(f"Safe travels, {name}! Come back anytime. Goodbye! ✈", Fore.CYAN)
            break
        else:
            bot_say(
                "I didn't quite catch that. Could you rephrase? "
                "(Type 'help' to see what I can do.)",
                Fore.RED,
            )


if __name__ == "__main__":
    chat()
