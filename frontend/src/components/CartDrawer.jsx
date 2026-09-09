import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { X, Trash2, Plus, Minus, ShoppingBag, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useCart } from '../context/CartContext';
import api from '../services/api';

export default function CartDrawer() {
  const {
    cart,
    isCartOpen,
    setIsCartOpen,
    updateQuantity,
    removeFromCart,
    clearCart,
    cartTotal,
    showToast,
    openChatWithPrompt,
  } = useCart();

  const history = useHistory();
  const [customerName, setCustomerName] = useState('Alex Morgan');
  const [customerPhone, setCustomerPhone] = useState('+1 555-0199');
  const [orderType, setOrderType] = useState('Dine-in');
  const [tableNumber, setTableNumber] = useState('3');
  const [paymentMethod, setPaymentMethod] = useState('Card');
  const [specialInstructions, setSpecialInstructions] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isCartOpen) return null;

  const tax = cartTotal * 0.08;
  const grandTotal = cartTotal + tax;

  const handleCheckout = async (e) => {
    e.preventDefault();
    if (cart.length === 0) {
      showToast('Your cart is empty', 'info');
      return;
    }

    setIsSubmitting(true);
    try {
      const orderPayload = {
        customer_name: customerName,
        customer_phone: customerPhone,
        order_type: orderType,
        table_number: orderType === 'Dine-in' ? parseInt(tableNumber) || null : null,
        payment_method: paymentMethod,
        special_instructions: specialInstructions,
        items: cart.map((item) => ({
          menu_item_id: item.id,
          quantity: item.quantity,
        })),
      };

      const response = await api.createOrder(orderPayload);
      clearCart();
      setIsCartOpen(false);
      showToast(`Order #${response.id} placed successfully! 🎉`, 'success');
      history.push(`/tracking?order_id=${response.id}`);
    } catch (error) {
      console.error('Checkout error:', error);
      showToast('Failed to place order. Please try again.', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="cart-backdrop" onClick={() => setIsCartOpen(false)}>
      <div className="cart-drawer" onClick={(e) => e.stopPropagation()}>
        <div className="cart-header">
          <div className="cart-title-row">
            <ShoppingBag size={22} color="#ea580c" />
            <h3>Your Order Cart</h3>
            <span className="cart-count-pill">{cart.length} items</span>
          </div>
          <button className="cart-close-btn" onClick={() => setIsCartOpen(false)}>
            <X size={20} />
          </button>
        </div>

        {cart.length === 0 ? (
          <div className="cart-empty-state">
            <div className="cart-empty-icon">🍽️</div>
            <h4>Your cart is currently empty</h4>
            <p>Explore our handcrafted seasonal dishes or ask the AI assistant for instant recommendations!</p>
            <button
              className="btn btn-primary"
              onClick={() => {
                setIsCartOpen(false);
                history.push('/menu');
              }}
            >
              Browse Menu
            </button>
          </div>
        ) : (
          <form className="cart-content-form" onSubmit={handleCheckout}>
            {/* Items List */}
            <div className="cart-items-list">
              {cart.map((item) => (
                <div key={item.id} className="cart-item-card">
                  {item.image && (
                    <img src={item.image} alt={item.name} className="cart-item-thumb" />
                  )}
                  <div className="cart-item-info">
                    <div className="cart-item-header">
                      <h5>{item.name}</h5>
                      <button
                        type="button"
                        className="cart-item-del-btn"
                        onClick={() => removeFromCart(item.id)}
                        title="Remove item"
                      >
                        <Trash2 size={15} />
                      </button>
                    </div>
                    <span className="cart-item-single-price">${item.price.toFixed(2)} ea</span>
                    <div className="cart-item-bottom">
                      <div className="qty-controls">
                        <button
                          type="button"
                          className="qty-btn"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        >
                          <Minus size={13} />
                        </button>
                        <span className="qty-num">{item.quantity}</span>
                        <button
                          type="button"
                          className="qty-btn"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        >
                          <Plus size={13} />
                        </button>
                      </div>
                      <span className="cart-item-subtotal">
                        ${(item.price * item.quantity).toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Order Settings */}
            <div className="cart-options-section">
              <h4>Order Preferences</h4>
              <div className="cart-field-row">
                <div className="cart-field">
                  <label>Order Mode</label>
                  <select value={orderType} onChange={(e) => setOrderType(e.target.value)}>
                    <option value="Dine-in">Dine-in</option>
                    <option value="Takeaway">Takeaway (Pickup)</option>
                    <option value="Delivery">Room / Express Delivery</option>
                  </select>
                </div>
                {orderType === 'Dine-in' && (
                  <div className="cart-field">
                    <label>Table #</label>
                    <input
                      type="number"
                      value={tableNumber}
                      onChange={(e) => setTableNumber(e.target.value)}
                      placeholder="e.g. 3"
                    />
                  </div>
                )}
              </div>

              <div className="cart-field-row">
                <div className="cart-field">
                  <label>Your Name</label>
                  <input
                    type="text"
                    required
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                  />
                </div>
                <div className="cart-field">
                  <label>Phone Number</label>
                  <input
                    type="text"
                    required
                    value={customerPhone}
                    onChange={(e) => setCustomerPhone(e.target.value)}
                  />
                </div>
              </div>

              <div className="cart-field">
                <label>Payment Method</label>
                <div className="payment-options-grid">
                  {['Card', 'UPI', 'Cash'].map((pm) => (
                    <button
                      key={pm}
                      type="button"
                      className={`pm-choice-btn ${paymentMethod === pm ? 'active' : ''}`}
                      onClick={() => setPaymentMethod(pm)}
                    >
                      {pm}
                    </button>
                  ))}
                </div>
              </div>

              <div className="cart-field">
                <label>Special Kitchen Instructions (Optional)</label>
                <input
                  type="text"
                  placeholder="e.g. Extra spicy, sauce on the side..."
                  value={specialInstructions}
                  onChange={(e) => setSpecialInstructions(e.target.value)}
                />
              </div>
            </div>

            {/* Bill Summary */}
            <div className="cart-bill-summary">
              <div className="bill-row">
                <span>Subtotal</span>
                <span>${cartTotal.toFixed(2)}</span>
              </div>
              <div className="bill-row">
                <span>Tax & Service (8%)</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <div className="bill-row bill-total">
                <span>Total Amount</span>
                <span>${grandTotal.toFixed(2)}</span>
              </div>
            </div>

            {/* Place Order CTA */}
            <button
              type="submit"
              className="btn btn-primary cart-checkout-btn"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                'Processing Order...'
              ) : (
                <>
                  <span>Place Order • ${grandTotal.toFixed(2)}</span>
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
