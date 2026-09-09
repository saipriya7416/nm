import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Compass,
  Search,
  CheckCircle2,
  Clock,
  ChefHat,
  Utensils,
  Sparkles,
  AlertCircle,
  ShoppingBag,
  Calendar,
} from 'lucide-react';
import { useCart } from '../context/CartContext';
import api from '../services/api';

export default function OrderTrackingPage() {
  const { openChatWithPrompt, showToast } = useCart();
  const location = useLocation();

  const [searchId, setSearchId] = useState('');
  const [activeTab, setActiveTab] = useState('order'); // 'order' or 'booking'
  const [orderData, setOrderData] = useState(null);
  const [bookingData, setBookingData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check URL search query for auto-lookup (e.g. ?order_id=1)
    const params = new URLSearchParams(location.search);
    const orderIdParam = params.get('order_id');
    const bookingIdParam = params.get('booking_id');

    if (orderIdParam) {
      setSearchId(orderIdParam);
      setActiveTab('order');
      handleLookup(orderIdParam, 'order');
    } else if (bookingIdParam) {
      setSearchId(bookingIdParam);
      setActiveTab('booking');
      handleLookup(bookingIdParam, 'booking');
    } else {
      // Default to lookup order #1 if available
      handleLookup('1', 'order');
    }
  }, [location.search]);

  const handleLookup = async (idToLook = null, tabToUse = null) => {
    const queryId = idToLook || searchId;
    const tab = tabToUse || activeTab;

    if (!queryId) return;

    setLoading(true);
    setError(null);

    try {
      if (tab === 'order') {
        const res = await api.getOrder(parseInt(queryId));
        setOrderData(res);
        setBookingData(null);
      } else {
        const res = await api.getBooking(parseInt(queryId));
        setBookingData(res);
        setOrderData(null);
      }
    } catch (err) {
      console.error(err);
      setError(
        tab === 'order'
          ? `Order #${queryId} not found. Please verify your reference number.`
          : `Booking #${queryId} not found. Please verify your reservation ID.`
      );
      setOrderData(null);
      setBookingData(null);
    } finally {
      setLoading(false);
    }
  };

  const getStepIndex = (status) => {
    const steps = ['Order Placed', 'Confirmed', 'Preparing', 'Ready', 'Served', 'Completed'];
    const idx = steps.indexOf(status);
    return idx === -1 ? 0 : idx;
  };

  const currentStep = orderData ? getStepIndex(orderData.status) : 0;

  return (
    <div className="tracking-page">
      <section className="page-hero-banner">
        <div className="container">
          <div className="page-hero-content">
            <span className="section-tag">Real-Time Status</span>
            <h1>Live Order & Booking Tracker</h1>
            <p>
              Check the live preparation status of your culinary orders or view your upcoming dining reservations.
            </p>
          </div>
        </div>
      </section>

      <section className="tracking-search-section">
        <div className="container">
          {/* Tab Switcher */}
          <div className="tracking-tab-switch">
            <button
              className={`tracking-tab-btn ${activeTab === 'order' ? 'active' : ''}`}
              onClick={() => {
                setActiveTab('order');
                setOrderData(null);
                setBookingData(null);
              }}
            >
              <ShoppingBag size={16} />
              <span>Track Food Order</span>
            </button>
            <button
              className={`tracking-tab-btn ${activeTab === 'booking' ? 'active' : ''}`}
              onClick={() => {
                setActiveTab('booking');
                setOrderData(null);
                setBookingData(null);
              }}
            >
              <Calendar size={16} />
              <span>Check Table Booking</span>
            </button>
          </div>

          {/* Search Box */}
          <div className="tracking-search-bar">
            <div className="tracking-input-wrapper">
              <Search size={18} color="#a8a29e" />
              <input
                type="number"
                placeholder={activeTab === 'order' ? 'Enter Order Reference (e.g. 1)' : 'Enter Booking Reference (e.g. 1)'}
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleLookup();
                }}
              />
            </div>
            <button
              className="btn btn-primary"
              onClick={() => handleLookup()}
              disabled={loading || !searchId}
            >
              {loading ? 'Searching...' : 'Track Status'}
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => openChatWithPrompt(`Where is my ${activeTab} #${searchId || 1}?`)}
            >
              <Sparkles size={16} color="#f59e0b" />
              <span>Ask AI Status</span>
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="tracking-error-box">
              <AlertCircle size={20} color="#f87171" />
              <span>{error}</span>
            </div>
          )}

          {/* Order Details Display */}
          {orderData && (
            <div className="tracking-result-card">
              <div className="tracking-card-header">
                <div>
                  <span className="tracking-tag">Order Reference</span>
                  <h2>Order #{orderData.id.toString().padStart(4, '0')}</h2>
                  <span className="order-customer-name">Guest: {orderData.customer_name}</span>
                </div>
                <div className="order-header-right">
                  <span className="order-total-badge">${orderData.total_amount.toFixed(2)}</span>
                  <span className="order-type-badge">{orderData.order_type}</span>
                </div>
              </div>

              {/* Progress Timeline Bar */}
              <div className="progress-timeline">
                {[
                  { title: 'Order Placed', desc: 'Received by kitchen', icon: Clock },
                  { title: 'Preparing', desc: 'Chef crafting dishes', icon: ChefHat },
                  { title: 'Ready', desc: 'Plated & garnished', icon: CheckCircle2 },
                  { title: 'Served', desc: 'Enjoy your meal', icon: Utensils },
                ].map((step, idx) => {
                  const isDone = currentStep >= idx;
                  const isCurrent = currentStep === idx;
                  const Icon = step.icon;

                  return (
                    <div
                      key={idx}
                      className={`timeline-step ${isDone ? 'done' : ''} ${isCurrent ? 'current' : ''}`}
                    >
                      <div className="step-circle">
                        <Icon size={18} />
                      </div>
                      <div className="step-info">
                        <span className="step-title">{step.title}</span>
                        <span className="step-desc">{step.desc}</span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Items Bill */}
              <div className="order-details-grid">
                <div className="order-items-box">
                  <h4>Ordered Dishes</h4>
                  <div className="order-items-table">
                    {orderData.items?.map((it) => (
                      <div key={it.id} className="order-item-row">
                        <span className="item-name">
                          <strong>{it.quantity}x</strong> {it.name}
                        </span>
                        <span className="item-price">${(it.price * it.quantity).toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="order-meta-box">
                  <h4>Order Summary</h4>
                  <div className="meta-line">
                    <span>Payment Status:</span>
                    <strong style={{ color: '#4ade80' }}>{orderData.payment_status} ({orderData.payment_method})</strong>
                  </div>
                  <div className="meta-line">
                    <span>Dining Mode:</span>
                    <strong>{orderData.order_type} {orderData.table_number ? `(Table #${orderData.table_number})` : ''}</strong>
                  </div>
                  {orderData.special_instructions && (
                    <div className="meta-line">
                      <span>Kitchen Notes:</span>
                      <em>"{orderData.special_instructions}"</em>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Booking Details Display */}
          {bookingData && (
            <div className="tracking-result-card">
              <div className="tracking-card-header">
                <div>
                  <span className="tracking-tag">Table Reservation Pass</span>
                  <h2>Booking #{bookingData.id.toString().padStart(4, '0')}</h2>
                  <span className="order-customer-name">Guest: {bookingData.customer_name}</span>
                </div>
                <div className="order-header-right">
                  <span className="badge badge-gold">✅ {bookingData.status}</span>
                </div>
              </div>

              <div className="booking-pass-grid">
                <div className="booking-pass-item">
                  <span className="pass-label">Date & Time</span>
                  <span className="pass-val">{bookingData.date} at {bookingData.time}</span>
                </div>
                <div className="booking-pass-item">
                  <span className="pass-label">Party Size</span>
                  <span className="pass-val">{bookingData.number_of_people} Guests</span>
                </div>
                <div className="booking-pass-item">
                  <span className="pass-label">Seating Preference</span>
                  <span className="pass-val">{bookingData.table_preference || 'Main Dining Hall'}</span>
                </div>
                <div className="booking-pass-item">
                  <span className="pass-label">Special Requests</span>
                  <span className="pass-val">{bookingData.special_requests || 'Standard Table Setting'}</span>
                </div>
              </div>

              <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
                <button
                  className="btn btn-secondary"
                  onClick={() => openChatWithPrompt(`Show me the menu for booking #${bookingData.id}`)}
                >
                  <Sparkles size={16} color="#f59e0b" />
                  <span>Pre-Order Food with AI</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
