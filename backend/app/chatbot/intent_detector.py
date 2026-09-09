import re
from typing import Dict, Any, List, Optional, Tuple


class SemanticIntentDetector:
    """
    Step 3 & Step 4: Semantic Intent Detection & Google-Like Information Engine.

    Understands the *meaning* of a message — not just individual keywords.
    Supports:
    - Context-first evaluation (active simulation/learning, mood, interests, last knowledge topic)
    - Contextual follow-up queries (e.g., "When?", "Capital?", "Why?", "How long?")
    - Knowledge comparisons (e.g., "Python vs JavaScript", "iPhone vs Android", "Rice vs Wheat")
    - Step-by-step How-To queries (e.g., "How to create a website", "How to grow paddy")
    - Knowledge simplifications ("Explain like I'm a beginner", "I don't understand")
    - Knowledge deep dives ("Explain deeply", "In detail")
    - Knowledge-to-Quiz transitions ("Ask me questions", "Quiz me")
    - Telugu-English mixed language (Tenglish: "photosynthesis ante enti ra?", "paddy ela pandinchali")
    - Multi-intent compound messages
    - Live current information detection (Wikipedia & Search)
    """

    # ═══════════════════════════════════════════════════════════════
    # TELUGU-ENGLISH PHRASE BANKS (Tenglish NLP lexicon)
    # ═══════════════════════════════════════════════════════════════

    TELUGU_FOOD = [
        "food kavali", "naaku food kavali", "naaku biryani kavali", "biryani kavali",
        "biryani unda", "food unda", "tinali", "edo okati tinali", "food order cheyyali",
        "order cheyyi", "aakali vesthundi", "aakali", "bhojanam", "tiffin kavali",
        "emi tindamu", "em tindamu", "em tinu", "snacks kavali", "meals kavali",
        "lunch kavali", "dinner kavali", "breakfast kavali", "coffee kavali", "tea kavali",
        "naaku aakali", "pedda aakali", "bhojnam", "nenu food order cheyyali",
        "em undhi menu lo", "menu chupinchu", "em baguntundi tinu", "em tintavu",
        "em tintam", "naaku em kavali ante food", "rice kavali", "curry kavali",
        "dosa kavali", "idli kavali", "vada kavali", "upma kavali",
    ]

    TELUGU_GAME = [
        "game aadudama", "game aadali", "edo oka game", "aadudam", "game cheppu",
        "timepass kavali", "game cheydam", "oka game aadu", "boring ga undi",
        "bayata adutam", "game addam", "riddle cheppu", "joke cheppu",
        "entertain cheyyi", "vinnod kavali",
    ]

    TELUGU_FARMING = [
        "paddy ela pandinchali", "farming nerchukovali", "vyavasayam", "vari sagu",
        "penta ela veyyali", "crop ela veyyali", "vari ela pandinchali", "rythu",
        "panta ela veyyali", "vyavasaya tips", "vari pandinchu ela", "pandinchu ela",
        "vari sagu ela cheyyali", "panta ela pandinchali", "farming ela cheyyali",
        "nenu farm cheyyali", "agriculture nerchukovali",
    ]

    TELUGU_LEARNING = [
        "nerchukovali", "naku nerpichu", "explain cheyyi", "cheppinchu",
        "python nerchukovali", "coding nerchukovali", "oka concept cheppu",
        "ela cheyyali", "ela chestaru", "ela pandinchali", "naku teliyadu cheppu",
        "oka step step ga cheppu", "oka example cheppu", "naku nerpinchu",
    ]

    TELUGU_KNOWLEDGE = [
        "ante enti", "ante enti ra", "ante emiti", "ela pani chestadi",
        "photosynthesis ante enti", "photosynthesis ante enti ra", "democracy ante enti",
        "python explain cheyyi", "concept explain cheyyi", "gurinchi explain cheyyi",
    ]

    TELUGU_BOOKING = [
        "table book cheyyi", "seat reserve cheyyi", "table kavali",
        "dinner book cheyyi", "lunch book cheyyi", "reservation kavali",
        "table reserve cheyyi", "booking kavali",
    ]

    TELUGU_BORED = [
        "boring ga undi", "em cheyali teliyadu", "vere em cheyali",
        "timepass kavali", "em cheyalo telidu", "inkemi cheyyali",
        "bore ga undi", "chala bore ga undi",
    ]

    TELUGU_EMOTION = [
        "chala happy ga undi", "super happy undi", "chala sad ga undi",
        "stress ga undi", "tired ga undi", "excited ga undi",
        "bore ga undi", "anxious ga undi", "tension ga undi",
    ]

    TELUGU_TRAVEL = [
        "trip plan cheyyi", "travel plan kavali", "trip vellali",
        "goa vellali", "manali vellali", "ooty vellali", "tour plan kavali",
    ]

    TELUGU_BUSINESS = [
        "business start cheyyali", "startup petali", "business nerchukovali",
        "business plan kavali", "nenu business cheyali",
    ]

    # ═══════════════════════════════════════════════════════════════
    # SEMANTIC CLUSTERS (meaning-based signal lists)
    # ═══════════════════════════════════════════════════════════════

    FOOD_SIGNALS = [
        "food", "hungry", "hunger", "eat", "eating", "meal", "meals", "mealtime",
        "snack", "snacks", "starving", "famished", "craving", "what to eat",
        "something to eat", "let's eat", "i want to eat", "want food",
        "biryani", "pizza", "burger", "pasta", "rice", "curry", "dosa", "idli",
        "dessert", "desserts", "beverage", "beverages", "coffee", "tea", "juice",
        "lassi", "pancake", "pancakes", "truffle fries", "lava cake", "sandwich",
        "salad", "soup", "noodles", "wrap", "thali",
        "order", "ordering", "want to order", "place an order", "add to cart",
        "menu", "dish", "dishes", "specials", "recommend dish",
        "lunch", "dinner", "breakfast", "brunch",
        "vegetarian", "vegan", "spicy", "mild", "gluten free",
        "treat myself", "comfort food", "reward", "celebrate with food",
        "బిర్యానీ", "ఆహారం", "టిఫిన్", "భోజనం", "ఆర్డర్", "తినాలి", "మెనూ", "ఫుడ్",
    ]


    GAME_SIGNALS = [
        "game", "games", "play", "playing", "bored", "boring",
        "entertainment", "entertain me", "fun", "distract me",
        "riddle", "riddles", "trivia", "puzzle", "puzzles",
        "joke", "jokes", "challenge", "quiz",
        "word game", "guessing game", "cricket quiz", "cricket trivia",
        "movie quiz", "keep me company", "let's play", "something fun",
        "pass the time", "timepass",
    ]

    LEARNING_SIGNALS = [
        "teach me", "teach", "learn", "learning", "tutorial", "how to",
        "explain", "concept", "understand", "study", "course", "lesson",
        "lessons", "step by step", "guide me", "guide",
        "python", "coding", "programming", "code", "javascript", "java",
        "html", "css", "sql", "react", "node", "typescript",
        "algorithm", "data structure", "machine learning", "ai", "deep learning",
        "math", "science", "physics", "chemistry", "biology", "history",
        "geography", "economics",
    ]

    FARMING_SIGNALS = [
        "farm", "farming", "paddy", "cultivate", "cultivation", "crop", "crops",
        "rice field", "agriculture", "grow rice", "grow paddy", "grow wheat",
        "sow seeds", "harvest", "irrigation", "fertilizer", "soil",
        "virtual farm", "agriculture simulation", "farmer", "field",
        "plant crops", "yield", "organic farming", "sustainable farming",
        "rice cultivation", "paddy field", "transplant seedlings",
    ]

    BUSINESS_SIGNALS = [
        "business", "startup", "start a business", "launch a business",
        "entrepreneur", "business plan", "business idea", "market research",
        "funding", "investment", "revenue", "profit", "company", "brand",
        "product launch", "e-commerce", "business simulation", "franchise",
        "business model", "pitch deck", "venture", "enterprise",
    ]

    TRAVEL_SIGNALS = [
        "trip", "travel", "vacation", "holiday", "visit", "journey", "tour",
        "plan a trip", "itinerary", "destination", "flight", "hotel",
        "booking hotel", "tourist", "explore", "backpack", "road trip",
        "goa", "paris", "london", "manali", "himalayas", "ooty",
        "beach", "mountain", "travel planner", "sightseeing", "getaway",
    ]

    COOKING_SIGNALS = [
        "cook", "cooking", "recipe", "how to make", "how to cook",
        "bake", "baking", "ingredients", "kitchen", "chef",
        "prepare food", "make biryani", "make pasta", "cooking tutorial",
        "cooking guide", "cooking steps", "teach me to cook",
    ]

    CURRENT_INFO_SIGNALS = [
        "current", "latest", "today", "right now", "this year",
        "who is the", "who is currently", "what is the current",
        "prime minister", "president", "pm of", "pm india",
        "news", "breaking news", "today's news", "headlines", "political headlines",
        "weather", "temperature", "forecast",
        "cricket score", "match score", "live score", "sports result", "who won today",
        "stock price", "market", "exchange rate", "gold price", "today's gold price",
        "latest movies", "new movie", "what happened yesterday",
        "election result", "current status", "latest update",
        "currently", "as of now",
    ]

    KNOWLEDGE_SIGNALS = [
        "what is", "what are", "who is", "who was", "who invented",
        "who discovered", "when was", "when did", "where is", "where was",
        "how does", "how do", "why is", "why does", "why are",
        "explain", "definition of", "define", "meaning of", "what does",
        "tell me about", "describe",
        "democracy", "capitalism", "socialism", "photosynthesis", "evolution",
        "gravity", "relativity", "quantum", "black hole", "climate change",
        "solar system", "atoms", "elements", "water cycle", "thermodynamics",
        "big bang", "ancient egypt", "indus valley", "constitution",
        "history of", "origin of", "invention of", "discovery of",
        "science", "philosophy", "art", "culture", "technology",
        "binary search", "algorithm", "data structure", "api", "database",
    ]

    BOOKING_SIGNALS = [
        "book a table", "reserve a table", "table reservation", "book table",
        "reserve table", "reserve a seat", "table for", "dinner reservation",
        "lunch reservation", "make a reservation", "reservation for",
        "want a table", "need a table", "get a table", "seat for",
        "book my table", "reserve my seat",
        "టేబుల్", "బుకింగ్", "బుక్ చేయాలి", "రిజర్వేషన్", "table book",
    ]


    PAYMENT_SIGNALS = [
        "pay", "payment", "bill", "checkout", "upi", "google pay", "gpay",
        "phonepe", "paytm", "credit card", "debit card", "cash",
        "pay now", "make payment", "total amount", "pay bill",
        "online payment", "neft", "wallet", "net banking",
        "settle bill", "clear the bill", "how much do i owe",
    ]

    GAME_WIN_SIGNALS = [
        "won the game", "i won", "game won", "won!", "victory",
        "i beat", "beat the game", "finished the game", "game complete",
        "level up", "i won the quiz", "won the quiz", "won the trivia",
        "got the answer", "i was right", "i guessed it", "nailed it",
        "got it right", "i won!", "we won", "nailed the riddle",
        "solved it", "i solved",
    ]

    # ═══════════════════════════════════════════════════════════════
    # MAIN DETECT METHOD
    # ═══════════════════════════════════════════════════════════════

    def detect(
        self,
        msg: str,
        raw_msg: str,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Semantic intent detection pipeline.

        Returns:
            {
                "primary_intent": str,
                "secondary_intent": Optional[str],
                "confidence": float (0.0–1.0),
                "entities": Dict[str, Any],
                "is_multi_intent": bool
            }
        """
        cleaned = msg.strip().lower()

        # ── Phase 1: Context-Aware Continuations & Follow-Ups ──
        context_intent = self._check_context_continuation(cleaned, session)
        if context_intent:
            return context_intent

        # ── Phase 2: Step 4 Specific Knowledge Patterns (Comparisons / How-To / Simplifications / Quizzes) ──
        special_gk = self._check_special_knowledge_intents(cleaned, session)
        if special_gk:
            return special_gk

        # ── Phase 3: Multi-Intent Compound Detection ──
        multi = self._detect_multi_intent(cleaned, session)
        if multi:
            return multi

        # ── Phase 4: Single-Intent Scoring ──
        scores = self._score_all_intents(cleaned, session)

        if not scores:
            if self._is_very_vague(cleaned):
                return self._clarification_result()
            return self._general_conversation_result()

        scores.sort(key=lambda x: x[1], reverse=True)
        top = scores[0]
        second = scores[1] if len(scores) > 1 else None

        # Very low confidence → ask clarification
        if top[1] < 0.30:
            return self._clarification_result()

        entities = top[2] if len(top) > 2 else {}
        is_explicit = entities.get("explicit", False) or (top[1] >= 0.99 and top[0] not in ["GREETING", "CASUAL_CHAT", "ANSWER_TO_PREVIOUS_QUESTION"])

        return {
            "primary_intent": top[0],
            "secondary_intent": second[0] if second and second[1] >= 0.40 else None,
            "confidence": top[1],
            "entities": entities,
            "is_multi_intent": bool(second and second[1] >= 0.40),
            "is_explicit_intent": is_explicit
        }

    # ═══════════════════════════════════════════════════════════════
    # PHASE 1 — CONTEXT CONTINUATIONS & FOLLOW-UPS
    # ═══════════════════════════════════════════════════════════════

    # Negation / rejection signals — any of these mean the user is CHANGING intent
    NEGATION_SIGNALS = [
        # English
        "no", "nope", "not this", "not that", "something else", "i don't want",
        "i dont want", "i want something different", "instead", "different",
        "not interested", "stop", "skip", "change", "switch", "another",
        "no thanks", "no thank you", "nevermind", "never mind", "forget it",
        "i want games", "i want to play", "i want food", "actually",
        # Telugu / Tenglish
        "vaddu", "naaku adi vaddu", "adi kaadu", "adi kaadhu", "vere di kavali",
        "vere game", "inkoti", "adi oddu", "naaku game kavali", "game aadali",
        "games aadali", "game kavali", "food kavali", "vere topic", "veru",
        "adi vedu", "adi ok kaadu", "ok kaadu",
    ]

    def _check_context_continuation(
        self, msg: str, session: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Check for active simulation/learning or contextual follow-up questions.
        Returns None immediately if the user is rejecting / changing intent.
        """
        # ── 0. NEGATION / INTENT CHANGE — always takes priority ──
        cleaned_words = msg.strip().lower().split()
        for signal in self.NEGATION_SIGNALS:
            signal_words = signal.split()
            if len(signal_words) == 1 and signal in cleaned_words:
                # Clear current activity so Phase 4 scoring picks the new intent
                session["current_activity"] = None
                session["active_simulation"] = None
                session["active_learning"] = None
                return None
            elif len(signal_words) > 1 and signal in msg:
                session["current_activity"] = None
                session["active_simulation"] = None
                session["active_learning"] = None
                return None

        active_sim = session.get("active_simulation")
        active_learning = session.get("active_learning")
        pending_secondary = session.get("pending_secondary_intent")
        last_gk_topic = session.get("last_knowledge_topic") or (
            session.get("last_topic", {}).get("subject")
            if isinstance(session.get("last_topic"), dict)
            else session.get("last_topic")
        )

        CONTINUATION_WORDS = [

            "what should i do", "tell me more", "more", "okay", "ok",
            "yes", "yeah", "yep", "sure", "let's do it", "start",
            "alright", "got it", "understood", "and then", "after that",
            "keep going", "go ahead", "what do i do next", "sounds good",
        ]

        SIM_ACTION_WORDS = {
            "farming": ["water", "harvest", "sow", "plant", "irrigate", "fertilize",
                        "weed", "pesticide", "transplant", "till", "plow", "spray",
                        "seedling", "nursery", "drain", "flood", "yield"],
            "business": ["invest", "market", "sell", "buy", "hire", "launch",
                         "fund", "pitch", "revenue", "profit", "customer", "product"],
            "travel": ["book flight", "check hotel", "pack", "depart", "arrive",
                       "sightseeing", "day 1", "day 2", "itinerary", "explore"],
            "cooking": ["add ingredient", "mix", "heat", "boil", "fry", "stir",
                        "chop", "slice", "bake", "simmer", "season"],
        }

        # ── 1. Active Simulation ──
        if active_sim:
            sim_type = active_sim.get("type", "")
            sim_words = SIM_ACTION_WORDS.get(sim_type, [])
            is_continuation = any(w in msg for w in CONTINUATION_WORDS)
            is_sim_action = any(w in msg for w in sim_words)

            if is_continuation or is_sim_action:
                return {
                    "primary_intent": f"SIMULATION_{sim_type.upper()}_STEP",
                    "secondary_intent": None,
                    "confidence": 0.95,
                    "entities": {"simulation": sim_type, "step_action": msg},
                    "is_multi_intent": False,
                }

        # ── 2. Active Learning ──
        if active_learning:
            topic = active_learning.get("topic", "general")
            LEARN_CONTINUE = [
                "next", "more", "continue", "next concept", "next topic",
                "example", "quiz me", "quiz", "test me", "practice",
                "got it", "understood", "okay what's next", "show code",
                "show me an example", "one more", "next lesson", "next step",
                "what's next", "i understand", "clear",
            ]
            if any(w in msg for w in LEARN_CONTINUE):
                return {
                    "primary_intent": "LEARNING_CONTINUE",
                    "secondary_intent": None,
                    "confidence": 0.95,
                    "entities": {"topic": topic},
                    "is_multi_intent": False,
                }

        # ── 3. Step 4: Context-Aware Knowledge Follow-Up Queries ──
        # E.g. Previous topic = "Python", user asks "When?" or "Who created it?"
        # Previous topic = "India", user asks "Capital?" or "How long?"
        if last_gk_topic:
            FOLLOWUP_PATTERNS = [
                "when?", "when was it", "when did it", "when was that", "when was this", "when",
                "capital?", "what is the capital", "capital",
                "why?", "why is that", "why so", "why",
                "how long?", "how long have they been in office", "how long has it been", "how long",
                "who created it?", "who invented it?", "who was the founder", "who made it",
                "where?", "where is it located", "where was it",
                "population?", "how many people",
                "more details", "tell me more",
            ]
            clean_q = msg.strip(" ?.!").lower()
            if clean_q in [p.strip(" ?.!").lower() for p in FOLLOWUP_PATTERNS] or any(p == clean_q for p in ["when", "capital", "why", "who", "where", "how long"]):
                return {
                    "primary_intent": "KNOWLEDGE_FOLLOWUP",
                    "secondary_intent": None,
                    "confidence": 0.94,
                    "entities": {"followup_type": clean_q, "topic": last_gk_topic},
                    "is_multi_intent": False,
                }

        # ── 4. Pending Secondary Intent (queued multi-intent) ──
        if pending_secondary:
            food_trigger = (
                any(t in msg for t in ["now", "hungry", "food", "eat", "order", "biryani", "menu"])
                or any(p in msg for p in self.TELUGU_FOOD)
            )
            if food_trigger:
                return {
                    "primary_intent": pending_secondary,
                    "secondary_intent": None,
                    "confidence": 0.92,
                    "entities": {"from_pending": True},
                    "is_multi_intent": False,
                }

        return None

    # ═══════════════════════════════════════════════════════════════
    # PHASE 2 — SPECIAL KNOWLEDGE INTENTS (Step 4)
    # ═══════════════════════════════════════════════════════════════

    def _check_special_knowledge_intents(
        self, msg: str, session: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect Step 4 special knowledge modes:
        - Comparisons ("Python vs JavaScript", "iPhone vs Android", "Rice vs Wheat")
        - Step-by-step How-To ("How to create a website", "How to grow paddy")
        - Knowledge simplification ("I don't understand", "Explain like I'm a beginner")
        - Knowledge deep dive ("Explain deeply", "In detail")
        - Knowledge quiz ("Ask me questions", "Quiz me")
        """
        last_topic = session.get("last_knowledge_topic")

        # ── A. Comparisons ──
        COMPARE_TRIGGERS = [" vs ", " versus ", "compare ", "which is better", "difference between"]
        if any(w in msg for w in COMPARE_TRIGGERS):
            return {
                "primary_intent": "KNOWLEDGE_COMPARISON",
                "secondary_intent": None,
                "confidence": 0.94,
                "entities": {"query": msg},
                "is_multi_intent": False,
            }

        # ── B. Knowledge Quiz Trigger ("Ask me questions", "Quiz me") ──
        QUIZ_TRIGGERS = [
            "ask me questions", "ask me question", "quiz me", "test me",
            "test my knowledge", "quiz on this", "ask questions", "test me on this"
        ]
        if any(w in msg for w in QUIZ_TRIGGERS):
            return {
                "primary_intent": "KNOWLEDGE_QUIZ",
                "secondary_intent": None,
                "confidence": 0.95,
                "entities": {"topic": last_topic or "general"},
                "is_multi_intent": False,
            }

        # ── C. Simplification ("I don't understand", "Explain like a beginner") ──
        SIMPLIFY_TRIGGERS = [
            "i don't understand", "dont understand", "i do not understand",
            "explain like i'm a beginner", "explain like im a beginner",
            "explain like i'm 5", "explain simply", "eli5",
            "in simple terms", "too complicated", "too complex", "make it simple",
            "simple explanation"
        ]
        if any(w in msg for w in SIMPLIFY_TRIGGERS):
            return {
                "primary_intent": "KNOWLEDGE_SIMPLIFY",
                "secondary_intent": None,
                "confidence": 0.94,
                "entities": {"topic": last_topic},
                "is_multi_intent": False,
            }

        # ── D. Deep Dive ("Explain deeply", "In detail") ──
        DEEPEN_TRIGGERS = [
            "explain deeply", "deep dive", "in detail", "more technical",
            "advanced explanation", "explain in depth", "detailed explanation"
        ]
        if any(w in msg for w in DEEPEN_TRIGGERS):
            return {
                "primary_intent": "KNOWLEDGE_DEEPEN",
                "secondary_intent": None,
                "confidence": 0.93,
                "entities": {"topic": last_topic},
                "is_multi_intent": False,
            }

        # ── E. How-To Questions ──
        HOW_TO_TRIGGERS = [
            "how to ", "how do i ", "how do you ", "steps to ", "guide to ",
            "how can i "
        ]
        # Ignore cooking/food ordering ("how to order") which map to their specific flows
        if any(msg.startswith(w) for w in HOW_TO_TRIGGERS) and not any(w in msg for w in ["order", "book"]):
            return {
                "primary_intent": "KNOWLEDGE_HOW_TO",
                "secondary_intent": None,
                "confidence": 0.92,
                "entities": {"query": msg},
                "is_multi_intent": False,
            }

        return None

    # ═══════════════════════════════════════════════════════════════
    # PHASE 3 — MULTI-INTENT DETECTION
    # ═══════════════════════════════════════════════════════════════

    def _detect_multi_intent(
        self, msg: str, session: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect compound messages that contain two distinct intents.
        """
        COMPOUND_JOINS = [
            " and then ", " and after ", " then ", " after that ", " after ",
            " also ", " as well as ", " plus ", " followed by ", " along with ",
        ]
        has_compound = any(w in msg for w in COMPOUND_JOINS)

        has_food = self._signal_hit(msg, self.FOOD_SIGNALS) or self._tel_hit(msg, self.TELUGU_FOOD)
        has_farming = self._signal_hit(msg, self.FARMING_SIGNALS) or self._tel_hit(msg, self.TELUGU_FARMING)
        has_game_win = self._tel_hit(msg, self.GAME_WIN_SIGNALS)
        has_game_play = self._signal_hit(msg, self.GAME_SIGNALS) or self._tel_hit(msg, self.TELUGU_GAME)
        has_business = self._signal_hit(msg, self.BUSINESS_SIGNALS) or self._tel_hit(msg, self.TELUGU_BUSINESS)
        has_travel = self._signal_hit(msg, self.TRAVEL_SIGNALS) or self._tel_hit(msg, self.TELUGU_TRAVEL)
        has_learning = self._signal_hit(msg, self.LEARNING_SIGNALS) or self._tel_hit(msg, self.TELUGU_LEARNING)

        # Game victory + food
        if has_game_win and has_food:
            return {
                "primary_intent": "GAME_VICTORY_FOOD",
                "secondary_intent": "RESTAURANT_FOOD",
                "confidence": 0.96,
                "entities": {"celebration": True, "game_won": True},
                "is_multi_intent": True,
            }

        if has_game_win and not has_food:
            return {
                "primary_intent": "GAME_VICTORY",
                "secondary_intent": "RESTAURANT_FOOD",
                "confidence": 0.88,
                "entities": {"celebration": True},
                "is_multi_intent": True,
            }

        if not has_compound:
            return None

        # Compound pairs
        if has_farming and has_food:
            return {
                "primary_intent": "SIMULATION_FARMING",
                "secondary_intent": "RESTAURANT_FOOD",
                "confidence": 0.93,
                "entities": {"multi": True},
                "is_multi_intent": True,
            }
        if has_learning and has_food:
            return {
                "primary_intent": "LEARNING",
                "secondary_intent": "RESTAURANT_FOOD",
                "confidence": 0.90,
                "entities": {"multi": True},
                "is_multi_intent": True,
            }
        if has_game_play and has_food:
            return {
                "primary_intent": "ENTERTAINMENT",
                "secondary_intent": "RESTAURANT_FOOD",
                "confidence": 0.90,
                "entities": {"multi": True},
                "is_multi_intent": True,
            }
        if has_business and has_food:
            return {
                "primary_intent": "SIMULATION_BUSINESS",
                "secondary_intent": "RESTAURANT_FOOD",
                "confidence": 0.88,
                "entities": {"multi": True},
                "is_multi_intent": True,
            }
        if has_travel and has_food:
            return {
                "primary_intent": "SIMULATION_TRAVEL",
                "secondary_intent": "RESTAURANT_FOOD",
                "confidence": 0.88,
                "entities": {"multi": True},
                "is_multi_intent": True,
            }

        return None

    # ═══════════════════════════════════════════════════════════════
    # PHASE 4 — SINGLE-INTENT SEMANTIC SCORING
    # ═══════════════════════════════════════════════════════════════

    def _score_all_intents(
        self, msg: str, session: Dict[str, Any]
    ) -> List[Tuple[str, float, Dict]]:
        scores: List[Tuple[str, float, Dict]] = []
        mood = session.get("current_mood", "neutral")
        interests = session.get("interests", {})

        # 0. GREETINGS (English, Telugu, Tenglish)
        greetings = [
            "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
            "good night", "namaskaram", "namaste", "నమస్కారం", "హలో", "బాగున్నారా",
            "ela unnav", "ela unnaru", "baagunnava", "bagunnava", "hi ra", "hey there",
            "hello ela unnav", "namaskaram ela unnav", "how are you", "how are you doing"
        ]
        if any(msg == g or msg.startswith(g + " ") or msg.endswith(" " + g) for g in greetings):
            scores.append(("GREETING", 0.98, {}))

        # 0.1. EXPLICIT CRICKET CONVERSATION & TOPIC SWITCH (0.99)
        cricket_quiz_cues = ["quiz", "trivia", "challenge", "test", "game"]
        is_cricket_quiz = "cricket" in msg and any(q in msg for q in cricket_quiz_cues)
        cricket_cues = [
            "about cricket", "cricket gurinchi", "cricket gurinchi cheppu", "ledu naku cricket gurinchi cheppu",
            "naku cricket gurinchi cheppu", "virat kohli gurinchi", "virat kohli gurinchi cheppu",
            "virat kohli", "rohit sharma", "ms dhoni", "ipl updates", "cricket updates",
            "cricket matladudam", "cricket news", "team india", "ipl gurinchi", "ipl"
        ]
        if not is_cricket_quiz and (any(c in msg for c in cricket_cues) or ("cricket" in msg and not any(w in msg for w in ["food", "order", "table", "menu"])) or msg in ["virat", "kohli", "dhoni", "ipl", "team india"]):
            scores.append(("CRICKET", 0.99, {"explicit": True}))

        # 0.2. EXPLICIT MUSIC & SONG REQUESTS (0.99 - Always beats boredom / games)
        music_cues = [
            "songs vinalani", "songs vinali", "song vinali", "song vinalani", "music vinali",
            "music vinalani", "paatalu vinali", "paatalu vinalani", "songs kavali", "song kavali",
            "music kavali", "songs suggest", "song suggest", "suggest songs", "listen to songs",
            "listen to music", "melody songs", "playlist kavali", "paatalu", "oka song suggest",
            "oka song suggest cheyyi", "song suggest cheyyi", "songs suggest cheyyi",
            "songs vinadaniki", "paatalu vinadaniki", "songs ante istam", "music ante istam"
        ]
        if any(m in msg for m in music_cues) or (msg in ["music", "songs", "song", "paatalu"]) or (any(w in msg for w in ["song", "songs", "music", "paata", "paatalu"]) and any(w in msg for w in ["vinali", "vinalani", "kavali", "suggest", "listen", "playlist", "undhi", "undi", "play", "ante"])):
            scores.append(("MUSIC", 0.99, {"explicit": True}))

        # 0.3. EXPLICIT MOVIES & CINEMA (0.99)
        movie_cues = [
            "about movies", "about movie", "movie gurinchi", "movie gurinchi cheppu",
            "movies gurinchi", "movies gurinchi cheppu", "cinema gurinchi", "cinema gurinchi cheppu",
            "movie suggest", "suggest movie", "movie suggest cheyyi", "movies suggest cheyyi",
            "cinema kavali", "films gurinchi", "cinema chudali", "movie chudali"
        ]
        if any(m in msg for m in movie_cues) or msg in ["movies", "movie", "cinema", "films"] or (any(w in msg for w in ["movie", "movies", "cinema", "film", "films"]) and any(w in msg for w in ["gurinchi", "suggest", "kavali", "chudali", "chuddam", "undhi", "undi"])):
            scores.append(("MOVIES", 0.99, {"explicit": True}))

        # 0.4. EXPLICIT GAMES REQUEST (0.99)
        games_cues = [
            "game adadam", "game aadadam", "games aadali", "game aadali", "game kavali",
            "games kavali", "let's play a game", "play games", "play game", "games aadudam",
            "game adali", "games adali", "games adalani undi", "games aadalani undi",
            "game adalani undi", "game aadalani undi", "games adalani", "games aadalani",
            "game adalani", "game aadalani", "games aadali ani undi", "game aadali ani undi",
            "games aadudama", "game aadudama", "games adudama", "game adudama",
            "naku games adalani undi", "naku game adalani undi", "naku games aadalani undi"
        ]
        if any(g in msg for g in games_cues) or msg in ["games", "game"] or (any(w in msg for w in ["game", "games"]) and any(w in msg for w in ["adalani", "aadalani", "aadali", "adali", "kavali", "play", "undhi", "undi", "adadam", "aadadam", "adudam", "aadudam"])):
            scores.append(("GAMES", 0.99, {"explicit": True}))

        # 0.5. EXPLICIT FOOD REQUEST (0.99)
        food_explicit_cues = [
            "naku food kavali", "food kavali", "naaku food kavali", "biryani kavali",
            "food order cheyyali", "order food", "tinali", "aakali vesthundi", "edo okati tinali",
            "food tinali", "food tinalani undi"
        ]
        if any(f in msg for f in food_explicit_cues) or msg in ["food", "biryani"] or (any(w in msg for w in ["food", "biryani", "tiffin", "meals"]) and any(w in msg for w in ["kavali", "order", "tinali", "undhi", "undi"])):
            scores.append(("RESTAURANT_FOOD", 0.99, {"explicit": True}))

        # 0.6. EXPLICIT STUDY / EXAM / CODING REQUEST (0.99)
        study_cues = [
            "exam ki help kavali", "exams help", "study help", "exam help",
            "exam ki prepare", "preparing for exam", "exam undi", "exams unnayi",
            "help me study", "study ki help"
        ]
        if any(s in msg for s in study_cues):
            scores.append(("STUDY", 0.99, {"topic": "study", "explicit": True}))

        coding_cues = [
            "coding help", "code help", "coding help kavali", "python help kavali",
            "python nerchukovali", "programming help", "write python code", "write code",
            "coding nerchukovali", "programming nerchukovali"
        ]
        if any(c in msg for c in coding_cues):
            scores.append(("CODING", 0.99, {"topic": "coding", "explicit": True}))

        # 0.7. ANSWER TO PREVIOUS QUESTION (Conversation Continuity - 0.98)
        history = session.get("history", [])
        last_bot_msg = next((h.get("text", "") for h in reversed(history) if h.get("sender") in ["assistant", "bot"]), None)
        if last_bot_msg and ("?" in last_bot_msg or any(q in last_bot_msg.lower() for q in ["istam", "evaru", "which", "who", "favourite", "favorite", "choice", "genre", "player", "team", "mood"])):
            # Check if current user message is not a distinct command or new activity
            not_new_command = not any(c in msg for c in ["book table", "table book", "pay", "order", "cancel", "reset", "clear"])
            if not_new_command and len(msg.split()) <= 6:
                scores.append(("ANSWER_TO_PREVIOUS_QUESTION", 0.98, {"last_bot_question": last_bot_msg}))

        # 0.8. PREFERENCE SHARING (Statements like 'naku cricket ante istam', 'coding nerchukuntunna' - 0.97)
        preference_cues = [
            "ante istam", "chala istam", "ante chaala istam", "ante pichi", "naku istam",
            "i like", "i love", "my favourite", "my favorite", "nerchukuntunna",
            "prepare avtunna", "preparing for", "nerchuko", "nerchukunna"
        ]
        if any(p in msg for p in preference_cues):
            scores.append(("PREFERENCE_SHARING", 0.97, {}))

        # 0.9. CASUAL CHAT & TODAY'S SPECIALS (0.96 - Never route to Knowledge Hub)
        casual_cues = [
            "am good", "i'm good", "im good", "i am good", "doing good", "doing well",
            "bagunna", "nenu bagunna", "baagunnanu", "all good", "fine", "i am fine",
            "im fine", "i'm fine", "chala bagunna", "super unna", "mast unna",
            "enati special", "em special", "enti special", "eanti special", "yenti special",
            "what's special", "whats special", "special today", "today em undi", "ivala em special",
            "eeroju special", "ee roju special", "today special", "what is special",
            "what is happening today", "what's happening today", "whats happening today",
            "em undi ivala", "em undi eeroju", "any plans for today", "plans today",
            "what can i do today", "what should i do", "tell me something fun",
            "em chestunnav", "em chestunnaru", "let's chat", "let's talk", "matladudam"
        ]
        if any(c in msg for c in casual_cues):
            scores.append(("CASUAL_CHAT", 0.96, {}))

        # 1. PAYMENT
        s = self._score_payment(msg)
        if s > 0:
            scores.append(("PAYMENT", s, {}))


        # 2. TABLE BOOKING
        s = self._score_booking(msg)
        if s > 0:
            scores.append(("TABLE_BOOKING", s, {}))

        # 3. GAME VICTORY alone
        if self._tel_hit(msg, self.GAME_WIN_SIGNALS):
            scores.append(("GAME_VICTORY", 0.88, {"celebration": True}))

        # 4. CURRENT INFO — before general knowledge (more specific)
        s = self._score_current_info(msg)
        if s > 0:
            scores.append(("CURRENT_INFO", s, {}))

        # 5. RESTAURANT / FOOD
        s = self._score_food(msg)
        if s > 0:
            scores.append(("RESTAURANT_FOOD", s, {}))

        # 6. FARMING SIMULATION
        s = self._score_farming(msg)
        if s > 0:
            scores.append(("SIMULATION_FARMING", s, {}))

        # 7. BUSINESS SIMULATION
        s = self._score_business(msg)
        if s > 0:
            scores.append(("SIMULATION_BUSINESS", s, {}))

        # 8. TRAVEL PLANNING
        s = self._score_travel(msg)
        if s > 0:
            scores.append(("SIMULATION_TRAVEL", s, {}))

        # 9. COOKING ASSISTANT
        s = self._score_cooking(msg)
        if s > 0:
            scores.append(("SIMULATION_COOKING", s, {}))

        # 10. LEARNING / TUTORIALS
        s, entities = self._score_learning(msg)
        if s > 0:
            scores.append(("LEARNING", s, entities))

        # 11. ENTERTAINMENT
        s, entities = self._score_entertainment(msg, mood, interests)
        if s > 0:
            scores.append(("ENTERTAINMENT", s, entities))

        # 12. GENERAL KNOWLEDGE (covers wide breadth of topics + Tenglish)
        s = self._score_knowledge(msg)
        if s > 0:
            scores.append(("GENERAL_KNOWLEDGE", s, {}))

        return scores

    # ═══════════════════════════════════════════════════════════════
    # INDIVIDUAL SCORERS
    # ═══════════════════════════════════════════════════════════════

    def _score_payment(self, msg: str) -> float:
        explicit = [
            "pay", "payment", "bill", "upi", "google pay", "gpay", "phonepe",
            "paytm", "credit card", "debit card", "cash", "checkout",
            "pay now", "pay bill", "online payment", "wallet",
            "settle bill", "how much do i owe",
        ]
        hits = sum(1 for w in explicit if w in msg)
        if hits >= 2:
            return 0.95
        if hits == 1:
            return 0.85
        return 0.0

    def _score_booking(self, msg: str) -> float:
        for phrase in self.BOOKING_SIGNALS + self.TELUGU_BOOKING:
            if phrase in msg:
                return 0.95
        has_action = any(w in msg for w in ["book", "reserve", "reservation"])
        has_target = any(w in msg for w in ["table", "seat", "dinner", "lunch", "spot"])
        if has_action and has_target:
            return 0.90
        return 0.0

    def _score_food(self, msg: str) -> float:
        for phrase in self.TELUGU_FOOD:
            if phrase in msg:
                return 0.93

        if any(w in msg for w in [
            "hungry", "starving", "famished", "craving", "i need food",
            "i want food", "let's eat", "want to eat", "need to eat",
        ]):
            return 0.92

        if re.search(r'\border\s+\d+|\bi\s+want\s+to\s+order\b|\bplace\s+an\s+order\b', msg):
            return 0.95

        hits = sum(1 for w in self.FOOD_SIGNALS if w in msg)
        if hits >= 3:
            return 0.90
        if hits == 2:
            return 0.82
        if hits == 1:
            return 0.70
        return 0.0

    def _score_current_info(self, msg: str) -> float:
        very_explicit = [
            "who is the current", "who is the pm", "who is the prime minister",
            "who is the president", "current prime minister", "latest news",
            "today's news", "cricket score", "live score", "weather today",
            "today's weather", "current weather", "stock price",
            "election result", "breaking news", "who won the election",
            "current leader", "current cm", "current chief minister",
            "latest cricket", "latest match", "who is pm", "today's headlines",
            "political headlines", "today's gold price", "gold price today",
            "latest movies", "what happened yesterday", "who won today's match",
        ]
        for phrase in very_explicit:
            if phrase in msg:
                return 0.95

        has_current_word = any(w in msg for w in [
            "current", "latest", "now", "today", "right now",
            "currently", "as of now", "2024", "2025", "2026", "yesterday",
        ])
        has_info_word = any(w in msg for w in [
            "news", "update", "score", "result", "leader", "pm", "president",
            "minister", "weather", "temperature", "price", "rate", "gold",
            "headlines", "match", "movie",
        ])
        if has_current_word and has_info_word:
            return 0.88
        return 0.0

    def _score_knowledge(self, msg: str) -> float:
        if self._signal_hit(msg, self.FOOD_SIGNALS[:20]):
            return 0.0

        # Telugu-English knowledge starters
        for tel_k in self.TELUGU_KNOWLEDGE:
            if tel_k in msg:
                return 0.90

        knowledge_starters = [
            "what is ", "what are ", "who was ", "who invented ", "who discovered ",
            "when was ", "when did ", "where is ", "where was ",
            "how does ", "how do ", "why is ", "why does ", "why are ",
            "explain ", "define ", "definition of ", "meaning of ",
            "tell me about ", "describe ", "what does ", "which is ",
            "can you explain ",
        ]
        for starter in knowledge_starters:
            if msg.startswith(starter.strip()) or f" {starter.strip()} " in f" {msg} ":
                return 0.85

        hits = sum(1 for w in self.KNOWLEDGE_SIGNALS if w in msg)
        if hits >= 2:
            return 0.80
        if hits == 1:
            return 0.60
        return 0.0

    def _score_farming(self, msg: str) -> float:
        for phrase in self.TELUGU_FARMING:
            if phrase in msg:
                return 0.95
        hits = sum(1 for w in self.FARMING_SIGNALS if w in msg)
        if hits >= 2:
            return 0.90
        if hits == 1:
            return 0.75
        return 0.0

    def _score_business(self, msg: str) -> float:
        for phrase in self.TELUGU_BUSINESS:
            if phrase in msg:
                return 0.92
        if any(w in msg for w in [
            "start a business", "launch a startup", "business plan",
            "business simulation", "startup idea",
        ]):
            return 0.95
        hits = sum(1 for w in self.BUSINESS_SIGNALS if w in msg)
        if hits >= 2:
            return 0.88
        if hits == 1:
            return 0.65
        return 0.0

    def _score_travel(self, msg: str) -> float:
        for phrase in self.TELUGU_TRAVEL:
            if phrase in msg:
                return 0.92
        if any(w in msg for w in [
            "plan a trip", "plan my trip", "travel itinerary", "vacation plan",
            "holiday plan",
        ]):
            return 0.95
        hits = sum(1 for w in self.TRAVEL_SIGNALS if w in msg)
        if hits >= 2:
            return 0.88
        if hits == 1:
            return 0.65
        return 0.0

    def _score_cooking(self, msg: str) -> float:
        if any(w in msg for w in [
            "how to cook", "recipe for", "cooking tutorial", "teach me to cook",
            "how to make", "give me a recipe",
        ]):
            return 0.92
        hits = sum(1 for w in self.COOKING_SIGNALS if w in msg)
        if hits >= 2:
            return 0.85
        if hits == 1:
            return 0.65
        return 0.0

    def _score_learning(self, msg: str) -> Tuple[float, Dict]:
        entities: Dict[str, Any] = {}

        for phrase in self.TELUGU_LEARNING:
            if phrase in msg:
                entities["topic"] = "general"
                return 0.88, entities

        TECH_TOPICS = {
            "python": "python",
            "javascript": "javascript",
            "java": "java",
            "html": "html",
            "css": "css",
            "sql": "sql",
            "react": "react",
            "node": "node.js",
            "c++": "c++",
            "c#": "c#",
            "typescript": "typescript",
            "machine learning": "machine learning",
            "deep learning": "deep learning",
            "data science": "data science",
        }
        is_info_question = any(q in msg for q in ["who ", "what is", "what are", "when ", "why ", "tell me about", "history of", "origin of"])
        for keyword, topic in TECH_TOPICS.items():
            if keyword in msg:
                entities["topic"] = topic
                if any(w in msg for w in ["teach", "learn", "tutorial", "course", "how to code"]):
                    return 0.95, entities
                if is_info_question:
                    return 0.0, entities
                return 0.70, entities

        if any(w in msg for w in [
            "teach me", "i want to learn", "step by step guide",
            "tutorial for", "how to learn",
        ]):
            return 0.85, entities


        hits = sum(1 for w in self.LEARNING_SIGNALS if w in msg)
        if hits >= 3:
            return 0.80, entities
        if hits == 2:
            return 0.65, entities
        return 0.0, entities

    def _score_entertainment(
        self, msg: str, mood: str, interests: Dict[str, Any]
    ) -> Tuple[float, Dict]:
        entities: Dict[str, Any] = {}

        # If user explicitly requested music, movies, or food along with boredom, do not trigger game/riddle
        if any(w in msg for w in ["song", "songs", "music", "paata", "paatalu", "movie", "movies", "cinema", "film", "food", "biryani", "order", "table book"]):
            return 0.0, entities

        for phrase in self.TELUGU_GAME:
            if phrase in msg:
                entities["game_type"] = "general"
                return 0.93, entities

        for phrase in self.TELUGU_BORED:
            if phrase in msg:
                entities["mood"] = "bored"
                return 0.88, entities

        if any(w in msg for w in [
            "entertain me", "entertain", "play a game", "let's play", "play game",
        ]):
            return 0.92, entities

        if any(w in msg for w in ["tell me a joke", "tell a joke", "make me laugh", "joke"]):
            entities["game_type"] = "joke"
            return 0.90, entities

        if any(w in msg for w in ["riddle", "give me a riddle", "puzzle", "brain teaser"]):
            entities["game_type"] = "riddle"
            return 0.90, entities

        if any(w in msg for w in ["trivia", "quiz me", "fun fact", "interesting fact", "quiz"]):
            entities["game_type"] = "trivia"
            return 0.88, entities

        if "cricket" in msg and any(w in msg for w in ["quiz", "trivia", "game", "challenge", "test", "adudama", "aadudama"]):
            entities["game_type"] = "cricket_trivia"
            boost = 0.05 if interests.get("sports") == "cricket" else 0.0
            return 0.85 + boost, entities

        mood_boost = 0.10 if mood == "bored" else 0.0
        hits = sum(1 for w in self.GAME_SIGNALS if w in msg)
        if hits >= 2:
            return 0.82 + mood_boost, entities
        if hits == 1:
            return 0.65 + mood_boost, entities
        return 0.0, entities

    # ═══════════════════════════════════════════════════════════════
    # UTILITY HELPERS
    # ═══════════════════════════════════════════════════════════════

    def _signal_hit(self, msg: str, cluster: List[str]) -> bool:
        return any(w in msg for w in cluster)

    def _tel_hit(self, msg: str, phrases: List[str]) -> bool:
        return any(p in msg for p in phrases)

    def _is_very_vague(self, msg: str) -> bool:
        very_vague_exact = {
            "i need something", "help me", "something", "i want something",
            "anything", "whatever", "idk", "i don't know", "dunno",
            "maybe", "i guess", "hmm", "uh", "er", "ok", "okay", "fine",
        }
        if msg.strip() in very_vague_exact:
            return True
        words = msg.split()
        has_signal = (
            self._signal_hit(msg, self.FOOD_SIGNALS[:15])
            or self._signal_hit(msg, self.GAME_SIGNALS[:10])
            or self._signal_hit(msg, self.LEARNING_SIGNALS[:10])
            or self._signal_hit(msg, self.KNOWLEDGE_SIGNALS[:10])
        )
        return len(words) <= 2 and not has_signal

    def _clarification_result(self) -> Dict[str, Any]:
        return {
            "primary_intent": "CLARIFICATION_NEEDED",
            "secondary_intent": None,
            "confidence": 0.25,
            "entities": {},
            "is_multi_intent": False,
        }

    def _general_conversation_result(self) -> Dict[str, Any]:
        return {
            "primary_intent": "GENERAL_CONVERSATION",
            "secondary_intent": None,
            "confidence": 0.50,
            "entities": {},
            "is_multi_intent": False,
        }


# ── Singletons ─────────────────────────────────────────────────────
semantic_intent_detector = SemanticIntentDetector()
intent_detector = semantic_intent_detector

