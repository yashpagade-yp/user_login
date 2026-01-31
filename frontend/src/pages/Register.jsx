import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

const Register = () => {
    const [formData, setFormData] = useState({
        first_name: '', last_name: '', email: '', mobile_number: '', password: '',
        address: { street_address: '', city: '', state: '', postal_code: '', country: 'India' }
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name.startsWith('addr_')) {
            const addrField = name.replace('addr_', '');
            setFormData(prev => ({
                ...prev,
                address: { ...prev.address, [addrField]: value }
            }));
        } else {
            setFormData(prev => ({ ...prev, [name]: value }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const result = await register(formData);

        if (result.success) {
            navigate('/');
        } else {
            if (Array.isArray(result.error)) {
                // Format Pydantic validation errors
                const messages = result.error.map(err => {
                    const field = err.loc[err.loc.length - 1]; // Get the last part of location (field name)
                    return `${field}: ${err.msg}`;
                }).join(', ');
                setError(messages);
            } else {
                setError(typeof result.error === 'string' ? result.error : 'Registration failed. Please check your inputs.');
            }
        }
        setLoading(false);
    };

    return (
        <div className="flex-center" style={{ minHeight: '90vh', padding: '2rem 0' }}>
            <div className="container" style={{ maxWidth: '600px', width: '100%' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <h1 style={{
                        background: 'linear-gradient(to right, var(--primary), var(--secondary))',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        fontSize: '2.5rem',
                        fontWeight: 800,
                        marginBottom: '0.5rem'
                    }}>
                        Create Account
                    </h1>
                    <p style={{ color: 'var(--text-secondary)' }}>Join us to start ordering</p>
                </div>

                <Card>
                    <form onSubmit={handleSubmit}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <Input label="First Name" name="first_name" value={formData.first_name} onChange={handleChange} required />
                            <Input label="Last Name" name="last_name" value={formData.last_name} onChange={handleChange} required />
                        </div>

                        <Input label="Email" name="email" type="email" value={formData.email} onChange={handleChange} required />
                        <Input label="Mobile Number" name="mobile_number" value={formData.mobile_number} onChange={handleChange} placeholder="10 digits" required />
                        <Input label="Password" name="password" type="password" value={formData.password} onChange={handleChange} minLength={8} required />

                        <div style={{ margin: '1.5rem 0 1rem 0', borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                            <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: 'var(--text-main)' }}>Address Details</h3>
                            <Input label="Street Address" name="addr_street_address" value={formData.address.street_address} onChange={handleChange} required />

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <Input label="City" name="addr_city" value={formData.address.city} onChange={handleChange} required />
                                <Input label="State" name="addr_state" value={formData.address.state} onChange={handleChange} required />
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <Input label="Postal Code" name="addr_postal_code" value={formData.address.postal_code} onChange={handleChange} required />
                                <Input label="Country" name="addr_country" value={formData.address.country} onChange={handleChange} required />
                            </div>
                        </div>

                        {error && (
                            <div style={{ color: 'var(--error)', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>
                        )}

                        <Button isLoading={loading} type="submit" style={{ marginTop: '0.5rem' }}>
                            Create Account
                        </Button>
                    </form>

                    <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>Already have an account? </span>
                        <Link to="/login" style={{ color: 'var(--primary-light)', fontWeight: 500 }}>Sign In</Link>
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default Register;
