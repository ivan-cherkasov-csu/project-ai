import React, { useEffect, useState } from "react";
import axios from "axios";
import ProjectControl from "./ProjectControl";
import ThemeToggle from "./ThemeToggle";

interface Task {
  id: number;
  name: string;
  description: string;
}

interface Resource {
  id?: number; // Optional for new resources
  name: string;
  project_id: number;
  description: string;
}

interface Project {
  id: number;
  name: string;
  description: string;
  tasks: Task[];
  resources: Resource[];
}


const ProjectList: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  // Function to handle updated project
  const handleProjectUpdate = (updatedProject: Project) => {
    setProjects((prevProjects) =>
      prevProjects.map((project) =>
        project.id === updatedProject.id ? updatedProject : project
      )
    );
  };

  const handleDelete = (projectId: number) => {
    setProjects((prevProjects) => prevProjects.filter((project) => project.id !== projectId));
  };


  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get<Project[]>("http://localhost:8000/projects");
        setProjects(response.data);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch projects");
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  if (loading) {
    return <div className="text-center mt-10 text-black dark:text-white">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 dark:text-red-300">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-black dark:text-white">Projects</h1>
      </div>
      <ThemeToggle/>
      {projects.map((project) => (
        <ProjectControl
          key={project.id}
          project={project}
          onDelete={handleDelete}
          onProjectUpdate={handleProjectUpdate} // Pass the callback
        />
      ))}

    </div>
  );
};


export default ProjectList;