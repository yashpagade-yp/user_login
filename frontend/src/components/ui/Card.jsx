import React from 'react';
import { motion } from 'framer-motion';

const Card = ({ children, className = '', title, ...props }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className={`glass-panel ${className}`}
            style={{ padding: '2rem', ...props.style }}
            {...props}
        >
            {title && (
                <h2 style={{
                    marginBottom: '1.5rem',
                    fontSize: '1.5rem',
                    fontWeight: 600,
                    color: 'var(--text-main)'
                }}>
                    {title}
                </h2>
            )}
            {children}
        </motion.div>
    );
};

export default Card;
