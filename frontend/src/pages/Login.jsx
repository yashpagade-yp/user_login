import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

const Login = () => {
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const result = await login(formData.email, formData.password);

        if (result.success) {
            navigate('/');
        } else {
            setError(typeof result.error === 'string' ? result.error : 'Invalid credentials');
        }
        setLoading(false);
    };

    return (
        <div className="flex-center" style={{ minHeight: '80vh' }}>
            <div className="container" style={{ maxWidth: '400px', width: '100%' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <h1 style={{
                        background: 'linear-gradient(to right, var(--primary), var(--secondary))',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        fontSize: '2.5rem',
                        fontWeight: 800,
                        marginBottom: '0.5rem'
                    }}>
                        Welcome Back
                    </h1>
                    <p style={{ color: 'var(--text-secondary)' }}>Sign in to manage your orders</p>
                </div>

                <Card>
                    <form onSubmit={handleSubmit}>
                        <Input
                            label="Email Address"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="you@example.com"
                            required
                        />
                        <Input
                            label="Password"
                            name="password"
                            type="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="••••••••"
                            required
                        />

                        {error && (
                            <div style={{
                                padding: '0.75rem',
                                background: 'rgba(239, 68, 68, 0.1)',
                                border: '1px solid rgba(239, 68, 68, 0.2)',
                                borderRadius: '8px',
                                color: 'var(--error)',
                                fontSize: '0.9rem',
                                marginBottom: '1rem'
                            }}>
                                {error}
                            </div>
                        )}

                        <Button isLoading={loading} type="submit" style={{ marginTop: '0.5rem' }}>
                            Sign In
                        </Button>
                    </form>

                    <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>Don't have an account? </span>
                        <Link to="/register" style={{ color: 'var(--primary-light)', fontWeight: 500 }}>
                            Create Account
                        </Link>
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default Login;
