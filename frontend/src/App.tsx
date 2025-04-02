import './app.css';
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProjectList from "./components/ProjectList";
import TaskControl from "./components/TaskControl";
import ChatControl from "./components/ChatControl"; // Import the ChatControl component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ProjectList />} />
        <Route path="/task/:projectId" element={<TaskControl />} />
        <Route path="/chat" element={<ChatControl />} /> {/* Add ChatControl route */}
      </Routes>
    </Router>
  );
}

export default App;
