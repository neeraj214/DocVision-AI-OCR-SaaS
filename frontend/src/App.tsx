import React, { useEffect, useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import HomePage from "./pages/Home/HomePage";
import UploadPage from "./pages/Upload/UploadPage";
import LoginPage from "./pages/Auth/LoginPage";
import RegisterPage from "./pages/Auth/RegisterPage";
import { getToken, isTokenExpired } from "./services/api";

type Page = "home" | "upload" | "login" | "register";

const App: React.FC = () => {
  const [page, setPage] = useState<Page>("home");

  useEffect(() => {
    const tok = getToken();
    if (page === "upload" && (!tok || isTokenExpired(tok))) {
      setPage("login");
    }
  }, [page]);

  return (
    <AppLayout onNavigate={(p: Page) => setPage(p)} currentPage={page}>
      {page === "home" && <HomePage onNavigate={(p) => setPage(p)} />}
      {page === "login" && <LoginPage onNavigate={(p) => setPage(p)} />}
      {page === "register" && <RegisterPage onNavigate={(p) => setPage(p)} />}
      {page === "upload" && <UploadPage />}
    </AppLayout>
  );
};

export default App;
