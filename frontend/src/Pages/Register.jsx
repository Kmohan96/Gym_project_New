import { useState } from "react";
import api from "../Api/Axios";
import "../Styles/Auth.css";

function Register() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    age: "",
    height: "",
    weight: "",
    goal: "weight_loss",
    gym_type: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    // ✅ Validations
    if (form.username.trim().length < 3) {
      alert("Username must be at least 3 characters");
      return;
    }

    if (form.password.length < 6) {
      alert("Password must be at least 6 characters");
      return;
    }

    if (!form.age || form.age < 10 || form.age > 100) {
      alert("Enter a valid age (10–100)");
      return;
    }

    if (!form.height || form.height < 50 || form.height > 300) {
      alert("Enter a valid height in cm (50–300)");
      return;
    }

    if (!form.weight || form.weight < 20 || form.weight > 300) {
      alert("Enter a valid weight in kg (20–300)");
      return;
    }

    if (!form.gym_type.trim()) {
      alert("Gym type is required");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post("/api/accounts/register/", form);

      alert("Registration successful. Please login.");
      window.location.href = "/login";
    } catch (err) {
      console.error(err.response?.data);
      alert("Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>User Register</h2>

        <form onSubmit={handleRegister}>
          <input name="username" placeholder="Username" onChange={handleChange} disabled={loading} required />
          <input name="password" type="password" placeholder="Password" onChange={handleChange} disabled={loading} required />
          <input name="age" type="number" placeholder="Age" onChange={handleChange} disabled={loading} required />
          <input name="height" type="number" placeholder="Height (cm)" onChange={handleChange} disabled={loading} required />
          <input name="weight" type="number" placeholder="Weight (kg)" onChange={handleChange} disabled={loading} required />

          <select name="goal" onChange={handleChange} disabled={loading}>
            <option value="weight_loss">Weight Loss</option>
            <option value="muscle_gain">Muscle Gain</option>
            <option value="fitness">General Fitness</option>
          </select>

          <input name="gym_type" placeholder="Gym Type" onChange={handleChange} disabled={loading} required />

          <button type="submit" disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </button>

          {loading && <div className="spinner"></div>}

          <p className="auth-switch">
            Already registered?{" "}
            <span className="auth-link" onClick={() => (window.location.href = "/login")}>
              Login
            </span>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Register;
