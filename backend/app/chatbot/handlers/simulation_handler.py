from typing import Dict, Any, List, Optional

class SimulationHandler:
    """
    Handles interactive simulations:
    - Virtual Paddy/Rice Farming Simulation (5 Stages from Soil Prep to Golden Harvest)
    - Virtual Business & Startup Builder
    - Virtual Travel Planner
    - Gourmet Cooking Assistant
    """

    def handle_farming_simulation(self, msg: str, user_name: str, session: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = msg.lower()
        sim = session.get("active_simulation")
        if not sim or sim.get("type") != "farming":
            sim = {"type": "farming", "crop": "Paddy (Basmati Rice)", "stage": 1}
            session["active_simulation"] = sim

        stage = sim.get("stage", 1)

        # Stage Progression
        if any(w in cleaned for w in ["sow", "nursery", "seed", "stage 2", "next"]) and stage == 1:
            sim["stage"] = 2
            return {
                "message": (
                    f"🌾 **{user_name}'s Virtual Paddy Farm — Stage 2: Nursery & Sowing**\n\n"
                    f"🚜 Your soil is puddled, flooded (2 inches), and leveled!\n\n"
                    f"**Next Action:** We soak high-yield organic seeds in water for 24 hours, sprout them in darkness, "
                    f"and broadcast them across the raised nursery bed.\n\n"
                    f"🌱 *Seedlings take ~21 days in the nursery before transplantation.* Ready to transplant?"
                ),
                "intent": "simulation_farming_stage2",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌱 Next: Transplant Seedlings", "payload": "Transplant seedlings to main field", "icon": "Leaf"},
                    {"label": "💧 Check Water Management", "payload": "How much water is needed?", "icon": "Droplet"},
                    {"label": "📊 View Farm Status", "payload": "Show my farm status", "icon": "Check"}
                ],
                "structured_data": {"farm": {"stage": 2, "crop": "Paddy", "health": "100%", "progress": "40%"}}
            }

        if any(w in cleaned for w in ["transplant", "main field", "stage 3", "next"]) and stage == 2:
            sim["stage"] = 3
            return {
                "message": (
                    f"🌾 **{user_name}'s Virtual Paddy Farm — Stage 3: Field Transplantation**\n\n"
                    f"🌱 The 21-day-old vibrant green saplings are ready! We transplant 2–3 seedlings per hill, "
                    f"spaced 15 cm apart into the flooded main field.\n\n"
                    f"**Field Condition:**\n"
                    f"• Soil: Loamy fertile clay\n"
                    f"• Water level: 3–5 cm standing water maintained\n\n"
                    f"Ready for **Stage 4: Organic Nutrition & Pest Care**?"
                ),
                "intent": "simulation_farming_stage3",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌿 Next: Nutrient & Weed Care", "payload": "Apply organic bio-fertilizer", "icon": "Shield"},
                    {"label": "📊 View Farm Status", "payload": "Show my farm status", "icon": "Check"}
                ],
                "structured_data": {"farm": {"stage": 3, "crop": "Paddy", "health": "100%", "progress": "65%"}}
            }

        if any(w in cleaned for w in ["nutrient", "fertilizer", "weed", "stage 4", "next"]) and stage == 3:
            sim["stage"] = 4
            return {
                "message": (
                    f"🌾 **{user_name}'s Virtual Paddy Farm — Stage 4: Crop Care & Panicle Emergence**\n\n"
                    f"✨ We applied organic compost and neem-oil spray for natural pest prevention. "
                    f"The paddy crops have now tillered and the flowering panicles are developing!\n\n"
                    f"**Days to Harvest:** ~30 days as grains turn from green to rich golden amber.\n\n"
                    f"Ready to reap your harvest?"
                ),
                "intent": "simulation_farming_stage4",
                "action_type": None,
                "quick_replies": [
                    {"label": "🌾 Next: Golden Harvest!", "payload": "Harvest the paddy crop", "icon": "Sun"},
                    {"label": "📊 View Farm Status", "payload": "Show my farm status", "icon": "Check"}
                ],
                "structured_data": {"farm": {"stage": 4, "crop": "Paddy", "health": "100%", "progress": "85%"}}
            }

        if any(w in cleaned for w in ["harvest", "reap", "stage 5", "next"]) and stage == 4:
            sim["stage"] = 5
            return {
                "message": (
                    f"🎉 **{user_name}, your crop has reached the harvest stage! 🌾**\n\n"
                    f"The golden panicles are harvested, threshed, and dried under the sun!\n\n"
                    f"🏆 **Harvest Results:**\n"
                    f"• **Crop:** Premium Aromatic Basmati Paddy\n"
                    f"• **Yield:** 28 Quintals per acre (Exceptional Grade A!)\n"
                    f"• **Farm Health:** 100% Organic\n\n"
                    f"Congratulations, Farmer {user_name}! 🌾 That was a masterclass in agriculture!"
                ),
                "intent": "simulation_farming_harvest",
                "action_type": None,
                "quick_replies": [
                    {"label": "👑 Celebrate with Biryani!", "payload": "I want to order Royal Chicken Biryani", "icon": "Utensils"},
                    {"label": "🌾 Start New Virtual Farm", "payload": "Start farming simulation", "icon": "Leaf"},
                    {"label": "💼 Try Business Simulation", "payload": "I want to start a business", "icon": "Briefcase"}
                ],
                "structured_data": {"farm": {"stage": 5, "crop": "Paddy", "health": "100%", "progress": "100%", "harvested": True}}
            }

        # Stage 1: Initiation / Soil Preparation
        sim["stage"] = 1
        return {
            "message": (
                f"🌾 **Welcome to the Virtual Paddy Farm, Farmer {user_name}!**\n\n"
                f"Let's cultivate a thriving crop of aromatic rice step-by-step:\n\n"
                f"**Stage 1: Land & Soil Preparation**\n"
                f"We plough the soil twice, flood the plot with 2 inches of water, and perform 'puddling' to create an impervious clay bed that retains moisture.\n\n"
                f"Ready to prepare your nursery bed and sow sprouted seeds?"
            ),
            "intent": "simulation_farming_stage1",
            "action_type": None,
            "quick_replies": [
                {"label": "🌱 Next: Sow Seeds in Nursery", "payload": "Sow seeds in nursery", "icon": "Leaf"},
                {"label": "💧 Water Management Info", "payload": "How much water is needed for paddy?", "icon": "Droplet"},
                {"label": "🍽️ View Menu", "payload": "Show me the menu", "icon": "Utensils"}
            ],
            "structured_data": {"farm": {"stage": 1, "crop": "Paddy", "health": "100%", "progress": "20%"}}
        }

    def handle_business_simulation(self, msg: str, user_name: str, session: Dict[str, Any]) -> Dict[str, Any]:
        sim = {"type": "business", "step": 1}
        session["active_simulation"] = sim

        return {
            "message": (
                f"💼 **Welcome to the Startup Builder Simulation, {user_name}!**\n\n"
                f"Let's build a profitable business venture together:\n\n"
                f"**Step 1: The Core Value Proposition**\n"
                f"What type of venture would you like to build?\n"
                f"• 📱 **Tech SaaS / AI Tool**\n"
                f"• 🍽️ **Gourmet Cloud Kitchen / Restaurant**\n"
                f"• 🌿 **Organic Agri-Tech & Farm Direct**"
            ),
            "intent": "simulation_business_start",
            "action_type": None,
            "quick_replies": [
                {"label": "📱 Tech & AI SaaS", "payload": "Build an AI SaaS startup", "icon": "Cpu"},
                {"label": "🍽️ Gourmet Cloud Kitchen", "payload": "Build a Cloud Kitchen venture", "icon": "Utensils"},
                {"label": "🌿 Organic Agri-Tech", "payload": "Build an Agri-Tech business", "icon": "Leaf"}
            ],
            "structured_data": None
        }

    def handle_travel_planner(self, msg: str, user_name: str, session: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "message": (
                f"✈️ **Virtual Travel Planner for {user_name}:**\n\n"
                f"Where is your dream destination? Tell me the place (e.g. *Goa, Paris, Kyoto, Swiss Alps*) "
                f"and how many days you plan to travel, and I'll craft a customized day-by-day itinerary with food & sights!"
            ),
            "intent": "simulation_travel_start",
            "action_type": None,
            "quick_replies": [
                {"label": "🏖️ 3-Day Beach Trip (Goa)", "payload": "Plan a 3-day trip to Goa", "icon": "Sun"},
                {"label": "🏔️ 5-Day Mountain Retreat", "payload": "Plan a 5-day mountain trip", "icon": "Compass"},
                {"label": "🎌 Kyoto Cultural Tour", "payload": "Plan a 4-day trip to Kyoto", "icon": "MapPin"}
            ],
            "structured_data": None
        }

    def handle_cooking_assistant(self, msg: str, user_name: str) -> Dict[str, Any]:
        return {
            "message": (
                f"👨‍🍳 **Chef's Culinary Masterclass with {user_name}:**\n\n"
                f"I can guide you through cooking signature delicacies step-by-step:\n"
                f"• 🍗 **Dum Biryani Perfection** (layering, saffron infusion, dum seal)\n"
                f"• 🍝 **Creamy Truffle Pasta** (al dente timing, emulsion secrets)\n"
                f"• 🍫 **Molten Chocolate Lava Cake** (foolproof 12-min bake time)\n\n"
                f"Which dish would you like to master today?"
            ),
            "intent": "simulation_cooking_start",
            "action_type": None,
            "quick_replies": [
                {"label": "🍗 Master Biryani", "payload": "Teach me how to cook Royal Biryani", "icon": "Utensils"},
                {"label": "🍫 Master Lava Cake", "payload": "Teach me how to bake Lava Cake", "icon": "Cake"},
                {"label": "🛍️ Order Ready Food", "payload": "I'd rather order food right now", "icon": "ShoppingBag"}
            ],
            "structured_data": None
        }

simulation_handler = SimulationHandler()
