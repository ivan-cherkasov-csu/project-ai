import React, { useEffect, useState } from "react";
import axios from "axios";
import TaskControl from "./TaskControl.tsx";
import { useParams } from "react-router-dom";

interface Task {
  id?: number; // Optional for new tasks
  name: string;
  project_id: number;
  description: string;
  acceptance_criteria: string;
  priority: "LOW" | "NORMAL" | "HIGH" | "CRITICAL"; // Matches FastAPI Enum
}
  
  const TaskList: React.FC = () => {
    const { projectId } = useParams<{ projectId: string }>();
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>("");
    const [showTaskModal, setShowTaskModal] = useState<boolean>(false);

    const handleAddTask = (savedTask: Task) => {
      setTasks((prevTasks) => [...prevTasks, savedTask]); // Add the new resource to the list
    };
    const p_id = parseInt(projectId || "0"); // Convert projectId to number
    useEffect(() => {
      const fetchTasks = async () => {
        try {
          let response;
          if (p_id > 0) {
             response = await axios.get<Task[]>("http://localhost:8000/tasks");
          } else {
               response = await axios.get<Task[]>(`http://localhost:8000/tasks/${p_id}`);
          }
          setTasks(response.data);
          setLoading(false);
        } catch (err) {
          setError("Failed to fetch tasks");
          setLoading(false);
        }
      };
  
      fetchTasks();
    }, []);
  
    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;
  
    return (
      <div className="task-list">
        {tasks.map((task) => (
          <div key={task.id} className="task-item border p-2 mb-2 rounded dark:bg-gray-700 dark:text-white"
            onClick={() => setShowTaskModal(true)}> // Open modal on task click
            <h2 className="text-xl font-bold">{task.name}</h2>
            <p>{task.description}</p>
            <p>Acceptance Criteria: {task.acceptance_criteria}</p>
            <p>Priority: {task.priority}</p>
          </div>
        ))}
        {(p_id > 0) && <button onClick={() => setShowTaskModal(true)} className="bg-blue-500 text-white p-2 rounded">Add Task</button> }
        {showTaskModal && (
          <TaskControl task={{id: -1, name: "", project_id: p_id, description: "", acceptance_criteria: "", priority: "NORMAL" } as Task} onClose={() => setShowTaskModal(false)} onSave={handleAddTask} />
        )} 
      </div>
    );
  }
  export default TaskList;