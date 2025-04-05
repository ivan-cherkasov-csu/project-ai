import React, { useEffect, useState } from "react";
import axios from "axios";
import ResourceControl from "./ResourceControl";
import { useParams } from "react-router-dom";

interface Resource {
  id?: number; // Optional for new resources
  name: string;
  project_id: number;
  description: string;
}

const ResourceList: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");
  const [showResourceModal, setShowResourceModal] = useState<boolean>(false);
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);

  const handleAddResource = (savedResource: Resource) => {
    setResources((prevResources) => [...prevResources, savedResource]); // Add the new resource to the list
  };

  const p_id = parseInt(projectId || "0"); // Convert projectId to number

  useEffect(() => {
    const fetchResources = async () => {
      try {
        let response;
        if (p_id > 0) {
          response = await axios.get<Resource[]>(`http://localhost:8000/resources/${p_id}`);
        } else {
          response = await axios.get<Resource[]>("http://localhost:8000/resources");
        }
        setResources(response.data);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch resources");
        setLoading(false);
      }
    };

    fetchResources();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="resource-list">
      {resources.map((resource) => (
        <div
          key={resource.id}
          className="resource-item border p-2 mb-2 rounded dark:bg-gray-700 dark:text-white"
          onClick={() => {
            setSelectedResource(resource);
            setShowResourceModal(true);
          }}
        >
          <h2 className="text-xl font-bold">{resource.name}</h2>
          <p>{resource.description}</p>
        </div>
      ))}
      {p_id > 0 && (
        <button
          onClick={() => {
            setSelectedResource({
              id: -1,
              name: "",
              project_id: p_id,
              description: "",
            });
            setShowResourceModal(true);
          }}
          className="bg-blue-500 text-white p-2 rounded"
        >
          Add Resource
        </button>
      )}
      {showResourceModal && selectedResource && (
        <ResourceControl
          resource={selectedResource}
          onClose={() => setShowResourceModal(false)}
          onSave={handleAddResource}
        />
      )}
    </div>
  );
};

export default ResourceList;