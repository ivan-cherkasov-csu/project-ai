import React, { useState } from "react";
import axios from "axios";

interface Resource {
  id?: number; // Optional for new resources
  name: string;
  project_id: number;
  description: string;
}

interface ResourceControlProps {
  resource: Resource; // New resource passed from ProjectControl
  onClose: () => void; // Function to close the modal
  onSave: (savedResource: Resource) => void; // Callback to return saved resource to ProjectControl
}

const ResourceControl: React.FC<ResourceControlProps> = ({ resource, onClose, onSave }) => {
  const [editedResource, setEditedResource] = useState<Resource>(resource);

  const handleSave = async () => {
    try {
      console.log(JSON.stringify(editedResource))
      const response = await axios.post<Resource>("http://localhost:8000/resource", editedResource);
      onSave(response.data); // Pass the saved resource back to ProjectControl
      onClose(); // Close the modal
    } catch (error) {
      console.error("Failed to save resource:", error);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="block w-full border p-2 mb-2 rounded dark:bg-gray-700 dark:text-white w-1/2">
        <h2 className="text-xl font-bold mb-4">Add Resource</h2>
        <div className="mb-4">
          <label className="block text-gray-700">Name</label>
          <input
            type="text"
            value={editedResource.name}
            onChange={(e) => setEditedResource({ ...editedResource, name: e.target.value })}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Description</label>
          <textarea
            value={editedResource.description}
            onChange={(e) => setEditedResource({ ...editedResource, description: e.target.value })}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="flex justify-end">
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

export default ResourceControl;