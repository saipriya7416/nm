import React, { useState, useEffect } from 'react';
import {
  Calendar as CalendarIcon,
  Clock,
  Users,
  MapPin,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import { useCart } from '../context/CartContext';
import api from '../services/api';

export default function BookingPage() {
  const { openChatWithPrompt, showToast } = useCart();
  const [tables, setTables] = useState([]);
  const [loadingTables, setLoadingTables] = useState(true);

  // Form State
  const [name, setName] = useState('Alex Morgan');
  const [phone, setPhone] = useState('+1 555-0199');
  const [email, setEmail] = useState('alex@example.com');
  const [guests, setGuests] = useState(2);
  const [date, setDate] = useState(() => {
    const today = new Date();
    today.setDate(today.getDate() + 1);
    return today.toISOString().split('T')[0];
  });
  const [time, setTime] = useState('19:30');
  const [tablePref, setTablePref] = useState('Window View');
  const [specialRequests, setSpecialRequests] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [confirmedBooking, setConfirmedBooking] = useState(null);

  useEffect(() => {
    api.getTables().then((res) => {
      setTables(res);
      setLoadingTables(false);
    }).catch((e) => {
      console.error(e);
      setLoadingTables(false);
    });
  }, []);

  const handleReserve = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const payload = {
        customer_name: name,
        customer_phone: phone,
        customer_email: email,
        date: date,
        time: time,
        number_of_people: parseInt(guests),
        table_preference: tablePref,
        special_requests: specialRequests,
      };

      const res = await api.createBooking(payload);
      setConfirmedBooking(res);
      showToast('Table reserved successfully! 🎉', 'success');
    } catch (err) {
      console.error(err);
      showToast('Reservation could not be completed. Please try again.', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="booking-page">
      {/* Banner */}
      <section className="page-hero-banner">
        <div className="container">
          <div className="page-hero-content">
            <span className="section-tag">Intimate & Group Dining</span>
            <h1>Reserve Your Table</h1>
            <p>
              Experience fine dining in our architecturally designed dining rooms, garden patio, or skyline balcony. Book below or simply ask our AI concierge.
            </p>
            <div style={{ marginTop: '16px' }}>
              <button
                className="btn btn-secondary"
                onClick={() => openChatWithPrompt('I would like to book a table for 4 guests tomorrow at 7:30 PM')}
              >
                <Sparkles size={16} color="#f59e0b" />
                <span>Or Book Instantly with AI Concierge</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Main Reservation Content */}
      <section className="booking-content-section">
        <div className="container">
          <div className="booking-layout-grid">
            {/* Left Column: Interactive Table Visualizer */}
            <div className="table-visualizer-card">
              <div className="visualizer-header">
                <h3>Live Dining Room Ambiances</h3>
                <span className="live-status-tag">
                  <span className="status-dot" /> Live Availability
                </span>
              </div>
              <p className="visualizer-sub">
                Explore seating zones and select your preference.
              </p>

              <div className="tables-grid">
                {loadingTables ? (
                  <p>Loading table layouts...</p>
                ) : (
                  tables.map((t) => (
                    <div
                      key={t.id}
                      className={`table-node ${tablePref.toLowerCase().includes(t.location.toLowerCase()) ? 'selected' : ''}`}
                      onClick={() => setTablePref(t.location)}
                    >
                      <div className="table-node-top">
                        <span className="table-id-tag">Table #{t.id}</span>
                        <span className="table-status-tag">{t.status}</span>
                      </div>
                      <div className="table-loc">{t.location}</div>
                      <div className="table-cap">
                        <Users size={14} /> Capacity: {t.capacity} Guests
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div className="seating-features-list">
                <div className="seating-feat">
                  <ShieldCheck size={16} color="#4ade80" />
                  <span>Complimentary Valet Parking included with all reservations</span>
                </div>
                <div className="seating-feat">
                  <Clock size={16} color="#4ade80" />
                  <span>15-Minute grace period held for your party</span>
                </div>
              </div>
            </div>

            {/* Right Column: Reservation Form */}
            <div className="booking-form-card">
              {confirmedBooking ? (
                <div className="booking-success-view">
                  <div className="success-icon-box">
                    <CheckCircle2 size={48} color="#22c55e" />
                  </div>
                  <h2>Reservation Confirmed!</h2>
                  <p>
                    Thank you, <strong>{confirmedBooking.customer_name}</strong>! We look forward to hosting your party of{' '}
                    <strong>{confirmedBooking.number_of_people} guests</strong>.
                  </p>

                  <div className="booking-ticket">
                    <div className="ticket-row">
                      <span className="ticket-label">Booking Reference</span>
                      <span className="ticket-val code">#{confirmedBooking.id.toString().padStart(4, '0')}</span>
                    </div>
                    <div className="ticket-row">
                      <span className="ticket-label">Date & Time</span>
                      <span className="ticket-val">{confirmedBooking.date} at {confirmedBooking.time}</span>
                    </div>
                    <div className="ticket-row">
                      <span className="ticket-label">Seating Preference</span>
                      <span className="ticket-val">{confirmedBooking.table_preference}</span>
                    </div>
                    <div className="ticket-row">
                      <span className="ticket-label">Status</span>
                      <span className="ticket-val status-confirmed">✅ Confirmed</span>
                    </div>
                  </div>

                  <div className="booking-success-actions">
                    <button
                      className="btn btn-secondary"
                      onClick={() => setConfirmedBooking(null)}
                    >
                      Make Another Booking
                    </button>
                    <button
                      className="btn btn-primary"
                      onClick={() => openChatWithPrompt(`Tell me more about menu options for my reservation #${confirmedBooking.id}`)}
                    >
                      <Sparkles size={16} />
                      <span>Ask AI for Menu Recommendations</span>
                    </button>
                  </div>
                </div>
              ) : (
                <form onSubmit={handleReserve}>
                  <div className="form-header">
                    <h3>Table Reservation Details</h3>
                    <p>Instant confirmation with zero booking fees</p>
                  </div>

                  <div className="form-grid">
                    <div className="form-group">
                      <label><CalendarIcon size={14} /> Reservation Date</label>
                      <input
                        type="date"
                        required
                        value={date}
                        min={new Date().toISOString().split('T')[0]}
                        onChange={(e) => setDate(e.target.value)}
                      />
                    </div>

                    <div className="form-group">
                      <label><Clock size={14} /> Time Slot</label>
                      <select value={time} onChange={(e) => setTime(e.target.value)}>
                        <option value="12:00 PM">12:00 PM (Lunch)</option>
                        <option value="1:00 PM">1:00 PM (Lunch)</option>
                        <option value="1:30 PM">1:30 PM (Lunch)</option>
                        <option value="6:00 PM">6:00 PM (Dinner)</option>
                        <option value="7:00 PM">7:00 PM (Dinner)</option>
                        <option value="7:30 PM">7:30 PM (Prime Dinner)</option>
                        <option value="8:00 PM">8:00 PM (Prime Dinner)</option>
                        <option value="8:30 PM">8:30 PM (Dinner)</option>
                        <option value="9:00 PM">9:00 PM (Late Dinner)</option>
                      </select>
                    </div>
                  </div>

                  <div className="form-grid">
                    <div className="form-group">
                      <label><Users size={14} /> Number of Guests</label>
                      <select value={guests} onChange={(e) => setGuests(e.target.value)}>
                        <option value="1">1 Guest (Solo)</option>
                        <option value="2">2 Guests (Couple)</option>
                        <option value="3">3 Guests</option>
                        <option value="4">4 Guests (Family/Small Group)</option>
                        <option value="5">5 Guests</option>
                        <option value="6">6 Guests (Party)</option>
                        <option value="8">8 Guests (VIP Lounge)</option>
                        <option value="10">10+ Guests (Large Celebration)</option>
                      </select>
                    </div>

                    <div className="form-group">
                      <label><MapPin size={14} /> Seating Ambiance</label>
                      <select value={tablePref} onChange={(e) => setTablePref(e.target.value)}>
                        <option value="Window View">Window View</option>
                        <option value="Garden Patio">Garden Patio (Outdoor)</option>
                        <option value="Skyline Balcony">Skyline Balcony</option>
                        <option value="Private VIP Lounge">Private VIP Lounge</option>
                        <option value="Cozy Corner">Cozy Corner</option>
                        <option value="Main Dining Hall">Main Dining Hall</option>
                      </select>
                    </div>
                  </div>

                  <div className="form-grid">
                    <div className="form-group">
                      <label>Full Name</label>
                      <input
                        type="text"
                        required
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label>Phone Number</label>
                      <input
                        type="text"
                        required
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="form-group">
                    <label>Email Address (for confirmation pass)</label>
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>

                  <div className="form-group">
                    <label>Special Requests / Celebrations (Optional)</label>
                    <input
                      type="text"
                      placeholder="e.g. Birthday candle, quiet table for meeting, high chair..."
                      value={specialRequests}
                      onChange={(e) => setSpecialRequests(e.target.value)}
                    />
                  </div>

                  <button
                    type="submit"
                    className="btn btn-primary booking-submit-btn"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Confirming Reservation...' : 'Confirm Table Reservation'}
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
