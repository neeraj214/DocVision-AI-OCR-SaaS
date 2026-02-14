import React, { useState, useEffect } from "react";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { login, getToken, isTokenExpired } from "../../services/api";

type Props = {
  onNavigate: (page: "home" | "upload" | "register") => void;
};

const LoginPage: React.FC<Props> = ({ onNavigate }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const tok = getToken();
    if (tok && !isTokenExpired(tok)) {
      onNavigate("upload");
    }
  }, [onNavigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      onNavigate("upload");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-white mb-6">Login</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-text-secondary mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-md bg-white/5 border border-white/10 px-3 py-2 text-white"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-text-secondary mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-md bg-white/5 border border-white/10 px-3 py-2 text-white"
              required
              minLength={8}
            />
          </div>
          {error && <div className="text-red-400 text-sm">{error}</div>}
          <div className="flex items-center justify-between">
            <Button type="submit" disabled={loading} className="bg-action-primary text-white">
              {loading ? "Signing in..." : "Login"}
            </Button>
            <Button variant="ghost" onClick={() => onNavigate("register")}>Create account</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default LoginPage;
