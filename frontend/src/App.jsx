import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { useState } from "react";

import HomePage from "./pages/HomePage";
import TrendsPage from "./pages/TrendsPage";
import ReflectionPage from "./pages/ReflectionPage";
import SimulationPage from "./pages/SimulationPage";
import ChatbotPage from "./pages/ChatbotPage";
import SettingsPage from "./pages/SettingsPage";

export default function App() {

  const [cyclePhase, setCyclePhase] = useState("follicular");
  const [predictionInfo, setPredictionInfo] = useState(null);
  const [availableUsers] = useState([1]);
  const [selectedUser, setSelectedUser] = useState(1);

  const navStyle = {
    display: "flex",
    justifyContent: "center",
    gap: "28px",
    padding: "14px",
    background: "rgba(255,255,255,0.35)",
    backdropFilter: "blur(10px)",
    borderBottom: "1px solid rgba(255,255,255,0.4)",
    position: "sticky",
    top: 0,
    zIndex: 1000,
    fontFamily: "var(--font-body)"
  };

  const linkStyle = {
    textDecoration: "none",
    fontSize: "0.8rem",
    fontWeight: 500,
    color: "var(--text-secondary)"
  };

  return (
    <BrowserRouter>

      {/* Navigation Bar */}
      <nav style={navStyle}>
        <Link style={linkStyle} to="/">Home</Link>
        <Link style={linkStyle} to="/trends">Trends</Link>
        <Link style={linkStyle} to="/reflection">Reflection</Link>
        <Link style={linkStyle} to="/simulate">Simulate</Link>
        <Link style={linkStyle} to="/chat">Chat</Link>
        <Link style={linkStyle} to="/settings">Settings</Link>
      </nav>

      <Routes>

        <Route
          path="/"
          element={
            <HomePage
              cyclePhase={cyclePhase}
              onCyclePhaseChange={setCyclePhase}
              predictionInfo={predictionInfo}
              availableUsers={availableUsers}
              selectedUser={selectedUser}
              onUserChange={setSelectedUser}
            />
          }
        />

        <Route path="/trends" element={<TrendsPage />} />
        <Route path="/reflection" element={<ReflectionPage />} />
        <Route path="/simulate" element={<SimulationPage />} />
        <Route path="/chat" element={<ChatbotPage />} />
        <Route path="/settings" element={<SettingsPage />} />

      </Routes>

    </BrowserRouter>
  );
}
