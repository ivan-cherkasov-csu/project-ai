import React, { useState } from "react";
import axios from "axios";
import { ChatQuery, ChatResponse, Project, Task, Resource } from "../models/interfaces";

interface ChatSidebarProps {
  attached?: Project | Task | Resource | null; // Optional attached object
}

const ChatSidebar: React.FC<ChatSidebarProps> = ({ attached = null }) => {
  const [textareaContent, setTextareaContent] = useState<string>(""); // Conversation history
  const [query, setQuery] = useState<string>(""); // Input for the query

  const handleSend = async () => {
    if (!query.trim()) return; // Prevent sending empty queries

    const chatQuery: ChatQuery = { query, attached };

    try {
      const response = await axios.post<ChatResponse>("http://localhost:8000/chat", chatQuery);
      const receivedAnswer = response.data.answer;

      // Append query and answer to the textarea content
      setTextareaContent((prev) =>
        prev + `\nUser: ${query}\nAI: ${receivedAnswer}\n`
      );
      setQuery(""); // Clear the input field
    } catch (error) {
      console.error("Error communicating with the server:", error);
    }
  };

  return (
    <div className="flex flex-col h-full w-full">
      {/* Textarea for displaying chat history */}
      <textarea
        value={textareaContent}
        readOnly
        className="flex-grow border rounded p-2 resize-none bg-gray-100 dark:bg-gray-800 dark:text-white"
      />

      {/* Panel with input and button */}
      <div className="p-4 border-t flex justify-between items-center bg-white dark:bg-gray-700">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your query here..."
          className="flex-grow border rounded p-2 mr-4 bg-gray-100 dark:bg-gray-800 dark:text-white"
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatSidebar;