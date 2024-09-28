import { useState } from 'react'
import Header from './Header.jsx'
import Footer from './Footer.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      {/* Остальная часть сайта */}
      {/* Тут будет основная часть */}
      <div className='flex-grow'></div>
      <Footer />
    </div>
  )
}
export default App
