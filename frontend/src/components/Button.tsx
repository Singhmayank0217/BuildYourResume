'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface ButtonProps {
  children: ReactNode;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  loading?: boolean;
  icon?: ReactNode;
}

export default function Button({
  children,
  onClick,
  disabled = false,
  type = 'submit', // ✅ FIX: better default for forms
  variant = 'primary',
  size = 'md',
  className,
  loading = false,
  icon,
}: ButtonProps) {
  const baseClasses =
    'font-semibold rounded-lg transition-all duration-300 flex items-center gap-2 justify-center';

  const variantClasses = {
    primary: 'bg-primary text-white hover:bg-secondary active:scale-95',
    secondary: 'bg-secondary text-white hover:bg-primary active:scale-95',
    outline:
      'border-2 border-primary text-primary hover:bg-primary/10 active:scale-95',
  };

  const sizeClasses = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-6 py-2 text-base',
    lg: 'px-8 py-3 text-lg',
  };

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={clsx(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        (disabled || loading) && 'opacity-50 cursor-not-allowed',
        className
      )}
      whileHover={{ translateY: -2 }}
      whileTap={{ translateY: 0 }}
    >
      {loading && <span className="animate-spin">⚙️</span>}
      {!loading && icon}
      <span>{children}</span>
    </motion.button>
  );
}
