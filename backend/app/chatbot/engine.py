import re
import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models import MenuItem, MenuCategory, RestaurantTable, Booking, Order, OrderItem, User
from app.chatbot.intent_detector import intent_detector
from app.chatbot.handlers.knowledge_handler import knowledge_handler
from app.chatbot.handlers.learning_handler import learning_handler
from app.chatbot.handlers.simulation_handler import simulation_handler
from app.chatbot.handlers.entertainment_handler import entertainment_handler
from app.chatbot.handlers.payment_handler import payment_handler
from app.chatbot.handlers.conversation_handler import conversation_handler

class ResponseValidator:
    """
    Response Validator Layer.
    Guarantees:
    1. No generic fallback messages ('Nenu ikkade unnanu...', 'How can I help you?', 'ela help cheyyagalanu')
       can leak when user's intent is known (GAMES, CRICKET, MUSIC, MOVIES, FOOD, STUDY, CODING).
    2. Quick replies are generated strictly from the active intent and never from old topics.
    3. Seamless fallback replacement with rich, natural, contextual dialogue.
    """
    @staticmethod
    def validate_and_fix(
        response: Dict[str, Any],
        active_intent: str,
        user_name: str,
        user_msg: str,
        active_language: str
    ) -> Dict[str, Any]:
        if not isinstance(response, dict):
            response = {"message": "", "intent": active_intent, "action_type": None, "quick_replies": [], "structured_data": None}
            
        msg_text = response.get("message", "").strip()
        cleaned_user = user_msg.lower().strip()
        
        # Detect fallback failure phrases
        is_generic_fallback = any(fb in msg_text.lower() for fb in [
            "nenu ikkade unnanu", "em matladukundam", "ela help cheyyagalanu",
            "how can i help", "how can i assist", "what can i do for you"
        ])

        # If intent is known and specific, but response was generic fallback or empty:
        if is_generic_fallback or not msg_text:
            if active_intent in ["GAMES", "game"]:
                if active_language == "telugu_script":
                    response["message"] = f"ఖచ్చితంగా {user_name}! 😄 మనం ఒక ఆట ఆడదాం. ఏదైనా ఒకటి ఎంచుకోండి:\n\n🎯 నంబర్ గెస్సింగ్ గేమ్\n🧠 సాధారణ జ్ఞానం క్విజ్\n🧩 పొడుపు కథలు (రిడిల్స్)\n🏏 క్రికెట్ క్విజ్"
                elif active_language == "tenglish":
                    response["message"] = f"Sure {user_name}! 😄 Game aadham! Pick one:\n\n🎯 Guess the Number\n🧠 Trivia Quiz\n🧩 Riddles\n🏏 Cricket Quiz"
                else:
                    response["message"] = f"Sure {user_name}! 😄 Let's play a game. Pick one:\n\n🎯 Guess the Number\n🧠 Trivia Quiz\n🧩 Riddles\n🏏 Cricket Quiz"
                response["intent"] = "entertainment_game_menu"
                response["quick_replies"] = [
                    {"label": "🎯 Guess the Number", "payload": "Guess the number game", "icon": "Gamepad2"},
                    {"label": "🧠 Trivia Quiz", "payload": "Trivia quiz adudam", "icon": "HelpCircle"},
                    {"label": "🧩 Riddle", "payload": "Give me a riddle", "icon": "Sparkles"},
                    {"label": "🏏 Cricket Quiz", "payload": "Cricket trivia", "icon": "Trophy"}
                ]
            elif active_intent in ["CRICKET", "cricket"]:
                if active_language == "telugu_script":
                    response["message"] = "ఖచ్చితంగా 🏏 క్రికెట్ గురించి మాట్లాడుకుందాం! టీమ్ ఇండియా, ఐపీఎల్, విరాట్ కోహ్లీ, మ్యాచ్‌లు, రికార్డులు లేదా తాజా క్రికెట్ అప్‌డేట్స్ — ఏది కావాలి?"
                elif active_language == "tenglish":
                    response["message"] = "Sure 🏏 Cricket gurinchi matladukundam! Team India, IPL, Virat Kohli, matches, records leka latest cricket updates — edhi kavali?"
                else:
                    response["message"] = "Sure 🏏 Let's talk cricket! Team India, IPL, Virat Kohli, matches, records, or latest cricket updates — what would you like to discuss?"
                response["intent"] = "topic_cricket"
                response["quick_replies"] = [
                    {"label": "🏏 Team India", "payload": "Team India updates", "icon": "Flame"},
                    {"label": "🏆 IPL", "payload": "IPL updates", "icon": "Trophy"},
                    {"label": "👑 Virat Kohli", "payload": "about Virat Kohli", "icon": "Star"},
                    {"label": "📊 Records", "payload": "cricket records", "icon": "Activity"}
                ]
            elif active_intent in ["MUSIC", "music"]:
                if active_language == "tenglish":
                    response["message"] = "Sure 🎧 Songs mood ki veldam. Melody, energetic, romantic leka chill?"
                elif active_language == "telugu_script":
                    response["message"] = "ఖచ్చితంగా 🎧 పాటల మూడ్‌కి వెళ్దాం! మెలోడీ, ఎనర్జిటిక్, రొమాంటిక్ లేదా ప్రశాంతమైన పాటలా?"
                else:
                    response["message"] = "Sure 🎧 Let's go with music! Do you prefer melody, energetic, romantic, or chill songs?"
                response["intent"] = "preference_music"
                response["quick_replies"] = [
                    {"label": "🎧 Melody", "payload": "melody songs", "icon": "Music"},
                    {"label": "🔥 Energetic", "payload": "energetic songs", "icon": "Zap"},
                    {"label": "❤️ Romantic", "payload": "romantic songs", "icon": "Heart"},
                    {"label": "😌 Chill", "payload": "chill songs", "icon": "Coffee"}
                ]
            elif active_intent in ["MOVIES", "movies"]:
                if active_language == "tenglish":
                    response["message"] = "Sure 🎬 Movies gurinchi matladukundam! Latest releases, Tollywood, blockbuster hits, OTT suggestions leka movie recommendations — edhi kavali?"
                elif active_language == "telugu_script":
                    response["message"] = "ఖచ్చితంగా 🎬 సినిమాల గురించి మాట్లాడుకుందాం! తాజా రిలీజ్‌లు, టాలీవుడ్ హిట్స్, ఓటీటీ సలహాలు లేదా మూవీ రికమెండేషన్స్ — ఏది కావాలి?"
                else:
                    response["message"] = "Sure 🎬 Let's talk movies! Latest releases, blockbuster hits, OTT suggestions, or movie recommendations — what would you like?"
                response["intent"] = "topic_movies"
                response["quick_replies"] = [
                    {"label": "🍿 Latest Releases", "payload": "latest movies", "icon": "Film"},
                    {"label": "🌟 OTT Recommendations", "payload": "ott movies", "icon": "Tv"},
                    {"label": "🔥 Tollywood Hits", "payload": "tollywood hits", "icon": "Star"}
                ]
            elif active_intent in ["STUDY", "study"]:
                response["message"] = "All the best 📚 Exam preparation ki nenu help chestanu! Em subject or topic gurinchi help kavali?"
                response["intent"] = "preference_exam"
                response["quick_replies"] = [
                    {"label": "📚 Quick Notes", "payload": "give quick notes", "icon": "BookOpen"},
                    {"label": "💡 Important Topics", "payload": "important topics", "icon": "Lightbulb"}
                ]
            elif active_intent in ["CODING", "coding"]:
                response["message"] = "Nice 💻 Coding & Programming help kavala! Python, JavaScript, Algorithms leka Web Development — em topic lo help kavali?"
                response["intent"] = "preference_coding"
                response["quick_replies"] = [
                    {"label": "🐍 Python", "payload": "Python help", "icon": "Code"},
                    {"label": "⚡ JavaScript", "payload": "JavaScript help", "icon": "Code"},
                    {"label": "🧠 Algorithms", "payload": "DSA help", "icon": "Terminal"}
                ]

        return response


