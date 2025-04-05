import React from "react";
import ChatSidebar from "./ChatSidebar";

const ChatControl: React.FC = () => {
  return (
    <div className="flex flex-col h-screen">
      <ChatSidebar /> {/* No attachments passed */}
    </div>
  );
};

export default ChatControl;