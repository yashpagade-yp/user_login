import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

const OrderCreate = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const [formData, setFormData] = useState({
        item_name: '',
        price: '',
        order_number: Math.floor(Math.random() * 100000),
        item_list_str: '',
        address: {
            street_address: '',
            city: '',
            state: '',
            postal_code: '',
            country: 'India'
        }
    });

    useEffect(() => {
        // Pre-fill address if user has one
        if (user && user.address) {
            setFormData(prev => ({
                ...prev,
                address: {
                    street_address: user.address.street_address || '',
                    city: user.address.city || '',
                    state: user.address.state || '',
                    postal_code: user.address.postal_code || '',
                    country: user.address.country || 'India'
                }
            }));
        }
    }, [user]);

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

        try {
            const payload = {
                user_id: user.id,
                item_name: formData.item_name,
                price: parseFloat(formData.price),
                order_number: parseInt(formData.order_number),
                item_list: formData.item_list_str.split(',').map(item => item.trim()).filter(i => i),
                Address: formData.address, // Note: Schema expects 'Address' capitalized based on backend
                status: 'BOOKED'
            };

            await api.post('/orders', payload);
            navigate('/');
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Failed to create order');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h1 style={{ marginBottom: '2rem' }}>Create New Order</h1>
            <Card>
                <form onSubmit={handleSubmit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <Input label="Item Name" name="item_name" value={formData.item_name} onChange={handleChange} required />
                        <Input label="Price" name="price" type="number" step="0.01" value={formData.price} onChange={handleChange} required />
                    </div>

                    <Input label="Order Number (Auto-generated)" name="order_number" type="number" value={formData.order_number} readOnly />
                    <Input label="Items (comma separated)" name="item_list_str" value={formData.item_list_str} onChange={handleChange} placeholder="Apple, Banana, Orange" required />

                    <div style={{ margin: '1.5rem 0 1rem 0', borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                        <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: 'var(--text-main)' }}>Shipping Address</h3>
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

                    {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}

                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <Button type="button" variant="secondary" onClick={() => navigate('/')}>Cancel</Button>
                        <Button type="submit" isLoading={loading}>Place Order</Button>
                    </div>
                </form>
            </Card>
        </div>
    );
};

export default OrderCreate;
