import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Menu, X, Activity, Phone, Mail, MapPin, ChevronRight, ArrowRight, User, LogOut, Facebook, ArrowUp } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { NAV_ITEMS } from '../constants';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoggedIn, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setIsMobileMenuOpen(false);
    window.scrollTo(0, 0);
  }, [location]);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="flex flex-col min-h-screen font-sans bg-slate-50 text-slate-800 selection:bg-blue-100 selection:text-blue-900">

      {/* Modern Floating Header */}
      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 cubic-bezier(0.4, 0, 0.2, 1) px-4 md:px-6 ${scrolled ? 'py-4' : 'py-6'
          }`}
      >
        <div
          className={`mx-auto max-w-7xl transition-all duration-500 backdrop-blur-xl border shadow-[0_8px_30px_rgba(0,0,0,0.04)] rounded-full flex items-center justify-between pl-0 pr-2 ${scrolled
            ? 'bg-white border-slate-200 h-16'
            : 'bg-white border-slate-100 h-20'
            }`}
        >
          {/* Official Logo Integration */}
          <NavLink to="/" className="flex items-center gap-0 group mr-8 -ml-4">
            <div className="relative group-hover:scale-105 transition duration-300">
              <img
                src="/logo/logo 2.png"
                alt="Swift Sales Logo"
                className={`${scrolled ? 'h-32 mt-2' : 'h-48 mt-[18px]'} w-auto object-contain transition-all duration-500`}
              />
            </div>
            <div className={`flex flex-col transition-all duration-500 ${scrolled ? '-ml-8' : '-ml-12'}`}>
              <span className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight leading-none">Swift Sales</span>
              <span className="text-[9px] md:text-[10px] font-bold text-blue-600 uppercase tracking-[0.2em] leading-none mt-1">Medicine Distributor</span>
            </div>
          </NavLink>

          {/* Desktop Nav */}
          <nav className="hidden lg:flex items-center gap-1">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `relative px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-300 ${isActive
                    ? 'text-blue-600 bg-blue-50/80 shadow-sm'
                    : 'text-slate-600 hover:bg-slate-100/50 hover:text-slate-900'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          {/* Right Side Actions */}
          <div className="flex items-center gap-3">
            {/* {isLoggedIn ? (
              <div className="hidden md:flex items-center gap-4 pl-4 border-l border-slate-200 ml-2">
                <div className="flex flex-col items-end">
                  <span className="text-xs font-bold text-slate-900 leading-none">{user?.name}</span>
                  <span className="text-[9px] font-bold text-blue-600 uppercase tracking-wider mt-1">{user?.organization}</span>
                </div>
                <div className="relative group">
                  <button className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-blue-50 hover:text-blue-600 transition-all border border-slate-200">
                    <User size={18} />
                  </button>
                  <div className="absolute top-full right-0 mt-2 w-48 bg-white rounded-2xl shadow-2xl border border-slate-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 p-2 z-[60]">
                    <button
                      onClick={logout}
                      className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-xs font-bold text-red-600 hover:bg-red-50 transition-colors"
                    >
                      <LogOut size={16} />
                      TERMINATE SESSION
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <NavLink
                to="/login"
                className="hidden md:block text-xs font-bold text-slate-500 hover:text-blue-600 px-4 transition-colors uppercase tracking-wider"
              >
                Login
              </NavLink>
            )} */}

            <NavLink
              to="/contact"
              className={`hidden md:flex items-center gap-2 bg-slate-900 text-white rounded-full px-6 font-medium transition-all hover:bg-blue-600 hover:shadow-lg hover:shadow-blue-900/20 active:scale-95 group ${scrolled ? 'py-2.5 text-xs' : 'py-3 text-sm'
                }`}
            >
              Get Started <ChevronRight size={14} className="group-hover:translate-x-0.5 transition-transform" />
            </NavLink>

            {/* Mobile Menu Toggle */}
            <button
              className="lg:hidden p-3 text-slate-600 hover:text-blue-600 transition bg-slate-100/50 hover:bg-blue-50 rounded-full"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown */}
        <div
          className={`lg:hidden absolute top-full left-0 right-0 mt-2 px-4 transition-all duration-300 transform origin-top ${isMobileMenuOpen ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 -translate-y-4 pointer-events-none'
            }`}
        >
          <div className="bg-white/90 backdrop-blur-xl rounded-[2rem] shadow-2xl border border-white/50 overflow-hidden p-3">
            <nav className="flex flex-col space-y-1">
              {NAV_ITEMS.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `px-5 py-4 rounded-2xl text-base font-medium transition-all flex justify-between items-center ${isActive
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    }`
                  }
                >
                  {({ isActive }) => (
                    <>
                      {item.label}
                      {isActive && <div className="w-1.5 h-1.5 rounded-full bg-blue-600"></div>}
                    </>
                  )}
                </NavLink>
              ))}
              <div className="h-px bg-slate-100 my-2 mx-4"></div>
              {/* {isLoggedIn ? (
                <div className="px-5 py-4 border-b border-slate-50">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                      <User size={24} />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-slate-900">{user?.name}</p>
                      <p className="text-[10px] font-bold text-blue-600 uppercase tracking-widest">{user?.organization}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => { logout(); setIsMobileMenuOpen(false); }}
                    className="w-full flex items-center justify-center gap-3 py-3 rounded-xl bg-red-50 text-red-600 text-sm font-bold active:scale-95 transition-all"
                  >
                    <LogOut size={18} />
                    Sign Out
                  </button>
                </div>
              ) : (
                <>
                  <NavLink to="/login" onClick={() => setIsMobileMenuOpen(false)} className="px-5 py-4 rounded-2xl text-base font-bold text-slate-500 hover:text-blue-600 hover:bg-slate-50 transition-colors">
                    Login
                  </NavLink>
                  <NavLink to="/register" onClick={() => setIsMobileMenuOpen(false)} className="px-5 py-4 rounded-2xl text-base font-bold text-slate-500 hover:text-blue-600 hover:bg-slate-50 transition-colors">
                    Partner Registry
                  </NavLink>
                </>
              )} */}
              <NavLink to="/contact" onClick={() => setIsMobileMenuOpen(false)} className="px-5 py-4 rounded-2xl text-base font-medium bg-slate-900 text-white text-center hover:bg-slate-800 shadow-lg shadow-slate-900/10">
                Get Started
              </NavLink>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow relative z-10">
        {children}
      </main>

      {/* Footer - Professional Dark Contrast */}
      <footer className="bg-slate-900 border-t border-slate-800 text-slate-300 pt-20 pb-10 relative z-10">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
            <div>
              <div className="flex items-center gap-0 mb-6">
                <img
                  src="/logo/logo 2.png"
                  alt="Swift Sales Logo"
                  className="h-48 w-auto object-contain bg-white p-1 rounded-lg mt-[15px]"
                />
                <span className="text-2xl font-bold text-white tracking-tight -ml-4">Swift Sales</span>
              </div>
              <p className="text-slate-400 mb-6 leading-relaxed text-sm">
                Empowering healthcare globally through reliable distribution, innovation, and unwavering compliance standards.
              </p>
              <div className="flex gap-4">
                <a href="https://www.facebook.com/profile.php?id=100063927496765" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 hover:bg-blue-600 hover:text-white transition-all duration-300">
                  <Facebook size={20} />
                </a>
              </div>
            </div>

            <div>
              <h3 className="text-white font-semibold text-lg mb-6">Explore</h3>
              <ul className="grid grid-cols-2 gap-x-8 gap-y-3">
                {NAV_ITEMS.map((item) => (
                  <li key={item.path}>
                    <NavLink
                      to={item.path}
                      className={({ isActive }) => `text-slate-400 hover:text-white transition-colors duration-200 flex items-center gap-2 text-sm ${isActive ? 'text-blue-500 font-bold' : ''}`}
                    >
                      <span className="w-1 h-1 bg-blue-500 rounded-full"></span>
                      {item.label}
                    </NavLink>
                  </li>
                ))}
                {/* {!isLoggedIn && (
                  <li>
                    <NavLink to="/login" className="text-blue-400 hover:text-white transition-colors duration-200 flex items-center gap-2 text-sm font-bold">
                      <span className="w-1.5 h-1.5 bg-blue-400 rounded-full"></span>
                      Login
                    </NavLink>
                  </li>
                )}
                <li>
                  <NavLink to="/register" className="text-slate-400 hover:text-white transition-colors duration-200 flex items-center gap-2 text-sm">
                    <span className="w-1 h-1 bg-blue-500 rounded-full"></span>
                    Partner Registration
                  </NavLink>
                </li> */}
              </ul>
            </div>

            <div>
              <h3 className="text-white font-semibold text-lg mb-6">Contact</h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3 text-slate-400 hover:text-white transition-colors">
                  <MapPin size={20} className="text-blue-500 mt-1 shrink-0" />
                  <span className="text-sm">C8GM+HFF, Sardar Colony<br />Rahim Yar Khan, Pakistan</span>
                </li>
                <li className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
                  <Phone size={20} className="text-blue-500 shrink-0" />
                  <span className="text-sm">0301 8670511</span>
                </li>
                <li className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
                  <Mail size={20} className="text-blue-500 shrink-0" />
                  <span className="text-sm">colab@qintellecttechnologies.com</span>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="text-white font-semibold text-lg mb-6">Accreditation</h3>
              <div className="flex gap-4">
                {['ISO 9001', 'GDP', 'FDA'].map(cert => (
                  <div key={cert} className="bg-slate-800 border border-slate-700 p-2 rounded-lg text-center w-16 h-16 flex flex-col items-center justify-center gap-1 group hover:border-blue-500 transition-colors">
                    <span className="text-[10px] text-slate-400 group-hover:text-white font-bold">{cert}</span>
                    <div className="w-2 h-2 rounded-full bg-slate-600 group-hover:bg-blue-500 transition-colors"></div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
            <div className="flex flex-col md:flex-row items-center gap-4 text-xs opacity-70">
              <p>&copy; {new Date().getFullYear()} Swift Sales Healthcare. All rights reserved. | Developed by <span className="text-blue-500 font-semibold">QIntellect Technologies</span> | <a href="mailto:colab@qintellecttechnologies.com" className="hover:text-blue-400 transition-colors">colab@qintellecttechnologies.com</a> | 2206 ok</p>
            </div>
            <div className="flex space-x-6 mt-4 md:mt-0 font-medium">
              <NavLink to="/privacy" className="hover:text-white transition">Privacy Policy</NavLink>
              <NavLink to="/terms" className="hover:text-white transition">Terms of Service</NavLink>
            </div>
          </div>
        </div>
      </footer>

      {/* Scroll to Top Button */}
      <button
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        className={`fixed bottom-8 right-8 z-50 p-4 bg-blue-600 text-white rounded-full shadow-lg shadow-blue-600/30 transition-all duration-300 hover:bg-blue-700 hover:scale-110 active:scale-95 flex items-center justify-center ${scrolled ? 'opacity-100 translate-y-0 visible' : 'opacity-0 translate-y-10 invisible'
          }`}
      >
        <ArrowUp size={24} strokeWidth={2.5} />
      </button>
    </div>
  );
};