from typing import Dict, Any, List, Optional

class LearningHandler:
    """
    Interactive Learning and Tutorials Handler (e.g. Python, Programming, Logic).
    Maintains learning progress across the session.
    """

    def handle_python_tutorial(self, msg: str, user_name: str, session: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = msg.lower()
        active = session.get("active_learning") or {"topic": "python", "step": 1}
        session["active_learning"] = active

        step = active.get("step", 1)

        # Handle user progression through tutorial steps
        if any(w in cleaned for w in ["next", "continue", "step 2", "loops", "condition"]) and step == 1:
            active["step"] = 2
            return {
                "message": (
                    f"🐍 **Python Masterclass — Stage 2: Conditions & Loops**\n\n"
                    f"Great job, {user_name}! Now let's make decisions and repeat actions:\n\n"
                    f"```python\n"
                    f"# If-Else Condition\n"
                    f"score = 95\n"
                    f"if score >= 90:\n"
                    f"    print('Outstanding grade! 🌟')\n\n"
                    f"# For Loop\n"
                    f"for i in range(3):\n"
                    f"    print(f'Iteration #{{i+1}}')\n"
                    f"```\n\n"
                    f"Ready for **Stage 3: Functions**, or want a quick coding puzzle?"
                ),
                "intent": "learning_python_step2",
                "action_type": None,
                "quick_replies": [
                    {"label": "⚡ Next: Functions (Stage 3)", "payload": "Teach me python functions", "icon": "Code"},
                    {"label": "🧩 Mini Python Quiz", "payload": "Give me a python quiz", "icon": "HelpCircle"},
                    {"label": "💬 Let's take a break", "payload": "Let's take a break", "icon": "Coffee"}
                ],
                "structured_data": None
            }

        if any(w in cleaned for w in ["next", "continue", "step 3", "functions", "func"]) or (step == 2 and "function" in cleaned):
            active["step"] = 3
            return {
                "message": (
                    f"🐍 **Python Masterclass — Stage 3: Functions & Reusability**\n\n"
                    f"Functions let you write clean, reusable blocks of code:\n\n"
                    f"```python\n"
                    f"def calculate_total(price: float, quantity: int) -> float:\n"
                    f"    subtotal = price * quantity\n"
                    f"    tax = subtotal * 0.08\n"
                    f"    return round(subtotal + tax, 2)\n\n"
                    f"# Calling the function\n"
                    f"final_bill = calculate_total(150.0, 2)\n"
                    f"print(f'Total Bill: ${{final_bill}}')  # Output: $324.0\n"
                    f"```\n\n"
                    f"You've mastered the foundations of Python, {user_name}! 🎉"
                ),
                "intent": "learning_python_step3",
                "action_type": None,
                "quick_replies": [
                    {"label": "🧩 Test my Python skills", "payload": "Give me a python quiz", "icon": "HelpCircle"},
                    {"label": "🌾 Try Farming Simulation", "payload": "How to grow paddy?", "icon": "Leaf"},
                    {"label": "🍽️ Treat myself to food", "payload": "Show me the menu", "icon": "Utensils"}
                ],
                "structured_data": None
            }

        if "quiz" in cleaned:
            return {
                "message": (
                    f"🧠 **Quick Python Quiz for {user_name}:**\n\n"
                    f"What is the output of the following code snippet?\n\n"
                    f"```python\n"
                    f"nums = [1, 2, 3]\n"
                    f"print(len(nums) * 2)\n"
                    f"```\n\n"
                    f"A) `3`\n"
                    f"B) `6`\n"
                    f"C) `[1, 2, 3, 1, 2, 3]`"
                ),
                "intent": "learning_quiz",
                "action_type": None,
                "quick_replies": [
                    {"label": "🅰️ Answer: 3", "payload": "Quiz answer is 3", "icon": "HelpCircle"},
                    {"label": "🅱️ Answer: 6", "payload": "Quiz answer is 6", "icon": "Check"},
                    {"label": "🅲️ Answer: [1, 2, 3, 1, 2, 3]", "payload": "Quiz answer is C", "icon": "HelpCircle"}
                ],
                "structured_data": None
            }

        if "6" in cleaned or "answer is 6" in cleaned or "answer: 6" in cleaned:
            return {
                "message": f"Correct! 🎯 `len(nums)` is 3, and `3 * 2 = 6`. You're writing Python like a pro, {user_name}! 🚀",
                "intent": "learning_quiz_passed",
                "action_type": None,
                "quick_replies": [
                    {"label": "⚡ Next: Functions", "payload": "Teach me python functions", "icon": "Code"},
                    {"label": "🌾 Virtual Paddy Farm", "payload": "How to grow paddy?", "icon": "Leaf"},
                    {"label": "🍽️ View Restaurant Menu", "payload": "Show me the menu", "icon": "Utensils"}
                ],
                "structured_data": None
            }

        # Default: Stage 1 (Variables & Data Types)
        active["step"] = 1
        return {
            "message": (
                f"🐍 **Welcome to Python for Beginners, {user_name}!**\n\n"
                f"Python is one of the world's most popular and readable languages. Let's start with **Stage 1: Variables & Data Types**:\n\n"
                f"```python\n"
                f"# Creating variables\n"
                f"user_name = '{user_name}'        # String\n"
                f"items_ordered = 3               # Integer\n"
                f"is_happy = True                 # Boolean\n"
                f"total_price = 24.50             # Float\n\n"
                f"print(f'Hello {user_name}, your total is ${{total_price}}')\n"
                f"```\n\n"
                f"Would you like to move to **Stage 2: Conditions & Loops**, or try a practice puzzle?"
            ),
            "intent": "learning_python_step1",
            "action_type": None,
            "quick_replies": [
                {"label": "⚡ Next: Conditions & Loops", "payload": "Teach me python loops", "icon": "Code"},
                {"label": "🧩 Mini Python Quiz", "payload": "Give me a python quiz", "icon": "HelpCircle"},
                {"label": "🎮 Let's play a game instead", "payload": "Give me a riddle", "icon": "Gamepad2"}
            ],
            "structured_data": None
        }

learning_handler = LearningHandler()
