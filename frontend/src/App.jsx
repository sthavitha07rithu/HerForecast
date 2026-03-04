import { useState } from "react";
import HomePage from "./pages/HomePage";

export default function App() {
  const [cyclePhase, setCyclePhase] = useState("follicular");
  const [predictionInfo, setPredictionInfo] = useState(null);
  const [availableUsers] = useState([1]);
  const [selectedUser, setSelectedUser] = useState(1);

  return (
    <HomePage
      cyclePhase={cyclePhase}
      onCyclePhaseChange={setCyclePhase}
      predictionInfo={predictionInfo}
      availableUsers={availableUsers}
      selectedUser={selectedUser}
      onUserChange={setSelectedUser}
    />
  );
}
