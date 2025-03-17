import React from 'react';
import Chat from './components/Chat'; // Assuming the Chat component is in the components folder

const Start: React.FC = () => {
  return (
    <div>
      <h1>Basic Chat with Ollama</h1>
      <Chat />
    </div>
  );
};

export default Start;