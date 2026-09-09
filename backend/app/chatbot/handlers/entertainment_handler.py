import re
import random
from typing import Dict, Any, List, Optional

class EntertainmentHandler:
    """
    Handles interactive entertainment:
    - Riddles, Puzzles & Mind Challenges
    - Trivia (Cricket, Movies, Science, Gaming)
    - Standup Jokes & Humor
    - Game Victory Celebrations (fuses naturally with food rewards)
    """

    RIDDLES = [
        {
            "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I? 🧠",
            "answer": "an echo",
            "options": ["An Echo", "A Cloud", "A Whisper"]
        },
        {
            "question": "The more of this there is, the less you see. What is it? 🌑",
            "answer": "darkness",
            "options": ["Darkness", "Fog", "Silence"]
        },
        {
            "question": "What has keys but can't open locks? 🎹",
            "answer": "a piano",
            "options": ["A Piano", "A Keyboard", "A Map"]
        }
    ]

    JOKES = [
        "Why did the scarecrow win an award? 🌾 Because he was outstanding in his field! 😂",
        "Why did the tomato blush? 🍅 Because it saw the salad dressing! 😄",
        "Parallel lines have so much in common... it's a shame they'll never meet! 📐😆",
        "Why don't scientists trust atoms? ⚛️ Because they make up everything! 😂"
    ]

    def handle_games_menu(self, msg: str, user_name: str, session: Dict[str, Any], active_language: str = "english") -> Dict[str, Any]:
        """Serves the game options menu when the user wants to play games or rejects a riddle."""
        session["active_riddle"] = None
        session["current_activity"] = "game"

        if active_language == "telugu_script":
            return {
                "message": f"ఖచ్చితంగా {user_name}! 😄 మనం ఒక ఆట ఆడదాం. ఏదైనా ఒకటి ఎంచుకోండి:\n\n🎯 నంబర్ గెస్సింగ్ గేమ్\n🧠 సాధారణ జ్ఞానం క్విజ్\n🧩 పొడుపు కథలు (రిడిల్స్)\n🏏 క్రికెట్ క్విజ్",
                "intent": "entertainment_game_menu",
                "action_type": None,
                "quick_replies": [
                    {"label": "🎯 నంబర్ గెస్సింగ్", "payload": "నంబర్ గేమ్ ఆడాలి", "icon": "Gamepad2"},
                    {"label": "🧠 క్విజ్", "payload": "నాకు క్విజ్ కావాలి", "icon": "HelpCircle"},
                    {"label": "🧩 రిడిల్", "payload": "ఒక రిడిల్ చెప్పండి", "icon": "Sparkles"},
                    {"label": "🏏 క్రికెట్ క్విజ్", "payload": "క్రికెట్ క్విజ్", "icon": "Trophy"}
                ],
                "structured_data": None
            }
        elif active_language == "tenglish":
            return {
                "message": f"Sure {user_name}! 😄 Game aadham! Pick one:\n\n🎯 Guess the Number\n🧠 Trivia Quiz\n🧩 Riddles\n🏏 Cricket Quiz",
                "intent": "entertainment_game_menu",
                "action_type": None,
                "quick_replies": [
                    {"label": "🎯 Guess the Number", "payload": "Guess the number game", "icon": "Gamepad2"},
                    {"label": "🧠 Trivia Quiz", "payload": "Trivia quiz adudam", "icon": "HelpCircle"},
                    {"label": "🧩 Riddle", "payload": "Give me a riddle", "icon": "Sparkles"},
                    {"label": "🏏 Cricket Quiz", "payload": "Cricket trivia", "icon": "Trophy"}
                ],
                "structured_data": None
            }

        return {
            "message": f"Sure {user_name}! 😄 Let's play a game. Pick one:\n\n🎯 Guess the Number\n🧠 Trivia Quiz\n🧩 Riddles\n🏏 Cricket Quiz",
            "intent": "entertainment_game_menu",
            "action_type": None,
            "quick_replies": [
                {"label": "🎯 Guess the Number", "payload": "Guess the number game", "icon": "Gamepad2"},
                {"label": "🧠 Trivia Quiz", "payload": "Trivia quiz", "icon": "HelpCircle"},
                {"label": "🧩 Riddle", "payload": "Give me a riddle", "icon": "Sparkles"},
                {"label": "🏏 Cricket Quiz", "payload": "Cricket trivia", "icon": "Trophy"}
            ],
            "structured_data": None
        }

    def handle_game_riddle(self, msg: str, user_name: str, session: Dict[str, Any], active_language: str = "english") -> Dict[str, Any]:
        cleaned = msg.lower().strip()
        words = set(re.findall(r'\b\w+\b', cleaned))

        # Check for rejection or intent change away from riddle
        negation_cues = ["no", "vaddu", "not", "different", "game", "games", "bore", "something else", "stop", "change"]
        if any(c in words for c in negation_cues) or any(c in cleaned for c in ["games aadali", "game aadali", "i want games", "play games"]):
            session["active_riddle"] = None
            if any(g in cleaned for g in ["game", "games", "aadali", "play"]):
                return self.handle_games_menu(msg, user_name, session, active_language)

        # Check if user answered a previous riddle
        active_riddle = session.get("active_riddle")
        if active_riddle:
            ans = active_riddle.get("answer", "").lower().strip()
            # Extract meaningful key tokens (ignore stopwords like 'a', 'an', 'the')
            ans_keywords = [w for w in re.findall(r'\b\w+\b', ans) if w not in {"a", "an", "the"}]

            # Check if user's words match any meaningful answer keywords
            if ans in cleaned or (ans_keywords and all(k in words for k in ans_keywords)):
                session["active_riddle"] = None
                return {
                    "message": f"Spot on, {user_name}! 🎯 That's correct — it's **{ans.title()}**! You're sharp! 🔥\n\nWant another challenge, or should we do something else?",
                    "intent": "riddle_solved",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🧩 Another Riddle", "payload": "Give me a riddle", "icon": "HelpCircle"},
                        {"label": "🏏 Cricket Trivia", "payload": "Give me cricket trivia", "icon": "Trophy"},
                        {"label": "🍽️ Celebrate with Food", "payload": "I want to celebrate with food", "icon": "Utensils"}
                    ],
                    "structured_data": None
                }

        # If user explicitly requested games, show game menu instead of another riddle
        if any(w in cleaned for w in ["play game", "play games", "games aadali", "game aadali", "game kavali", "games kavali", "i want games"]):
            return self.handle_games_menu(msg, user_name, session, active_language)

        # Serve new riddle
        riddle = random.choice(self.RIDDLES)
        session["active_riddle"] = riddle

        return {
            "message": f"Here is a fun challenge for you, {user_name}: 🧠\n\n*\"{riddle['question']}\"*\n\nTake a guess! 😄",
            "intent": "entertainment_riddle",
            "action_type": None,
            "quick_replies": [
                {"label": f"💡 {riddle['options'][0]}", "payload": riddle['options'][0], "icon": "HelpCircle"},
                {"label": f"✨ {riddle['options'][1]}", "payload": riddle['options'][1], "icon": "HelpCircle"},
                {"label": f"🤔 {riddle['options'][2]}", "payload": riddle['options'][2], "icon": "HelpCircle"}
            ],
            "structured_data": None
        }

    def handle_cricket_trivia(self, msg: str, user_name: str) -> Dict[str, Any]:
        return {
            "message": (
                f"🏏 **Cricket Trivia Challenge for {user_name}:**\n\n"
                f"Who holds the record for the highest individual score in an ODI innings (264 runs)?\n\n"
                f"A) Virat Kohli\n"
                f"B) Rohit Sharma\n"
                f"C) Sachin Tendulkar"
            ),
            "intent": "entertainment_cricket_trivia",
            "action_type": None,
            "quick_replies": [
                {"label": "🏏 Rohit Sharma (264)", "payload": "Rohit Sharma", "icon": "Check"},
                {"label": "👑 Virat Kohli", "payload": "Virat Kohli", "icon": "Star"},
                {"label": "🏏 Sachin Tendulkar", "payload": "Sachin Tendulkar", "icon": "Trophy"}
            ],
            "structured_data": None
        }

    def handle_joke(self, msg: str, user_name: str) -> Dict[str, Any]:
        joke = random.choice(self.JOKES)
        return {
            "message": f"{joke}\n\nWant another one, a puzzle, or should we talk about something else?",
            "intent": "entertainment_joke",
            "action_type": None,
            "quick_replies": [
                {"label": "😂 Another Joke", "payload": "Tell me a joke", "icon": "Smile"},
                {"label": "🧩 Give me a Riddle", "payload": "Give me a riddle", "icon": "HelpCircle"},
                {"label": "💬 Let's Chat", "payload": "Let's just chat", "icon": "MessageSquare"}
            ],
            "structured_data": None
        }

    def handle_game_victory_food(self, user_name: str) -> Dict[str, Any]:
        """Handles Game Victory + Food Intent fusion naturally."""
        return {
            "message": (
                f"Yesss! 🏆 That's worth celebrating, {user_name}! Congratulations on the victory!\n\n"
                f"Every great win deserves a feast. What are you craving to reward yourself with — "
                f"something spicy like our **Royal Chicken Biryani**, or a decadent dessert like **Molten Lava Cake**?"
            ),
            "intent": "game_victory_food_celebration",
            "action_type": "SHOW_MENU",
            "quick_replies": [
                {"label": "👑 Royal Chicken Biryani", "payload": "I want to order Royal Chicken Biryani", "icon": "Utensils"},
                {"label": "🍫 Molten Lava Cake", "payload": "Order 1 Molten Chocolate Lava Cake", "icon": "Cake"},
                {"label": "🍟 Truffle Fries", "payload": "Order 1 Crispy Golden Truffle Fries", "icon": "ShoppingBag"},
                {"label": "📜 Full Menu", "payload": "Show me the menu", "icon": "BookOpen"}
            ],
            "structured_data": None
        }

entertainment_handler = EntertainmentHandler()
