import { useEffect, useState } from "react";
import api from "../Api/Axios";
import Navbar from "../Components/Navbar";

function AdminCreateTrainer() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [trainerId, setTrainerId] = useState("");

  // 🔹 Load users created by admin
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await api.get("/api/accounts/users/");
        setUsers(res.data.users);
      } catch (err) {
        alert("Failed to load users");
      }
    };

    fetchUsers();
  }, []);

  // 🔹 Create trainer
  const handleCreate = async (e) => {
    e.preventDefault();

    if (!selectedUser || !trainerId) {
      alert("Select user and enter trainer ID");
      return;
    }

    try {
      const res = await api.post("/api/accounts/trainer/create/", {
        username: selectedUser,
        trainer_id: trainerId,
      });

      alert(res.data.message);
      setTrainerId("");
      setSelectedUser("");
    } catch (err) {
      alert("Trainer creation failed");
    }
  };

  return (
    <div>
      <Navbar />
      <h2>Create Trainer</h2>

      <form onSubmit={handleCreate}>
        <select
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
        >
          <option value="">Select User</option>
          {users.map((u, index) => (
            <option key={index} value={u.username}>
              {u.username}
            </option>
          ))}
        </select>

        <input
          placeholder="Trainer ID (T001)"
          value={trainerId}
          onChange={(e) => setTrainerId(e.target.value)}
        />

        <button type="submit">Create Trainer</button>
      </form>
    </div>
  );
}

export default AdminCreateTrainer;
