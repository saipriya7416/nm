"""
Semantic Memory and RAG Layer
Provides vector retrieval and episodic memory for user preferences and context facts.
"""
from typing import List, Dict, Any, Optional

class SemanticMemoryStore:
    """
    Lightweight vector-like retrieval for conversation memory and RAG context.
    Embeds preferences, restaurant knowledge, and factual snippets.
    """

    def __init__(self):
        # In-memory document collection for RAG
        self.documents = [
            {
                "id": "doc_restaurant_profile",
                "category": "restaurant",
                "content": "Gourmet Haven is a premium dining destination with chef specials including Royal Chicken Biryani, Truffle Fries, Lava Cake, and fresh mocktails.",
                "keywords": ["restaurant", "food", "biryani", "menu", "dishes", "truffle", "dessert"]
            },
            {
                "id": "doc_booking_rules",
                "category": "booking",
                "content": "Table reservations are available daily for Lunch (12-3 PM) and Dinner (6:30-10:30 PM). Seating zones: Main Hall, Window View, Garden Patio, VIP Balcony.",
                "keywords": ["book", "table", "reservation", "seats", "party", "timing"]
            },
            {
                "id": "doc_cricket_facts",
                "category": "sports",
                "content": "Cricket updates cover Team India international matches, IPL tournament schedules, player records for Virat Kohli, Rohit Sharma, and live scores.",
                "keywords": ["cricket", "ipl", "virat", "match", "score", "india"]
            }
        ]
        self.user_memories: Dict[str, List[str]] = {}

    def add_user_memory(self, session_id: str, memory_fact: str):
        """Stores a relevant user preference or fact."""
        if session_id not in self.user_memories:
            self.user_memories[session_id] = []
        if memory_fact not in self.user_memories[session_id]:
            self.user_memories[session_id].append(memory_fact)

    def retrieve_context(self, query: str, session_id: Optional[str] = None, top_k: int = 2) -> Dict[str, Any]:
        """
        Retrieves relevant RAG documents and user memory facts matching query.
        """
        words = set(query.lower().split())
        scored_docs = []

        for doc in self.documents:
            match_score = len(words.intersection(set(doc["keywords"])))
            if match_score > 0:
                scored_docs.append((match_score, doc["content"]))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        retrieved_texts = [d[1] for d in scored_docs[:top_k]]

        user_facts = []
        if session_id and session_id in self.user_memories:
            user_facts = self.user_memories[session_id][-3:]

        return {
            "rag_snippets": retrieved_texts,
            "user_preferences": user_facts
        }

rag_memory = SemanticMemoryStore()