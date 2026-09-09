import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models import Order

class PaymentHandler:
    """
    Handles payment method selection, UPI/Card/Cash simulation, and digital receipt generation.
    """

    def handle_payment(self, msg: str, user_name: str, db: Session, session: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = msg.lower()

        # Check for latest active order
        latest_order = db.query(Order).order_by(Order.id.desc()).first()
        order_amount = latest_order.total_amount if latest_order else 520.00
        order_id = latest_order.id if latest_order else 1

        if any(w in cleaned for w in ["upi", "gpay", "phonepe", "paytm", "qr"]):
            txn_id = "TXN_UPI_" + uuid.uuid4().hex[:8].upper()
            return {
                "message": (
                    f"💳 **UPI Instant Payment for Order #{order_id:04d}**\n\n"
                    f"• **Amount Payable:** **${order_amount:.2f}**\n"
                    f"• **UPI ID:** `gourmethaven@bank`\n"
                    f"• **Transaction Ref:** `{txn_id}`\n"
                    f"• **Status:** ✅ Payment Completed via UPI Verified\n\n"
                    f"Thank you, {user_name}! Your payment has been processed and confirmed to the kitchen!"
                ),
                "intent": "payment_confirmed_upi",
                "action_type": "PAYMENT_RECEIPT",
                "quick_replies": [
                    {"label": f"📦 Track Order #{order_id}", "payload": f"Track order #{order_id}", "icon": "Compass"},
                    {"label": "📅 Book a Table", "payload": "Book a table for 2", "icon": "Calendar"}
                ],
                "structured_data": {
                    "payment": {
                        "order_id": order_id,
                        "amount": order_amount,
                        "method": "UPI",
                        "status": "Paid",
                        "txn_id": txn_id
                    }
                }
            }

        if any(w in cleaned for w in ["card", "credit", "debit"]):
            txn_id = "TXN_CARD_" + uuid.uuid4().hex[:8].upper()
            return {
                "message": (
                    f"💳 **Card Payment Receipt for Order #{order_id:04d}**\n\n"
                    f"• **Total Paid:** **${order_amount:.2f}**\n"
                    f"• **Card:** Visa/Mastercard Ending in •••• 4242\n"
                    f"• **Auth Code:** `{txn_id}`\n"
                    f"• **Status:** ✅ Approved & Settled\n\n"
                    f"Your receipt has been generated, {user_name}!"
                ),
                "intent": "payment_confirmed_card",
                "action_type": "PAYMENT_RECEIPT",
                "quick_replies": [
                    {"label": f"📦 Track Order #{order_id}", "payload": f"Track order #{order_id}", "icon": "Compass"},
                    {"label": "🍽️ View Menu", "payload": "Show me the menu", "icon": "Utensils"}
                ],
                "structured_data": {
                    "payment": {
                        "order_id": order_id,
                        "amount": order_amount,
                        "method": "Card",
                        "status": "Paid",
                        "txn_id": txn_id
                    }
                }
            }

        # Payment options prompt
        return {
            "message": (
                f"💳 **Payment Checkout for Order #{order_id:04d}**\n\n"
                f"**Total Due:** **${order_amount:.2f}**\n\n"
                f"How would you like to settle your bill, {user_name}?\n"
                f"• 📱 **UPI** (Google Pay, PhonePe, Paytm)\n"
                f"• 💳 **Credit / Debit Card**\n"
                f"• 💵 **Cash on Dine-in / Delivery**"
            ),
            "intent": "payment_options",
            "action_type": None,
            "quick_replies": [
                {"label": "📱 Pay with UPI", "payload": "I want to pay with UPI", "icon": "Smartphone"},
                {"label": "💳 Pay with Card", "payload": "I want to pay with Card", "icon": "CreditCard"},
                {"label": "💵 Pay with Cash", "payload": "I will pay with Cash", "icon": "DollarSign"}
            ],
            "structured_data": None
        }

payment_handler = PaymentHandler()
