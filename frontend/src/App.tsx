import "./app.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar"; // Import Navbar
import ProjectList from "./components/ProjectList";
import TaskList from "./components/TaskList";
import ResourceList from "./components/ResourceList";
import ChatControl from "./components/ChatControl";

function App() {
  return (
    <Router>
      <div className="flex flex-col h-screen">
        {/* Navbar */}
        <Navbar />

        {/* Main Content */}
        <div className="flex-grow overflow-auto">
          <Routes>
            <Route path="/" element={<ProjectList />} />
            <Route path="/tasks/:projectId" element={<TaskList />} />
            <Route path="/resources/:projectId" element={<ResourceList />} />
            <Route path="/chat" element={<ChatControl />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
