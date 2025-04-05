import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ResourceControl from "./ResourceControl";
import ChatSidebar from "./ChatSidebar";
import TaskControl from "./TaskControl"; // Import TaskControl
import axios from "axios";
import { Project, Task, Resource } from "../models/interfaces";

interface ProjectProps {
  project: Project;
  onDelete: (projectId: number) => void; // Callback to remove project from parent state
  onProjectUpdate: (updatedProject: Project) => void; // Callback for updating project
}

const ProjectControl: React.FC<ProjectProps> = ({ project, onDelete, onProjectUpdate }) => {
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [editedProject, setEditedProject] = useState<Project>(project);
  const [showResourceModal, setShowResourceModal] = useState<boolean>(false);
  const [resources, setResources] = useState<Resource[]>(project.resources);
  const [tasks, setTasks] = useState<Task[]>(project.tasks); // Manage tasks locally
  const [showTaskModal, setShowTaskModal] = useState<boolean>(false); // State for task modal
  const [showChat, setShowChat] = useState<boolean>(false);

  const handleAddResource = (savedResource: Resource) => {
    setResources((prevResources) => [...prevResources, savedResource]); // Add the new resource to the list
  };

  const handleAddTask = (savedTask: Task) => {
    setTasks((prevTasks) => [...prevTasks, savedTask]); // Add the new task to the list
  };

  const navigate = useNavigate();

  const handleEdit = async () => {
    try {
      const response = await axios.patch("http://localhost:8000/project", editedProject);
      console.log("Project updated:", response.data);
      onProjectUpdate(response.data); // Pass the updated project to the parent
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update project:", error);
    }
  };

  const handleDelete = async () => {
    try {
      const response = await axios.delete("http://localhost:8000/project", {
        data: project, // Send the full project object in the body
      });
      onDelete(project.id); // Notify parent to remove the project
      console.log("Project deleted successfully:", response.data);
    } catch (error) {
      console.error("Failed to delete project:", error);
    }
  };

  return (
    <div className="border p-4 rounded shadow-md bg-white dark:bg-gray-800 dark:border-gray-700 mb-4">
      {isEditing ? (
        <div>
          <input
            type="text"
            value={editedProject.name}
            onChange={(e) => setEditedProject({ ...editedProject, name: e.target.value })}
            className="block w-full border p-2 mb-2 rounded dark:bg-gray-700 dark:text-white"
          />
          <textarea
            value={editedProject.description}
            onChange={(e) => setEditedProject({ ...editedProject, description: e.target.value })}
            className="block w-full border p-2 rounded dark:bg-gray-700 dark:text-white"
          />
          <button
            onClick={handleEdit}
            className="px-4 py-2 mr-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Save
          </button>
          <button
            onClick={() => setIsEditing(false)}
            className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 dark:bg-gray-600 dark:text-white"
          >
            Cancel
          </button>
        </div>
      ) : (
        <div>
          <h2 className="text-xl font-semibold text-black dark:text-white">{project.name}</h2>
          <p className="text-gray-600 dark:text-gray-400">{project.description}</p>

          <h3 className="text-lg font-medium text-black dark:text-white mt-4">Tasks:</h3>
          <ul className="list-disc pl-5">
            {tasks.map((task) => (
              <li key={task.id} className="text-gray-700 dark:text-gray-300">
                {task.name}
              </li>
            ))}
          </ul>
          <button
            onClick={() => setShowTaskModal(true)} // Open the task modal
            className="px-4 py-2 mt-4 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Add Task
          </button>

          {showTaskModal && (
            <TaskControl
              task={{
                id: -1,
                name: "",
                project_id: project.id,
                description: "",
                acceptance_criteria: "",
                priority: "NORMAL",
              }}
              onClose={() => setShowTaskModal(false)} // Close the modal
              onSave={handleAddTask} // Add the new task to the list
            />
          )}

          <h3 className="text-lg font-medium text-black dark:text-white mt-4">Resources:</h3>
          <ul className="list-disc pl-5">
            {resources.map((resource) => (
              <li key={resource.id} className="text-gray-700 dark:text-gray-300">
                {resource.name}
              </li>
            ))}
          </ul>
          <button
            onClick={() => setShowResourceModal(true)}
            className="px-4 py-2 mt-4 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Add Resource
          </button>

          {showResourceModal && (
            <ResourceControl
              resource={{ id: -1, name: "", project_id: project.id, description: "" }} // Pass new resource
              onClose={() => setShowResourceModal(false)}
              onSave={handleAddResource}
            />
          )}
          <div className="mt-4">
            <button
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 mr-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Delete
            </button>
          </div>
          <button
            onClick={() => setShowChat(!showChat)}
            className="px-4 py-2 mt-4 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            {showChat ? "Hide Chat" : "Show Chat"}
          </button>

          {showChat && (
            <div className="mt-4">
              <ChatSidebar attached={project} /> {/* Pass the project as the attached object */}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ProjectControl;
