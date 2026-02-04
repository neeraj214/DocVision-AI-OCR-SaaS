import React from "react";

type Props = {
  children: React.ReactNode;
};

const AppLayout: React.FC<Props> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-primary-base text-text-neutral font-sans selection:bg-ai-highlight1 selection:text-primary-base">
      <header className="border-b border-white/10 backdrop-blur-md bg-primary-base/80 sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-action-primary to-ai-highlight1 flex items-center justify-center">
              <span className="text-white font-bold text-lg">D</span>
            </div>
            <h1 className="text-xl font-bold tracking-tight text-white">
              DocVision <span className="text-action-primary">AI</span>
            </h1>
          </div>
          <span className="text-xs font-medium px-2 py-1 rounded-full bg-white/5 text-text-secondary border border-white/10">
            v1.0.0 Beta
          </span>
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
