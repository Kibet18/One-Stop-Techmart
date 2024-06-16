import { Link } from 'react-router-dom'

function Header() {
  return (
    <header className="bg-gray-800 text-white py-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">OneStopTechMart</h1>
        <nav>
          <Link to="/" className="mx-2 hover:text-gray-300">Home</Link>
          <Link to="/products" className="mx-2 hover:text-gray-300">Products</Link>
        </nav>
      </div>
    </header>
  )
}

export default Header