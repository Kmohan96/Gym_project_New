import { useEffect, useState } from "react";
import api from "../Api/Axios";
import NavbarUser from "../Components/NavbarUser";
import Footer from "../Components/Footer";
import "../Styles/Layout.css";
import "../Styles/UserAdding.css";

function UserDashboard() {
  const [data, setData] = useState(null);
  const [updates, setUpdates] = useState([]);
  const [presentDays, setPresentDays] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // ✅ Fetch user profile (JWT based)
    api.get("/api/accounts/profile/")
      .then((res) => {
        setData(res.data);
      })
      .catch((err) => {
        if (err.response?.status === 403) {
          alert("Your account is not approved yet");
        } else if (err.response?.status === 401) {
          alert("Session expired. Please login again.");
          localStorage.clear();
          window.location.href = "/login";
        } else {
          alert("Failed to load profile");
        }
      });

    // ✅ Fetch daily updates (JWT based)
    api.get("/api/accounts/user/updates/")
      .then((res) => {
        setUpdates(res.data.updates || []);
        setPresentDays(res.data.present_days || 0);
      })
      .catch(() => {
        console.log("No daily updates yet");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="loading-text">Loading...</p>;
  if (!data) return null;

  const gymImages = [
    "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200",
    "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1200",
    "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1200",
  ];

  return (
    <div className="app-container">
      <NavbarUser />

      <div className="page-content">

        {/* Hero Carousel */}
        <div className="hero-carousel">
          {gymImages.map((img, i) => (
            <div key={i} className="hero-slide">
              <img src={img} alt={`Gym ${i + 1}`} className="hero-img" />
              <div className="hero-overlay">
                <h1 className="hero-title">Welcome, {data.username}!</h1>
                <p className="hero-subtitle">Your fitness journey starts here.</p>
              </div>
            </div>
          ))}
        </div>

        {!data.approved ? (
          <div className="card warning-card">
            <p>Your account is waiting for admin approval.</p>
          </div>
        ) : (
          <div className="dashboard-grid">

            {/* Profile Card */}
            <div className="card info-card">
              <h3>Profile</h3>
              <p><b>Username:</b> {data.username}</p>
              <p><b>Goal:</b> {data.goal}</p>
              <p>
                <b>Status:</b>{" "}
                <span className="status-approved">Approved</span>
              </p>
              <p><b>Trainer:</b> {data.trainer || "Not assigned yet"}</p>
            </div>

            {/* Attendance Card */}
            <div className="card stats-card">
              <h3>Monthly Attendance</h3>
              <div className="stat-item">
                <span className="stat-label">Present Days</span>
                <span className="stat-value">{presentDays}</span>
              </div>
            </div>

            {/* Daily Updates */}
            <div className="card updates-card">
              <h3>Daily Updates</h3>

              {updates.length === 0 ? (
                <p className="empty-text">No daily updates yet</p>
              ) : (
                <div className="updates-list">
                  {updates.map((u, i) => (
                    <div key={i} className="update-item">
                      <p><b>Date:</b> {u.date}</p>
                      <p><b>Diet:</b> {u.diet}</p>
                      <p>
                        <b>Attendance:</b>{" "}
                        {u.attendance ? "Present" : "Absent"}
                      </p>
                      <p><b>Notes:</b> {u.description}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}

export default UserDashboard;
