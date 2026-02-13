import React from "react";
import { Button } from "../ui/Button";

type Props = {
  children: React.ReactNode;
};

const AppLayout: React.FC<Props> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-primary-base text-text-neutral font-sans selection:bg-ai-highlight1 selection:text-primary-base">
      <header className="border-b border-white/10 backdrop-blur-md bg-primary-base/80 sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-12">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-action-primary flex items-center justify-center shadow-lg shadow-action-primary/20">
                <span className="text-white font-bold text-lg italic">D</span>
              </div>
              <h1 className="text-xl font-bold tracking-tight text-white">
                DocVision <span className="text-text-secondary font-normal">AI</span>
              </h1>
            </div>

            {/* Navigation Links */}
            <nav className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm font-semibold text-white relative group">
                Features
                <span className="absolute -bottom-[21px] left-0 w-full h-0.5 bg-white scale-x-100 transition-transform" />
              </a>
              <a href="#pricing" className="text-sm font-semibold text-text-secondary hover:text-white transition-colors">Pricing</a>
              <a href="#docs" className="text-sm font-semibold text-text-secondary hover:text-white transition-colors">API Docs</a>
              <a href="#about" className="text-sm font-semibold text-text-secondary hover:text-white transition-colors">About</a>
            </nav>
          </div>

          <div className="flex items-center gap-6">
            <button className="hidden sm:block text-sm font-semibold text-text-secondary hover:text-white transition-colors">
              Login
            </button>
            <Button size="sm" className="bg-action-primary hover:bg-action-hover text-white rounded-lg px-6 py-2 text-sm font-bold shadow-lg shadow-action-primary/25 transition-all">
              Sign Up
            </Button>
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
