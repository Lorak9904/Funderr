import { useState } from 'react'
import Header from './Header.jsx'
import Footer from './Footer.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <Footer />
    </div>
  )
}
export default App
