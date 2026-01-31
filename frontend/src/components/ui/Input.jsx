import React from 'react';

const Input = ({ label, error, ...props }) => {
    return (
        <div style={{ marginBottom: '1rem', width: '100%' }}>
            {label && (
                <label style={{
                    display: 'block',
                    marginBottom: '0.5rem',
                    fontSize: '0.9rem',
                    color: 'var(--text-secondary)',
                    fontWeight: 500
                }}>
                    {label}
                </label>
            )}
            <input
                className="premium-input"
                style={{ borderColor: error ? 'var(--error)' : 'var(--border)' }}
                {...props}
            />
            {error && (
                <span style={{
                    display: 'block',
                    marginTop: '0.25rem',
                    fontSize: '0.8rem',
                    color: 'var(--error)'
                }}>
                    {error}
                </span>
            )}
        </div>
    );
};

export default Input;
