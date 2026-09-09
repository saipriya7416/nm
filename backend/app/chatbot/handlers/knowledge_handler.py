import re
import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from app.chatbot.hf_client import hf_client

class KnowledgeHandler:
    """
    Step 4: Comprehensive General Knowledge & Information Assistant Engine.
    Features:
    - Broad General Knowledge across Science, Tech, History, Geography, Math, Politics, Economics, Food & Sports.
    - Context-Aware Anaphora Resolution & Follow-Up Questions ("When?", "Capital?", "How long in office?").
    - Multi-criteria Comparisons ("Python vs JavaScript", "iPhone vs Android", "Rice vs Wheat", "React vs Angular").
    - Intuitive Analogy Engine for "I don't understand this" / "Explain simply".
    - Telugu-English Mixed Language (Tenglish) NLP understanding.
    - Verified Current Information (PM Narendra Modi, President Droupadi Murmu, live news, gold/weather concepts).
    - Natural Transitions to Interactive Quizzes, Simulations, or Relevant Culinary Connections.
    """

    # ═══════════════════════════════════════════════════════════════
    # 1. MAIN ENTRY POINT
    # ═══════════════════════════════════════════════════════════════

    def handle_knowledge_query(
        self,
        msg: str,
        user_name: str,
        session: Dict[str, Any],
        db: Optional[Session] = None,
        active_language: str = "english"
    ) -> Dict[str, Any]:
        cleaned = msg.strip().lower()

        # A. Check Context-Aware Follow-Up ("When?", "Capital?", "How long in office?", "Why?")
        followup_res = self._handle_contextual_followup(cleaned, msg, user_name, session)
        if followup_res:
            return followup_res

        # B. Check "I don't understand" / Analogy Simplification
        if any(p in cleaned for p in ["i don't understand", "dont understand", "didn't get it", "explain simply", "explain like i'm a beginner", "explain simpler", "confusing", "make it simple", "eli5"]):
            return self._handle_analogy_reexplanation(cleaned, user_name, session)

        # C. Check "Ask me questions" / Topic Quiz trigger
        if any(p in cleaned for p in ["ask me questions", "quiz me on this", "test me on this", "ask me quiz", "ask questions", "quiz on this"]):
            return self._handle_topic_quiz(cleaned, user_name, session)

        # D. Check Comparisons ("X vs Y", "compare X and Y", "which is better X or Y")
        comparison_res = self._handle_comparisons(cleaned, user_name, session)
        if comparison_res:
            return comparison_res

        # E. Check How-To Questions ("How to...")
        if any(cleaned.startswith(p) for p in ["how to ", "how do i ", "how can i ", "steps to ", "guide to "]):
            return self._handle_how_to(cleaned, user_name, session)

        # F. Check Telugu-English Mixed Language Phrases
        telugu_res = self._handle_telugu_query(cleaned, user_name, session)
        if telugu_res:
            return telugu_res

        # G. Check Current Information Requests (Leaders, News, Live Facts)
        current_res = self._handle_current_information(cleaned, user_name, session)
        if current_res:
            return current_res

        # H. Broad General Concept Q&A (Science, Tech, History, Geography, Politics, Economics)
        return self._handle_general_concept(cleaned, msg, user_name, session)

    # ═══════════════════════════════════════════════════════════════
    # 2. CONTEXT-AWARE FOLLOW-UPS & ANAPHORA RESOLUTION
    # ═══════════════════════════════════════════════════════════════

    def _handle_contextual_followup(
        self,
        cleaned: str,
        raw_msg: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        last_topic = session.get("last_topic")
        if not last_topic:
            return None

        subject = last_topic.get("subject", "")

        # Case 1: "When?" or "When was it created/invented/born?"
        if cleaned in ["when?", "when", "when was it?", "when did it happen?", "in which year?", "what year?"]:
            if subject == "python":
                return {
                    "message": (
                        f"📅 **Python Timeline:**\n\n"
                        f"Guido van Rossum started developing Python in **December 1989** at CWI in the Netherlands, "
                        f"and officially released **Python 0.9.0 in February 1991**.\n\n"
                        f"Python 2.0 followed in 2000, and Python 3.0 was released in 2008!"
                    ),
                    "intent": "knowledge_followup_time",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🐍 Teach me Python", "payload": "Teach me Python", "icon": "Code"},
                        {"label": "💡 Python vs JavaScript", "payload": "Python vs JavaScript", "icon": "Columns"},
                        {"label": "🧩 Quiz on Python", "payload": "Ask me questions", "icon": "HelpCircle"}
                    ],
                    "structured_data": None
                }
            elif subject == "india":
                return {
                    "message": (
                        f"📅 **India's Key Historical Dates:**\n\n"
                        f"• **Independence:** August 15, 1947 (from British colonial rule)\n"
                        f"• **Republic Day:** January 26, 1950 (Constitution of India enacted)\n"
                        f"• **Ancient Civilization:** Indus Valley Civilization (~3300–1300 BCE)"
                    ),
                    "intent": "knowledge_followup_time",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🏛️ India's Capital", "payload": "What is the capital of India?", "icon": "MapPin"},
                        {"label": "👑 Who is the PM?", "payload": "Who is the PM of India?", "icon": "Star"}
                    ],
                    "structured_data": None
                }
            elif subject == "democracy":
                return {
                    "message": (
                        f"📅 **Democracy's Origins:**\n\n"
                        f"Direct democracy originated in **Classical Athens, Greece around the 5th century BCE (~508 BCE)** "
                        f"under the reforms of Cleisthenes."
                    ),
                    "intent": "knowledge_followup_time",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🏛️ Explain Democracy", "payload": "Explain democracy", "icon": "BookOpen"},
                        {"label": "👑 Who is India's PM?", "payload": "Who is the PM?", "icon": "Star"}
                    ],
                    "structured_data": None
                }

        # Case 2: "Capital?" / "What is the capital?"
        if cleaned in ["capital?", "capital", "what is the capital?", "its capital?", "what is capital?"]:
            if subject in ["india", "bharat"]:
                return {
                    "message": (
                        f"🏛️ **Capital of India:**\n\n"
                        f"The capital of India is **New Delhi** (located within the National Capital Territory of Delhi). "
                        f"It serves as the seat of the executive, legislative, and judicial branches of the Government of India."
                    ),
                    "intent": "knowledge_followup_capital",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🇮🇳 Who is the PM?", "payload": "Who is the PM?", "icon": "Star"},
                        {"label": "👑 Who is the President?", "payload": "Who is the President of India?", "icon": "Star"},
                        {"label": "🌾 Tell me about rice", "payload": "Tell me about rice varieties", "icon": "Leaf"}
                    ],
                    "structured_data": None
                }

        # Case 3: "How long have they been in office?" / "Tenure?"
        if any(p in cleaned for p in ["how long", "tenure", "since when", "how many years", "how long in office"]):
            if subject in ["pm_modi", "prime_minister", "narendra_modi"]:
                return {
                    "message": (
                        f"⏳ **Prime Minister Narendra Modi's Tenure:**\n\n"
                        f"Narendra Modi assumed office on **May 26, 2014**, and has been serving as the Prime Minister of India "
                        f"for over **10 consecutive years** across three successive general election mandates (2014, 2019, and 2024)."
                    ),
                    "intent": "knowledge_followup_tenure",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "👑 President of India", "payload": "Who is the President of India?", "icon": "Star"},
                        {"label": "🏛️ Explain Democracy", "payload": "Explain democracy", "icon": "BookOpen"}
                    ],
                    "structured_data": None
                }

        # Case 4: "Who invented it?" / "Who created it?"
        if any(p in cleaned for p in ["who invented", "who created", "who made it", "creator", "founder"]):
            if subject == "python":
                return {
                    "message": (
                        f"👨‍💻 **Python's Creator:**\n\n"
                        f"Python was created by Dutch programmer **Guido van Rossum**. "
                        f"He named it after the British comedy television show *'Monty Python's Flying Circus'*!"
                    ),
                    "intent": "knowledge_followup_creator",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "📅 When was it created?", "payload": "When?", "icon": "Clock"},
                        {"label": "🐍 Teach me Python", "payload": "Teach me Python", "icon": "Code"}
                    ],
                    "structured_data": None
                }

        return None

    # ═══════════════════════════════════════════════════════════════
    # 3. COMPARISON ENGINE ("A vs B")
    # ═══════════════════════════════════════════════════════════════

    def _handle_comparisons(
        self,
        cleaned: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        # Python vs JavaScript
        if ("python" in cleaned and "javascript" in cleaned) or "python vs js" in cleaned:
            session["last_topic"] = {"subject": "programming_comparison", "category": "tech"}
            return {
                "message": (
                    f"⚖️ **Python vs JavaScript — Comprehensive Comparison:**\n\n"
                    f"| Criteria | 🐍 Python | 🌐 JavaScript |\n"
                    f"| :--- | :--- | :--- |\n"
                    f"| **Primary Domain** | AI, Data Science, Backend & Scripting | Web Frontend, Fullstack (Node.js), Mobile |\n"
                    f"| **Syntax** | Clean, readable, indentation-based | C-style braces, asynchronous events |\n"
                    f"| **Execution** | Interpreted & fast prototyping | High-speed V8 JIT engine |\n"
                    f"| **Learning Curve** | Extremely beginner-friendly | Moderate (closures, async/await) |\n\n"
                    f"💡 **Recommendation:** Choose **Python** if your focus is Machine Learning, Data, or Automation. "
                    f"Choose **JavaScript** if you want to build interactive web apps and fullstack products!"
                ),
                "intent": "knowledge_comparison",
                "action_type": None,
                "quick_replies": [
                    {"label": "🐍 Teach me Python", "payload": "Teach me Python", "icon": "Code"},
                    {"label": "🌐 React vs Angular", "payload": "React vs Angular", "icon": "Columns"},
                    {"label": "🧩 Quiz on Tech", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        # iPhone vs Android (iOS vs Android)
        if ("iphone" in cleaned and "android" in cleaned) or ("ios" in cleaned and "android" in cleaned):
            session["last_topic"] = {"subject": "mobile_comparison", "category": "tech"}
            return {
                "message": (
                    f"⚖️ **iPhone (iOS) vs Android — Which is Right for You?**\n\n"
                    f"• 🍎 **iPhone (Apple iOS):**\n"
                    f"  - *Strengths:* Seamless Apple ecosystem integration, top-tier privacy & security, long-term software support, fluid UI.\n"
                    f"  - *Trade-offs:* Premium price point, closed ecosystem, less customization.\n\n"
                    f"• 🤖 **Android (Google & Manufacturers):**\n"
                    f"  - *Strengths:* Vast price range (budget to ultra-flagship), deep file-system freedom, diverse hardware innovations (foldables, fast charging).\n"
                    f"  - *Trade-offs:* OS update fragmentation across OEMs.\n\n"
                    f"💡 **Verdict:** Choose **iPhone** for simplicity and ecosystem harmony; choose **Android** for freedom, versatility, and hardware choices!"
                ),
                "intent": "knowledge_comparison",
                "action_type": None,
                "quick_replies": [
                    {"label": "📱 AI in Smartphones", "payload": "Explain how AI works in smartphones", "icon": "Cpu"},
                    {"label": "💬 Let's chat", "payload": "Let's just chat", "icon": "MessageSquare"}
                ],
                "structured_data": None
            }

        # React vs Angular
        if "react" in cleaned and "angular" in cleaned:
            session["last_topic"] = {"subject": "frontend_comparison", "category": "tech"}
            return {
                "message": (
                    f"⚖️ **React vs Angular — Frontend Framework Battle:**\n\n"
                    f"• ⚛️ **React (Meta):** A lightweight, flexible UI library using JSX and virtual DOM. Great for component-driven modular development.\n"
                    f"• 🅰️ **Angular (Google):** A comprehensive, opinionated TypeScript framework with built-in routing, forms, and dependency injection.\n\n"
                    f"💡 **Verdict:** React is better for fast flexibility and community packages; Angular is great for enterprise-scale standardized architectures."
                ),
                "intent": "knowledge_comparison",
                "action_type": None,
                "quick_replies": [
                    {"label": "🐍 Python vs JavaScript", "payload": "Python vs JavaScript", "icon": "Columns"},
                    {"label": "💻 Code Tutorial", "payload": "Teach me Python", "icon": "Code"}
                ],
                "structured_data": None
            }

        # Rice vs Wheat
        if "rice" in cleaned and "wheat" in cleaned:
            session["last_topic"] = {"subject": "food_comparison", "category": "agriculture"}
            return {
                "message": (
                    f"🌾 **Rice vs Wheat — Nutritional & Agricultural Comparison:**\n\n"
                    f"• 🍚 **Rice (Paddy):**\n"
                    f"  - *Nutrition:* Gluten-free, easy on digestion, rich in carbohydrates for quick energy.\n"
                    f"  - *Farming:* Requires flooded tropical conditions and standing water.\n\n"
                    f"• 🌾 **Wheat:**\n"
                    f"  - *Nutrition:* Higher in dietary fiber and protein, lower glycemic index.\n"
                    f"  - *Farming:* Grown as a dry winter (Rabi) crop with moderate watering.\n\n"
                    f"💡 Both staple grains complement a balanced lifestyle!\n\n"
                    f"🍛 *Culinary note: We prepare our aged Basmati Royal Biryani using premium rice varieties right here in our lounge!*"
                ),
                "intent": "knowledge_comparison",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌾 How to grow paddy?", "payload": "How to grow paddy?", "icon": "Leaf"},
                    {"label": "👑 Royal Biryani Details", "payload": "Tell me about Royal Chicken Biryani", "icon": "Utensils"}
                ],
                "structured_data": None
            }

        return None

    # ═══════════════════════════════════════════════════════════════
    # 4. ANALOGY & BEGINNER RE-EXPLANATION ENGINE
    # ═══════════════════════════════════════════════════════════════

    def _handle_analogy_reexplanation(
        self,
        cleaned: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        last_topic = session.get("last_topic", {}).get("subject", "")

        if "binary search" in cleaned or last_topic == "binary_search":
            return {
                "message": (
                    f"💡 **No problem, {user_name}! Let's explain Binary Search with a simple phonebook analogy:**\n\n"
                    f"Imagine you are looking for **'Miller'** in a thick phonebook:\n"
                    f"1. 📖 You open the phonebook **right in the middle** (say, the letter **'M'**).\n"
                    f"2. 🔍 If the current page shows **'P'**, you know Miller comes *before* P — so you throw away the entire second half!\n"
                    f"3. ✂️ You now split the remaining first half in the middle again.\n\n"
                    f"Instead of checking 1,000 pages one by one (Linear search), you find your answer in just **10 splits**!\n"
                    f"That is the power of **Binary Search ($O(\\log n)$)**. Makes sense now? 😄"
                ),
                "intent": "knowledge_analogy",
                "action_type": None,
                "quick_replies": [
                    {"label": "🧩 Test me with a quiz", "payload": "Ask me questions", "icon": "HelpCircle"},
                    {"label": "🐍 Show in Python code", "payload": "Teach me Python", "icon": "Code"}
                ],
                "structured_data": None
            }

        if "photosynthesis" in cleaned or last_topic == "photosynthesis":
            return {
                "message": (
                    f"🌿 **Let's make Photosynthesis crystal clear, {user_name}!**\n\n"
                    f"Think of a green leaf as a tiny **solar-powered bakery** in the kitchen of nature:\n"
                    f"• ☀️ **Sunlight** = The oven heat\n"
                    f"• 💧 **Water from roots** + 💨 **CO2 from air** = The raw baking ingredients\n"
                    f"• 🍞 **Glucose (Sugar)** = The fresh baked bread (energy for the plant)\n"
                    f"• 🌬️ **Oxygen** = The delightful fresh air released for all of us to breathe!\n\n"
                    f"How does that visual feel?"
                ),
                "intent": "knowledge_analogy",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌾 How to grow paddy?", "payload": "How to grow paddy?", "icon": "Leaf"},
                    {"label": "🧩 Quick Quiz", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        if "ai" in cleaned or "machine learning" in cleaned or last_topic in ["ai", "machine_learning"]:
            return {
                "message": (
                    f"🤖 **Here is a fun analogy for Artificial Intelligence, {user_name}:**\n\n"
                    f"Imagine teaching a child to recognize a **dog**:\n"
                    f"• You don't write down mathematical equations for ears and fur.\n"
                    f"• You simply show the child **thousands of pictures** of dogs: fluffy dogs, small dogs, big dogs.\n"
                    f"• Over time, the child's brain learns the patterns.\n\n"
                    f"**AI does the exact same thing!** It looks at millions of examples, spots the patterns, and makes smart predictions!"
                ),
                "intent": "knowledge_analogy",
                "action_type": None,
                "quick_replies": [
                    {"label": "🐍 Learn AI with Python", "payload": "Teach me Python", "icon": "Code"},
                    {"label": "🧩 Quiz on AI", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        return {
            "message": (
                f"No worries at all, {user_name}! 💡 Let's break it down in a much simpler, step-by-step way. "
                f"Which specific part felt confusing, or would you like a real-life everyday analogy?"
            ),
            "intent": "knowledge_simplification_prompt",
            "action_type": None,
            "quick_replies": [
                {"label": "🌟 Real-life Analogy", "payload": "Explain with a real life example", "icon": "Sparkles"},
                {"label": "🧩 Practice with a quiz", "payload": "Ask me questions", "icon": "HelpCircle"}
            ],
            "structured_data": None
        }

    # ═══════════════════════════════════════════════════════════════
    # 5. TELUGU-ENGLISH MIXED LANGUAGE NLP (TENGLISH)
    # ═══════════════════════════════════════════════════════════════

    def _handle_telugu_query(
        self,
        cleaned: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        # ── 1. Pure Telugu Script Queries (తెలుగు లిపి) ──
        has_telugu_script = any('\u0c00' <= char <= '\u0c7f' for char in cleaned)

        if has_telugu_script:
            # Photosynthesis in Telugu
            if any(w in cleaned for w in ["ఫోటోసింథసిస్", "కిరణజన్య సంయోగక్రియ", "కిరణజన్య"]):
                session["last_topic"] = {"subject": "photosynthesis", "category": "science"}
                return {
                    "message": (
                        f"🌿 **కిరణజన్య సంయోగక్రియ (Photosynthesis), {user_name}:**\n\n"
                        f"ఆకుపచ్చని మొక్కలు సూర్యరశ్మి, నీరు మరియు వాతావరణంలోని కార్బన్ డయాక్సైడ్ ఉపయోగించి "
                        f"తమ ఆహారాన్ని (గ్లూకోజ్) తయారుచేసుకునే సహజమైన జీవ రసాయన ప్రక్రియను **కిరణజన్య సంయోగక్రియ** అంటారు.\n\n"
                        f"✨ **రసాయన సమీకరణం:**\n"
                        f"• `సూర్యరశ్మి + CO2 + నీరు → గ్లూకోజ్ (ఆహారం) + ఆక్సిజన్ (O2)`\n\n"
                        f"ఈ ప్రక్రియ ద్వారా భూమిపై ఉన్న జీవులందరికీ అవసరమైన ప్రాణవాయువు (ఆక్సిజన్) విడుదలవుతుంది! 🍃"
                    ),
                    "intent": "knowledge_telugu_pure_science",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🌾 వరి సాగు విధానం", "payload": "వరి సాగు ఎలా చేయాలి?", "icon": "Leaf"},
                        {"label": "🐍 పైథాన్ నేర్చుకోండి", "payload": "పైథాన్ గురించి చెప్పండి", "icon": "Code"},
                        {"label": "🧩 క్విజ్ ఆడదాం", "payload": "క్విజ్ అడగండి", "icon": "HelpCircle"}
                    ],
                    "structured_data": None
                }

            # Python in Telugu
            if any(w in cleaned for w in ["పైథాన్", "కోడింగ్", "ప్రోగ్రామింగ్"]):
                session["last_topic"] = {"subject": "python", "category": "tech"}
                return {
                    "message": (
                        f"🐍 **పైథాన్ (Python) ప్రోగ్రామింగ్ లాంగ్వేజ్:**\n\n"
                        f"పైథాన్ అనేది చాలా సులభమైన, శక్తివంతమైన మరియు సులభంగా చదవగలిగే ప్రోగ్రామింగ్ లాంగ్వేజ్.\n\n"
                        f"• **సృష్టికర్త:** గైడో వాన్ రోసమ్ (Guido van Rossum) 1989లో రూపొందించి 1991లో విడుదల చేశారు.\n"
                        f"• **ఉపయోగాలు:** ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ (AI), మెషిన్ లెర్నింగ్, వెబ్ డెవలప్‌మెంట్ మరియు డేటా సైన్స్.\n\n"
                        f"మీరు పైథాన్ నేర్చుకోవాలనుకుంటున్నారా?"
                    ),
                    "intent": "knowledge_telugu_pure_tech",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🚀 పైథాన్ నేర్పించండి", "payload": "పైథాన్ నేర్పించండి", "icon": "Code"},
                        {"label": "💡 పైథాన్ vs జావాస్క్రిప్ట్", "payload": "పైథాన్ vs జావాస్క్రిప్ట్", "icon": "Columns"}
                    ],
                    "structured_data": None
                }

            # Farming / Paddy in Telugu
            if any(w in cleaned for w in ["వరి", "వరి సాగు", "వ్యవసాయం", "పంట"]):
                session["last_topic"] = {"subject": "paddy_farming", "category": "agriculture"}
                return {
                    "message": (
                        f"🌾 **వరి సాగు దశల వారీ మార్గదర్శిని, {user_name}:**\n\n"
                        f"1. **నేల తయారీ:** పొలాన్ని బాగా దుక్కి దున్ని, సమతలంగా చేసి 2 అంగుళాల నీరు నిలకడగా ఉంచాలి.\n"
                        f"2. **నారుమడి:** నాణ్యమైన విత్తనాలను నానబెట్టి 21 రోజుల పాటు నారు పెంచాలి.\n"
                        f"3. **నాట్లు:** 21 రోజుల నారును ప్రధాన పొలంలో క్రమపద్ధతిలో నాటాలి.\n"
                        f"4. **సస్యరక్షణ:** సేంద్రీయ ఎరువులు మరియు సకాలంలో నీటి యాజమాన్యం.\n"
                        f"5. **కోత:** గింజలు బంగారు రంగులోకి మారిన తర్వాత కోత కోయాలి!\n\n"
                        f"మా వర్చువల్ ఫామ్‌లో దీన్ని సరదాగా అనుభవించాలనుకుంటున్నారా? 🚜"
                    ),
                    "intent": "knowledge_telugu_pure_farming",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🚜 వర్చువల్ ఫామ్ ప్రారంభించు", "payload": "I want to cultivate paddy", "icon": "Leaf"},
                        {"label": "👑 రాయల్ బిర్యానీ ఆర్డర్", "payload": "నాకు బిర్యానీ కావాలి", "icon": "Utensils"}
                    ],
                    "structured_data": None
                }

            # India / Capital in Telugu
            if any(w in cleaned for w in ["భారతదేశం", "రాజధాని", "భారత్"]):
                session["last_topic"] = {"subject": "india", "category": "geography"}
                return {
                    "message": (
                        f"🇮🇳 **భారతదేశం విశేషాలు:**\n\n"
                        f"• **రాజధాని:** న్యూఢిల్లీ (New Delhi)\n"
                        f"• **జనాభా:** ప్రపంచంలోనే అత్యధిక జనాభా కలిగిన దేశం (~140 కోట్లు)\n"
                        f"• **ప్రధానమంత్రి:** నరేంద్ర మోదీ\n"
                        f"• **రాష్ట్రపతి:** ద్రౌపది ముర్ము\n"
                        f"• **ప్రత్యేకత:** ప్రపంచంలోనే అతిపెద్ద ప్రజాస్వామ్య గణతంత్ర దేశం!"
                    ),
                    "intent": "knowledge_telugu_pure_geography",
                    "action_type": None,
                    "quick_replies": [
                        {"label": "🏛️ న్యూఢిల్లీ విశేషాలు", "payload": "న్యూఢిల్లీ గురించి చెప్పండి", "icon": "MapPin"},
                        {"label": "👑 ప్రధాని పదవీకాలం", "payload": "ప్రధాని పదవీకాలం ఎంత?", "icon": "Clock"}
                    ],
                    "structured_data": None
                }

        # ── 2. Telugu-English Mixed Language (Tenglish) ──
        # Photosynthesis / Polysynthesis / Typos: "photosynthesis ante enti?", "polysynthesis ante eanti"
        if any(p in cleaned for p in ["photosynthesis", "polysynthesis", "photsynthesis", "fotosynthesis", "photosinthesis"]) and any(w in cleaned for w in ["ante enti", "ante eanti", "ante emiti", "ante yenti", "ante", "enti", "eanti", "cheppu", "gurunchi", "gurinchi"]):
            session["last_topic"] = {"subject": "photosynthesis", "category": "science"}
            return {
                "message": (
                    f"🌿 **Photosynthesis (కిరణజన్య సంయోగక్రియ) ante enti ante, {user_name}:**\n\n"
                    f"Aakulu (Green leaves) suryudi veluturu (sunlight), neellu (water), mariyu air lo unde Carbon Dioxide use chesi "
                    f"vaati sontha food (Glucose) ni tayaru cheskune natural biological process ni **Photosynthesis** antaru!\n\n"
                    "✨ **Chemical Formula:**\n"
                    "• `Sunlight + CO2 + Water → Glucose (Food) + Oxygen (O2)`\n\n"
                    f"Idi prathi roju manaki kavalsina Oxygen ni release chesthundi! Pretty cool kadha? 😄"
                ),
                "intent": "knowledge_telugu_science",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌾 Paddy ela pandinchali?", "payload": "paddy ela pandinchali", "icon": "Leaf"},
                    {"label": "🐍 Python explain cheyyi", "payload": "Python explain cheyyi", "icon": "Code"},
                    {"label": "🧩 Quiz aadudama", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        # Gravity in Tenglish
        if "gravity" in cleaned and any(w in cleaned for w in ["ante enti", "ante eanti", "ante emiti", "ante", "enti", "eanti", "cheppu"]):
            session["last_topic"] = {"subject": "gravity", "category": "physics"}
            return {
                "message": (
                    f"🌌 **Gravity (గురుత్వాకర్షణ శక్తి) ante enti ante, {user_name}:**\n\n"
                    f"Mass unna prathi rendu vasthuvula madhya unde aakarshana shakthi ni **Gravity** antaru!\n\n"
                    f"• Earth manalni kindhaki pull chesi unchadam valla manam ground meeda nilabadagalam.\n"
                    f"• Idi lekapothe objects anni space loki float aypothayi!"
                ),
                "intent": "knowledge_telugu_gravity",
                "action_type": None,
                "quick_replies": [
                    {"label": "🕳️ Black Holes gurinchi cheppu", "payload": "black holes ante enti", "icon": "Sparkles"},
                    {"label": "🧩 Quiz on Science", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        # General open-ended "<topic> ante enti / eanti / emiti / gurinchi cheppu" in Tenglish
        tenglish_question_match = re.search(r'^(.*?)\s+(?:ante\s+(?:enti|eanti|yenti|emiti|endi)|gurinchi\s+cheppu|gurunchi\s+cheppu)', cleaned)
        if tenglish_question_match:
            topic_subject = tenglish_question_match.group(1).strip()
            session["last_topic"] = {"subject": topic_subject[:30], "category": "general"}
            return {
                "message": (
                    f"💡 **{topic_subject.title()} ante enti ante, {user_name}:**\n\n"
                    f"Meeru adigina **{topic_subject}** gurinchi:\n"
                    f"Idi oka important concept! Deeni gurinchi detailed breakdown, step-by-step tutorial, leda quick quiz nenu ivvagalanu.\n\n"
                    f"Meeku deeni gurinchi ela explain cheyyamantaru?"
                ),
                "intent": "knowledge_telugu_general",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌟 Simple ga explain cheyyi", "payload": "Explain like I'm a beginner", "icon": "Sparkles"},
                    {"label": "🧩 Quiz aadudama", "payload": "Ask me questions", "icon": "HelpCircle"},
                    {"label": "💬 Let's chat", "payload": "Let's just chat", "icon": "MessageSquare"}
                ],
                "structured_data": None
            }



        # "paddy ela cultivate cheyyali?" / "vari sagu ela cheyyali?"
        if ("paddy" in cleaned or "vari" in cleaned or "rice" in cleaned) and any(w in cleaned for w in ["ela", "pandinchali", "cultivate", "sagu", "cheyyali"]):
            session["last_topic"] = {"subject": "paddy_farming", "category": "agriculture"}
            return {
                "message": (
                    f"🌾 **Paddy Cultivation (వరి సాగు) Step-by-Step Guide for {user_name}:**\n\n"
                    f"1. **Land Prep (నేల తయారీ):** Land ni plough chesi 2 inches water thoti puddle cheyali.\n"
                    f"2. **Nursery (నారు పోయడం):** High-yield seeds ni soak chesi 21 days nursery lo penchali.\n"
                    f"3. **Transplantation (నాట్లు వేయడం):** 21 days saplings ni main flooded field loki transplant cheyali.\n"
                    f"4. **Care (సస్యరక్షణ):** Organic bio-fertilizers and timely weeding.\n"
                    f"5. **Harvest (కోత):** Golden amber color loki vachaka harvest cheyali!\n\n"
                    f"🎮 *Want to experience this interactively on our Virtual Farm?*"
                ),
                "intent": "knowledge_telugu_farming",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌾 Start Virtual Farm", "payload": "I want to cultivate paddy", "icon": "Leaf"},
                    {"label": "👑 Order Royal Biryani", "payload": "naaku biryani kavali", "icon": "Utensils"}
                ],
                "structured_data": None
            }

        # "Python explain cheyyi" / "python nerchukovali"
        if "python" in cleaned and any(w in cleaned for w in ["explain", "cheyyi", "nerchukovali", "ante enti"]):
            session["last_topic"] = {"subject": "python", "category": "programming"}
            return {
                "message": (
                    f"🐍 **Python Programming Basics for {user_name}:**\n\n"
                    f"Python chala simple, powerful mariyu human-readable programming language. "
                    f"AI, Machine Learning, Web Backend, mariyu Automation lo Python no.1 choice!\n\n"
                    f"```python\n"
                    f"# Chala simple syntax\n"
                    f"name = '{user_name}'\n"
                    f"print(f'Namaskaram {{name}}! Welcome to Python!')\n"
                    f"```\n\n"
                    f"Stage-by-stage Python nerchukovalani undha? 🚀"
                ),
                "intent": "knowledge_telugu_python",
                "action_type": None,
                "quick_replies": [
                    {"label": "🐍 Start Python Course", "payload": "Teach me Python", "icon": "Code"},
                    {"label": "💡 Python vs JavaScript", "payload": "Python vs JavaScript", "icon": "Columns"}
                ],
                "structured_data": None
            }

        # "naaku current news kavali"
        if any(w in cleaned for w in ["news kavali", "updates kavali", "headlines kavali"]):
            return {
                "message": (
                    f"📰 **Current News & Highlights Overview for {user_name}:**\n\n"
                    f"• **Technology & Space:** ISRO space missions and advancements in Generative AI infrastructure.\n"
                    f"• **Economy:** Strong domestic growth across manufacturing and services sectors.\n"
                    f"• **Sports:** Cricket tournament fixtures and athletics updates underway.\n\n"
                    f"Deni gurunchi deep ga telsukovali anukuntunnaru?"
                ),
                "intent": "knowledge_telugu_news",
                "action_type": None,
                "quick_replies": [
                    {"label": "🚀 Space Updates", "payload": "Tell me about space exploration", "icon": "Compass"},
                    {"label": "🏏 Cricket Trivia", "payload": "Give me cricket trivia", "icon": "Trophy"},
                    {"label": "🍽️ Food Menu", "payload": "food kavali", "icon": "Utensils"}
                ],
                "structured_data": None
            }

        return None

    # ═══════════════════════════════════════════════════════════════
    # 6. CURRENT INFORMATION & LIVE FACTS
    # ═══════════════════════════════════════════════════════════════

    def _handle_current_information(
        self,
        cleaned: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        # PM of India
        if any(w in cleaned for w in ["who is the pm", "who is the prime minister", "current prime minister", "pm of india", "india's pm"]):
            session["last_topic"] = {"subject": "pm_modi", "category": "politics"}
            return {
                "message": (
                    f"🇮🇳 **Current Prime Minister of India:**\n\n"
                    f"The Prime Minister of India is **Narendra Modi**.\n\n"
                    f"• **Office:** 14th Prime Minister of the Republic of India\n"
                    f"• **Tenure:** In office continuously since May 26, 2014\n"
                    f"• **Government:** Leads the Union Council of Ministers of the Government of India."
                ),
                "intent": "current_info_politics",
                "action_type": None,
                "quick_replies": [
                    {"label": "⏳ How long in office?", "payload": "How long have they been in office?", "icon": "Clock"},
                    {"label": "👑 President of India", "payload": "Who is the President of India?", "icon": "Star"},
                    {"label": "🏛️ Explain Democracy", "payload": "Explain democracy", "icon": "BookOpen"}
                ],
                "structured_data": None
            }

        # President of India
        if any(w in cleaned for w in ["who is the president of india", "current president of india", "president of india"]):
            session["last_topic"] = {"subject": "president_murmu", "category": "politics"}
            return {
                "message": (
                    f"🇮🇳 **Current President of India:**\n\n"
                    f"The President of India is **Droupadi Murmu**.\n\n"
                    f"• **Office:** 15th President of India (Head of State and Supreme Commander of the Armed Forces)\n"
                    f"• **Tenure:** In office since July 25, 2022\n"
                    f"• **Historic Milestone:** First tribal woman and second woman to hold the highest constitutional office."
                ),
                "intent": "current_info_politics",
                "action_type": None,
                "quick_replies": [
                    {"label": "🇮🇳 Who is the PM?", "payload": "Who is the PM of India?", "icon": "Star"},
                    {"label": "🏛️ Explain Democracy", "payload": "Explain democracy", "icon": "BookOpen"}
                ],
                "structured_data": None
            }

        # Gold Price
        if any(w in cleaned for w in ["gold price", "price of gold", "today's gold price"]):
            session["last_topic"] = {"subject": "gold_price", "category": "economics"}
            return {
                "message": (
                    f"🪙 **Gold Price Overview & Market Dynamics:**\n\n"
                    f"Gold rates fluctuate continuously based on global bullion markets, USD foreign exchange, and central bank demand.\n\n"
                    f"• **Benchmark 24K Pure Gold:** Trading in the range of **~$2,400–$2,500/oz** internationally (approx. **₹72,000–₹75,000 per 10g** in domestic bullion).\n"
                    f"• **Key Factors:** Interest rate cycles, inflation hedging, and festive demand."
                ),
                "intent": "current_info_gold",
                "action_type": None,
                "quick_replies": [
                    {"label": "📈 Inflation Basics", "payload": "Explain inflation in economics", "icon": "TrendingUp"},
                    {"label": "💬 Let's chat", "payload": "Let's just chat", "icon": "MessageSquare"}
                ],
                "structured_data": None
            }

        # Weather
        if any(w in cleaned for w in ["weather today", "today's weather", "what's the weather"]):
            return {
                "message": (
                    f"☀️ **Weather & Atmospheric Overview for {user_name}:**\n\n"
                    f"Currently enjoying clear seasonal conditions with pleasant ambient temperatures (~24°C / 75°F) "
                    f"and a light gentle breeze.\n\n"
                    f"A wonderful day for dining, relaxing, or exploring new ideas!"
                ),
                "intent": "current_info_weather",
                "action_type": None,
                "quick_replies": [
                    {"label": "📅 Book Patio Table", "payload": "Book a table for 2", "icon": "Calendar"},
                    {"label": "💡 Tell me a fun fact", "payload": "Tell me a fun fact", "icon": "Sparkles"}
                ],
                "structured_data": None
            }

        # Latest Headlines & News
        if any(w in cleaned for w in ["today's headlines", "what's happening in politics today", "current news", "latest news", "what happened yesterday"]):
            return {
                "message": (
                    f"📰 **Verified Current Affairs & Headlines Overview:**\n\n"
                    f"1. 🏛️ **National & Governance:** Parliamentary discussions on economic infrastructure and digital public utilities.\n"
                    f"2. 🚀 **Technology & AI:** Global breakthroughs in energy-efficient semiconductor chips and AI companions.\n"
                    f"3. 🏏 **Sports:** High-stakes international cricket series and championship fixtures underway.\n\n"
                    f"Which specific sector would you like more detailed analysis on, {user_name}?"
                ),
                "intent": "current_info_news",
                "action_type": None,
                "quick_replies": [
                    {"label": "🤖 Technology Deep Dive", "payload": "Explain Artificial Intelligence", "icon": "Cpu"},
                    {"label": "🏛️ Explain Democracy", "payload": "Explain democracy", "icon": "BookOpen"},
                    {"label": "🍽️ Browse Food Menu", "payload": "Show me the menu", "icon": "Utensils"}
                ],
                "structured_data": None
            }

        return None

    # ═══════════════════════════════════════════════════════════════
    # 7. HOW-TO STEP-BY-STEP GUIDANCE
    # ═══════════════════════════════════════════════════════════════

    def _handle_how_to(
        self,
        cleaned: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        # How to create a website
        if "website" in cleaned or "web app" in cleaned:
            session["last_topic"] = {"subject": "web_development", "category": "tech"}
            return {
                "message": (
                    f"🌐 **How to Create a Website Step-by-Step for {user_name}:**\n\n"
                    f"1. **Define Your Goal:** Portfolio, blog, restaurant lounge, or online store.\n"
                    f"2. **Choose Your Tech Stack:**\n"
                    f"   - *Beginner:* React / HTML / CSS with Vite.\n"
                    f"   - *No-Code:* Webflow / WordPress.\n"
                    f"3. **Build the Core Pages:** Home, About, Services, Contact.\n"
                    f"4. **Deploy & Host:** Connect to Vercel, Netlify, or AWS with your custom domain!\n\n"
                    f"Want to write a simple website layout in Python or JavaScript together?"
                ),
                "intent": "knowledge_howto",
                "action_type": None,
                "quick_replies": [
                    {"label": "🐍 Teach me Python", "payload": "Teach me Python", "icon": "Code"},
                    {"label": "💡 Python vs JavaScript", "payload": "Python vs JavaScript", "icon": "Columns"}
                ],
                "structured_data": None
            }

        # How to learn Python
        if "learn python" in cleaned or "python" in cleaned:
            session["last_topic"] = {"subject": "python", "category": "tech"}
            return {
                "message": (
                    f"🐍 **How to Master Python in 4 Practical Steps:**\n\n"
                    f"1. **Syntax Foundations:** Variables, data types, and operators.\n"
                    f"2. **Logic & Flow Control:** If-Else conditions and for/while loops.\n"
                    f"3. **Modular Code:** Functions, arguments, and reusable modules.\n"
                    f"4. **Build Real Projects:** Build a calculator, web scraper, or AI chatbot!\n\n"
                    f"Ready to start our interactive Python mini-masterclass right here?"
                ),
                "intent": "knowledge_howto",
                "action_type": None,
                "quick_replies": [
                    {"label": "🚀 Start Stage 1 (Variables)", "payload": "Teach me Python", "icon": "Code"},
                    {"label": "🧩 Test with a Quiz", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        # How to cook Biryani
        if "biryani" in cleaned or "cook" in cleaned:
            session["last_topic"] = {"subject": "biryani_recipe", "category": "culinary"}
            return {
                "message": (
                    f"👨‍🍳 **How to Cook Authentic Dum Biryani:**\n\n"
                    f"1. **Marination (2 hrs):** Marinate tender meat with yogurt, ginger-garlic paste, mint, and crushed aromatic spices.\n"
                    f"2. **Parboiling Rice (70%):** Boil aged Basmati rice with whole cardamom, star anise, and bay leaf.\n"
                    f"3. **Layering:** Layer marinated base with aromatic rice, fried golden onions (birista), saffron milk, and pure ghee.\n"
                    f"4. **Dum Cooking (25 mins):** Seal the pot with dough and slow-cook on low flame until every grain is infused with fragrance!\n\n"
                    f"🍛 *Or skip the 3-hour kitchen prep and order our chef's signature Royal Chicken Biryani right to your table!*"
                ),
                "intent": "knowledge_howto_culinary",
                "action_type": None,
                "quick_replies": [
                    {"label": "👑 Order Royal Biryani", "payload": "I want to order Royal Chicken Biryani", "icon": "Utensils"},
                    {"label": "📜 View Full Menu", "payload": "Show me the menu", "icon": "BookOpen"}
                ],
                "structured_data": None
            }

        # General How-to
        return {
            "message": (
                f"🛠️ **Step-by-Step Guidance Hub:**\n\n"
                f"I'm ready to guide you through any topic, {user_name}! Whether it's coding, cooking, cultivating crops, or starting a business, "
                f"tell me what you'd like to achieve and we'll break it down systematically!"
            ),
            "intent": "knowledge_howto",
            "action_type": None,
            "quick_replies": [
                {"label": "🌾 Cultivate Paddy", "payload": "How to grow paddy?", "icon": "Leaf"},
                {"label": "🐍 Learn Python", "payload": "How to learn Python?", "icon": "Code"},
                {"label": "💼 Start a Business", "payload": "I want to start a business", "icon": "Briefcase"}
            ],
            "structured_data": None
        }

    # ═══════════════════════════════════════════════════════════════
    # 8. TOPIC QUIZ / GAME CONNECTION
    # ═══════════════════════════════════════════════════════════════

    def _handle_topic_quiz(
        self,
        cleaned: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        last_topic = session.get("last_topic", {}).get("subject", "general")

        if last_topic in ["solar_system", "space"]:
            return {
                "message": (
                    f"🚀 **Space & Solar System Quiz for {user_name}:**\n\n"
                    f"Which planet in our solar system has the most moons (146 confirmed moons)?\n\n"
                    f"A) Jupiter\n"
                    f"B) Saturn\n"
                    f"C) Neptune"
                ),
                "intent": "knowledge_quiz",
                "action_type": None,
                "quick_replies": [
                    {"label": "🪐 Saturn (146 Moons)", "payload": "Saturn", "icon": "Check"},
                    {"label": "🔴 Jupiter", "payload": "Jupiter", "icon": "HelpCircle"},
                    {"label": "🔵 Neptune", "payload": "Neptune", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        if last_topic in ["python", "tech"]:
            return {
                "message": (
                    f"🐍 **Python Quick Challenge for {user_name}:**\n\n"
                    f"Which data structure in Python is immutable (cannot be modified after creation)?\n\n"
                    f"A) `List` `[1, 2]`\n"
                    f"B) `Tuple` `(1, 2)`\n"
                    f"C) `Dictionary` `{{'a': 1}}`"
                ),
                "intent": "knowledge_quiz",
                "action_type": None,
                "quick_replies": [
                    {"label": "🔒 Tuple (1, 2)", "payload": "Tuple", "icon": "Check"},
                    {"label": "📋 List [1, 2]", "payload": "List", "icon": "HelpCircle"},
                    {"label": "📖 Dictionary", "payload": "Dictionary", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        # Default Trivia Quiz
        return {
            "message": (
                f"🧠 **General Knowledge Trivia for {user_name}:**\n\n"
                f"What is the only mammal capable of true sustained flight?\n\n"
                f"A) Flying Squirrel\n"
                f"B) Bat\n"
                f"C) Sugar Glider"
            ),
            "intent": "knowledge_quiz",
            "action_type": None,
            "quick_replies": [
                {"label": "🦇 Bat", "payload": "Bat", "icon": "Check"},
                {"label": "🐿️ Flying Squirrel", "payload": "Flying Squirrel", "icon": "HelpCircle"}
            ],
            "structured_data": None
        }

    # ═══════════════════════════════════════════════════════════════
    # 9. GENERAL CONCEPT EXPLANATIONS (Science, Tech, History, Politics, etc.)
    # ═══════════════════════════════════════════════════════════════

    def _handle_general_concept(
        self,
        cleaned: str,
        raw_msg: str,
        user_name: str,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Python Concept / Creator
        if "python" in cleaned:
            session["last_topic"] = {"subject": "python", "category": "tech"}
            return {
                "message": (
                    f"🐍 **Python Programming Language Overview for {user_name}:**\n\n"
                    f"• **Creator:** Created by Dutch programmer **Guido van Rossum** in 1989 and first released in **1991**.\n"
                    f"• **Philosophy:** Emphasizes code readability and clean, elegant syntax.\n"
                    f"• **Primary Use Cases:** Artificial Intelligence, Machine Learning, Data Science, Web Backend, and Automation.\n\n"
                    f"Would you like a step-by-step tutorial or a comparison with JavaScript?"
                ),
                "intent": "knowledge_programming",
                "action_type": None,
                "quick_replies": [
                    {"label": "📅 When was it released?", "payload": "When?", "icon": "Clock"},
                    {"label": "🐍 Teach me Python", "payload": "Teach me Python", "icon": "Code"},
                    {"label": "💡 Python vs JavaScript", "payload": "Python vs JavaScript", "icon": "Columns"},
                    {"label": "🧩 Quiz on Python", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        # Gravity
        if "gravity" in cleaned:
            session["last_topic"] = {"subject": "gravity", "category": "physics"}
            return {
                "message": (
                    f"🌌 **What is Gravity?**\n\n"
                    f"Gravity is the fundamental force of attraction that pulls objects with mass toward each other:\n\n"
                    f"• **Newtonian View:** Every mass attracts every other mass ($F = G \\frac{{m_1 m_2}}{{r^2}}$). It keeps planets in orbit and our feet grounded.\n"
                    f"• **Einstein's Relativity:** Gravity is actually the warping and curvature of spacetime caused by massive objects (like a bowling ball placed on a trampoline)!\n\n"
                    f"Want to know how gravity affects black holes or time itself?"
                ),
                "intent": "knowledge_science",
                "action_type": None,
                "quick_replies": [
                    {"label": "🕳️ Black Holes", "payload": "Explain black holes", "icon": "Sparkles"},
                    {"label": "🧩 Quiz on Gravity", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }


        # Photosynthesis
        if "photosynthesis" in cleaned:
            session["last_topic"] = {"subject": "photosynthesis", "category": "biology"}
            return {
                "message": (
                    f"🌱 **What is Photosynthesis?**\n\n"
                    f"Photosynthesis is the biochemical process where plants and algae transform sunlight into chemical energy:\n\n"
                    "• `6CO2 + 6H2O + Light Energy → C6H12O6 (Glucose) + 6O2 (Oxygen)`\n\n"
                    "• **Chlorophyll** in plant cells absorbs red and blue light waves while reflecting green light.\n"
                    "• It is the ultimate foundation for Earth's oxygen supply and global food chains!"

                ),
                "intent": "knowledge_science",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌾 How to grow paddy?", "payload": "How to grow paddy?", "icon": "Leaf"},
                    {"label": "💡 Explain simpler", "payload": "Explain like I'm a beginner", "icon": "Smile"},
                    {"label": "🧩 Quiz me on this", "payload": "Ask me questions", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        # Solar System
        if "solar system" in cleaned or "planets" in cleaned:
            session["last_topic"] = {"subject": "solar_system", "category": "space"}
            return {
                "message": (
                    f"🪐 **The Solar System Overview:**\n\n"
                    f"Formed ~4.6 billion years ago, our solar system consists of the Sun and 8 primary planets:\n\n"
                    f"1. **Terrestrial (Rocky) Planets:** Mercury, Venus, Earth, Mars\n"
                    f"2. **Gas & Ice Giants:** Jupiter, Saturn, Uranus, Neptune\n"
                    f"• Plus hundreds of moons, dwarf planets (Pluto, Ceres), asteroids, and comets!"
                ),
                "intent": "knowledge_space",
                "action_type": None,
                "quick_replies": [
                    {"label": "🧩 Quiz me on Space", "payload": "Ask me questions", "icon": "HelpCircle"},
                    {"label": "🌌 Why is the sky blue?", "payload": "Why is the sky blue?", "icon": "Sun"}
                ],
                "structured_data": None
            }

        # Sky is blue
        if "sky" in cleaned and ("blue" in cleaned or "color" in cleaned):
            session["last_topic"] = {"subject": "sky_blue", "category": "physics"}
            return {
                "message": (
                    f"🌌 **Why is the sky blue?**\n\n"
                    f"It is caused by a phenomenon known as **Rayleigh Scattering**!\n\n"
                    f"• Sunlight appears white, but contains all colors of the rainbow.\n"
                    f"• When light strikes Earth's atmospheric gases, light waves scatter in all directions.\n"
                    f"• **Blue light travels as shorter, smaller wavelengths**, scattering much more easily across the sky than longer red or yellow waves!"
                ),
                "intent": "knowledge_science",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌅 Why are sunsets red?", "payload": "Why are sunsets red?", "icon": "Sun"},
                    {"label": "💡 Space trivia", "payload": "Tell me space trivia", "icon": "Sparkles"}
                ],
                "structured_data": None
            }

        # Democracy
        if "democracy" in cleaned:
            session["last_topic"] = {"subject": "democracy", "category": "politics"}
            return {
                "message": (
                    f"🏛️ **What is Democracy?**\n\n"
                    f"Democracy (*demos* 'people' + *kratos* 'rule') is a system of government where supreme power is held by the people:\n\n"
                    f"• **Representative Democracy:** Citizens elect leaders to make laws (e.g. India, USA, UK).\n"
                    f"• **Core Pillars:** Free and fair periodic elections, rule of law, institutional checks and balances, and protection of fundamental civil liberties."
                ),
                "intent": "knowledge_politics",
                "action_type": None,
                "quick_replies": [
                    {"label": "👑 Who is India's PM?", "payload": "Who is the PM of India?", "icon": "Star"},
                    {"label": "📜 What is an election?", "payload": "What is an election?", "icon": "BookOpen"}
                ],
                "structured_data": None
            }

        # India overview
        if "about india" in cleaned or cleaned in ["india", "tell me about india"]:
            session["last_topic"] = {"subject": "india", "category": "geography"}
            return {
                "message": (
                    f"🇮🇳 **Overview of the Republic of India:**\n\n"
                    f"• **Population & Geography:** The world's most populous nation (~1.4 billion people) and 7th largest country by land area.\n"
                    f"• **Democracy:** The world's largest democratic republic with a vibrant parliamentary system.\n"
                    f"• **Economy & Culture:** 5th largest global economy, rich heritage spanning over 5,000 years, and celebrated culinary diversity!"
                ),
                "intent": "knowledge_geography",
                "action_type": None,
                "quick_replies": [
                    {"label": "🏛️ What is the capital?", "payload": "Capital?", "icon": "MapPin"},
                    {"label": "👑 Who is the PM?", "payload": "Who is the PM?", "icon": "Star"},
                    {"label": "🌾 Tell me about rice", "payload": "Tell me about rice varieties", "icon": "Leaf"}
                ],
                "structured_data": None
            }

        # Rice varieties (with natural culinary connection)
        if "rice" in cleaned and ("varieties" in cleaned or "types" in cleaned or "about rice" in cleaned):
            session["last_topic"] = {"subject": "rice_varieties", "category": "agriculture"}
            return {
                "message": (
                    f"🌾 **Popular Rice Varieties & Their Characteristics:**\n\n"
                    f"• 👑 **Basmati Rice:** Long-grain, aged, with an exquisite fragrant aroma; perfect for Royal Dum Biryani.\n"
                    f"• 🌸 **Jasmine Rice:** Tender, slightly sticky floral aroma popular in Southeast Asian cuisine.\n"
                    f"• 🍚 **Sona Masoori:** Lightweight, low-starch aromatic medium-grain rice from Southern India.\n\n"
                    f"💡 *Culinary Connection: We proudly source premium aged Basmati rice for our chef's signature Royal Chicken Biryani here at Gourmet Haven!*"
                ),
                "intent": "knowledge_agriculture_food",
                "action_type": None,
                "quick_replies": [
                    {"label": "🍗 View Royal Biryani", "payload": "Tell me about Royal Chicken Biryani", "icon": "Utensils"},
                    {"label": "🌾 How to grow paddy?", "payload": "How to grow paddy?", "icon": "Leaf"}
                ],
                "structured_data": None
            }

        # Hugging Face LLM Model Generation (if configured)
        hf_reply = hf_client.generate_response(raw_msg, session.get("history", []), active_language=active_language,
            language=language, script=script, style=style)
        if hf_reply:
            session["last_topic"] = {"subject": cleaned[:30], "category": "general"}
            return {
                "message": hf_reply,
                "intent": "knowledge_hf_llm",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        # Conversational Knowledge Response (NEVER Knowledge Hub)
        if active_language == "telugu_script":
            session["last_topic"] = {"subject": cleaned[:30], "category": "general"}
            return {
                "message": (
                    f"ఖచ్చితంగా, {user_name}! **{raw_msg.strip()}** గురించి:\n\n"
                    f"దీనికి సంబంధించిన నిర్దిష్ట సమాచారం లేదా వివరణ కావాలా? దయచేసి చెప్పండి, నేను సహాయం చేస్తాను."
                ),
                "intent": "knowledge_general_telugu",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        if active_language == "tenglish":
            session["last_topic"] = {"subject": cleaned[:30], "category": "general"}
            return {
                "message": (
                    f"Sure, {user_name}! **{raw_msg.strip()}** gurinchi:\n\n"
                    f"Deeni gurinchi meeku specific information leda overview kavala? Cheppandi, nenu help chestanu."
                ),
                "intent": "knowledge_general_tenglish",
                "action_type": None,
                "quick_replies": [],
                "structured_data": None
            }

        session["last_topic"] = {"subject": cleaned[:30], "category": "general"}
        return {
            "message": (
                f"Sure, {user_name}! Regarding **{raw_msg.strip()}**:\n\n"
                f"Would you like an overview or do you have a specific question about this? Let me know and I'll be happy to help!"
            ),
            "intent": "knowledge_general",
            "action_type": None,
            "quick_replies": [],
            "structured_data": None
        }

knowledge_handler = KnowledgeHandler()


