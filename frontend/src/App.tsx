import React, { useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import HomePage from "./pages/Home/HomePage";
import UploadPage from "./pages/Upload/UploadPage";

type Page = "home" | "upload";

const App: React.FC = () => {
  const [page, setPage] = useState<Page>("home");

  return (
    <AppLayout onNavigate={(p: Page) => setPage(p)} currentPage={page}>
      {page === "home" && <HomePage onNavigate={(p) => setPage(p)} />}
      {page === "upload" && <UploadPage />}
    </AppLayout>
  );
};

export default App;
