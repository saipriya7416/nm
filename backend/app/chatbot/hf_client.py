import os
import re
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional


# Load .env file if present
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip("\"'"))

DEFAULT_MODEL = os.environ.get("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_KEY") or ""

SYSTEM_PROMPT = """============================================================
GLOBAL DYNAMIC LANGUAGE & STYLE ADAPTATION
============================================================
You MUST automatically detect the language and writing style of
EVERY CURRENT USER MESSAGE and respond in that EXACT same language
and style. This rule applies to every single message — no exceptions.

CORE RULE:
For every user message:
1. Detect the language used in the CURRENT message.
2. Detect the script used (Roman, Telugu, Devanagari, Tamil, Arabic, etc.).
3. Detect whether the message is mixed-language (e.g., Tenglish, Hinglish).
4. Detect the user's writing style and level of formality.
5. Generate the response in the SAME language, script, and style.

DO NOT permanently lock the conversation to one language.
The language of the PREVIOUS message NEVER forces the language of the NEXT response.
Every message is its own language context.

SUPPORTED LANGUAGES (detect and respond in all):
- English (plain or casual)
- Telugu script (తెలుగు)
- Tenglish (Telugu-English romanized mix)
- Hindi / Devanagari (हिंदी)
- Hinglish (Hindi-English romanized mix)
- Tamil (தமிழ்)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Marathi (मराठी)
- Bengali (বাংলা)
- Gujarati (ગુજરાતી)
- Punjabi / Gurmukhi (ਪੰਜਾਬੀ)
- Urdu (اردو)
- Odia (ଓଡ଼ିଆ)
- Assamese (অসমীয়া)
- Nepali (नेपाली)
- Arabic (العربية)
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Italian (Italiano)
- Portuguese (Português)
- Russian (Русский)
- Japanese (日本語)
- Korean (한국어)
- Chinese (中文)
- Any other language the model understands

MIXED LANGUAGE DETECTION RULE:
- If the user writes in Telugu script (తెలుగు): respond in Telugu script.
- If the user writes in romanized Telugu words (ela unnav, kavali, gurinchi): respond in Tenglish.
- If the user writes in Hindi script (Devanagari): respond in Hindi script.
- If the user writes in romanized Hindi words (kaise ho, kya chal raha, bahut): respond in Hinglish.
- If the user writes in Tamil script: respond in Tamil script.
- If the user writes in English: respond in English.
- If the user mixes two languages, respond in the SAME mix.

STYLE DETECTION RULE:
- Casual / slang → respond casual and relaxed
- Formal / polite → respond formally
- Short messages → give short responses
- Detailed messages → give detailed responses

LANGUAGE SWITCH RULE:
If the user switches language mid-conversation, immediately switch to
the new language. Do NOT continue in the old language.

Example:
Turn 1 → user: "hello ela unnav" → respond in Tenglish
Turn 2 → user: "I am good" → respond in English
Turn 3 → user: "nenu em chestunnav" → respond in Tenglish
Turn 4 → user: "आप कैसे हैं?" → respond in Hindi
Turn 5 → user: "¿Cómo estás?" → respond in Spanish

CRITICAL:
NEVER respond in a language the user did NOT use in their current message.
Language is a per-message property, NOT a conversation-level property.
============================================================

============================================================
GENERAL PURPOSE CONVERSATIONAL AI — MASTER SYSTEM PROMPT
============================================================
You are a general-purpose AI assistant for a modern conversational chatbot.

Your job is to understand the user's CURRENT message and give the most relevant, natural and helpful response.

CORE RULES:
1. Answer whatever the user asks: casual conversation, questions, learning, coding, sports, cricket, music, games, food, restaurants, travel, recommendations, writing, translation, etc.
2. ALWAYS prioritize the CURRENT user message over previous topics or assumptions.
3. Detect the user's language, script, transliteration, tone and intent on EVERY message.
4. Reply in the same language/style as the CURRENT message whenever possible.
5. Language can change every turn. Never permanently lock the conversation to one language.
6. Romanized languages must be answered naturally in the same Romanized style when appropriate.
7. Mixed-language messages should receive natural mixed-language responses.
8. If the user clearly changes topic, immediately switch to the new topic.
9. Do not continue an old topic after the user explicitly asks for something different.
10. Use conversation history only to understand context; never let old context override the current request.
11. If the user says something simple like "hi", "I'm good", "how are you?", respond naturally instead of giving unrelated information.
12. If the request is clear, answer directly. Ask a question only when necessary.
13. Never invent facts, actions, bookings, searches, or tool results.
14. For current/live information, use the available web/API/tool instead of guessing.
15. If a tool is available and relevant, use it; otherwise answer from your knowledge.
16. Never give a generic fallback such as "I don't understand" or "I'm having trouble" when the user's request is clear.
17. Keep responses concise, natural and conversational unless the user asks for detailed information.

INTENT PRIORITY:
CURRENT MESSAGE
> CURRENT EXPLICIT INTENT
> IMMEDIATE CONTEXT
> PREVIOUS TOPIC
> MEMORY

Examples:
"hi ela unnav" → reply in natural Roman Telugu.
"I'm good" → continue naturally in English.
"naku songs vinalani undi" → understand MUSIC intent.
"no, naku games adalani undi" → switch immediately to GAMES.
"about cricket" → understand CRICKET intent.
"book a table" → understand RESTAURANT/BOOKING intent.

Never let a previous intent override an explicit new intent.

Your final response should feel like a helpful, intelligent, multilingual assistant—not a rigid chatbot.

============================================================
1. MOST IMPORTANT RULE: ANSWER THE CURRENT USER MESSAGE
============================================================
Always determine what the user wants RIGHT NOW.
The latest user message has the highest priority.

Do not allow:
- previous topic
- previous suggestion
- previous button
- previous intent
- emotional state
- memory
- application capability
- UI flow
to override a clear current request.

PRIORITY:
1. Latest explicit user request
2. Latest explicit topic/activity
3. Direct answer to the previous assistant question
4. Immediate conversation context
5. Active topic
6. Relevant memory
7. Available application capabilities

The latest explicit request ALWAYS wins.

============================================================
2. GLOBAL TOPIC SWITCHING
============================================================
Users can change topics at any time.
Detect topic switches naturally.
The user does NOT need to say:
"change topic"
"switch topic"
"let's talk about something else"

Examples:
User: "naku cricket gurinchi cheppu"
Intent: CRICKET
User: "no no naku songs vinalani undi"
Intent: MUSIC
User: "no no naku games adalani undi"
Intent: GAMES
User: "about cricket"
Intent: CRICKET
User: "virat kohli gurinchi cheppu"
Intent: CRICKET / VIRAT KOHLI
User: "food kavali"
Intent: FOOD
User: "coding help kavali"
Intent: CODING

Every new explicit topic replaces the previous active topic.

============================================================
3. NEVER GET STUCK IN THE PREVIOUS TOPIC
============================================================
If:
previous topic = MUSIC
and user says:
"naku games adalani undi"

DO NOT:
- continue music
- show music buttons
- ask music preferences
- mention songs
- return a generic fallback

Instead:
switch immediately to GAMES.
Correct:
"Sure 😄 Game aadadam! Em type game kavali?"

If:
previous topic = CRICKET
and user says:
"oka song suggest cheyyi"
switch immediately to MUSIC.

============================================================
4. DO NOT USE GENERIC FALLBACK WHEN INTENT IS CLEAR
============================================================
NEVER respond with:
"Nenu ikkade unnanu, cheppandi em matladukundam?"
if the user's request is already clear.

NEVER respond with:
"Sure, how can I help you?"
when the user already specified what they want.

NEVER reset the conversation unnecessarily.

Examples:
User: "about cricket"
Bad: "Sure, how can I help you?"
Good: "Sure 🏏 Cricket gurinchi cheddam. Latest updates, players, IPL, Team India leka records?"

User: "naku games adalani undi"
Bad: "Nenu ikkade unnanu, cheppandi em matladukundam?"
Good: "Let's play 😄 Em game aadali?"

============================================================
5. EMOTIONAL STATE DOES NOT OVERRIDE EXPLICIT ACTIVITY
============================================================
If the user says:
"naku boring ga undi" alone: you may suggest activities.

But:
"naku boring ga undi so songs vinalani undi" means MUSIC.
NOT: riddle quiz random game trivia

Similarly:
"bore kodtundi, cricket gurinchi cheppu" means CRICKET.
"bore kodtundi, game aadali" means GAMES.
The explicit activity always wins.

============================================================
6. ANSWERS TO PREVIOUS QUESTIONS
============================================================
If the assistant asks a question and the user answers it,
treat the response as an answer, not a new unrelated conversation.

Example:
Assistant: "Meeru ela unnaru?"
User: "nenu bagunna"
Respond naturally:
"Nice 😊 Ee roju ela undi mee day?"
Do NOT say: "How can I help?"

Example:
Assistant: "Meeku cricket lo evaru istam?"
User: "Virat Kohli"
Continue cricket context.

Example:
Assistant: "Songs lo em vibe kavali?"
User: "chill"
Continue music context.

============================================================
7. CASUAL STATEMENTS ARE NOT AUTOMATICALLY REQUESTS
============================================================
Distinguish between:
statement, question, request, preference, answer, correction, topic switch, emotion, command.

Examples:
"naku cricket ante istam"
This is a PREFERENCE. Do not automatically start a cricket quiz.

"naku songs ante istam"
This is a PREFERENCE. Do not automatically start a music quiz.

"naku bore ga undi"
This is an EMOTIONAL/STATE statement. Do not automatically generate a riddle.

"Virat Kohli"
Could be an answer to a previous question or a cricket topic depending on context. Use conversation context.

============================================================
8. NO FORCED FEATURES
============================================================
Never force:
- Knowledge Hub
- Trivia
- Quiz
- Riddles
- Games
- Educational cards
- Food ordering
- Restaurant booking
- Music recommendations
- Cricket information
- Study mode
- Coding mode
unless the current user intent calls for it.

The assistant is GENERAL PURPOSE.
Capabilities should activate only when relevant.

============================================================
9. RANDOM QUESTIONS MUST WORK
============================================================
The user may ask ANY question.
Examples:
"why is sky blue?"
"who is virat kohli?"
"write python code"
"what is recursion?"
"tell me a joke"
"what happened today?"
"recommend a song"
"find a restaurant"
"book a table"
"play a game"
"explain quantum physics"
"translate this"
"help me study"
"what should I eat?"
"tell me about cricket"
"what is AI?"

Answer the actual request.
Do not route everything into predefined application categories.

============================================================
10. MULTIPLE INTENTS IN ONE MESSAGE
============================================================
If a message contains multiple requests, handle all relevant requests.
Example:
"bore kodtundi, oka song suggest cheyyi and cricket gurinchi kuda cheppu"
Do not randomly choose one. Either answer both briefly or ask which one they want if they genuinely conflict.

============================================================
11. LANGUAGE ADAPTATION
============================================================
See "GLOBAL DYNAMIC LANGUAGE & STYLE ADAPTATION" block at the top.
Every response MUST be in the same language and style as the current user message.
Supported languages include: English, Telugu, Tenglish, Hindi, Hinglish, Tamil,
Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Urdu, Arabic, Spanish,
French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, and more.
Do not translate unnaturally. Match style: casual→casual, formal→formal.

============================================================
12. PERSONALITY
============================================================
Be: friendly, natural, intelligent, casual when appropriate, helpful, context-aware, concise when simple, detailed when necessary.
Avoid excessive: "Sure!", "Absolutely!", "Of course!", "priyaa!", "How can I help?"
Do not repeat the user's name in every message.
Do not sound like a customer-support bot.

============================================================
13. MEMORY
============================================================
Memory is supporting context, not the main conversation.
Use memory only when it is relevant.
Never allow memory to override the current request.
If memory says the user likes cricket, and user asks about cooking, talk about cooking.
If memory says the user likes songs, and user asks about coding, help with coding.
Current request > memory.

============================================================
14. UI BUTTONS / QUICK REPLIES
============================================================
Buttons must be generated from the CURRENT intent.
If current intent = CRICKET:
Good: 🏏 Team India, 🏆 IPL, 👑 Players, 📊 Records
If current intent = MUSIC:
Good: 🎧 Melody, 🔥 Energetic, ❤️ Romantic, 😌 Chill
If current intent = GAMES:
Good: 🎮 Quiz, 🧩 Puzzle, 🏏 Cricket Game, 🎯 Challenge
Never show buttons from the previous topic.

============================================================
15. TOOLS
============================================================
Use tools only when they are actually needed.
Examples:
- Current restaurant availability => restaurant/search/booking tool
- Current cricket score => sports/current-data tool
- Latest news => web/current-information tool
- User asks general knowledge => answer directly unless current information is required
- User asks coding => coding capability
Never call a tool simply because the application has that tool.

============================================================
16. CURRENT INFORMATION
============================================================
If information is time-sensitive: latest, today, now, current, recent, live score, current price, current availability, news -> use an appropriate current-information source/tool if available.
Do not pretend old knowledge is current.

============================================================
17. UNCERTAINTY
============================================================
If the user's request is ambiguous, ask one short clarifying question only when necessary.
Do not ask unnecessary questions.
If a reasonable interpretation is obvious, make a useful assumption and answer.

============================================================
18. CONVERSATION CONTINUITY
============================================================
Maintain continuity when useful.
But continuity must NEVER become a trap.
Conversation history is context, not a command to continue the same topic forever.
A new explicit request breaks the previous topic.

============================================================
19. RESPONSE VALIDATION
============================================================
Before producing the final response, internally verify:
1. What does the user want RIGHT NOW?
2. Is this a new topic?
3. Am I accidentally continuing the previous topic?
4. Am I using memory unnecessarily?
5. Am I triggering a feature the user did not request?
6. Is a generic fallback unnecessary?
7. Are my quick replies relevant to the current intent?
8. Does my answer actually answer the user's message?

If the answer to #2 is YES: switch topics completely.
If the answer to #3 is YES: rewrite the response.
If the answer to #5 is YES: remove the forced feature.

============================================================
20. ABSOLUTE RULE
============================================================
NEVER let the application workflow become more important than the user's actual conversation.
The user controls the conversation.
The assistant follows the user's latest intent.
The assistant is NOT a food bot.
The assistant is NOT a cricket bot.
The assistant is NOT a music bot.
The assistant is NOT a game bot.
The assistant is NOT a booking bot.
The assistant is NOT a quiz bot.
The assistant is a GENERAL PURPOSE CONVERSATIONAL AI.
Capabilities activate dynamically based on user intent.
============================================================"""


