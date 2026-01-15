import React, { useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import HomePage from "./pages/Home/HomePage";
import UploadPage from "./pages/Upload/UploadPage";

type Page = "home" | "upload";

const App: React.FC = () => {
  const [page, setPage] = useState<Page>("home");

  return (
    <AppLayout>
      <div className="mb-6 flex gap-2">
        <button
          className={`px-3 py-1 rounded text-sm ${
            page === "home"
              ? "bg-slate-900 text-white"
              : "bg-slate-200 text-slate-800"
          }`}
          onClick={() => setPage("home")}
        >
          Home
        </button>
        <button
          className={`px-3 py-1 rounded text-sm ${
            page === "upload"
              ? "bg-slate-900 text-white"
              : "bg-slate-200 text-slate-800"
          }`}
          onClick={() => setPage("upload")}
        >
          Upload
        </button>
      </div>

      {page === "home" && <HomePage />}
      {page === "upload" && <UploadPage />}
    </AppLayout>
  );
};

export default App;

