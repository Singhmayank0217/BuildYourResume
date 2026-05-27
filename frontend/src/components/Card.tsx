'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export default function Card({ children, className, onClick, hoverable = true }: CardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={hoverable ? { translateY: -4 } : {}}
      onClick={onClick}
      className={clsx(
        'bg-white rounded-xl shadow-md p-6 transition-all duration-300',
        hoverable && 'cursor-pointer hover:shadow-xl',
        className
      )}
    >
      {children}
    </motion.div>
  );
}
