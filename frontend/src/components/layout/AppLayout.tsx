import React from "react";

type Props = {
  children: React.ReactNode;
};

const AppLayout: React.FC<Props> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-semibold text-slate-900">
            DocVision AI
          </h1>
          <span className="text-xs text-slate-500">
            Intelligent OCR SaaS Platform
          </span>
        </div>
      </header>

      <main className="flex-1 mx-auto max-w-5xl px-4 py-8">
        {children}
      </main>

      <footer className="border-t bg-white">
        <div className="mx-auto max-w-5xl px-4 py-3 text-xs text-slate-500 text-right">
          © {new Date().getFullYear()} DocVision AI
        </div>
      </footer>
    </div>
  );
};

export default AppLayout;

