import React from "react";
import { Button } from "../ui/Button";

type Props = {
  children: React.ReactNode;
  onNavigate?: (page: 'home' | 'upload') => void;
  currentPage?: 'home' | 'upload';
};

const AppLayout: React.FC<Props> = ({ children, onNavigate, currentPage }) => {
  return (
    <div className="min-h-screen flex flex-col bg-[#0B0F19] text-text-neutral font-sans selection:bg-ai-highlight1 selection:text-primary-base">
      <header className="border-b border-white/10 backdrop-blur-md bg-[#0B0F19]/80 sticky top-0 z-50 h-24 flex items-center">
        <div className="mx-auto max-w-7xl w-full px-4 flex items-center justify-between">
          <div className="flex items-center gap-16">
            <div 
              className="flex items-center gap-2.5 cursor-pointer group"
              onClick={() => onNavigate?.('home')}
            >
              <div className="w-9 h-9 rounded-xl bg-action-primary flex items-center justify-center shadow-lg shadow-action-primary/30 group-hover:scale-110 transition-transform">
                <span className="text-white font-bold text-xl italic">D</span>
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-white">
                DocVision <span className="text-text-secondary font-normal">AI</span>
              </h1>
            </div>

            {/* Navigation Links - Centered-right organization */}
            <nav className="hidden md:flex items-center gap-10">
              <button 
                onClick={() => onNavigate?.('home')}
                className={`text-sm font-semibold transition-colors ${currentPage === 'home' ? 'text-white' : 'text-text-secondary hover:text-white'}`}
              >
                Home
              </button>
              <button 
                onClick={() => onNavigate?.('upload')}
                className={`text-sm font-semibold transition-colors ${currentPage === 'upload' ? 'text-white' : 'text-text-secondary hover:text-white'}`}
              >
                Upload
              </button>
              <a href="#features" className="text-sm font-semibold text-text-secondary hover:text-white transition-colors">Features</a>
              <a href="#about" className="text-sm font-semibold text-text-secondary hover:text-white transition-colors">About</a>
            </nav>
          </div>

          <div className="flex items-center gap-10">
            <button className="hidden sm:block text-sm font-semibold text-text-secondary hover:text-white transition-colors">
              Login
            </button>
            <Button size="lg" className="bg-action-primary hover:bg-action-hover text-white rounded-xl px-8 py-3 text-sm font-bold shadow-[0_0_20px_rgba(99,102,241,0.4)] transition-all hover:shadow-[0_0_30px_rgba(99,102,241,0.6)] ring-1 ring-white/20">
              Sign Up
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 mx-auto max-w-7xl w-full px-4 py-8">
        {children}
      </main>

      <footer className="border-t border-white/10 bg-[#0B0F19] mt-auto">
        <div className="mx-auto max-w-7xl px-4 py-6 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-text-secondary">
          <p>© {new Date().getFullYear()} DocVision AI. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="#" className="hover:text-action-primary transition-colors">Privacy</a>
            <a href="#" className="hover:text-action-primary transition-colors">Terms</a>
            <a href="#" className="hover:text-action-primary transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AppLayout;
