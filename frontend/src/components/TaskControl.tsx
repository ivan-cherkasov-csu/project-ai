import React, { useState } from "react";
import axios from "axios";

interface Task {
    id?: number; // Optional for new tasks
    name: string;
    project_id: number;
    description: string;
    acceptance_criteria: string;
    priority: "LOW" | "NORMAL" | "HIGH" | "CRITICAL"; // Matches FastAPI Enum
}
interface TaskControlProps {
    task: Task; // Optional for new tasks
    onClose: () => void; // Callback for updating task   
    onSave: (task: Task) => void; // Callback for deleting task
}
const TaskControl: React.FC<TaskControlProps> = ({ task, onClose, onSave }) => {
    const [editedTask, setTask] = useState<Task>(task);

    const handleSave = async () => {
        try {
            const response = await axios.post("http://localhost:8000/task", task);
            onSave(response.data); // Pass the saved resource back to ProjectControl
            onClose(); // Close the modal
        } catch (error) {
            console.error("Failed to create task:", error);
        }
    };

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="block w-full border p-2 mb-2 rounded dark:bg-gray-700 dark:text-white w-1/2">
                <div className="container mx-auto p-4">
                    <h1 className="text-2xl font-bold mb-4">Add Task</h1>
                    <div className="mb-4">
                        <label className="block text-gray-700">Task Name</label>
                        <input
                            type="text"
                            value={editedTask.name}
                            onChange={(e) => setTask({ ...editedTask, name: e.target.value })}
                            className="w-full border rounded px-3 py-2"
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-gray-700">Description</label>
                        <textarea
                            value={editedTask.description}
                            onChange={(e) => setTask({ ...editedTask, description: e.target.value })}
                            className="w-full border rounded px-3 py-2"
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-gray-700">Acceptance Criteria</label>
                        <textarea
                            value={editedTask.acceptance_criteria}
                            onChange={(e) => setTask({ ...editedTask, acceptance_criteria: e.target.value })}
                            className="w-full border rounded px-3 py-2"
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-gray-700">Priority</label>
                        <select
                            value={editedTask.priority}
                            onChange={(e) => setTask({ ...editedTask, priority: e.target.value as Task["priority"] })}
                            className="w-full border rounded px-3 py-2"
                        >
                            <option value="LOW">Low</option>
                            <option value="NORMAL">Normal</option>
                            <option value="HIGH">High</option>
                            <option value="CRITICAL">Critical</option>
                        </select>
                    </div>
                    <button
                        onClick={onClose}
                        className="px-4 py-2 mr-4 bg-gray-300 rounded hover:bg-gray-400"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={handleSave}
                        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                        Save
                    </button>
                </div>
            </div>
        </div>
    );
};

export default TaskControl;