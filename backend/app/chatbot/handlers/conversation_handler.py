import datetime
from typing import Dict, Any, List, Optional
from app.chatbot.hf_client import detect_language, detect_message_language

class ConversationHandler:
    """
    Handles conversational small-talk, greetings, emotional empathy, and ambiguity clarification
    with full language-mirroring support (Telugu Script, Tenglish, English).
    """

    def handle_time_greeting(self, user_name: str, msg: str, active_language: str) -> Dict[str, Any]:
        cleaned = msg.lower()
        asks_how_are_you = any(w in cleaned for w in ["ela unnav", "ela unnaru", "bagunnara", "baagunnara", "bagunava", "how are you", "how r u", "ఎలా ఉన్నారు", "బాగున్నారా"])

        if active_language == "telugu_script":
            if asks_how_are_you:
                reply_msg = f"నమస్కారం! నేను బాగున్నాను 😊 మీరు ఎలా ఉన్నారు?"
            else:
                reply_msg = f"నమస్కారం, {user_name}! 😊 ఈరోజు మీ రోజు ఎలా గడుస్తోంది?"
            return {"message": reply_msg, "intent": "greeting_telugu", "action_type": None, "quick_replies": [], "structured_data": None}

        if active_language == "tenglish":
            if asks_how_are_you:
                reply_msg = "Hello! Nenu baagunnanu 😊 Meeru ela unnaru?"
            else:
                reply_msg = f"Hello, {user_name}! 😊 Eeroju mee day ela nadusthundi?"
            return {"message": reply_msg, "intent": "greeting_tenglish", "action_type": None, "quick_replies": [], "structured_data": None}

        if asks_how_are_you:
            reply_msg = "Hello! I'm doing great 😊 How are you doing today?"
        else:
            reply_msg = f"Hello, {user_name}! 😊 How's your day going so far?"

        return {"message": reply_msg, "intent": "greeting", "action_type": None, "quick_replies": [], "structured_data": None}

    def handle_clarification(self, user_name: str, msg: str, active_language: str) -> Dict[str, Any]:
        if active_language == "telugu_script":
            return {
                "message": f"ఖచ్చితంగా 😄 {user_name}, నేను మీకు ఏ విధంగా సహాయపడగలను?",
                "intent": "clarification_prompt_telugu",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }
        elif active_language == "tenglish":
            return {
                "message": f"Sure 😄 {user_name}, nenu meeku ela help cheyyagalanu?",
                "intent": "clarification_prompt_tenglish",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        return {
            "message": f"Sure 😄 How can I help you, {user_name}?",
            "intent": "clarification_prompt",
            "action_type": None,
            "quick_replies": [],
            "structured_data": None
        }

    def handle_chill_nothing(self, user_name: str, msg: str, active_language: str) -> Dict[str, Any]:
        if active_language == "telugu_script":
            return {
                "message": f"ప్రశాంతంగా విశ్రాంతి తీసుకోండి! 😊 {user_name}, ఏమీ చేయకుండా ఉండడం కూడా కొన్నిసార్లు చాలా బాగుంటుంది. మీరు ఏదైనా మాట్లాడాలనుకుంటే నన్ను అడగండి!",
                "intent": "chill_telugu",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }
        elif active_language == "tenglish":
            return {
                "message": f"Chilling is totally fine! 😊 {user_name}, eppudaina em cheyyakunda relax avvadam kuda manchide. Edo oka topic gurinchi matladudama?",
                "intent": "chill_tenglish",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        return {
            "message": f"Chilling is totally valid! 😊 Sometimes doing nothing is the best plan. Just let me know if you want to chat, {user_name}!",
            "intent": "chill",
            "action_type": None,
            "quick_replies": [],
            "structured_data": None
        }

    def handle_empathy_mood(self, msg: str, user_name: str, session: Dict[str, Any], active_language: str) -> Dict[str, Any]:
        cleaned = msg.lower()
        
        # Happy
        if any(p in cleaned for p in ["super happy", "so happy", "great day", "awesome day", "wonderful day", "feeling amazing", "very happy", "బాగా ఉన్నాను", "సంతోషంగా ఉన్నాను", "chala happy"]):
            session["current_mood"] = "happy"
            if active_language == "telugu_script":
                return {"message": f"అద్భుతం! 🔥 మీరు సంతోషంగా ఉన్నందుకు నాకు చాలా ఆనందంగా ఉంది, {user_name}! ఏమి జరిగింది?", "intent": "mood_happy_telugu", "action_type": None, "quick_replies": [], "structured_data": None}
            elif active_language == "tenglish":
                return {"message": f"Super! 🔥 Meeru happy ga unnanduku chala santhosham, {user_name}! Emaindi cheppandi?", "intent": "mood_happy_tenglish", "action_type": None, "quick_replies": [], "structured_data": None}
            return {"message": "Yesss! 🔥 I love that energy! What happened?", "intent": "mood_happy", "action_type": None, "quick_replies": [], "structured_data": None}

        # Bored
        if any(p in cleaned for p in ["i'm bored", "im bored", "bored", "so bored", "nothing to do", "బోరింగ్", "బోర్ కొడుతోంది", "bore ga undi"]):
            session["current_mood"] = "bored"
            if active_language == "telugu_script":
                return {"message": f"బోర్ కొడుతోందా? 😄 రండి, దాన్ని మార్చేద్దాం! మీరు ఏదైనా మాట్లాడాలనుకుంటున్నారా?", "intent": "mood_bored_telugu", "action_type": None, "quick_replies": [], "structured_data": None}
            elif active_language == "tenglish":
                return {"message": f"Bore ga undha? 😂 Don't worry! Edaina fun topic gurinchi matladudama?", "intent": "mood_bored_tenglish", "action_type": None, "quick_replies": [], "structured_data": None}
            return {"message": "Nothing happening huh? 😂 Let's change that. Do you want to chat about something fun?", "intent": "mood_bored", "action_type": None, "quick_replies": [], "structured_data": None}

        # Sad / Bad day
        if any(p in cleaned for p in ["terrible", "today was terrible", "bad day", "rough day", "sad", "feeling down", "feeling sad", "బాధగా ఉంది", "bad day ga undi", "nenu balenu"]):
            session["current_mood"] = "sad"
            if active_language == "telugu_script":
                return {"message": f"అయ్యో 😟 ఏమి జరిగింది? చెప్పండి, నేను వింటాను.", "intent": "mood_sad_telugu", "action_type": None, "quick_replies": [], "structured_data": None}
            elif active_language == "tenglish":
                return {"message": f"Ayyoo 😟 Em ayyindi? Cheppandi, nenu vintanu.", "intent": "mood_sad_tenglish", "action_type": None, "quick_replies": [], "structured_data": None}
            return {"message": "Ah, I'm sorry 😕 Sounds like today didn't go your way. Want to tell me what happened?", "intent": "mood_sad", "action_type": None, "quick_replies": [], "structured_data": None}

        if active_language == "telugu_script":
            return {"message": f"నేను మీ కోసం ఇక్కడ ఉన్నాను, {user_name}! మీరు ఇప్పుడు ఎలా ఉన్నారు?", "intent": "mood_check", "action_type": None, "quick_replies": [], "structured_data": None}
        elif active_language == "tenglish":
            return {"message": f"Nenu mee kosam ikkada unnanu, {user_name}! Meeru ippudu ela unnaru?", "intent": "mood_check", "action_type": None, "quick_replies": [], "structured_data": None}
        
        return {"message": f"I'm here for you, {user_name}! How are you feeling right now?", "intent": "mood_check", "action_type": None, "quick_replies": [], "structured_data": None}

    def handle_casual_chat(self, msg: str, user_name: str, session: Dict[str, Any], active_language: str = "english",
                           language: str = "english", script: str = "roman", style: str = "casual") -> Dict[str, Any]:
        """
        Handles general casual chit-chat, status updates (am good, bagunna),
        asking what is special today, or casual conversation without forcing educational / knowledge UI.
        """
        cleaned = msg.lower().strip()

        # 1. Asking about what's special today / happening today
        special_cues = [
            "enati special", "em special", "enti special", "eanti special", "yenti special",
            "what's special", "whats special", "special today", "today em undi", "ivala em special",
            "eeroju special", "ee roju special", "today special", "what is special",
            "what is happening today", "what's happening today", "whats happening today",
            "em undi ivala", "em undi eeroju", "any plans for today", "plans today"
        ]
        if any(cue in cleaned for cue in special_cues):
            if active_language == "telugu_script":
                return {
                    "message": f"మంచిది 😄 {user_name}, ఈరోజు ఏదైనా ప్రత్యేకమైన ప్లాన్ ఉందా? లేక ఈవెంట్స్, ఫుడ్ స్పెషల్స్ లేదా సరదా విషయాల గురించి తెలుసుకోవాలనుకుంటున్నారా?",
                    "intent": "casual_today_special",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🎉 ఈవెంట్స్", "payload": "ఈరోజు ఈవెంట్స్", "icon": "Sparkles"},
                        {"label": "🍽️ ఫుడ్ స్పెషల్స్", "payload": "ఈరోజు ఫుడ్ స్పెషల్స్", "icon": "Utensils"},
                        {"label": "🎬 సరదా విషయాలు", "payload": "ఏదైనా సరదాగా చెప్పండి", "icon": "Smile"}
                    ],
                    "structured_data": None
                }
            elif active_language == "tenglish":
                return {
                    "message": "Nice 😄 Ee roju special ga emaina plan unda? Leka today special events, festivals or food specials gurinchi adugutunnava?",
                    "intent": "casual_today_special",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🎉 Events", "payload": "what events are today", "icon": "Sparkles"},
                        {"label": "🍽️ Food specials", "payload": "food specials", "icon": "Utensils"},
                        {"label": "🎬 Things to do", "payload": "something fun to do", "icon": "Smile"},
                        {"label": "😄 Something fun", "payload": "tell me something fun", "icon": "MessageSquare"}
                    ],
                    "structured_data": None
                }

            return {
                "message": "Nice 😄 Do you have anything special planned for today? Or are you looking for events, food specials, or something fun to do?",
                "intent": "casual_today_special",
                "action_type": None,
                "quick_replies": [
                    {"label": "🎉 Events", "payload": "what events are today", "icon": "Sparkles"},
                    {"label": "🍽️ Food specials", "payload": "food specials", "icon": "Utensils"},
                    {"label": "🎬 Things to do", "payload": "something fun to do", "icon": "Smile"},
                    {"label": "😄 Something fun", "payload": "tell me something fun", "icon": "MessageSquare"}
                ],
                "structured_data": None
            }

        # 2. Status replies ("am good", "bagunna", "doing well", "fine", "i am good")
        status_good_cues = [
            "am good", "i'm good", "im good", "i am good", "doing good", "doing well",
            "bagunna", "nenu bagunna", "baagunnanu", "all good", "fine", "i am fine",
            "im fine", "i'm fine", "chala bagunna", "super unna", "mast unna"
        ]
        if any(cleaned == cue or cleaned.startswith(cue + " ") or cleaned.endswith(" " + cue) for cue in status_good_cues):
            if active_language == "telugu_script":
                return {
                    "message": "చాలా సంతోషం 😊 ఈరోజు మీ రోజు ఎలా గడుస్తోంది?",
                    "intent": "casual_status_reply",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }
            elif active_language == "tenglish":
                return {
                    "message": "Nice 😊 Ee roju ela undi mee day?",
                    "intent": "casual_status_reply",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }

            return {
                "message": "That's wonderful to hear 😊 How is your day going so far?",
                "intent": "casual_status_reply",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        # 3. Explicit Topic Switches & Preference Sharing (Latest Intent Always Wins)
        
        # 3.1. CRICKET TOPIC SWITCH / PREFERENCE
        cricket_match_cues = [
            "about cricket", "cricket gurinchi", "ledu naku cricket", "naku cricket gurinchi",
            "virat kohli gurinchi", "cricket ante istam", "cricket istam", "cricket ante pichi",
            "love cricket", "like cricket", "cricket matladudam", "cricket news", "ipl gurinchi"
        ]
        if any(c in cleaned for c in cricket_match_cues) or cleaned in ["cricket", "virat", "ipl", "team india"]:
            if active_language == "telugu_script":
                return {
                    "message": "ఖచ్చితంగా 🏏 క్రికెట్ గురించి మాట్లాడుకుందాం! టీమ్ ఇండియా, ఐపీఎల్, విరాట్ కోహ్లీ, మ్యాచ్‌లు, రికార్డులు లేదా తాజా క్రికెట్ అప్‌డేట్స్ — ఏది కావాలి?",
                    "intent": "topic_cricket",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🏏 టీమ్ ఇండియా", "payload": "టీమ్ ఇండియా అప్‌డేట్స్", "icon": "Flame"},
                        {"label": "🏆 ఐపీఎల్", "payload": "ఐపీఎల్ అప్‌డేట్స్", "icon": "Trophy"},
                        {"label": "👑 విరాట్ కోహ్లీ", "payload": "విరాట్ కోహ్లీ", "icon": "Star"},
                        {"label": "📊 రికార్డులు", "payload": "క్రికెట్ రికార్డులు", "icon": "Activity"}
                    ],
                    "structured_data": None
                }
            elif active_language == "tenglish":
                return {
                    "message": "Sure 🏏 Cricket gurinchi matladukundam! Team India, IPL, Virat Kohli, matches, records leka latest cricket updates — edhi kavali?",
                    "intent": "topic_cricket",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🏏 Team India", "payload": "Team India updates", "icon": "Flame"},
                        {"label": "🏆 IPL", "payload": "IPL updates", "icon": "Trophy"},
                        {"label": "👑 Virat Kohli", "payload": "about Virat Kohli", "icon": "Star"},
                        {"label": "📊 Records", "payload": "cricket records", "icon": "Activity"}
                    ],
                    "structured_data": None
                }
            return {
                "message": "Sure 🏏 Let's talk cricket! Team India, IPL, Virat Kohli, matches, records, or latest cricket updates — what would you like to discuss?",
                "intent": "topic_cricket",
                "action_type": None,
                "quick_replies": [
                    {"label": "🏏 Team India", "payload": "Team India updates", "icon": "Flame"},
                    {"label": "🏆 IPL", "payload": "IPL updates", "icon": "Trophy"},
                    {"label": "👑 Virat Kohli", "payload": "about Virat Kohli", "icon": "Star"},
                    {"label": "📊 Records", "payload": "cricket records", "icon": "Activity"}
                ],
                "structured_data": None
            }

        # 3.2. MUSIC TOPIC SWITCH / PREFERENCE
        music_match_cues = [
            "songs vinalani", "songs vinali", "song vinali", "song vinalani", "music vinali",
            "music vinalani", "paatalu vinali", "paatalu vinalani", "songs kavali", "song kavali",
            "music kavali", "songs suggest", "song suggest", "suggest songs", "listen to songs",
            "listen to music", "melody songs", "playlist kavali", "paatalu", "oka song suggest",
            "oka song suggest cheyyi", "song suggest cheyyi", "songs suggest cheyyi"
        ]
        if any(m in cleaned for m in music_match_cues) or cleaned in ["music", "songs", "song", "paatalu"]:
            if active_language == "telugu_script":
                return {
                    "message": "ఖచ్చితంగా 🎧 పాటల మూడ్‌కి వెళ్దాం! మెలోడీ, ఎనర్జిటిక్, రొమాంటిక్ లేదా ప్రశాంతమైన పాటలా?",
                    "intent": "preference_music",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🎧 మెలోడీ", "payload": "మెలోడీ పాటలు", "icon": "Music"},
                        {"label": "🔥 ఎనర్జిటిక్", "payload": "ఎనర్జిటిక్ పాటలు", "icon": "Zap"},
                        {"label": "❤️ రొమాంటిక్", "payload": "రొమాంటిక్ పాటలు", "icon": "Heart"},
                        {"label": "😌 ప్రశాంతమైనవి", "payload": "ప్రశాంతమైన పాటలు", "icon": "Coffee"}
                    ],
                    "structured_data": None
                }
            elif active_language == "tenglish":
                return {
                    "message": "Sure 🎧 Songs mood ki veldam. Melody, energetic, romantic leka chill?",
                    "intent": "preference_music",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🎧 Melody", "payload": "melody songs", "icon": "Music"},
                        {"label": "🔥 Energetic", "payload": "energetic songs", "icon": "Zap"},
                        {"label": "❤️ Romantic", "payload": "romantic songs", "icon": "Heart"},
                        {"label": "😌 Chill", "payload": "chill songs", "icon": "Coffee"}
                    ],
                    "structured_data": None
                }
            return {
                "message": "Sure 🎧 Let's go with music! Do you prefer melody, energetic, romantic, or chill songs?",
                "intent": "preference_music",
                "action_type": None,
                "quick_replies": [
                    {"label": "🎧 Melody", "payload": "melody songs", "icon": "Music"},
                    {"label": "🔥 Energetic", "payload": "energetic songs", "icon": "Zap"},
                    {"label": "❤️ Romantic", "payload": "romantic songs", "icon": "Heart"},
                    {"label": "😌 Chill", "payload": "chill songs", "icon": "Coffee"}
                ],
                "structured_data": None
            }

        # 3.3. MOVIES TOPIC SWITCH / PREFERENCE
        movie_match_cues = [
            "about movies", "about movie", "movie gurinchi", "movie gurinchi cheppu",
            "movies gurinchi", "movies gurinchi cheppu", "cinema gurinchi", "cinema gurinchi cheppu",
            "movie suggest", "suggest movie", "movie suggest cheyyi", "movies suggest cheyyi",
            "movies ante istam", "movies istam", "cinema ante istam", "films istam"
        ]
        if any(m in cleaned for m in movie_match_cues) or cleaned in ["movies", "movie", "cinema", "films"]:
            if active_language == "telugu_script":
                return {
                    "message": "ఖచ్చితంగా 🎬 సినిమాల గురించి మాట్లాడుకుందాం! తాజా రిలీజ్‌లు, టాలీవుడ్ హిట్స్, ఓటీటీ సలహాలు లేదా మూవీ రికమెండేషన్స్ — ఏది కావాలి?",
                    "intent": "topic_movies",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🍿 తాజా రిలీజ్‌లు", "payload": "తాజా సినిమాలు", "icon": "Film"},
                        {"label": "🌟 ఓటీటీ సలహాలు", "payload": "ఓటీటీ సినిమాలు", "icon": "Tv"},
                        {"label": "🔥 టాలీవుడ్ హిట్స్", "payload": "టాలీవుడ్ హిట్స్", "icon": "Star"}
                    ],
                    "structured_data": None
                }
            elif active_language == "tenglish":
                return {
                    "message": "Sure 🎬 Movies gurinchi matladukundam! Latest releases, Tollywood, blockbuster hits, OTT suggestions leka movie recommendations — edhi kavali?",
                    "intent": "topic_movies",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🍿 Latest Releases", "payload": "latest movies", "icon": "Film"},
                        {"label": "🌟 OTT Recommendations", "payload": "ott movies", "icon": "Tv"},
                        {"label": "🔥 Tollywood Hits", "payload": "tollywood hits", "icon": "Star"}
                    ],
                    "structured_data": None
                }
            return {
                "message": "Sure 🎬 Let's talk movies! Latest releases, blockbuster hits, OTT suggestions, or movie recommendations — what would you like?",
                "intent": "topic_movies",
                "action_type": None,
                "quick_replies": [
                    {"label": "🍿 Latest Releases", "payload": "latest movies", "icon": "Film"},
                    {"label": "🌟 OTT Recommendations", "payload": "ott movies", "icon": "Tv"},
                    {"label": "🔥 Blockbuster Hits", "payload": "blockbuster movies", "icon": "Star"}
                ],
                "structured_data": None
            }

        # 3.4. GAMES TOPIC SWITCH
        games_match_cues = [
            "about games", "game adadam", "game aadadam", "games aadali", "game aadali",
            "game kavali", "games kavali", "let's play a game", "play games", "play game", "games aadudam"
        ]
        if any(g in cleaned for g in games_match_cues) or cleaned in ["games", "game"]:
            from app.chatbot.handlers.entertainment_handler import entertainment_handler
            return entertainment_handler.handle_games_menu(cleaned, user_name, session, active_language)

        # 3.5. FOOD PREFERENCE
        if any(p in cleaned for p in ["biryani ante istam", "biryani istam", "biryani ante chala istam"]):
            if active_language == "tenglish":
                return {
                    "message": "Sameee 😄🍛 Biryani lo chicken istama leka mutton?",
                    "intent": "preference_food",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }
            return {
                "message": "Same here 😄🍛 Do you prefer chicken or mutton biryani?",
                "intent": "preference_food",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        # 3.6. STUDY / EXAM / CODING PREFERENCE
        if any(p in cleaned for p in ["exam ki help kavali", "exams help", "study help", "exam ki prepare", "preparing for exam", "exam undi", "exams unnayi"]):
            if active_language == "tenglish":
                return {
                    "message": "All the best 📚 Exam preparation ki nenu help chestanu! Em subject or topic gurinchi help kavali?",
                    "intent": "preference_exam",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }
            return {
                "message": "All the best 📚 I'm here to help with your exam preparation! What subject or topic would you like to cover?",
                "intent": "preference_exam",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        if any(p in cleaned for p in ["coding nerchukuntunna", "learning coding", "programming nerchukuntunna", "python nerchukuntunna"]):
            if active_language == "tenglish":
                return {
                    "message": "Nice 😄 Em language nerchukuntunnav?",
                    "intent": "preference_coding",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }
            return {
                "message": "Nice 😄 What programming language are you learning right now?",
                "intent": "preference_coding",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        # 4. Smart context-aware answers to previous questions (Direct answers always preserve topic)
        history = session.get("history", [])
        last_bot_msg = next((h.get("text", "") for h in reversed(history) if h.get("sender") in ["assistant", "bot"]), "")
        last_bot_lower = last_bot_msg.lower()

        # Answering cricket question (e.g. Virat Kohli, Rohit, Dhoni, RCB, CSK)
        if any(w in last_bot_lower for w in ["cricket", "player", "team", "ipl", "batsman"]):
            if any(p in cleaned for p in ["virat", "kohli", "rohit", "dhoni", "rcb", "csk", "mi", "srh", "kkr"]):
                name_clean = msg.strip().title()
                return {
                    "message": f"Ahh {name_clean} fan aa 😄🏏 Aayana batting chala mandi ki favourite! Meeku aayana batting lo ekkuva nachhedi enti?",
                    "intent": "cricket_followup",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }

        # Answering music question (e.g. Melody, Romantic, Energetic, Chill)
        if any(w in last_bot_lower for w in ["songs", "melody", "energetic", "music", "chill", "romantic"]):
            if any(m in cleaned for m in ["melody", "energetic", "romantic", "chill", "classical"]):
                return {
                    "message": f"{msg.strip().title()} songs aa 🎧 Nice choice! Telugu {cleaned} songs kavala leka English / Hindi aa?",
                    "intent": "music_followup",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🎶 Telugu", "payload": f"Telugu {cleaned} songs", "icon": "Music"},
                        {"label": "🎵 Hindi", "payload": f"Hindi {cleaned} songs", "icon": "Music"},
                        {"label": "✨ English", "payload": f"English {cleaned} songs", "icon": "Music"}
                    ],
                    "structured_data": None
                }
            if any(l in cleaned for l in ["telugu", "english", "hindi"]):
                return {
                    "message": f"{msg.strip().title()} songs aa ❤️ Calm ga vinadaniki chala options unnayi! Edo oka manchi song suggest cheyyana?",
                    "intent": "music_followup",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }

        # Answering food question (e.g. Chicken, Mutton)
        if any(w in last_bot_lower for w in ["biryani", "chicken", "mutton", "food"]):
            if any(f in cleaned for f in ["chicken", "mutton", "veg", "paneer"]):
                return {
                    "message": f"{msg.strip().title()} biryani 😋 Nice choice! Spicy ga kavala mild ga?",
                    "intent": "food_followup",
                    "action_type": None,
                    "quick_replies": [],
                    "structured_data": None
                }

        # 5. LLM-powered natural response for open-ended conversation & continuity
        from app.chatbot.hf_client import hf_client
        hf_reply = hf_client.generate_response(msg, session.get("history", []), active_language=active_language,
            language=language, script=script, style=style)
        if hf_reply:
            return {
                "message": hf_reply,
                "intent": "casual_chat",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        # 6. Warm conversational fallback (NEVER Knowledge Hub)
        if active_language == "telugu_script":
            return {
                "message": f"నేను వింటున్నాను, {user_name}! 😊 చెప్పండి, మనం దేని గురించి మాట్లాడుకుందాం?",
                "intent": "casual_chat",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }
        elif active_language == "tenglish":
            return {
                "message": f"Nenu ikkade unnanu, {user_name}! 😊 Cheppandi, em matladukundam?",
                "intent": "casual_chat",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        return {
            "message": f"I'm right here with you, {user_name}! 😊 What's on your mind today?",
            "intent": "casual_chat",
            "action_type": None,
            "quick_replies": [],
            "structured_data": None
        }

conversation_handler = ConversationHandler()

