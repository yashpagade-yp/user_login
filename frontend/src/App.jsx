import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import OrderList from './pages/OrderList';
import OrderCreate from './pages/OrderCreate';

// Protected Route Wrapper
const ProtectedRoute = ({ children }) => {
    const { user, loading } = useAuth();

    if (loading) return <div className="flex-center" style={{ minHeight: '100vh' }}>Loading...</div>;

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

function App() {
    return (
        <Router>
            <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Navbar />
                <main style={{ flex: 1, padding: '2rem 0' }}>
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />

                        <Route path="/" element={
                            <ProtectedRoute>
                                <OrderList />
                            </ProtectedRoute>
                        } />
                        <Route path="/orders/new" element={
                            <ProtectedRoute>
                                <OrderCreate />
                            </ProtectedRoute>
                        } />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;
