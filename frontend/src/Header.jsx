import React, { useState } from 'react';
import './Header.css'; // Подключаем стили

const Header = () => {
  // Состояние для управления меню (открыто/закрыто)
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Функция для переключения состояния меню
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="header">
      <div className="logo">
        <img src="src/assets/logo.png" alt="logo" />
      </div>

      {/* Бургер-меню */}
      <div className={`burger ${isMenuOpen ? 'active' : ''}`} onClick={toggleMenu}>
        <span></span>
        <span></span>
        <span></span>
      </div>

      {/* Навигация, которая будет скрываться на мобильных */}
      <nav className={`nav ${isMenuOpen ? 'active' : ''}`}>
        <ul>
          <li><a href="#home">NEWS</a></li>
          <li><a href="#about">ABOUT US</a></li>
          <li><a href="#services">LOGIN</a></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
