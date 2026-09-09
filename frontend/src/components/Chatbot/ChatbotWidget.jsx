import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquare,
  X,
  Send,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Maximize2,
  Minimize2,
  RotateCcw,
  Sparkles,
  Utensils,
  Calendar,
  Leaf,
  Star,
  MapPin,
  Clock,
  ShoppingBag,
  Plus,
  CheckCircle2,
  Info,
  Phone,
  Compass,
  ArrowRight,
} from 'lucide-react';
import api from '../../services/api';
import { useCart } from '../../context/CartContext';
import './ChatbotWidget.css';

export default function ChatbotWidget() {
  const {
    isChatOpen,
    setIsChatOpen,
    pendingPrompt,
    setPendingPrompt,
    addToCart,
    showToast,
    userName,
  } = useCart();

  const getDynamicTimeGreeting = (name) => {
    const currentHour = new Date().getHours();
    const displayName = name || 'Friend';

    if (currentHour >= 5 && currentHour < 12) {
      return `🌅 Good Morning, ${displayName}!\nIt's nice to see you. How's your morning going?`;
    } else if (currentHour >= 12 && currentHour < 17) {
      return `☀️ Good Afternoon, ${displayName}!\nHow's your day going so far?`;
    } else if (currentHour >= 17 && currentHour < 21) {
      return `🌆 Good Evening, ${displayName}!\nHow was your day today?`;
    } else {
      return `🌙 Good Night, ${displayName}!\nStill up? 😄 What's on your mind?`;
    }
  };

  const [sessionId] = useState(() => {
    const existing = sessionStorage.getItem('chat_session_id');
    if (existing) return existing;
    const newId = 'session_' + Math.random().toString(36).substring(2, 9);
    sessionStorage.setItem('chat_session_id', newId);
    return newId;
  });

  const [messages, setMessages] = useState(() => [
    {
      id: 'init-msg',
      sender: 'bot',
      text: getDynamicTimeGreeting(userName),
      quickReplies: [
        { label: "😄 I'm good!", payload: "I'm good." },
        { label: "🥱 I'm bored", payload: "I'm bored." },
        { label: "📚 Studying for exam", payload: "I have an exam" },
        { label: "🍽️ I need food", payload: "I need food" },
        { label: "📅 Book a table", payload: "Book a table for 2" },
      ],
      structuredData: null,
      timestamp: new Date(),
    },
  ]);

  // Update greeting text when userName becomes available or changes
  useEffect(() => {
    if (userName) {
      setMessages((prev) => {
        if (prev.length === 1 && prev[0].id === 'init-msg') {
          return [
            {
              ...prev[0],
              text: getDynamicTimeGreeting(userName),
            },
          ];
        }
        return prev;
      });
    }
  }, [userName]);

  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [showTeaser, setShowTeaser] = useState(true);

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const recognitionRef = useRef(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isChatOpen) {
      scrollToBottom();
    }
  }, [messages, isTyping, isChatOpen]);

  // Handle external triggers (e.g. from hero button)
  useEffect(() => {
    if (pendingPrompt && isChatOpen) {
      handleSendMessage(pendingPrompt);
      setPendingPrompt(null);
    }
  }, [pendingPrompt, isChatOpen]);

  // Speech Recognition Setup (Web Speech API)
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputMessage(transcript);
        setIsListening(false);
        // Automatically send after voice capture
        setTimeout(() => {
          handleSendMessage(transcript);
        }, 300);
      };

      recognition.onerror = () => {
        setIsListening(false);
        showToast('Voice recognition failed or microphone denied', 'error');
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      showToast('Speech recognition is not supported in this browser.', 'info');
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
        showToast('🎙️ Listening... Speak now', 'info');
      } catch (e) {
        console.error(e);
      }
    }
  };

  const speakText = (text) => {
    if (!voiceEnabled || !window.speechSynthesis) return;
    try {
      window.speechSynthesis.cancel();
      // Strip markdown asterisks and emojis for speech synthesis
      const cleanText = text.replace(/[*_#`•]/g, '').replace(/[\u{1F300}-\u{1F9FF}]/gu, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn('Text-to-speech error', e);
    }
  };

  const handleSendMessage = async (customText = null) => {
    const textToSend = (customText || inputMessage).trim();
    if (!textToSend || isTyping) return;

    setShowTeaser(false);

    // Add user message
    const userMsg = {
      id: 'msg-' + Date.now(),
      sender: 'user',
      text: textToSend,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await api.sendMessage(sessionId, textToSend, null, userName);

      const botMsg = {
        id: 'msg-' + (Date.now() + 1),
        sender: 'bot',
        text: response.message,
        quickReplies: response.quick_replies || [],
        structuredData: response.structured_data || null,
        actionType: response.action_type || null,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMsg]);
      speakText(response.message);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMsg = {
        id: 'msg-' + (Date.now() + 1),
        sender: 'bot',
        text: "I'm having a little trouble reaching our server right now, but I'll be right back! Please try again in a moment.",
        quickReplies: [{ label: '🔄 Try Again', payload: textToSend }],
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleResetChat = async () => {
    try {
      await api.resetChatSession(sessionId);
      setMessages([
        {
          id: 'reset-' + Date.now(),
          sender: 'bot',
          text: getDynamicTimeGreeting(userName),
          quickReplies: [
            { label: "😄 I'm good!", payload: "I'm good." },
            { label: "🥱 I'm bored", payload: "I'm bored." },
            { label: "📚 Studying for exam", payload: "I have an exam" },
            { label: "🍽️ I need food", payload: "I need food" },
            { label: "📅 Book a table", payload: "Book a table for 2" },
          ],
          structuredData: null,
          timestamp: new Date(),
        },
      ]);
      showToast('Chat session reset', 'info');
    } catch (e) {
      console.error(e);
    }
  };

  const renderIcon = (name) => {
    switch (name) {
      case 'Utensils': return <Utensils size={14} />;
      case 'Calendar': return <Calendar size={14} />;
      case 'Leaf': return <Leaf size={14} />;
      case 'Star': return <Star size={14} />;
      case 'MapPin': return <MapPin size={14} />;
      case 'Clock': return <Clock size={14} />;
      case 'ShoppingBag': return <ShoppingBag size={14} />;
      case 'Phone': return <Phone size={14} />;
      case 'Compass': return <Compass size={14} />;
      case 'Info': return <Info size={14} />;
      default: return <Sparkles size={14} />;
    }
  };

  return (
    <>
      {/* Floating Trigger Button */}
      {!isChatOpen && (
        <div className="chatbot-trigger-container">
          {showTeaser && (
            <div className="chatbot-teaser" onClick={() => setIsChatOpen(true)}>
              <Sparkles size={16} color="#f59e0b" />
              <span>{userName ? `Hi ${userName}! How can I help you today?` : 'Ask our AI Assistant for anything you need!'}</span>
              <X
                size={14}
                style={{ marginLeft: 'auto', opacity: 0.6 }}
                onClick={(e) => {
                  e.stopPropagation();
                  setShowTeaser(false);
                }}
              />
            </div>
          )}
          <button
            className="chatbot-trigger-btn"
            onClick={() => setIsChatOpen(true)}
            aria-label="Open AI Assistant"
          >
            <div className="pulse-ring" />
            <MessageSquare size={28} />
          </button>
        </div>
      )}

      {/* Main Chatbot Floating Window */}
      {isChatOpen && (
        <div className={`chatbot-window ${isExpanded ? 'expanded' : ''}`}>
          {/* Header */}
          <div className="chatbot-header">
            <div className="chatbot-header-main">
              <div className="chatbot-header-top-row">
                <div className="header-brand-title">
                  <span className="header-food-icon" role="img" aria-label="assistant">🤖</span>
                  <span className="header-title-text">Restaurant AI Assistant</span>
                  <span className="header-online-pill">
                    <span className="status-dot" />
                    <span>Online</span>
                  </span>
                </div>

                <div className="chatbot-header-actions">
                  <button
                    className={`header-action-btn ${voiceEnabled ? 'active' : ''}`}
                    onClick={() => setVoiceEnabled(!voiceEnabled)}
                    title={voiceEnabled ? 'Disable Voice Audio' : 'Enable Voice Audio'}
                    aria-label="Toggle voice output"
                  >
                    {voiceEnabled ? <Volume2 size={15} /> : <VolumeX size={15} />}
                  </button>
                  <button
                    className="header-action-btn"
                    onClick={handleResetChat}
                    title="Reset Conversation"
                    aria-label="Reset conversation"
                  >
                    <RotateCcw size={14} />
                  </button>
                  <button
                    className="header-action-btn"
                    onClick={() => setIsExpanded(!isExpanded)}
                    title={isExpanded ? 'Restore Size' : 'Expand Window'}
                    aria-label="Toggle window size"
                  >
                    {isExpanded ? <Minimize2 size={14} /> : <Maximize2 size={14} />}
                  </button>
                  <button
                    className="header-close-btn"
                    onClick={() => setIsChatOpen(false)}
                    title="Close Assistant"
                    aria-label="Close chatbot"
                  >
                    <X size={16} />
                  </button>
                </div>
              </div>

              <div className="header-tagline-row">
                <span className="header-tagline-highlight">Ask me anything. I'm here to help! ✨</span>
              </div>

              <p className="header-friendly-sub">
                I'm here to help you with food orders, table bookings & more.
              </p>
            </div>
          </div>

          {/* Messages Stream */}
          <div className="chatbot-messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message-row ${msg.sender}`}>
                {msg.sender === 'bot' && (
                  <div className="bot-msg-avatar">
                    <Sparkles size={16} />
                  </div>
                )}
                <div className="message-bubble">
                  <div className="bot-text-content">{msg.text}</div>

                  {/* Render Menu Items Cards inside Chat */}
                  {msg.structuredData?.menu_items && (
                    <div className="chat-structured-cards">
                      <div className="chat-menu-grid">
                        {msg.structuredData.menu_items.map((item) => (
                          <div key={item.id} className="chat-menu-item-card">
                            {item.image && (
                              <img
                                src={item.image}
                                alt={item.name}
                                className="chat-menu-img"
                                loading="lazy"
                              />
                            )}
                            <div className="chat-menu-info">
                              <div>
                                <h4>{item.name}</h4>
                                <span className={item.is_vegetarian ? 'badge badge-veg' : 'badge badge-nonveg'}>
                                  {item.is_vegetarian ? 'Veg' : 'Non-Veg'}
                                </span>
                              </div>
                              <div className="chat-menu-price-row">
                                <span className="chat-menu-price">${item.price.toFixed(2)}</span>
                                <button
                                  className="chat-add-btn"
                                  onClick={() => addToCart(item, 1)}
                                  title="Add to order"
                                >
                                  <Plus size={13} /> Add
                                </button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Render Booking Pass Card */}
                  {msg.structuredData?.booking && (
                    <div className="chat-structured-cards">
                      <div className="chat-booking-card">
                        <div className="booking-card-header">
                          <span style={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 6 }}>
                            <CheckCircle2 size={16} color="#4ade80" /> Table Reserved
                          </span>
                          <span className="booking-ref-badge">
                            #{msg.structuredData.booking.booking_id.toString().padStart(4, '0')}
                          </span>
                        </div>
                        <div className="booking-details-grid">
                          <div className="booking-detail-item">
                            <span className="label">Guest</span>
                            <span className="val">{msg.structuredData.booking.customer_name}</span>
                          </div>
                          <div className="booking-detail-item">
                            <span className="label">Party</span>
                            <span className="val">{msg.structuredData.booking.guests} Guests</span>
                          </div>
                          <div className="booking-detail-item">
                            <span className="label">Date & Time</span>
                            <span className="val">{msg.structuredData.booking.date} @ {msg.structuredData.booking.time}</span>
                          </div>
                          <div className="booking-detail-item">
                            <span className="label">Seating Area</span>
                            <span className="val">{msg.structuredData.booking.table_location}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Render Order Summary Card */}
                  {msg.structuredData?.order && (
                    <div className="chat-structured-cards">
                      <div className="chat-order-card">
                        <div className="chat-order-header">
                          <span>Order #{msg.structuredData.order.id.toString().padStart(4, '0')}</span>
                          <span>${msg.structuredData.order.total_amount.toFixed(2)}</span>
                        </div>
                        <div className="chat-order-item-list">
                          {msg.structuredData.order.items?.map((it, idx) => (
                            <div key={idx} style={{ display: 'flex', justifyContent: 'space-between' }}>
                              <span>{it.quantity}x {it.name}</span>
                              <span>${(it.price * it.quantity).toFixed(2)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Quick Reply Chips */}
                  {msg.quickReplies && msg.quickReplies.length > 0 && (
                    <div className="quick-replies-container">
                      {msg.quickReplies.map((qr, idx) => (
                        <button
                          key={idx}
                          className="quick-reply-btn"
                          onClick={() => handleSendMessage(qr.payload)}
                        >
                          {qr.icon && renderIcon(qr.icon)}
                          <span>{qr.label}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="message-row bot">
                <div className="bot-msg-avatar">
                  <Sparkles size={16} />
                </div>
                <div className="typing-indicator">
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Footer Input Area */}
          <div className="chatbot-footer">
            <div className="chat-input-wrapper">
              <textarea
                ref={textareaRef}
                rows={1}
                className="chat-textarea"
                placeholder={isListening ? "Listening... speak now" : "Ask for food specials, table bookings, or orders..."}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage();
                  }
                }}
              />
              <div className="chat-input-actions">
                <button
                  className={`chat-mic-btn ${isListening ? 'listening' : ''}`}
                  onClick={toggleListening}
                  title="Voice Input (Speech-to-Text)"
                >
                  {isListening ? <MicOff size={18} /> : <Mic size={18} />}
                </button>
                <button
                  className="chat-send-btn"
                  onClick={() => handleSendMessage()}
                  disabled={!inputMessage.trim() || isTyping}
                  title="Send Message"
                >
                  <Send size={16} />
                </button>
              </div>
            </div>
            <div className="chat-footer-hint">
              <span>Press <strong>Enter</strong> to send • Voice input supported 🎙️</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
