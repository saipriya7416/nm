import React, { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext();

export function CartProvider({ children }) {
  const [userName, setUserName] = useState(() => {
    try {
      return localStorage.getItem('restaurant_user_name') || '';
    } catch {
      return '';
    }
  });

  const [isNameModalOpen, setIsNameModalOpen] = useState(() => {
    try {
      return !localStorage.getItem('restaurant_user_name');
    } catch {
      return true;
    }
  });

  const [cart, setCart] = useState(() => {
    try {
      const saved = localStorage.getItem('gourmet_cart');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [pendingPrompt, setPendingPrompt] = useState(null);
  const [toast, setToast] = useState({ message: '', type: 'info', visible: false });

  const saveUserName = (name) => {
    const trimmed = name.trim();
    if (!trimmed) return;
    setUserName(trimmed);
    try {
      localStorage.setItem('restaurant_user_name', trimmed);
    } catch (e) {
      console.error('Failed to save user name', e);
    }
    setIsNameModalOpen(false);
    showToast(`Welcome, ${trimmed}! ✨`, 'success');
  };

  useEffect(() => {
    try {
      localStorage.setItem('gourmet_cart', JSON.stringify(cart));
    } catch (e) {
      console.error('Failed to save cart to localStorage', e);
    }
  }, [cart]);

  const showToast = (message, type = 'info') => {
    setToast({ message, type, visible: true });
    setTimeout(() => {
      setToast((prev) => ({ ...prev, visible: false }));
    }, 3200);
  };

  const addToCart = (item, quantity = 1) => {
    setCart((prevCart) => {
      const existing = prevCart.find((ci) => ci.id === item.id);
      if (existing) {
        return prevCart.map((ci) =>
          ci.id === item.id ? { ...ci, quantity: ci.quantity + quantity } : ci
        );
      } else {
        return [
          ...prevCart,
          {
            id: item.id,
            name: item.name,
            price: item.price,
            image: item.image,
            is_vegetarian: item.is_vegetarian,
            quantity: quantity,
          },
        ];
      }
    });
    showToast(`Added "${item.name}" to cart! 🍽️`, 'success');
  };

  const removeFromCart = (itemId) => {
    setCart((prevCart) => prevCart.filter((item) => item.id !== itemId));
    showToast('Item removed from cart', 'info');
  };

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(itemId);
      return;
    }
    setCart((prevCart) =>
      prevCart.map((item) =>
        item.id === itemId ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const clearCart = () => {
    setCart([]);
  };

  const cartTotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  const openChatWithPrompt = (prompt) => {
    setPendingPrompt(prompt);
    setIsChatOpen(true);
  };

  return (
    <CartContext.Provider
      value={{
        userName,
        setUserName,
        isNameModalOpen,
        setIsNameModalOpen,
        saveUserName,
        cart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        cartTotal,
        cartCount,
        isCartOpen,
        setIsCartOpen,
        isChatOpen,
        setIsChatOpen,
        pendingPrompt,
        setPendingPrompt,
        openChatWithPrompt,
        toast,
        showToast,
      }}
    >
      {children}
      {toast.visible && (
        <div className={`toast-popup toast-${toast.type}`}>
          {toast.message}
        </div>
      )}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}
