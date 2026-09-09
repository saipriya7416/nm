from typing import Dict, Any, Optional
from sqlalchemy.orm import Session


class IntentRouter:
    """
    Step 3 & Step 4: Intent Router — Plugin-style dispatch from detected intent → engine handler.

    HOW TO ADD A NEW INTENT MODULE
    ───────────────────────────────
    1. Implement a handler on RestaurantChatbotEngine:
           def _handle_<intent_name>(self, msg, raw_msg, session[, db][, user_id]):
               ...
    2. Register it in INTENT_DISPATCH below:
           "MY_NEW_INTENT": ("_handle_my_new_intent", needs_db, needs_user_id),

    That's it. The router handles the rest.

    DISPATCH TABLE COLUMNS
    ──────────────────────
    intent_key          → the string returned by SemanticIntentDetector
    method_name         → name of the method on engine to call
    needs_db            → True if handler needs a DB session
    needs_user_id       → True if handler needs the user_id
    """

    # ═════════════════════════════════════════════════════════════
    # INTENT DISPATCH TABLE (plugin registry)
    # ═════════════════════════════════════════════════════════════
    INTENT_DISPATCH: Dict[str, tuple] = {

        # ─── Restaurant Core ─────────────────────────────────────
        "RESTAURANT_FOOD":               ("_handle_intent_food",              True,  True),
        "TABLE_BOOKING":                 ("_handle_intent_booking",            True,  True),
        "PAYMENT":                       ("_handle_intent_payment",            True,  True),

        # ─── Step 4: Knowledge & Information Engine ──────────────
        "GENERAL_KNOWLEDGE":             ("_handle_general_knowledge",         True,  False),
        "CURRENT_INFO":                  ("_handle_current_info",              False, False),
        "KNOWLEDGE_COMPARISON":          ("_handle_knowledge_comparison",      False, False),
        "KNOWLEDGE_HOW_TO":              ("_handle_knowledge_how_to",          False, False),
        "KNOWLEDGE_SIMPLIFY":            ("_handle_knowledge_simplify",        False, False),
        "KNOWLEDGE_DEEPEN":              ("_handle_knowledge_deepen",          False, False),
        "KNOWLEDGE_QUIZ":                ("_handle_knowledge_quiz",            False, False),
        "KNOWLEDGE_FOLLOWUP":            ("_handle_knowledge_followup",        False, False),

        # ─── Entertainment ────────────────────────────────────────
        "ENTERTAINMENT":                 ("_handle_entertainment",             False, False),
        "GAME_VICTORY":                  ("_handle_game_victory",              False, False),
        "GAME_VICTORY_FOOD":             ("_handle_game_victory_food",         True,  True),

        # ─── Learning ─────────────────────────────────────────────
        "LEARNING":                      ("_handle_learning",                  False, False),
        "LEARNING_CONTINUE":             ("_handle_learning_continue",         False, False),

        # ─── Simulations ──────────────────────────────────────────
        "SIMULATION_FARMING":            ("_handle_simulation_farming",        False, False),
        "SIMULATION_FARMING_STEP":       ("_handle_simulation_farming_step",   False, False),
        "SIMULATION_BUSINESS":           ("_handle_simulation_business",       False, False),
        "SIMULATION_BUSINESS_STEP":      ("_handle_simulation_business_step",  False, False),
        "SIMULATION_TRAVEL":             ("_handle_simulation_travel",         False, False),
        "SIMULATION_TRAVEL_STEP":        ("_handle_simulation_travel_step",    False, False),
        "SIMULATION_COOKING":            ("_handle_simulation_cooking",        True,  False),

        # ─── Conversation & Utility ───────────────────────────────
        "GENERAL_CONVERSATION":          ("_handle_general_conversation",      True,  False),
        "CLARIFICATION_NEEDED":          ("_handle_clarification",             False, False),
    }

    # ═════════════════════════════════════════════════════════════
    # MAIN ROUTE METHOD
    # ═════════════════════════════════════════════════════════════

    def route(
        self,
        intent_result: Dict[str, Any],
        msg: str,
        raw_msg: str,
        session: Dict[str, Any],
        db: Session,
        engine,
        user_id: Optional[int] = None,
        user_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Route the detected intent to the appropriate engine handler.

        Handles:
        - Multi-intent sequencing (stores secondary in session["pending_secondary_intent"])
        - Confidence-based clarification fallback
        - Graceful error handling per handler
        """
        primary    = intent_result["primary_intent"]
        secondary  = intent_result.get("secondary_intent")
        confidence = intent_result.get("confidence", 0.5)
        entities   = intent_result.get("entities", {})
        is_multi   = intent_result.get("is_multi_intent", False)

        # ─── Update session context (invisible to user) ───────────
        session["last_intent"] = primary
        session["intent_entities"] = entities

        # ─── Very low confidence → ask for clarification ──────────
        if confidence < 0.30:
            return engine._handle_clarification(msg, raw_msg, session)

        # ─── Queue secondary intent (multi-intent sequencing) ─────
        if is_multi and secondary and primary not in ("GAME_VICTORY_FOOD",):
            session["pending_secondary_intent"] = secondary

        # ─── Dispatch to handler ──────────────────────────────────
        return self._dispatch(primary, msg, raw_msg, session, db, engine, user_id, entities)

    # ═════════════════════════════════════════════════════════════
    # INTERNAL DISPATCH
    # ═════════════════════════════════════════════════════════════

    def _dispatch(
        self,
        intent: str,
        msg: str,
        raw_msg: str,
        session: Dict[str, Any],
        db: Session,
        engine,
        user_id: Optional[int],
        entities: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Lookup the registered handler and call it with the right args."""

        entry = self.INTENT_DISPATCH.get(intent)

        if not entry:
            user_name = session.get("user_name", "Friend")
            return engine._handle_general_fallback(msg, raw_msg, user_name, session, db)

        method_name, needs_db, needs_user_id = entry
        handler = getattr(engine, method_name, None)

        if not handler:
            user_name = session.get("user_name", "Friend")
            return engine._handle_general_fallback(msg, raw_msg, user_name, session, db)

        try:
            if needs_db and needs_user_id:
                return handler(msg, raw_msg, session, db, user_id)
            elif needs_db:
                return handler(msg, raw_msg, session, db)
            else:
                return handler(msg, raw_msg, session)

        except Exception as exc:
            user_name = session.get("user_name", "Friend")
            return {
                "message": (
                    f"Oops, I ran into a small snag 😅 Let me try again, {user_name}. "
                    "What would you like to do?"
                ),
                "intent": "handler_error",
                "action_type": None,
                "quick_replies": engine._default_quick_replies(user_name),
                "structured_data": None,
            }


# ── Singleton ──────────────────────────────────────────────────────
intent_router = IntentRouter()