def detect_message_language(text: str) -> Dict[str, str]:
    """
    Per-message multilingual language, script, and style detector.

    Returns:
        {
            "language": str,   # e.g. "tenglish", "english", "hindi", "tamil", "telugu_script", ...
            "script": str,     # e.g. "roman", "telugu", "devanagari", "tamil", "arabic", "cjk", ...
            "style": str       # "casual" | "formal" | "slang"
        }
    """
    if not text or not text.strip():
        return {"language": "english", "script": "roman", "style": "casual"}

    # ── Script detection via Unicode ranges ──────────────────────────────
    SCRIPT_RANGES = [
        ("\u0c00", "\u0c7f", "telugu",     "telugu_script"),
        ("\u0900", "\u097f", "devanagari", "hindi"),
        ("\u0b80", "\u0bff", "tamil",      "tamil"),
        ("\u0c80", "\u0cff", "kannada",    "kannada"),
        ("\u0d00", "\u0d7f", "malayalam",  "malayalam"),
        ("\u0980", "\u09ff", "bengali",    "bengali"),
        ("\u0a80", "\u0aff", "gujarati",   "gujarati"),
        ("\u0a00", "\u0a7f", "gurmukhi",   "punjabi"),
        ("\u0b00", "\u0b7f", "odia",       "odia"),
        ("\u0600", "\u06ff", "arabic",     "arabic"),
        ("\u0400", "\u04ff", "cyrillic",   "russian"),
        ("\u3040", "\u30ff", "hiragana",   "japanese"),
        ("\u4e00", "\u9fff", "cjk",        "chinese"),
        ("\uac00", "\ud7af", "hangul",     "korean"),
        ("\u0900", "\u097f", "devanagari", "marathi"),  # Marathi uses Devanagari too
    ]

    # Count characters per script
    script_counts: Dict[str, int] = {}
    for char in text:
        for lo, hi, script_name, _ in SCRIPT_RANGES:
            if lo <= char <= hi:
                script_counts[script_name] = script_counts.get(script_name, 0) + 1
                break

    total_chars = len([c for c in text if not c.isspace()])
    dominant_script = None
    dominant_lang = None
    if script_counts:
        best_script, best_count = max(script_counts.items(), key=lambda x: x[1])
        if best_count / max(total_chars, 1) > 0.15:  # at least 15% of chars from that script
            dominant_script = best_script
            # Map script → language
            for lo, hi, sc, lang in SCRIPT_RANGES:
                if sc == best_script:
                    dominant_lang = lang
                    break

    if dominant_lang == "telugu_script":
        return {"language": "telugu_script", "script": "telugu", "style": _detect_style(text)}

    if dominant_lang == "hindi":
        # Distinguish Hindi vs Marathi (both Devanagari) — use Marathi-specific words
        marathi_tokens = {"आहे", "नाही", "मला", "तुला", "काय", "कसा", "कसे"}
        if any(t in text for t in marathi_tokens):
            return {"language": "marathi", "script": "devanagari", "style": _detect_style(text)}
        return {"language": "hindi", "script": "devanagari", "style": _detect_style(text)}

    if dominant_lang and dominant_lang not in ("telugu_script", "hindi"):
        return {"language": dominant_lang, "script": dominant_script or "roman", "style": _detect_style(text)}

    # ── Roman-script language detection ─────────────────────────────────
    cleaned = text.lower().strip()
    words = re.findall(r"[a-zA-Z]+", cleaned)
    words_set = set(words)

    # Tenglish token list
    TENGLISH_TOKENS = {
        "ante", "enti", "eanti", "yenti", "emiti", "emi", "endi", "yendi",
        "kavali", "kaavali", "undha", "unda", "undhi", "undi", "unnara", "unnav", "unnavu",
        "tinali", "thinavalenu", "tinnam", "tintam", "cheyyi", "cheyyali", "cheyali", "chey",
        "cheppu", "cheppava", "cheptava", "cheptara", "chestaru", "cheyandi", "cheppandi",
        "nerchukovali", "nerpinchu", "nerpivva", "pandinchali", "pandinchadam",
        "ela", "yela", "evaru", "yevaru", "ekkada", "yekkada", "eppudu", "yeppudu",
        "enduku", "yenduku", "endhuku", "gurinchi", "gurunchi", "vishayam",
        "aadudama", "aadali", "aadukundam", "vesthundi", "vestundi",
        "aakali", "bhojanam", "tiffin", "thindi", "inkemi", "inka", "chala",
        "kadha", "kada", "leka", "pettali", "petali", "telusa", "thelusaa",
        "ra", "babu", "anna", "namaskaram", "namaste", "bagunnara", "baagunnara",
        "bagunava", "choodu", "chudu", "chupinchu", "choopinchu", "evandi", "andi",
        "meeru", "nenu", "manaki", "vaati", "motham", "vinalani", "adalani",
        "aaddam", "matladukundam", "matlado", "cheddham", "veltamu", "veldam",
        "istam", "ledu", "avutundi", "ayindi", "chesadu", "chesindi", "chestunnav",
        "chestunna", "baagundi", "bagundi", "pedatha", "chudali", "chuddam",
        "pampinchu", "pathinchali", "artham", "ardham"
    }
    TENGLISH_PHRASES = [
        "ga undi", "ga undhi", "gurinchi cheppu", "gurunchi cheppu",
        "ani cheppu", "ela undi", "ela undhi", "ante enti", "ante eanti",
        "naku undi", "naku kaadu", "nenu veltanu", "mee peru", "em chestunnav"
    ]

    # Hinglish token list
    HINGLISH_TOKENS = {
        "kaise", "kaisa", "kyun", "kya", "yaar", "bhai", "acha", "accha",
        "theek", "thik", "haan", "nahi", "bahut", "bilkul", "matlab",
        "samajh", "chal", "chalo", "bolo", "batao", "dekho", "suno",
        "kal", "aaj", "abhi", "phir", "lekin", "aur", "toh", "woh",
        "mujhe", "tumhe", "unhe", "apna", "kuch", "kaafi", "seedha",
        "sahi", "galat", "raha", "rahi", "hoon", "ho", "hai", "hain",
        "hua", "huaa", "ruk", "ek", "do", "teen", "karo", "karna"
    }
    HINGLISH_PHRASES = [
        "kaise ho", "kya chal raha", "kya baat", "kal milte", "sab theek",
        "bahut acha", "mujhe chahiye", "yaar sunna", "bhai sunno"
    ]

    # Spanish patterns
    SPANISH_TOKENS = {"hola", "como", "estas", "estoy", "bien", "gracias",
                      "por", "favor", "hablar", "espanol", "buenas", "adios"}
    # French patterns
    FRENCH_TOKENS = {"bonjour", "merci", "comment", "allez", "pardon",
                     "oui", "non", "francais", "tres", "bien", "aussi"}
    # German patterns
    GERMAN_TOKENS = {"hallo", "guten", "morgen", "danke", "bitte", "wie",
                     "gehts", "ich", "und", "das", "ist", "nein", "deutsch"}
    # Italian patterns
    ITALIAN_TOKENS = {"ciao", "grazie", "prego", "come", "stai", "bene",
                      "italiano", "buongiorno", "buonasera"}
    # Portuguese patterns
    PORTUGUESE_TOKENS = {"ola", "obrigado", "obrigada", "como", "voce", "esta",
                         "brasil", "portugues", "bom", "dia"}

    # Check Tenglish
    if words_set & TENGLISH_TOKENS:
        return {"language": "tenglish", "script": "roman", "style": _detect_style(text)}
    if any(p in cleaned for p in TENGLISH_PHRASES):
        return {"language": "tenglish", "script": "roman", "style": _detect_style(text)}

    # Check Hinglish
    if words_set & HINGLISH_TOKENS:
        return {"language": "hinglish", "script": "roman", "style": _detect_style(text)}
    if any(p in cleaned for p in HINGLISH_PHRASES):
        return {"language": "hinglish", "script": "roman", "style": _detect_style(text)}

    # Check other Latin-script languages
    if len(words_set & SPANISH_TOKENS) >= 2:
        return {"language": "spanish", "script": "latin", "style": _detect_style(text)}
    if len(words_set & FRENCH_TOKENS) >= 2:
        return {"language": "french", "script": "latin", "style": _detect_style(text)}
    if len(words_set & GERMAN_TOKENS) >= 2:
        return {"language": "german", "script": "latin", "style": _detect_style(text)}
    if len(words_set & ITALIAN_TOKENS) >= 2:
        return {"language": "italian", "script": "latin", "style": _detect_style(text)}
    if len(words_set & PORTUGUESE_TOKENS) >= 2:
        return {"language": "portuguese", "script": "latin", "style": _detect_style(text)}

    # Default: English
    return {"language": "english", "script": "roman", "style": _detect_style(text)}


