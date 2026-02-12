import React from "react";
import { Button } from "../ui/Button";

type Props = {
  children: React.ReactNode;
};

const AppLayout: React.FC<Props> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-primary-base text-text-neutral font-sans selection:bg-ai-highlight1 selection:text-primary-base">
      <header className="border-b border-white/10 backdrop-blur-md bg-primary-base/80 sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-action-primary to-ai-highlight1 flex items-center justify-center shadow-lg shadow-action-primary/20">
              <span className="text-white font-bold text-xl italic">D</span>
            </div>
            <h1 className="text-2xl font-black tracking-tighter text-white">
              DocVision<span className="text-action-primary">AI</span>
            </h1>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm font-medium text-text-secondary hover:text-white transition-colors">Features</a>
            <a href="#pricing" className="text-sm font-medium text-text-secondary hover:text-white transition-colors">Pricing</a>
            <a href="#docs" className="text-sm font-medium text-text-secondary hover:text-white transition-colors">API Docs</a>
            <a href="#about" className="text-sm font-medium text-text-secondary hover:text-white transition-colors">About</a>
          </nav>

          <div className="flex items-center gap-4">
            <button className="hidden sm:block text-sm font-semibold text-text-neutral hover:text-action-primary transition-colors px-4 py-2">
              Login
            </button>
            <Button size="sm" className="bg-action-primary hover:bg-action-hover text-white rounded-lg px-5 py-2 text-sm font-bold shadow-lg shadow-action-primary/25 transition-all hover:scale-105 active:scale-95">
              Sign Up
            </Button>
            <span className="hidden lg:block text-[10px] font-bold px-2 py-0.5 rounded bg-white/5 text-text-secondary border border-white/10 backdrop-blur-sm">
              v1.0.0 Beta
            </span>
          </div>
        </div>
      </header>

      <main className="flex-1 mx-auto max-w-7xl w-full px-4 py-8">
        {children}
      </main>

      <footer className="border-t border-white/10 bg-primary-base mt-auto">
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
