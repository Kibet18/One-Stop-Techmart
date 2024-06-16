import { Link } from 'react-router-dom'

function HomePage() {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold mb-4">Welcome to OneStopTechMart</h2>
      <p className="mb-8">Your one-stop shop for all tech gadgets and accessories.</p>
      <Link
        to="/products"
        className="bg-gray-800 text-white px-4 py-2 rounded hover:bg-gray-700"
      >
        Shop Now
      </Link>
    </div>
  )
}

export default HomePage