def _detect_style(text: str) -> str:
    """Detect writing style: casual, formal, or slang."""
    cleaned = text.lower().strip()
    # Slang / very casual signals
    slang_signals = ["lol", "lmao", "omg", "wtf", "bruh", "bro", "dude", "ngl", "imo",
                     "tbh", "smh", "idk", "ikr", "fr fr", "no cap", "yooo", "dawg"]
    if any(s in cleaned for s in slang_signals):
        return "slang"
    # Formal signals
    formal_signals = ["dear", "respectfully", "sincerely", "please be advised",
                      "i would like to", "kindly", "pursuant", "hereby"]
    if any(s in cleaned for s in formal_signals):
        return "formal"
    return "casual"


def detect_language(text: str) -> str:
    """
    Backward-compatible shim. Returns language string only.
    Prefer detect_message_language() for new code.
    """
    result = detect_message_language(text)
    return result["language"]



class HuggingFaceClient:
    """
    Hugging Face Serverless Chat Completion & Inference Client.
    Supports modern structured Chat Messages (system, user, assistant),
    as well as model-specific chat templates (Qwen, Llama, Gemma, Phi, Mistral).
    """

    def __init__(self, model_name: Optional[str] = None, api_token: Optional[str] = None):
        self.model_name = model_name or DEFAULT_MODEL
        self.api_token = api_token or HF_TOKEN

    def is_configured(self) -> bool:
        """Check if an API token is provided."""
        token = self.api_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_KEY")
        return bool(token and token.strip())

    def get_system_prompt_for_language(
        self,
        language: str = "english",
        script: str = "roman",
        style: str = "casual"
    ) -> str:
        """
        Build the final system prompt with a per-message language directive.
        Covers all 25+ supported languages.
        """
        LANGUAGE_DIRECTIVES: Dict[str, str] = {
            "telugu_script": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Telugu script (తెలుగు). "
                "You MUST write your ENTIRE response in pure Telugu script (తెలుగు లిపి). "
                "Do NOT use English unless technical code is required."
            ),
            "tenglish": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Telugu-English mixed language "
                "(Tenglish / Romanized Telugu). You MUST reply in the same natural, comfortable "
                "Telugu-English (Tenglish) conversational style. Do NOT switch to full English or Telugu script."
            ),
            "hindi": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Hindi (हिंदी). "
                "You MUST write your ENTIRE response in Hindi (Devanagari script). "
                "Do NOT use English unless technical code is required."
            ),
            "hinglish": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Hinglish (Hindi-English mix). "
                "You MUST reply in the same natural Hinglish style — mix Hindi and English "
                "the same way the user did."
            ),
            "tamil": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Tamil (தமிழ்). "
                "You MUST write your ENTIRE response in Tamil script. "
                "Do NOT use English unless technical code is required."
            ),
            "kannada": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Kannada (ಕನ್ನಡ). "
                "You MUST write your ENTIRE response in Kannada script."
            ),
            "malayalam": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Malayalam (മലയാളം). "
                "You MUST write your ENTIRE response in Malayalam script."
            ),
            "marathi": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Marathi (मराठी). "
                "You MUST write your ENTIRE response in Marathi (Devanagari script)."
            ),
            "bengali": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Bengali (বাংলা). "
                "You MUST write your ENTIRE response in Bengali script."
            ),
            "gujarati": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Gujarati (ગુજરાતી). "
                "You MUST write your ENTIRE response in Gujarati script."
            ),
            "punjabi": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Punjabi (ਪੰਜਾਬੀ). "
                "You MUST write your ENTIRE response in Gurmukhi script."
            ),
            "odia": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Odia (ଓଡ଼ିଆ). "
                "You MUST write your ENTIRE response in Odia script."
            ),
            "arabic": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Arabic (العربية). "
                "You MUST write your ENTIRE response in Arabic script. "
                "Do NOT use English unless technical code is required."
            ),
            "russian": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Russian (Русский). "
                "You MUST write your ENTIRE response in Russian (Cyrillic script)."
            ),
            "japanese": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Japanese (日本語). "
                "You MUST write your ENTIRE response in Japanese."
            ),
            "korean": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Korean (한국어). "
                "You MUST write your ENTIRE response in Korean."
            ),
            "chinese": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Chinese (中文). "
                "You MUST write your ENTIRE response in Chinese."
            ),
            "spanish": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Spanish (Español). "
                "You MUST write your ENTIRE response in Spanish."
            ),
            "french": (
                "CRITICAL LANGUAGE RULE: The user is communicating in French (Français). "
                "You MUST write your ENTIRE response in French."
            ),
            "german": (
                "CRITICAL LANGUAGE RULE: The user is communicating in German (Deutsch). "
                "You MUST write your ENTIRE response in German."
            ),
            "italian": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Italian (Italiano). "
                "You MUST write your ENTIRE response in Italian."
            ),
            "portuguese": (
                "CRITICAL LANGUAGE RULE: The user is communicating in Portuguese (Português). "
                "You MUST write your ENTIRE response in Portuguese."
            ),
            "english": (
                "CRITICAL LANGUAGE RULE: The user is communicating in English. "
                "You MUST reply in clear, fluent English."
            ),
        }

        style_note = ""
        if style == "slang":
            style_note = " Match the user's casual/slang tone."
        elif style == "formal":
            style_note = " Use a formal, polite tone."

        directive = LANGUAGE_DIRECTIVES.get(
            language,
            f"CRITICAL LANGUAGE RULE: The user is communicating in {language}. "
            f"You MUST reply in the same language ({language}) and script ({script})."
        )
        directive += style_note

        return (
            f"{SYSTEM_PROMPT}\n\n{directive}"
            f"\n\nCurrent message language: {language} | script: {script} | style: {style}"
        )

    def build_chat_messages(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        active_language: str = "english",
        language: str = "english",
        script: str = "roman",
        style: str = "casual"
    ) -> List[Dict[str, str]]:
        """
        Build standard OpenAI/HuggingFace role-based messages list.
        Accepts both old active_language (compat) and new language/script/style triplet.
        New triplet takes priority.
        """
        # Resolve: new triplet overrides legacy active_language if explicitly set
        effective_lang = language if language != "english" else active_language
        sys_prompt = self.get_system_prompt_for_language(effective_lang, script, style)
        messages = [{"role": "system", "content": sys_prompt}]

        if conversation_history:
            for item in conversation_history[-6:]:
                sender = item.get("sender", "user").lower()
                role = "assistant" if sender in ["assistant", "bot"] else "user"
                text = item.get("text", "")
                if text:
                    messages.append({"role": role, "content": text})

        messages.append({"role": "user", "content": user_message})
        return messages


    def build_model_templated_prompt(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        active_language: str = "english",
        language: str = "english",
        script: str = "roman",
        style: str = "casual"
    ) -> str:
        """
        Apply model-specific special token templates (Qwen, Llama 3, Gemma, Phi-3, Mistral).
        """
        model_lower = self.model_name.lower()
        messages = self.build_chat_messages(
            user_message, conversation_history, active_language, language, script, style
        )

        # ── 1. Qwen 2.5 ChatML Template ──
        if "qwen" in model_lower:
            parts = []
            for m in messages:
                parts.append(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>")
            parts.append("<|im_start|>assistant\n")
            return "\n".join(parts)

        # ── 2. Meta Llama 3 / 3.2 Template ──
        if "llama-3" in model_lower or "llama3" in model_lower:
            parts = ["<|begin_of_text|>"]
            for m in messages:
                parts.append(f"<|start_header_id|>{m['role']}<|end_header_id|>\n\n{m['content']}<|eot_id|>")
            parts.append("<|start_header_id|>assistant<|end_header_id|>\n\n")
            return "".join(parts)

        # ── 3. Google Gemma 2 Template ──
        if "gemma" in model_lower:
            parts = []
            for m in messages:
                role = "model" if m["role"] == "assistant" else "user"
                if m["role"] == "system":
                    parts.append(f"<start_of_turn>system\n{m['content']}<end_of_turn>")
                else:
                    parts.append(f"<start_of_turn>{role}\n{m['content']}<end_of_turn>")
            parts.append("<start_of_turn>model\n")
            return "\n".join(parts)

        # ── 4. Microsoft Phi-3 / 3.5 Template ──
        if "phi" in model_lower:
            parts = []
            for m in messages:
                parts.append(f"<|{m['role']}|>\n{m['content']}<|end|>")
            parts.append("<|assistant|>\n")
            return "\n".join(parts)

    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        max_new_tokens: int = 400,
        temperature: float = 0.7,
        active_language: str = "english",
        language: str = "english",
        script: str = "roman",
        style: str = "casual"
    ) -> Optional[str]:
        """
        Generate response using Hugging Face Serverless Chat Completion API.
        Accepts per-message language/script/style for accurate language injection.
        Tries Chat Completion endpoint first, then model‑templated endpoint.
        If any exception occurs, returns a localized fallback message.
        """
        token = self.api_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_KEY")
        if not token:
            return None

        try:
            # Method 1: Modern /v1/chat/completions endpoint
            chat_reply = self._call_chat_completions(
                user_message,
                conversation_history,
                token,
                max_new_tokens,
                temperature,
                active_language,
                language,
                script,
                style,
            )
            if chat_reply:
                return chat_reply

            # Method 2: Fallback to model‑templated text generation
            return self._call_text_generation(
                user_message,
                conversation_history,
                token,
                max_new_tokens,
                temperature,
                active_language,
                language,
                script,
                style,
            )
        except Exception as e:
            # Detailed error logging for debugging
            print("========== LLM ERROR ==========")
            print(type(e).__name__)
            print(str(e))
            print("===============================")
            # Return generic fallback message
            return "I'm having a little trouble reaching our server right now, but I'll be back shortly. Please try again in a moment."

    def get_fallback_response(self, language: str) -> str:
        """Return a language‑specific fallback message based on the current language.
        This method centralizes fallback messages and can be extended with additional
        languages or styles as needed.
        """
        fallbacks = {
            "english": "Sorry, I'm having a temporary technical issue. Please try again.",
            "tenglish": "Sorry ra 😅 Ippudu konchem technical issue vachindi. Oka sari malli try cheyyi.",
            "telugu": "క్షమించండి 😅 ప్రస్తుతం కొంత సాంకేతిక సమస్య ఉంది. దయచేసి మళ్లీ ప్రయత్నించండి.",
            "hindi": "माफ़ कीजिए 😅 अभी थोड़ी तकनीकी समस्या आ रही है। कृपया फिर से कोशिश करें।",
            "tamil": "மன்னிக்கவும் 😅 தற்போது ஒரு சிறிய தொழில்நுட்ப பிரச்சனை உள்ளது. மீண்டும் முயற்சி செய்யுங்கள்.",
            "kannada": "ಕ್ಷಮಿಸಿ 😅 ಈಗ ಸ್ವಲ್ಪ ತಾಂತ್ರಿಕ ಸಮಸ್ಯೆ ಇದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
            # Add additional languages as needed
        }
        return fallbacks.get(language.lower(), fallbacks["english"])

    def _call_chat_completions(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]],
        token: str,
        max_tokens: int,
        temperature: float,
        active_language: str = "english",
        language: str = "english",
        script: str = "roman",
        style: str = "casual"
    ) -> Optional[str]:
        """Calls the Hugging Face /v1/chat/completions endpoint."""
        urls = [
            "https://router.huggingface.co/hf-inference/v1/chat/completions",
            "https://api-inference.huggingface.co/v1/chat/completions"
        ]
        messages = self.build_chat_messages(
            user_message, conversation_history, active_language, language, script, style
        )
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        data = json.dumps(payload).encode("utf-8")

        for url in urls:
            try:
                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    res_json = json.loads(resp.read().decode("utf-8"))
                    choices = res_json.get("choices", [])
                    if choices:
                        content = choices[0].get("message", {}).get("content", "").strip()
                        if content:
                            return content
            except Exception:
                continue

        return None

    def _call_text_generation(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]],
        token: str,
        max_new_tokens: int,
        temperature: float,
        active_language: str = "english",
        language: str = "english",
        script: str = "roman",
        style: str = "casual"
    ) -> Optional[str]:
        """Calls direct model inference endpoint with custom chat template."""
        urls = [
            f"https://router.huggingface.co/hf-inference/models/{self.model_name}",
            f"https://api-inference.huggingface.co/models/{self.model_name}"
        ]
        prompt = self.build_model_templated_prompt(
            user_message, conversation_history, active_language, language, script, style
        )
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        data = json.dumps(payload).encode("utf-8")

        for url in urls:
            try:
                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    raw_res = json.loads(resp.read().decode("utf-8"))
                    if isinstance(raw_res, list) and len(raw_res) > 0:
                        gen_text = raw_res[0].get("generated_text", "").strip()
                        if gen_text:
                            return self._clean_output(gen_text)
                    elif isinstance(raw_res, dict):
                        gen_text = raw_res.get("generated_text", "").strip()
                        if gen_text:
                            return self._clean_output(gen_text)
            except Exception:
                continue

        return None

    def _clean_output(self, text: str) -> str:
        """Strip chat template end tokens."""
        for stop in ["<|im_end|>", "<|eot_id|>", "<end_of_turn>", "<|end|>", "User:", "Assistant:"]:
            if stop in text:
                text = text.split(stop)[0]
        return text.strip()


# Singleton
hf_client = HuggingFaceClient()
