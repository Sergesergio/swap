"use client";

import { useEffect, useState } from "react";
import { chatApi } from "@/lib/api-client";
import { useChatStore } from "@/stores/chat.store";
import { LoadingSpinner, EmptyState } from "@/components/LoadingStates";

export default function ChatPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [conversations, setConversations] = useState<any[]>([]);
  const [selectedChat, setSelectedChat] = useState<string | null>(null);
  const messages = useChatStore((state) => state.messages);
  const addMessage = useChatStore((state) => state.addMessage);
  const [messageText, setMessageText] = useState("");

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await chatApi.getConversations();
        const data = response.data.data || response.data;
        setConversations(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Failed to fetch conversations:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchConversations();
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageText.trim() || !selectedChat) return;

    try {
      await chatApi.sendMessage(selectedChat, messageText);
      setMessageText("");
      // In a real app, fetch new messages or use WebSocket
    } catch (error) {
      console.error("Failed to send message:", error);
    }
  };

  return (
    <main className="min-h-screen bg-white dark:bg-dark-900 flex">
      {/* Conversations Sidebar */}
      <div className="w-full md:w-80 bg-gray-50 dark:bg-dark-800 border-r border-gray-200 dark:border-dark-700 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 dark:border-dark-700">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Messages
          </h2>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto">
          {isLoading ? (
            <div className="p-4">
              <LoadingSpinner />
            </div>
          ) : conversations.length > 0 ? (
            <div className="space-y-1 p-2">
              {conversations.map((conv) => (
                <button
                  key={conv.id}
                  onClick={() => setSelectedChat(conv.id)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    selectedChat === conv.id
                      ? "bg-primary-600 text-white"
                      : "text-gray-900 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-dark-700"
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-sm">Conversation</h3>
                      <p
                        className={`text-xs mt-1 truncate ${
                          selectedChat === conv.id
                            ? "text-blue-100"
                            : "text-gray-600 dark:text-gray-400"
                        }`}
                      >
                        {conv.last_message?.content || "No messages yet"}
                      </p>
                    </div>
                    {conv.unread_count > 0 && (
                      <span className="bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center ml-2">
                        {conv.unread_count}
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="p-4">
              <EmptyState
                title="No conversations"
                description="Start a conversation by making an offer!"
              />
            </div>
          )}
        </div>
      </div>

      {/* Chat Area */}
      <div className="hidden md:flex flex-1 flex-col bg-white dark:bg-dark-900">
        {selectedChat ? (
          <>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.length > 0 ? (
                messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${
                      msg.sender_id === "current-user"
                        ? "justify-end"
                        : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-xs px-4 py-2 rounded-lg ${
                        msg.sender_id === "current-user"
                          ? "bg-primary-600 text-white"
                          : "bg-gray-200 dark:bg-dark-700 text-gray-900 dark:text-white"
                      }`}
                    >
                      <p className="text-sm">{msg.content}</p>
                      <p
                        className={`text-xs mt-1 ${
                          msg.sender_id === "current-user"
                            ? "text-blue-100"
                            : "text-gray-600 dark:text-gray-400"
                        }`}
                      >
                        {new Date(msg.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="flex items-center justify-center h-full">
                  <p className="text-gray-600 dark:text-gray-400">
                    Start a conversation
                  </p>
                </div>
              )}
            </div>

            {/* Input */}
            <form
              onSubmit={handleSendMessage}
              className="p-4 border-t border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-900"
            >
              <div className="flex gap-2">
                <input
                  type="text"
                  value={messageText}
                  onChange={(e) => setMessageText(e.target.value)}
                  placeholder="Type a message..."
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors"
                >
                  Send
                </button>
              </div>
            </form>
          </>
        ) : (
          <div className="flex items-center justify-center h-full">
            <EmptyState
              title="Select a conversation"
              description="Choose a conversation from the sidebar to start messaging"
            />
          </div>
        )}
      </div>
    </main>
  );
}
