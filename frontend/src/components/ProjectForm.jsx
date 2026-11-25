import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, Loader2, Sparkles, FolderPlus, Cpu, UserCheck, 
  Code2, Compass, X, CornerDownLeft, Layers, SlidersHorizontal,
  Flame, Globe, CreditCard, Hotel, Coffee, BarChart3
} from 'lucide-react';

const ProjectForm = ({ onSubmit, loading, initialDescription = '' }) => {
  const [description, setDescription] = useState(initialDescription);
  const [name, setName] = useState('');
  const [autonomousMode, setAutonomousMode] = useState(true);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (initialDescription) {
      setDescription(initialDescription);
      // If there's an enhanced prompt and name is empty, auto-suggest a name
      if (!name) {
        const firstLine = initialDescription.split('\n')[0];
        const match = firstLine.match(/App Name:\s*([A-Za-z0-9_\-\s]+)/i) || initialDescription.match(/([A-Z][a-zA-Z0-9]+(?:OS|App|SaaS|Studio|Hub|Pro)?)/);
        if (match && match[1]) {
          setName(match[1].trim().slice(0, 24));
        }
      }
      // Focus textarea
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    }
  }, [initialDescription]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (description.trim() && !loading) {
      onSubmit(description.trim(), name.trim() || undefined, autonomousMode);
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Ctrl+Enter or Cmd+Enter
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    }
  };

  const presets = [
    { 
      label: 'Cyberpunk OS Portfolio', 
      name: 'NexusOS',
      icon: Globe,
      prompt: 'Build a high-performance developer portfolio website that looks like a Cyberpunk desktop OS with terminal, draggable window frames, apps, and interactive project showcases.' 
    },
    { 
      label: 'Fintech SaaS Platform', 
      name: 'ApexPay',
      icon: CreditCard,
      prompt: 'Create a modern Fintech web application with Live Investment Dashboard, Multi-Tier Pricing Calculator, Feature Matrix, and Interactive KYC Onboarding modal.' 
    },
    { 
      label: 'Luxury Boutique Resort', 
      name: 'AuraResort',
      icon: Hotel,
      prompt: 'Design an ultra-luxurious boutique resort website with 360 Room Explorer, Date & Guest Booking flow, Dining Menus, Spa Amenities, and Guest Reviews.' 
    },
    { 
      label: 'Artisanal Coffee Roastery', 
      name: 'VelvetRoast',
      icon: Coffee,
      prompt: 'Develop a modern specialty coffee roastery web app with bean origins map, subscription builder, brewing recipe calculator, and shopping cart.' 
    },
    { 
      label: 'AI Analytics Platform', 
      name: 'QuantPulse',
      icon: BarChart3,
      prompt: 'Develop an AI Analytics web app with real-time metric charts, pipeline status, team role permissions, export reports modal, and billing tiers.' 
    }
  ];

  const applyPreset = (preset) => {
    setName(preset.name);
    setDescription(preset.prompt);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  const wordCount = description.trim() ? description.trim().split(/\s+/).length : 0;

  return (
    <div className="glass-card-glow rounded-3xl p-6 md:p-8 border border-primary-500/30 shadow-2xl shadow-primary-500/10">
      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        
        {/* Top Controls: App Name & Clear */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          
          {/* App Name Input */}
          <div className="flex-1 max-w-md relative bg-slate-950/80 rounded-2xl border border-white/10 shadow-inner focus-within:border-primary-500/80 transition-all">
            <div className="flex items-center px-4 py-3">
              <FolderPlus className="text-primary-400 mr-2.5 flex-shrink-0" size={17} />
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Project Name (e.g. NexusOS, ApexSaaS)"
                className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-sm font-semibold border-0 focus:outline-none"
                disabled={loading}
              />
              {name && (
                <button
                  type="button"
                  onClick={() => setName('')}
                  className="text-slate-500 hover:text-slate-300 p-0.5"
                >
                  <X size={14} />
                </button>
              )}
            </div>
          </div>

          {/* Quick Word & Char Counter */}
          <div className="flex items-center gap-3 text-xs text-slate-400 justify-end">
            <span className="font-mono bg-slate-950/60 px-3 py-1.5 rounded-xl border border-white/5">
              {wordCount} words • {description.length} chars
            </span>
            {description && (
              <button
                type="button"
                onClick={() => setDescription('')}
                className="text-xs text-slate-400 hover:text-rose-400 transition-colors flex items-center gap-1"
              >
                <X size={13} /> Clear
              </button>
            )}
          </div>
        </div>

        {/* Expansive Multi-Line Prompt Studio Textarea */}
        <div className="relative bg-slate-950/90 rounded-2xl border border-white/10 shadow-inner focus-within:border-primary-500 focus-within:ring-2 focus-within:ring-primary-500/20 transition-all">
          <textarea
            ref={textareaRef}
            rows={5}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your multi-page React application in detail...&#10;&#10;Example:&#10;• Pages: Home, About, Services, Pricing, Contact, Dashboard&#10;• Key Features: Interactive filtering, modal dialogs, live charts, stateful forms&#10;• Aesthetic Archetype: Dark futuristic cyberpunk, editorial luxury, or high-tech SaaS"
            className="w-full bg-transparent p-5 text-slate-100 placeholder-slate-500 text-sm md:text-base leading-relaxed font-sans border-0 focus:outline-none resize-y min-h-[140px] max-h-[400px]"
            disabled={loading}
          />

          {/* Bottom Inner Hint */}
          <div className="flex items-center justify-between px-5 py-2.5 bg-slate-950/60 border-t border-slate-800/80 text-[11px] text-slate-500">
            <span className="flex items-center gap-1.5 font-medium">
              <Sparkles size={12} className="text-primary-400" />
              Tip: Press <kbd className="px-1.5 py-0.5 bg-slate-900 border border-slate-700 rounded text-slate-300 font-mono text-[10px]">Ctrl + Enter</kbd> to launch immediately
            </span>
            <span className="hidden sm:inline text-slate-500 font-medium">
              React 18 • Vite 5.x • React Router v6
            </span>
          </div>
        </div>

        {/* Preset Inspiration Pills */}
        <div className="space-y-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <Compass size={13} className="text-primary-400" /> 1-Click Multi-Page Presets:
          </span>
          <div className="flex flex-wrap items-center gap-2">
            {presets.map((p, idx) => {
              const Icon = p.icon;
              return (
                <button
                  key={idx}
                  type="button"
                  onClick={() => applyPreset(p)}
                  className="text-xs font-semibold px-3.5 py-2 rounded-xl bg-slate-900/80 hover:bg-primary-600 hover:text-white text-slate-300 border border-slate-700/80 hover:border-primary-500 transition-all flex items-center gap-2 shadow-xs group"
                >
                  <Icon size={14} className="text-primary-400 group-hover:text-white transition-colors" />
                  <span>{p.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Action Bar: Mode Selector + Launch Button */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 pt-4 border-t border-slate-800">
          
          {/* Mode Switcher */}
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setAutonomousMode(!autonomousMode)}
              className={`text-xs px-4 py-2.5 rounded-2xl flex items-center gap-2.5 transition-all font-bold ${
                autonomousMode 
                  ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/40 shadow-sm shadow-emerald-500/10' 
                  : 'bg-indigo-500/15 text-indigo-300 border border-indigo-500/40 shadow-sm shadow-indigo-500/10'
              }`}
            >
              {autonomousMode ? (
                <Cpu size={15} className="text-emerald-400" />
              ) : (
                <UserCheck size={15} className="text-indigo-400" />
              )}
              <span>{autonomousMode ? 'Autonomous Mode (Full 8-Agent Pipeline)' : 'Collaborative Mode (Review Milestones)'}</span>
            </button>
          </div>

          {/* Launch AI Team CTA Button */}
          <button
            type="submit"
            disabled={loading || !description.trim()}
            className="bg-gradient-to-r from-primary-600 via-indigo-600 to-purple-600 hover:from-primary-500 hover:to-purple-500 text-white font-extrabold py-3.5 px-9 rounded-2xl transition-all duration-300 flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-primary-500/30 hover:shadow-primary-500/50 text-sm group"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin" size={18} />
                <span>Assembling React App...</span>
              </>
            ) : (
              <>
                <Sparkles size={18} className="group-hover:rotate-12 transition-transform text-amber-300" />
                <span>Launch AI Engineering Team</span>
                <CornerDownLeft size={14} className="opacity-60 hidden sm:inline" />
              </>
            )}
          </button>
        </div>

      </form>
    </div>
  );
};

export default ProjectForm;
