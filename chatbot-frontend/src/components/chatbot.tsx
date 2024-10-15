"use client";

import { useState } from "react";

type Message = {
  role: "user" | "bot";
  content: string;
};

const fetchChatResponse = async (prompt: string) => {
  const response = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch from API");
  }

  return response.json();
};

const MessageBox = ({ msg }: { msg: Message }) => (
  <div
    className={`my-2 p-2 rounded ${
      msg.role === "user"
        ? "bg-blue-600 text-white self-end"
        : "bg-gray-800 text-white self-start"
    }`}
  >
    {msg.content}
  </div>
);

const Chatbot = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() === "") return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const data = await fetchChatResponse(input);
      const botMessage: Message = { role: "bot", content: data.response };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error fetching from API:", error);
    }

    setInput("");
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 items-center">
      <div className="flex flex-col w-full max-w-4xl h-full bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="flex-1 p-4 overflow-y-auto flex flex-col">
          {messages.map((msg, index) => (
            <MessageBox key={index} msg={msg} />
          ))}
        </div>
        <form onSubmit={sendMessage} className="p-4 bg-gray-200 flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 p-2 border border-gray-400 rounded text-black bg-white"
            placeholder="Type your message..."
          />
          <button
            type="submit"
            className="ml-2 p-2 bg-blue-700 text-white rounded"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chatbot;