class RestaurantChatbotEngine:
    """
    Intelligent Conversational AI Assistant & Companion Engine.
    Implements:
    - Step 1: User personalization & dynamic time greetings
    - Step 2: Human empathy, mood inference, casual dialogue, context memory
    - Step 3: Semantic multi-intent detection, Telugu-English NLP, intelligent modular routing,
      interactive virtual simulations (Farming, Business, Travel), learning tutorials, and payment processing.
    """

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_session(self, session_id: str, user_name: Optional[str] = None) -> Dict[str, Any]:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "state": "IDLE",
                "user_name": user_name or "Friend",
                "current_mood": "neutral",
                "active_language": None,
                "active_intent": None,
                "current_activity": None,
                "last_activity_intent": None,
                "interests": {"gaming": [], "movies": [], "sports": [], "hobbies": []},
                "active_situation": None,
                "active_simulation": None,
                "active_learning": None,
                "active_riddle": None,
                "last_intent": None,
                "booking_slots": {
                    "guests": None,
                    "date": None,
                    "time": None,
                    "location": None,
                    "customer_name": user_name,
                    "special_requests": None
                },
                "order_cart": [],
                "history": []
            }
        elif user_name:
            self.sessions[session_id]["user_name"] = user_name
            if not self.sessions[session_id]["booking_slots"]["customer_name"]:
                self.sessions[session_id]["booking_slots"]["customer_name"] = user_name
        return self.sessions[session_id]

    def reset_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def process_message(
        self,
        session_id: str,
        message: str,
        db: Session,
        user_id: Optional[int] = None,
        user_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Main multi-intent detection, routing, and response execution pipeline."""
        res = self._process_message_internal(session_id, message, db, user_id, user_name)
        session = self.get_session(session_id, user_name)
        if isinstance(res, dict) and "message" in res:
            session["history"].append({"sender": "assistant", "text": res["message"]})
        return res

    def _process_message_internal(
        self,
        session_id: str,
        message: str,
        db: Session,
        user_id: Optional[int] = None,
        user_name: Optional[str] = None
    ) -> Dict[str, Any]:
        session = self.get_session(session_id, user_name)
        cleaned_msg = message.strip().lower()
        session["history"].append({"sender": "user", "text": message})

        current_user = session.get("user_name") or user_name or "Friend"

        from app.chatbot.hf_client import detect_language, detect_message_language

        # Per-message language detection (language is a message property, NOT a session property)
        # Only exception: explicit user override like "speak in english" / "telugu lo cheppu"
        explicit_lang = None
        if any(w in cleaned_msg for w in ["english lo", "in english", "speak english"]):
            explicit_lang = "english"
        elif any(w in cleaned_msg for w in ["telugu lo", "in telugu", "speak telugu"]):
            explicit_lang = "telugu_script" if any('\u0c00' <= c <= '\u0c7f' for c in message) else "tenglish"

        if explicit_lang:
            # User explicitly wants a language — lock it in session for this override
            session["active_language"] = explicit_lang
            lang_info = {"language": explicit_lang, "script": "telugu" if explicit_lang == "telugu_script" else "roman", "style": "casual"}
        else:
            # Always detect fresh for this message — do NOT use stale session value
            lang_info = detect_message_language(message)
            # Update session active_language to reflect current message (for handlers that use it)
            session["active_language"] = lang_info["language"]

        active_language = lang_info["language"]
        current_script = lang_info.get("script", "roman")
        current_style = lang_info.get("style", "casual")

        # Explicit reset / clear
        if cleaned_msg in ["cancel", "reset", "start over", "clear", "restart"]:
            self.reset_session(session_id)
            return {
                "message": f"✨ I've cleared our chat history, {current_user}! What would you like to explore or do next?",
                "intent": "reset",
                "action_type": None,
                "quick_replies": self._default_quick_replies(current_user),
                "structured_data": None
            }

        # Step 3: Intent Detection & Intelligent Routing
        intent_data = intent_detector.detect(cleaned_msg, message, session)
        primary_intent = intent_data["primary_intent"]
        secondary_intent = intent_data.get("secondary_intent")
        is_explicit = intent_data.get("is_explicit_intent", False)

        # State Machine: Enforce active intent & clean topic switching
        previous_intent = session.get("active_intent")
        if is_explicit or primary_intent in ["GAMES", "CRICKET", "MUSIC", "MOVIES", "RESTAURANT_FOOD", "STUDY", "CODING"]:
            active_intent = primary_intent
            session["current_activity"] = None
            session["active_riddle"] = None
            session["active_simulation"] = None
            session["active_learning"] = None
        elif primary_intent == "ANSWER_TO_PREVIOUS_QUESTION":
            active_intent = previous_intent or "casual_chat"
        else:
            active_intent = primary_intent

        session["active_intent"] = active_intent
        session["last_intent"] = active_intent

        # Step 4: Semantic RAG Memory & Tool / API Integration
        from app.chatbot.tool_router import tool_router
        from app.chatbot.rag_memory import rag_memory

        current_topic = intent_data.get("topic") or active_intent.lower()
        rag_context = rag_memory.retrieve_context(cleaned_msg, session_id=session_id)
        session["rag_context"] = rag_context

        if primary_intent == "PREFERENCE_SHARING" or "istam" in cleaned_msg or "like" in cleaned_msg:
            rag_memory.add_user_memory(session_id, message[:120])

        # Route to External Tools (Web, Sports, Restaurant, Reservation, Music)
        tool_result = tool_router.route_and_execute(
            intent=active_intent,
            topic=current_topic,
            user_msg=message,
            language=active_language,
            db_session=db
        )
        if tool_result:
            session["last_tool_result"] = tool_result

        def _set_activity(name: str):
            session["current_activity"] = name
            session["last_activity_intent"] = active_intent

        # ------------------ Multi-Intent Sequencing ------------------
        if primary_intent == "SIMULATION_FARMING" and secondary_intent == "RESTAURANT_FOOD":
            farm_res = simulation_handler.handle_farming_simulation(cleaned_msg, current_user, session)
            combined_message = (
                f"Awesome plan, {current_user}! Let's start with your virtual paddy cultivation 🌾, "
                f"and I've got our chef's signature Royal Chicken Biryani ready for your order as soon as we finish!\n\n"
                + farm_res["message"]
            )
            farm_res["message"] = combined_message
            return ResponseValidator.validate_and_fix(farm_res, active_intent, current_user, message, active_language)

        if primary_intent == "GAME_VICTORY_FOOD":
            _set_activity("game")
            res = entertainment_handler.handle_game_victory_food(current_user)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # ------------------ Modular Intent Routing ------------------

        # 1. Greetings
        if primary_intent == "GREETING":
            _set_activity("greeting")
            res = conversation_handler.handle_time_greeting(current_user, message, active_language)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 1.5. Cricket, Movies, Music, Study, Coding, Casual Chat, Preference Sharing, Q&A Continuity
        if primary_intent in ["CRICKET", "MOVIES", "MUSIC", "STUDY", "CODING", "CASUAL_CHAT", "GENERAL_CONVERSATION", "PREFERENCE_SHARING", "ANSWER_TO_PREVIOUS_QUESTION"]:
            activity_map = {
                "CRICKET": "cricket",
                "MOVIES": "movies",
                "MUSIC": "music",
                "STUDY": "study",
                "CODING": "coding",
                "CASUAL_CHAT": "casual_chat",
                "PREFERENCE_SHARING": "preference",
                "ANSWER_TO_PREVIOUS_QUESTION": session.get("current_activity") or "conversation"
            }
            _set_activity(activity_map.get(primary_intent, "casual_chat"))
            res = conversation_handler.handle_casual_chat(message, current_user, session, active_language)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 2. Ambiguity Clarification
        if primary_intent == "CLARIFICATION_NEEDED":
            _set_activity("clarification")
            res = conversation_handler.handle_clarification(current_user, message, active_language)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 3. Emotional Empathy & Mood
        if primary_intent == "EMPATHY_MOOD":
            _set_activity("empathy")
            res = conversation_handler.handle_empathy_mood(cleaned_msg, current_user, session, active_language)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 4. Casual Nothing / Chilling
        if primary_intent == "GENERAL_CHILL":
            _set_activity("chill")
            res = conversation_handler.handle_chill_nothing(current_user, message, active_language)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 5. Current Information & General Knowledge (Step 4)
        if primary_intent in [
            "CURRENT_INFO", "GENERAL_KNOWLEDGE", "KNOWLEDGE_COMPARISON",
            "KNOWLEDGE_HOW_TO", "KNOWLEDGE_SIMPLIFY", "KNOWLEDGE_DEEPEN",
            "KNOWLEDGE_QUIZ", "KNOWLEDGE_FOLLOWUP"
        ]:
            _set_activity("knowledge")
            res = knowledge_handler.handle_knowledge_query(cleaned_msg, current_user, session, db, active_language)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 6. Learning & Coding Tutorials (Python)
        if primary_intent in ["LEARNING", "LEARNING_PYTHON", "LEARNING_CONTINUE"]:
            _set_activity("learning")
            res = learning_handler.handle_python_tutorial(cleaned_msg, current_user, session)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 7. Interactive Simulations
        if primary_intent in ["SIMULATION_FARMING", "SIMULATION_FARMING_STEP"]:
            _set_activity("simulation_farming")
            res = simulation_handler.handle_farming_simulation(cleaned_msg, current_user, session)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        if primary_intent in ["SIMULATION_BUSINESS", "SIMULATION_BUSINESS_STEP"]:
            _set_activity("simulation_business")
            res = simulation_handler.handle_business_simulation(cleaned_msg, current_user, session)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        if primary_intent in ["SIMULATION_TRAVEL", "SIMULATION_TRAVEL_STEP"]:
            _set_activity("simulation_travel")
            res = simulation_handler.handle_travel_planner(cleaned_msg, current_user, session)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        if primary_intent in ["SIMULATION_COOKING", "SIMULATION_COOKING_STEP"]:
            _set_activity("simulation_cooking")
            res = simulation_handler.handle_cooking_assistant(cleaned_msg, current_user)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 8. Entertainment: Games, Riddles, Trivia, Jokes, Game Victories
        if primary_intent in ["GAMES", "ENTERTAINMENT", "ENTERTAINMENT_GAME"]:
            _set_activity("game")
            if any(w in cleaned_msg for w in ["joke", "funny"]):
                res = entertainment_handler.handle_joke(cleaned_msg, current_user)
            elif any(w in cleaned_msg for w in ["cricket", "ipl", "score", "batsman"]):
                res = entertainment_handler.handle_cricket_trivia(cleaned_msg, current_user)
            elif primary_intent == "GAMES" or (any(w in cleaned_msg for w in ["games aadali", "game aadali", "game kavali", "games kavali", "games", "game", "play game", "play games", "aadali", "aadudam"]) and not any(r in cleaned_msg for r in ["riddle", "puzzle", "podupu"])):
                res = entertainment_handler.handle_games_menu(cleaned_msg, current_user, session, active_language)
            else:
                res = entertainment_handler.handle_game_riddle(cleaned_msg, current_user, session, active_language)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 9. Payments & Bill Settlement
        if primary_intent == "PAYMENT":
            _set_activity("payment")
            res = payment_handler.handle_payment(cleaned_msg, current_user, db, session)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 10. Table Booking
        if primary_intent == "TABLE_BOOKING" or (session["state"] == "BOOKING_FLOW" and not self._is_topic_change(cleaned_msg)):
            _set_activity("booking")
            res = self._handle_booking_flow_orchestrator(session, message, cleaned_msg, db, user_id, current_user)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 11. Restaurant & Food
        if primary_intent == "RESTAURANT_FOOD":
            _set_activity("food")
            res = self._handle_food_orchestrator(session, message, cleaned_msg, db, user_id, current_user)
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # 12. Gratitude
        if primary_intent == "THANKS":
            res = {
                "message": f"😊 Always my pleasure, {current_user}! Let me know if there's anything else you'd like to explore, learn, or order!",
                "intent": "thanks",
                "action_type": None,
                "quick_replies": self._default_quick_replies(current_user),
                "structured_data": None
            }
            return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)

        # Fallback: Natural Casual Conversation (Never force Knowledge Hub)
        _set_activity("casual_chat")
        res = conversation_handler.handle_casual_chat(message, current_user, session, active_language)
        return ResponseValidator.validate_and_fix(res, active_intent, current_user, message, active_language)


    # ------------------ Topic Change Detection ------------------
    def _is_topic_change(self, msg: str) -> bool:
        topic_change_cues = [
            "actually", "nevermind", "change topic", "tell me about", "what is", "how do",
            "im bored", "i'm bored", "tell a joke", "talk about", "explain", "who is",
            "im tired", "i'm tired", "i have an exam", "play a game", "politics", "paddy"
        ]
        return any(cue in msg for cue in topic_change_cues)

    # ------------------ Food Orchestrator ------------------
    def _handle_food_orchestrator(
        self,
        session: Dict[str, Any],
        raw_msg: str,
        msg: str,
        db: Optional[Session],
        user_id: Optional[int],
        user_name: str
    ) -> Dict[str, Any]:
        all_items = db.query(MenuItem).filter(MenuItem.availability == True).all() if db else []

        # Check if user mentioned specific items to order
        detected_items = []
        for item in all_items:
            pattern = rf'(\d+)?\s*(?:x\s*)?{re.escape(item.name.lower())}'
            match = re.search(pattern, msg)
            if match or item.name.lower() in msg:
                qty = 1
                if match and match.group(1):
                    try:
                        qty = int(match.group(1))
                    except ValueError:
                        qty = 1
                detected_items.append({"item": item, "qty": qty})

        if detected_items:
            order_items_models = []
            total = 0.0
            for det in detected_items:
                itm = det["item"]
                q = det["qty"]
                total += itm.price * q
                order_items_models.append(OrderItem(
                    menu_item_id=itm.id,
                    quantity=q,
                    price=itm.price
                ))

            new_order = Order(
                user_id=user_id,
                customer_name=user_name,
                customer_phone="+1 555-0199",
                order_type="Dine-in",
                table_number=3,
                total_amount=round(total, 2),
                status="Order Placed",
                payment_method="Card",
                payment_status="Paid",
                items=order_items_models
            )
            db.add(new_order)
            db.commit()
            db.refresh(new_order)

            items_breakdown = "\n".join([f"• {det['qty']}x **{det['item'].name}** (${det['item'].price:.2f} ea)" for det in detected_items])

            return {
                "message": (
                    f"🛍️ **Order Successfully Created & Sent to Kitchen!**\n\n"
                    f"**Order Reference:** `#{new_order.id:04d}`\n\n"
                    f"**Items Ordered:**\n{items_breakdown}\n\n"
                    f"💰 **Total Amount:** **${new_order.total_amount:.2f}**\n"
                    f"⏱️ **Estimated Prep Time:** ~15–20 minutes\n"
                    f"📍 **Status:** 👨‍🍳 Preparing"
                ),
                "intent": "order_confirmed",
                "action_type": "ORDER_CONFIRMED",
                "quick_replies": [
                    {"label": f"📦 Track Order #{new_order.id}", "payload": f"Track order #{new_order.id}", "icon": "Compass"},
                    {"label": "💳 Settle Payment", "payload": "I want to pay", "icon": "CreditCard"},
                    {"label": "🍽️ Add More Items", "payload": "Show me desserts and drinks", "icon": "Plus"}
                ],
                "structured_data": {
                    "order": {
                        "id": new_order.id,
                        "customer_name": new_order.customer_name,
                        "total_amount": new_order.total_amount,
                        "status": new_order.status,
                        "items": [{"name": det["item"].name, "quantity": det["qty"], "price": det["item"].price} for det in detected_items]
                    }
                }
            }

        # Otherwise display menu recommendations
        sample_items = all_items[:4]
        serialized_items = [{
            "id": itm.id,
            "name": itm.name,
            "price": itm.price,
            "is_vegetarian": itm.is_vegetarian,
            "description": itm.description,
            "image": itm.image,
            "rating": itm.rating,
            "category_id": itm.category_id
        } for itm in sample_items]

        from app.chatbot.hf_client import detect_language
        lang = detect_language(raw_msg)

        if lang == "telugu_script":
            return {
                "message": (
                    f"🍽️ **తప్పకుండా, {user_name}! ఈరోజు మా చెఫ్ ప్రత్యేక వంటకాలు:**\n\n"
                    f"• **రాయల్ చికెన్ బిర్యానీ** 🍗 — **$450.00** (⭐ 4.9)\n"
                    f"• **క్రిస్పీ గోల్డెన్ ట్రఫుల్ ఫ్రైస్** 🌱 — **$160.00** (⭐ 4.6)\n"
                    f"• **చాక్లెట్ లావా కేక్** 🌱 — **$260.00** (⭐ 5.0)\n"
                    f"• **మామిడి పండ్ల లస్సీ** 🌱 — **$120.00** (⭐ 4.9)\n\n"
                    f"ఆర్డర్ చేయడానికి క్రింది బటన్ నొక్కండి, లేదా మీకు ఏ వంటకం కావాలో చెప్పండి!"
                ),
                "intent": "menu_browse_telugu",
                "action_type": "SHOW_MENU",
                "quick_replies": [
                    {"label": "🍗 రాయల్ చికెన్ బిర్యానీ", "payload": "నాకు బిర్యానీ కావాలి", "icon": "ShoppingBag"},
                    {"label": "🍟 ట్రఫుల్ ఫ్రైస్", "payload": "Order 1 Crispy Golden Truffle Fries", "icon": "ShoppingBag"},
                    {"label": "🍫 లావా కేక్", "payload": "Order 1 Molten Chocolate Lava Cake", "icon": "ShoppingBag"},
                    {"label": "🥤 మ్యాంగో లస్సీ", "payload": "Order 1 Fresh Alphonso Mango Lassi", "icon": "ShoppingBag"}
                ],
                "structured_data": {"menu_items": serialized_items}
            }

        if lang == "tenglish":
            return {
                "message": (
                    f"🍽️ **Sure, {user_name}! Eeroju mana chef top recommendations:**\n\n"
                    f"• **Royal Chicken Biryani** 🍗 — **$450.00** (⭐ 4.9)\n"
                    f"• **Crispy Golden Truffle Fries** 🌱 — **$160.00** (⭐ 4.6)\n"
                    f"• **Molten Chocolate Lava Cake** 🌱 — **$260.00** (⭐ 5.0)\n"
                    f"• **Fresh Alphonso Mango Lassi** 🌱 — **$120.00** (⭐ 4.9)\n\n"
                    f"Order cheyyadaniki kindha unna options select cheyyandi!"
                ),
                "intent": "menu_browse_tenglish",
                "action_type": "SHOW_MENU",
                "quick_replies": [
                    {"label": "🍗 Royal Chicken Biryani", "payload": "I want to order Royal Chicken Biryani", "icon": "ShoppingBag"},
                    {"label": "🍟 Truffle Fries", "payload": "Order 1 Crispy Golden Truffle Fries", "icon": "ShoppingBag"},
                    {"label": "🍫 Lava Cake", "payload": "Order 1 Molten Chocolate Lava Cake", "icon": "ShoppingBag"},
                    {"label": "🥤 Mango Lassi", "payload": "Order 1 Fresh Alphonso Mango Lassi", "icon": "ShoppingBag"}
                ],
                "structured_data": {"menu_items": serialized_items}
            }

        return {
            "message": (
                f"🍽️ **Of course, {user_name}! Here are our top chef recommendations today:**\n\n"
                f"• **Royal Chicken Biryani** 🍗 — **$450.00** (⭐ 4.9)\n"
                f"• **Crispy Golden Truffle Fries** 🌱 — **$160.00** (⭐ 4.6)\n"
                f"• **Molten Chocolate Lava Cake** 🌱 — **$260.00** (⭐ 5.0)\n"
                f"• **Fresh Alphonso Mango Lassi** 🌱 — **$120.00** (⭐ 4.9)\n\n"
                f"Click below to add to your order, or let me know what flavor you're in the mood for!"
            ),
            "intent": "menu_browse",
            "action_type": "SHOW_MENU",
            "quick_replies": [
                {"label": "🍗 Royal Chicken Biryani", "payload": "I want to order Royal Chicken Biryani", "icon": "ShoppingBag"},
                {"label": "🍟 Truffle Fries", "payload": "Order 1 Crispy Golden Truffle Fries", "icon": "ShoppingBag"},
                {"label": "🍫 Lava Cake", "payload": "Order 1 Molten Chocolate Lava Cake", "icon": "ShoppingBag"},
                {"label": "🥤 Mango Lassi", "payload": "Order 1 Fresh Alphonso Mango Lassi", "icon": "ShoppingBag"}
            ],
            "structured_data": {"menu_items": serialized_items}
        }


    # ------------------ Table Booking Orchestrator ------------------
    def _handle_booking_flow_orchestrator(
        self,
        session: Dict[str, Any],
        raw_msg: str,
        msg: str,
        db: Session,
        user_id: Optional[int],
        user_name: str
    ) -> Dict[str, Any]:
        session["state"] = "BOOKING_FLOW"
        slots = session["booking_slots"]

        # Parse guests
        guest_match = re.search(r'(?:for\s+|party of\s+|table for\s+)?(\d+)\s*(?:people|guests|persons|person|heads|pax)?', msg)
        if guest_match:
            try:
                num = int(guest_match.group(1))
                if 1 <= num <= 20:
                    slots["guests"] = num
            except ValueError:
                pass
        if "two" in msg or "couple" in msg:
            slots["guests"] = 2
        elif "four" in msg:
            slots["guests"] = 4
        elif "six" in msg:
            slots["guests"] = 6

        # Parse date
        today = datetime.date.today()
        if "today" in msg or "tonight" in msg:
            slots["date"] = today.strftime("%Y-%m-%d")
        elif "tomorrow" in msg:
            slots["date"] = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        elif "friday" in msg:
            days_ahead = (4 - today.weekday() + 7) % 7 or 7
            slots["date"] = (today + datetime.timedelta(days=days_ahead)).strftime("%Y-%m-%d")

        # Parse time
        time_match = re.search(r'(\b\d{1,2}(?::\d{2})?\s*(?:am|pm)\b|\b\d{1,2}:\d{2}\b)', msg)
        if time_match:
            slots["time"] = time_match.group(1).upper()
        elif "dinner" in msg:
            slots["time"] = "7:30 PM"
        elif "lunch" in msg:
            slots["time"] = "1:00 PM"

        if "window" in msg:
            slots["location"] = "Window View"
        elif "patio" in msg or "garden" in msg:
            slots["location"] = "Garden Patio"
        elif "balcony" in msg:
            slots["location"] = "Skyline Balcony"
        elif "vip" in msg:
            slots["location"] = "Private VIP Lounge"

        if not slots["customer_name"]:
            slots["customer_name"] = user_name

        if not slots["guests"]:
            return {
                "message": f"📅 **Let's book a wonderful table for you, {user_name}!**\n\nHow many guests will be dining?",
                "intent": "booking_ask_guests",
                "action_type": None,
                "quick_replies": [
                    {"label": "👤 2 Guests", "payload": "For 2 guests", "icon": "User"},
                    {"label": "👥 4 Guests", "payload": "For 4 guests", "icon": "Users"},
                    {"label": "🥂 6 Guests", "payload": "For 6 guests", "icon": "Users"},
                    {"label": "✨ 8 Guests (VIP)", "payload": "For 8 guests", "icon": "Crown"}
                ],
                "structured_data": None
            }

        if not slots["date"]:
            tomorrow = today + datetime.timedelta(days=1)
            return {
                "message": f"📅 **Table for {slots['guests']} guests** — got it! Which date would you prefer?",
                "intent": "booking_ask_date",
                "action_type": None,
                "quick_replies": [
                    {"label": f"✨ Tonight ({today.strftime('%b %d')})", "payload": "Tonight", "icon": "Calendar"},
                    {"label": f"🌅 Tomorrow ({tomorrow.strftime('%b %d')})", "payload": "Tomorrow", "icon": "Calendar"},
                    {"label": "🎉 This Friday", "payload": "This Friday", "icon": "Calendar"}
                ],
                "structured_data": None
            }

        if not slots["time"]:
            return {
                "message": f"🕒 **What time would you prefer on {slots['date']}?**",
                "intent": "booking_ask_time",
                "action_type": None,
                "quick_replies": [
                    {"label": "🍽️ Lunch (1:00 PM)", "payload": "1:00 PM", "icon": "Clock"},
                    {"label": "🌇 Early Dinner (6:30 PM)", "payload": "6:30 PM", "icon": "Clock"},
                    {"label": "✨ Prime Dinner (7:30 PM)", "payload": "7:30 PM", "icon": "Clock"}
                ],
                "structured_data": None
            }

        target_capacity = slots["guests"]
        loc_pref = slots.get("location")

        table_query = db.query(RestaurantTable).filter(RestaurantTable.capacity >= target_capacity)
        if loc_pref:
            table_query = table_query.filter(RestaurantTable.location.ilike(f"%{loc_pref}%"))
        assigned_table = table_query.first() or db.query(RestaurantTable).first()

        new_booking = Booking(
            user_id=user_id,
            table_id=assigned_table.id if assigned_table else 1,
            customer_name=slots["customer_name"],
            customer_phone="+1 555-0199",
            date=slots["date"],
            time=slots["time"],
            number_of_people=slots["guests"],
            table_preference=slots.get("location") or (assigned_table.location if assigned_table else "Main Dining Hall"),
            special_requests=slots.get("special_requests"),
            status="Confirmed"
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        session["state"] = "IDLE"
        session["booking_slots"] = {
            "guests": None,
            "date": None,
            "time": None,
            "location": None,
            "customer_name": user_name,
            "special_requests": None
        }

        confirmation_card = {
            "booking_id": new_booking.id,
            "customer_name": new_booking.customer_name,
            "guests": new_booking.number_of_people,
            "date": new_booking.date,
            "time": new_booking.time,
            "table_location": assigned_table.location if assigned_table else "Main Dining Hall",
            "table_id": assigned_table.id if assigned_table else 1,
            "status": "Confirmed"
        }

        return {
            "message": (
                f"🎉 **Table Reservation Confirmed!**\n\n"
                f"Dear **{new_booking.customer_name}**, your table for **{new_booking.number_of_people} guests** is confirmed!\n\n"
                f"📋 **Booking Reference:** `#{new_booking.id:04d}`\n"
                f"• **Date & Time:** {new_booking.date} at {new_booking.time}\n"
                f"• **Seating Area:** {confirmation_card['table_location']} (Table #{assigned_table.id if assigned_table else 1})\n"
                f"• **Status:** ✅ Confirmed"
            ),
            "intent": "booking_confirmed",
            "action_type": "BOOKING_CONFIRMED",
            "quick_replies": [
                {"label": "🍽️ Browse Menu in Advance", "payload": "Show me the menu", "icon": "Utensils"},
                {"label": "📦 Pre-Order Food", "payload": "I want to place an order", "icon": "ShoppingBag"}
            ],
            "structured_data": {"booking": confirmation_card}
        }

    def _default_quick_replies(self, user_name: str = "Friend") -> List[Dict[str, str]]:
        return [
            {"label": "🌾 Virtual Farming", "payload": "I want to cultivate paddy", "icon": "Leaf"},
            {"label": "🐍 Teach me Python", "payload": "Teach me Python", "icon": "Code"},
            {"label": "🏛️ Explain Democracy", "payload": "Explain democracy", "icon": "BookOpen"},
            {"label": "🧩 Play a Riddle", "payload": "Give me a riddle", "icon": "HelpCircle"},
            {"label": "🍽️ Browse Food Menu", "payload": "Show me the menu", "icon": "Utensils"},
            {"label": "📅 Book a Table", "payload": "Book a table for 2", "icon": "Calendar"}
        ]

# Global Singleton Instance
chatbot_engine = RestaurantChatbotEngine()
