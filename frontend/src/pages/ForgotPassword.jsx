import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

const ForgotPassword = () => {
    const [step, setStep] = useState(1); // 1: Email, 2: OTP, 3: New Password
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const handleSendOtp = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccessMessage('');

        try {
            await api.post('/users/forgot_password', { email });
            setStep(2);
            setSuccessMessage(`OTP sent to ${email}`);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to send OTP. Please check the email.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleVerifyOtp = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccessMessage('');

        try {
            await api.post('/users/verify_otp', { email, otp });
            setStep(3); // Move to password reset step directly if verified
            setSuccessMessage('OTP Verified! Please set your new password.');
        } catch (err) {
            setError(err.response?.data?.detail || 'Invalid OTP or expired.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleResetPassword = async (e) => {
        e.preventDefault();

        if (newPassword !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setIsLoading(true);
        setError('');
        setSuccessMessage('');

        try {
            // We still send OTP here because the backend endpoint expects it for security double-check
            // Ideally backend would have a temporary token after verify_otp, but this works with current backend
            await api.post('/users/reset_password_with_otp', {
                email,
                otp,
                new_password: newPassword
            });
            setSuccessMessage('Password reset successfully! Redirecting to login...');
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to reset password.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex-center" style={{ minHeight: '80vh' }}>
            <div className="container" style={{ maxWidth: '400px', width: '100%' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <h1 style={{
                        background: 'linear-gradient(to right, var(--primary), var(--secondary))',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        fontSize: '2rem',
                        fontWeight: 800,
                        marginBottom: '0.5rem'
                    }}>
                        {step === 1 ? 'Forgot Password' : step === 2 ? 'Verify OTP' : 'Reset Password'}
                    </h1>
                    <p style={{ color: 'var(--text-secondary)' }}>
                        {step === 1 ? 'Enter your email to receive an OTP' :
                            step === 2 ? 'Enter the OTP sent to your email' :
                                'Create a new password'}
                    </p>
                </div>

                <Card>
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

                    {successMessage && (
                        <div style={{
                            padding: '0.75rem',
                            background: 'rgba(34, 197, 94, 0.1)',
                            border: '1px solid rgba(34, 197, 94, 0.2)',
                            borderRadius: '8px',
                            color: '#22c55e',
                            fontSize: '0.9rem',
                            marginBottom: '1rem'
                        }}>
                            {successMessage}
                        </div>
                    )}

                    {step === 1 && (
                        <form onSubmit={handleSendOtp}>
                            <Input
                                label="Email Address"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="you@example.com"
                                required
                            />
                            <Button isLoading={isLoading} type="submit" style={{ marginTop: '0.5rem' }}>
                                Send OTP
                            </Button>
                        </form>
                    )}

                    {step === 2 && (
                        <form onSubmit={handleVerifyOtp}>
                            <Input
                                label="OTP Code"
                                type="text"
                                value={otp}
                                onChange={(e) => setOtp(e.target.value)}
                                placeholder="Enter 4-digit OTP"
                                required
                                maxLength={4}
                            />
                            <Button isLoading={isLoading} type="submit" style={{ marginTop: '0.5rem' }}>
                                Verify OTP
                            </Button>
                            <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                                <button
                                    type="button"
                                    onClick={() => setStep(1)}
                                    style={{
                                        background: 'none',
                                        border: 'none',
                                        color: 'var(--text-secondary)',
                                        cursor: 'pointer',
                                        textDecoration: 'underline',
                                        fontSize: '0.9rem'
                                    }}
                                >
                                    Change Email
                                </button>
                            </div>
                        </form>
                    )}

                    {step === 3 && (
                        <form onSubmit={handleResetPassword}>
                            <Input
                                label="New Password"
                                type="password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                placeholder="Min 8 characters"
                                required
                                minLength={8}
                            />
                            <Input
                                label="Confirm New Password"
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Confirm new password"
                                required
                                minLength={8}
                            />
                            <Button isLoading={isLoading} type="submit" style={{ marginTop: '0.5rem' }}>
                                Reset Password
                            </Button>
                        </form>
                    )}

                    <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>Remember your password? </span>
                        <Link to="/login" style={{ color: 'var(--primary-light)', fontWeight: 500 }}>
                            Sign In
                        </Link>
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default ForgotPassword;
