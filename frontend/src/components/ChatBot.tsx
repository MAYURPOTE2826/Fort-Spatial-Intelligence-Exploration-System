import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Info, MapPin, X, MessageSquare, PlusCircle } from 'lucide-react';
import axios from 'axios';

interface Source {
  title: string;
  url?: string;
}

interface VisibleFort {
  name: string;
  distance: number;
  id?: number;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  visible_forts?: VisibleFort[];
}

interface ChatBotProps {
  onClose?: () => void;
  latitude?: number;
  longitude?: number;
}

export const ChatBot: React.FC<ChatBotProps> = ({ onClose, latitude, longitude }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'नमस्कार! (Hello!) I am FortSight AI. Ask me about the history of any fort or what you can see from your location.',
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/chat/`, {
        message: userMessage.content,
        session_id: sessionId,
        latitude,
        longitude
      });

      const { message, sources, visible_forts, session_id } = response.data;
      if (!sessionId && session_id) setSessionId(session_id);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: message,
        sources,
        visible_forts,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'क्षमस्व, काहीतरी चूक झाली. (Sorry, something went wrong.) Please try again later.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setSessionId(undefined);
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'नमस्कार! (Hello!) I am FortSight AI. Ask me about the history of any fort or what you can see from your location.',
      }
    ]);
  };

  return (
    <div className="flex flex-col w-full h-[600px] max-h-[80vh] bg-gray-900/80 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl overflow-hidden font-sans text-white">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-black/20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-amber-500 to-orange-400 flex items-center justify-center shadow-lg shadow-orange-500/20">
            <MessageSquare className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="font-semibold text-lg tracking-wide text-white">FortSight AI</h2>
            <p className="text-xs text-orange-200/70">RAG-powered Assistant</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleNewChat}
            className="p-2 rounded-full hover:bg-white/10 transition-colors text-gray-400 hover:text-white"
            title="New Chat"
          >
            <PlusCircle className="w-5 h-5" />
          </button>
          {onClose && (
            <button 
              onClick={onClose}
              className="p-2 rounded-full hover:bg-white/10 transition-colors text-gray-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
        {messages.map((msg) => (
          <div 
            key={msg.id} 
            className={`flex flex-col max-w-[85%] ${msg.role === 'user' ? 'self-end items-end ml-auto' : 'self-start items-start'}`}
          >
            <div 
              className={`p-4 rounded-2xl ${
                msg.role === 'user' 
                  ? 'bg-gradient-to-br from-orange-500 to-amber-600 text-white shadow-md rounded-br-sm' 
                  : 'bg-white/10 backdrop-blur-md text-gray-100 border border-white/5 shadow-md rounded-bl-sm'
              }`}
            >
              <p className="whitespace-pre-wrap leading-relaxed text-[15px]">{msg.content}</p>
            </div>
            
            {/* Sources & Visible Forts metadata */}
            {msg.role === 'assistant' && (msg.sources?.length! > 0 || msg.visible_forts?.length! > 0) && (
              <div className="mt-2 flex flex-col gap-2 w-full pl-2">
                {msg.visible_forts && msg.visible_forts.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {msg.visible_forts.map((fort, idx) => (
                      <span key={idx} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs text-blue-300">
                        <MapPin className="w-3 h-3" />
                        {fort.name} ({fort.distance.toFixed(1)}km)
                      </span>
                    ))}
                  </div>
                )}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {msg.sources.map((src, idx) => (
                      <a 
                        key={idx} 
                        href={src.url || '#'} 
                        target="_blank" 
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 hover:bg-emerald-500/20 transition-colors"
                      >
                        <Info className="w-3 h-3" />
                        {src.title}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="self-start max-w-[80%] flex items-center gap-3 p-4 rounded-2xl bg-white/5 border border-white/5 rounded-bl-sm">
            <Loader2 className="w-5 h-5 text-orange-400 animate-spin" />
            <span className="text-gray-400 text-sm animate-pulse">Thinking...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-black/20 border-t border-white/10">
        <form 
          onSubmit={handleSubmit}
          className="relative flex items-center bg-white/5 border border-white/10 rounded-full focus-within:ring-2 focus-within:ring-orange-500/50 focus-within:border-orange-500/50 transition-all shadow-inner overflow-hidden"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about forts, history, or visibility..."
            className="flex-1 bg-transparent px-6 py-4 outline-none text-white placeholder-gray-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-2 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 text-white disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-orange-500/20 transition-all transform hover:scale-105 active:scale-95 flex items-center justify-center"
          >
            <Send className="w-5 h-5 ml-0.5" />
          </button>
        </form>
      </div>
    </div>
  );
};
