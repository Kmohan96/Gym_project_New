import { useState } from "react";
import api from "../Api/Axios";
import NavbarUser from "../Components/NavbarUser";
import Footer from "../Components/Footer";
import "../Styles/Layouts.css";

function UserLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // 🔐 JWT login (JSON)
      const res = await api.post("/api/token/", {
        username,
        password,
      });

      // ✅ store JWT
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      // 🔹 optional: check approval via profile API
      const profile = await api.get("/api/accounts/profile/");

      if (!profile.data.approved) {
        alert("Your account is not approved yet");
        localStorage.clear();
        return;
      }

      // ✅ redirect
      window.location.href = "/user-dashboard";
    } catch (err) {
      alert("Invalid username or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <NavbarUser />

      <div
        className="page-content"
        style={{
          margin: "auto",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          border: "2px solid #1d2671",
          borderRadius: "12px",
          padding: "20px",
          minHeight: "300px",
        }}
      >
        <form onSubmit={handleLogin}>
          <h1 style={{ textAlign: "center" }}>User Login</h1>

          <input
            placeholder="Username"
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

      <Footer />
    </div>
  );
}

export default UserLogin;
