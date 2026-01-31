import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import Card from '../components/ui/Card';
import { Package, Clock, DollarSign, Calendar } from 'lucide-react';

const OrderList = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = async () => {
        try {
            const response = await api.get('/orders');
            setOrders(response.data.orders);
        } catch (error) {
            console.error("Failed to fetch orders", error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="container flex-center" style={{ paddingTop: '4rem' }}>Loading orders...</div>;

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>My Orders</h1>
                <Link to="/orders/new" className="premium-button">
                    Create New Order
                </Link>
            </div>

            {orders.length === 0 ? (
                <Card className="flex-center" style={{ flexDirection: 'column', padding: '4rem 2rem', textAlign: 'center' }}>
                    <Package size={64} color="var(--text-secondary)" style={{ marginBottom: '1rem', opacity: 0.5 }} />
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>No orders yet</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>Start by creating your first order today.</p>
                    <Link to="/orders/new" className="premium-button secondary">
                        Create Order
                    </Link>
                </Card>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
                    {orders.map((order) => (
                        <Card key={order.id} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                <div>
                                    <h3 style={{ fontSize: '1.25rem', fontWeight: 600 }}>{order.item_name}</h3>
                                    <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>#{order.order_number}</span>
                                </div>
                                <div style={{
                                    padding: '0.25rem 0.75rem',
                                    borderRadius: '999px',
                                    fontSize: '0.8rem',
                                    fontWeight: 600,
                                    background: order.status === 'DELIVERED' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(99, 102, 241, 0.2)',
                                    color: order.status === 'DELIVERED' ? 'var(--success)' : 'var(--primary-light)'
                                }}>
                                    {order.status}
                                </div>
                            </div>

                            <div style={{ height: '1px', background: 'var(--border)' }}></div>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.95rem', color: 'var(--text-secondary)' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <DollarSign size={16} />
                                    <span style={{ color: 'var(--text-main)', fontWeight: 500 }}>${order.price}</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <Package size={16} />
                                    <span>{order.item_list.length} items</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <Calendar size={16} />
                                    <span>{new Date(order.item_created_at).toLocaleDateString()}</span>
                                </div>
                            </div>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
};

export default OrderList;
