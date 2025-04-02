import React, { useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

interface Task {
    id?: number; // Optional for new tasks
    name: string;
    project_id: number;
    description: string;
    acceptance_criteria: string;
    priority: "LOW" | "NORMAL" | "HIGH" | "CRITICAL"; // Matches FastAPI Enum
}

const TaskControl: React.FC = () => {
    const { projectId } = useParams<{ projectId: string }>(); // Capture projectId from URL
    const navigate = useNavigate();

    const [task, setTask] = useState<Task>({
        id: 0,
        name: "",
        project_id: parseInt(projectId || "0"), // Convert projectId to number
        description: "",
        acceptance_criteria: "",
        priority: "NORMAL",
    });

    const handleSave = async () => {
        try {
            console.log(JSON.stringify(task))
            const response = await axios.post("http://localhost:8000/task", task);
            console.log("Task created:", response.data);
            navigate("/"); // Navigate back to ProjectList after saving
        } catch (error) {
            console.error("Failed to create task:", error);
        }
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Add Task</h1>
            <div className="mb-4">
                <label className="block text-gray-700">Task Name</label>
                <input
                    type="text"
                    value={task.name}
                    onChange={(e) => setTask({ ...task, name: e.target.value })}
                    className="w-full border rounded px-3 py-2"
                />
            </div>
            <div className="mb-4">
                <label className="block text-gray-700">Description</label>
                <textarea
                    value={task.description}
                    onChange={(e) => setTask({ ...task, description: e.target.value })}
                    className="w-full border rounded px-3 py-2"
                />
            </div>
            <div className="mb-4">
                <label className="block text-gray-700">Acceptance Criteria</label>
                <textarea
                    value={task.acceptance_criteria}
                    onChange={(e) => setTask({ ...task, acceptance_criteria: e.target.value })}
                    className="w-full border rounded px-3 py-2"
                />
            </div>
            <div className="mb-4">
                <label className="block text-gray-700">Priority</label>
                <select
                    value={task.priority}
                    onChange={(e) => setTask({ ...task, priority: e.target.value as Task["priority"] })}
                    className="w-full border rounded px-3 py-2"
                >
                    <option value="LOW">Low</option>
                    <option value="NORMAL">Normal</option>
                    <option value="HIGH">High</option>
                    <option value="CRITICAL">Critical</option>
                </select>
            </div>
            <button
                onClick={handleSave}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
                Save
            </button>
        </div>
    );
};

export default TaskControl;