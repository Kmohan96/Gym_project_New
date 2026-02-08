import { useState } from "react";
import api from "../Api/Axios";
import "../Styles/TrainerLogin.css";

function TrainerLogin() {
  const [username, setUsername] = useState(""); // trainer username
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      alert("Username and Password required");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post("/api/token/", {
        username,
        password,
      });

      // ✅ store JWT
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      // ✅ redirect
      window.location.href = "/trainer-dashboard";
    } catch (err) {
      alert("Trainer login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="trainer-login-page">
      <div className="trainer-login-card">
        <h2>Trainer Login</h2>

        <form onSubmit={handleLogin}>
          <input
            placeholder="Trainer Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={loading}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>

          {loading && <div className="spinner"></div>}
        </form>
      </div>
    </div>
  );
}

export default TrainerLogin;
