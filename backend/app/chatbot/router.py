import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatMessageIn, ChatMessageOut, ChatSuggestion
from app.chatbot.engine import chatbot_engine
from typing import List

router = APIRouter()

@router.post("/message", response_model=ChatMessageOut)
def chat_message(payload: ChatMessageIn, db: Session = Depends(get_db)):
    """
    Process incoming user message through the restaurant AI chatbot engine.
    Supports multi-turn intent slots, menu recommendations, table reservations, and orders.
    """
    try:
        result = chatbot_engine.process_message(
            session_id=payload.session_id,
            message=payload.message,
            db=db,
            user_id=payload.user_id,
            user_name=payload.user_name
        )
        return ChatMessageOut(
            session_id=payload.session_id,
            message=result["message"],
            intent=result.get("intent", "general"),
            action_type=result.get("action_type"),
            quick_replies=result.get("quick_replies", []),
            structured_data=result.get("structured_data"),
            timestamp=datetime.datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chatbot processing: {str(e)}")

@router.get("/suggestions", response_model=List[ChatSuggestion])
def get_suggestions():
    """Returns rich prompt starter suggestions for the chatbot UI."""
    return [
        {
            "title": "Bored? Let's Fix It",
            "prompt": "I'm bored. What should we do?",
            "category": "Companion",
            "icon": "Smile"
        },
        {
            "title": "Exam Prep Motivation",
            "prompt": "I have an exam coming up",
            "category": "Study",
            "icon": "BookOpen"
        },
        {
            "title": "Need a Mood Uplift",
            "prompt": "Today was terrible.",
            "category": "Empathy",
            "icon": "Heart"
        },
        {
            "title": "Gamer Chat",
            "prompt": "I play games like Valorant",
            "category": "Gaming",
            "icon": "Gamepad2"
        },
        {
            "title": "Curious Mind",
            "prompt": "Explain democracy to me",
            "category": "Learn",
            "icon": "Sparkles"
        },
        {
            "title": "Hungry? Order Food",
            "prompt": "I need food. Show me the best dishes",
            "category": "Dining",
            "icon": "Utensils"
        }
    ]

@router.post("/reset/{session_id}")
def reset_session(session_id: str):
    """Resets chatbot conversational session memory."""
    chatbot_engine.reset_session(session_id)
    return {"message": "Session reset successfully", "session_id": session_id}
