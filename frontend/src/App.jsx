import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import Header from './Header.jsx';
import Footer from './Footer.jsx';
import Rows from './Rows.jsx';
import Carousel from './Carousel.jsx';
import PartnersRow from './partners.Row.jsx';
import AboutUs from './pages/AboutUs.jsx';
import LogIn from './pages/Login.jsx';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Router>
      <MainContent />
    </Router>
  );
}

function MainContent() {
  const location = useLocation();

  const showHeaderFooter = location.pathname !== '/LogIn' && location.pathname !== '/AboutUs';

  return (
    <div className="min-h-screen flex flex-col">
      {showHeaderFooter && <Header />}

      <Routes>
        <Route path="/" element={
          <>
            <div style={{ marginTop: '-20px', marginBottom: '15px' }}>
              <PartnersRow />
            </div>
            <div><Carousel /></div>
            <Rows />
          </>
        } />
        <Route path="/AboutUs" element={<AboutUs />} />
        <Route path="/LogIn" element={<LogIn />} />
      </Routes>

      {showHeaderFooter && <Footer />}
    </div>
  );
}

export default App;
