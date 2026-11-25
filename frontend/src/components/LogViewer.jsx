import React from 'react';
import { Terminal, MessageSquare, Sparkles } from 'lucide-react';

const LogViewer = ({ messages }) => {
  if (!messages || messages.length === 0) {
    return (
      <div className="text-center py-10 text-slate-500 bg-slate-950/40 rounded-2xl border border-white/5">
        <Terminal size={28} className="mx-auto mb-2 opacity-30 text-primary-400" />
        <p className="text-xs font-medium">Listening for live agent communications...</p>
      </div>
    );
  }

  const getAgentAvatar = (fromAgent) => {
    if (fromAgent.includes('Alex') || fromAgent.includes('CEO')) return '👔';
    if (fromAgent.includes('Sarah') || fromAgent.includes('Project')) return '📊';
    if (fromAgent.includes('Maya') || fromAgent.includes('Designer')) return '🎨';
    if (fromAgent.includes('David') || fromAgent.includes('Architect')) return '🏗️';
    if (fromAgent.includes('Jordan') || fromAgent.includes('Developer')) return '💻';
    if (fromAgent.includes('Marcus') || fromAgent.includes('Integrity')) return '🛡️';
    if (fromAgent.includes('Sophia') || fromAgent.includes('Visual')) return '✨';
    if (fromAgent.includes('Chris') || fromAgent.includes('QA')) return '🔍';
    if (fromAgent.includes('Emily') || fromAgent.includes('Documentation')) return '📝';
    return '🤖';
  };

  return (
    <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1 font-sans">
      {messages.map((msg, index) => {
        const sender = msg.from_agent || msg.from || 'System Agent';
        const avatar = getAgentAvatar(sender);
        
        return (
          <div
            key={index}
            className="bg-slate-950/70 border border-white/10 hover:border-primary-500/30 p-3.5 rounded-2xl transition-all shadow-sm group"
          >
            <div className="flex items-start gap-3">
              <div className="text-lg p-1.5 bg-slate-900 rounded-xl border border-white/10 flex-shrink-0 shadow-inner">
                {avatar}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <span className="font-bold text-xs text-primary-300 truncate">
                    {sender}
                  </span>
                  {msg.timestamp && (
                    <span className="text-[10px] font-mono text-slate-500 flex-shrink-0">
                      {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-200 leading-relaxed font-normal">
                  {msg.content}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default LogViewer;