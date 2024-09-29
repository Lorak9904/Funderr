import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="header mb-14">
      <div className="logo">

        <Link to="/">
          <img src="src/assets/logo.png" alt="logo" />
        </Link>
      </div>


      <div className={`burger ${isMenuOpen ? 'active' : ''}`} onClick={toggleMenu}>
        <span></span>
        <span></span>
        <span></span>
      </div>

      <nav className={`nav ${isMenuOpen ? 'active' : ''}`}>
        <ul>
          <li><Link to="/AboutUs">ABOUT US</Link></li>
          <li><Link to="/LogIn">LOGIN</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;