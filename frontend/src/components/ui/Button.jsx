import React from 'react';

const Button = ({ children, variant = 'primary', isLoading, ...props }) => {
    return (
        <button
            className={`premium-button ${variant}`}
            disabled={isLoading || props.disabled}
            style={{ opacity: isLoading ? 0.7 : 1, width: '100%', ...props.style }}
            {...props}
        >
            {isLoading ? 'Processing...' : children}
        </button>
    );
};

export default Button;
