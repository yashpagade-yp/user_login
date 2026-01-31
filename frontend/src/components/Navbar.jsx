import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, User, Box, PlusCircle } from 'lucide-react';

const Navbar = () => {
    const { user, logout } = useAuth();

    if (!user) return null;

    return (
        <nav style={{
            borderBottom: '1px solid var(--border)',
            background: 'rgba(15, 23, 42, 0.8)',
            backdropFilter: 'blur(12px)',
            position: 'sticky',
            top: 0,
            zIndex: 50
        }}>
            <div className="container" style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                height: '4rem'
            }}>
                <NavLink to="/" style={{
                    fontSize: '1.5rem',
                    fontWeight: 700,
                    background: 'linear-gradient(to right, var(--primary-light), var(--secondary))',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                }}>
                    OmniOrder
                </NavLink>

                <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                    <NavLink
                        to="/"
                        style={({ isActive }) => ({
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            color: isActive ? 'var(--primary-light)' : 'var(--text-secondary)',
                            transition: 'color 0.2s'
                        })}
                    >
                        <Box size={20} />
                        <span>Orders</span>
                    </NavLink>

                    <NavLink
                        to="/orders/new"
                        style={({ isActive }) => ({
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            color: isActive ? 'var(--primary-light)' : 'var(--text-secondary)',
                            transition: 'color 0.2s'
                        })}
                    >
                        <PlusCircle size={20} />
                        <span>New Order</span>
                    </NavLink>

                    <div style={{ width: '1px', height: '1.5rem', background: 'var(--border)' }}></div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-main)' }}>
                            <User size={20} />
                            <span style={{ fontSize: '0.9rem' }}>{user.first_name}</span>
                        </div>
                        <button
                            onClick={logout}
                            style={{
                                background: 'transparent',
                                border: 'none',
                                color: 'var(--text-secondary)',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                padding: '0.5rem'
                            }}
                            title="Logout"
                        >
                            <LogOut size={20} />
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
