import { BrowserRouter, Routes, Route } from "react-router-dom";
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

  return (
    <BrowserRouter>
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
