"use client"
import React, { useState } from 'react';

const Chat: React.FC = (): React.ReactElement => {
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { text: input, isUser: true }]);

    try {
      const response = await fetch('/api/ollama-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: input }),
      });
      
      const data = await response.json();

      console.log(data);

      if (data.error) {
        throw new Error(data.error);
      }

      setMessages((prev) => [...prev, { text: data.response, isUser: false }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        { text: 'Error fetching response. Please try again.', isUser: false },
      ]);
    }

    setInput('');
  };

  return (
    <div>
      <div style={{ height: '300px', overflowY: 'scroll', border: '1px solid #ccc', padding: '1rem' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.isUser ? 'right' : 'left' }}>
            <p
              style={{
                background: msg.isUser ? '#daf8cb' : '#f0f0f0',
                display: 'inline-block',
                padding: '0.5rem',
                borderRadius: '10px',
              }}
            >
              {msg.text}
            </p>
          </div>
        ))}
      </div>
      <div style={{ marginTop: '1rem' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{ width: '80%', padding: '0.5rem', marginRight: '0.5rem' }}
        />
        <button onClick={sendMessage} style={{ padding: '0.5rem' }}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;