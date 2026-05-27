'use client';

import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface InputProps {
  name: string;
  type?: string;
  placeholder?: string;
  value: string;
  onChange: (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => void;
  label?: string;
  error?: string;
  disabled?: boolean;
  textarea?: boolean;
  className?: string;
}

export default function Input({
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  label,
  error,
  disabled = false,
  textarea = false,
  className,
}: InputProps) {
  const Component = textarea ? 'textarea' : 'input';

  return (
    <motion.div
      className="w-full"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {label && (
        <label className="block text-sm font-semibold text-neutral-dark mb-2">
          {label}
        </label>
      )}

      <Component
        name={name}
        type={textarea ? undefined : type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        disabled={disabled}
        className={clsx(
          'w-full px-4 py-2 border-2 border-neutral rounded-lg',
          'focus:border-primary focus:outline-none transition-all duration-300',
          'bg-white text-neutral-dark placeholder-gray-400',
          disabled && 'bg-gray-100 cursor-not-allowed',
          error && 'border-error',
          className,
          textarea && 'resize-vertical min-h-32',
        )}
      />

      {error && (
        <motion.p
          className="text-error text-sm mt-1"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {error}
        </motion.p>
      )}
    </motion.div>
  );
}
