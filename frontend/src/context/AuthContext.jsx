import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for stored token and user on mount
        const token = localStorage.getItem('token');

        // In a real app, you would validate the token with /me endpoint here
        // For now, we'll try to fetch the user if a token exists
        if (token) {
            fetchUser();
        } else {
            setLoading(false);
        }
    }, []);

    const fetchUser = async () => {
        try {
            const response = await api.get('/users/me');
            setUser(response.data);
        } catch (error) {
            console.error("Failed to fetch user", error);
            logout();
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        try {
            const response = await api.post('/user_login', { email, password });
            // The response structure based on backend code:
            // { user: {...}, access_token: "..." }
            const { user, access_token } = response.data;

            localStorage.setItem('token', access_token);
            setUser(user);
            return { success: true };
        } catch (error) {
            console.error("Login failed", error);
            return { success: false, error: error.response?.data?.detail || "Login failed" };
        }
    };

    const register = async (userData) => {
        try {
            // Backend expects: first_name, last_name, email, mobile_number, password, address
            const response = await api.post('/users', userData);
            const { user, access_token } = response.data;

            localStorage.setItem('token', access_token);
            setUser(user);
            return { success: true };
        } catch (error) {
            console.error("Registration failed", error);
            return { success: false, error: error.response?.data?.detail || "Registration failed" };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
