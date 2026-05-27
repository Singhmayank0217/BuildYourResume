'use client';

import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { motion } from 'framer-motion';
import Button from './Button';

export default function Header() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'Templates', path: '/templates' },
    { label: 'Builder', path: '/builder' },
    { label: 'Analyzer', path: '/analyzer' },
  ];

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <motion.div
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 cursor-pointer"
            whileHover={{ scale: 1.05 }}
          >
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white font-bold">
              R
            </div>
            <span className="font-bold text-lg text-neutral-dark hidden sm:inline">Resume Builder</span>
          </motion.div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <motion.a
                key={item.path}
                onClick={() => navigate(item.path)}
                className="text-neutral-dark hover:text-primary transition-colors cursor-pointer"
                whileHover={{ color: '#2563eb' }}
              >
                {item.label}
              </motion.a>
            ))}
          </nav>

          {/* User Menu */}
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2">
              <span className="text-sm text-neutral-dark">{user?.email}</span>
            </div>
            <motion.button
              onClick={handleLogout}
              className="flex items-center gap-2 text-neutral-dark hover:text-error transition-colors"
              whileHover={{ scale: 1.1 }}
            >
              <LogOut size={20} />
              <span className="hidden sm:inline text-sm">Logout</span>
            </motion.button>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-neutral-dark"
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <motion.nav
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-neutral py-4 space-y-2"
          >
            {navItems.map((item) => (
              <motion.a
                key={item.path}
                onClick={() => {
                  navigate(item.path);
                  setMobileMenuOpen(false);
                }}
                className="block px-4 py-2 text-neutral-dark hover:bg-neutral rounded-lg transition-colors cursor-pointer"
                whileHover={{ backgroundColor: '#f3f4f6' }}
              >
                {item.label}
              </motion.a>
            ))}
          </motion.nav>
        )}
      </div>
    </header>
  );
}
