import React, { useState } from 'react';
import { Wand2, Copy, Check, ArrowRight, Loader2, Sparkles, ChevronDown, ChevronUp, Zap } from 'lucide-react';
import { projectAPI } from '../services/api';

const PromptEnhancer = ({ onUsePrompt }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [enhancedPrompt, setEnhancedPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');

  const handleEnhance = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    setLoading(true);
    setError('');
    try {
      const data = await projectAPI.enhancePrompt(userInput.trim());
      if (data.status === 'success' && data.enhanced_prompt) {
        setEnhancedPrompt(data.enhanced_prompt);
      } else {
        setError('Failed to enhance prompt. Please try again.');
      }
    } catch (err) {
      console.error('Enhance prompt error:', err);
      setError('Failed to connect to prompt enhancer service.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (enhancedPrompt) {
      navigator.clipboard.writeText(enhancedPrompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleUsePrompt = () => {
    if (enhancedPrompt && typeof onUsePrompt === 'function') {
      onUsePrompt(enhancedPrompt);
      setIsOpen(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-6">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-6 py-3.5 bg-slate-900/70 hover:bg-slate-900/90 backdrop-blur-xl border border-primary-500/30 hover:border-primary-400/60 rounded-2xl shadow-lg shadow-primary-500/5 transition-all duration-300 group"
      >
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-primary-600 to-indigo-600 text-white flex items-center justify-center shadow-md shadow-primary-500/20 group-hover:scale-105 transition-transform">
            <Wand2 size={16} />
          </div>
          <div className="text-left">
            <span className="font-bold text-sm text-slate-100 flex items-center gap-1.5">
              AI Prompt Architect & Enhancer
              <span className="text-[10px] bg-primary-500/20 text-primary-300 font-semibold px-2 py-0.5 rounded-full border border-primary-500/30">
                Gemini 3.5
              </span>
            </span>
            <span className="text-xs text-slate-400 font-normal hidden sm:inline">
              Turn a one-line idea into a full multi-page React design prompt
            </span>
          </div>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-primary-400 font-semibold bg-primary-500/10 px-3 py-1.5 rounded-xl border border-primary-500/20 group-hover:bg-primary-500/20 transition-all">
          <span>{isOpen ? 'Collapse' : 'Try AI Enhancer'}</span>
          {isOpen ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
        </div>
      </button>

      {isOpen && (
        <div className="mt-3 p-6 bg-slate-900/80 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl animate-fade-in space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2.5 flex items-center gap-1.5">
              <Zap size={14} className="text-primary-400" /> Enter Your Raw Concept
            </label>
            <form onSubmit={handleEnhance} className="flex flex-col sm:flex-row gap-2.5">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="e.g. Luxury mechanical watch customizer with 3D dial explorer and booking checkout"
                className="flex-1 px-4 py-3.5 bg-slate-950/80 border border-white/10 rounded-2xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 text-sm transition-all"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !userInput.trim()}
                className="px-6 py-3.5 bg-gradient-to-r from-primary-600 via-indigo-600 to-purple-600 hover:from-primary-500 hover:to-purple-500 text-white font-semibold text-sm rounded-2xl transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-primary-500/25 hover:shadow-primary-500/40 whitespace-nowrap"
              >
                {loading ? (
                  <>
                    <Loader2 size={16} className="animate-spin" />
                    <span>Architecting...</span>
                  </>
                ) : (
                  <>
                    <Sparkles size={16} />
                    <span>Generate Rich Spec</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {error && (
            <p className="text-xs text-rose-400 font-medium bg-rose-500/10 border border-rose-500/20 p-2.5 rounded-xl">{error}</p>
          )}

          {enhancedPrompt && (
            <div className="mt-4 p-5 bg-slate-950/90 border border-primary-500/30 rounded-2xl space-y-3.5 shadow-inner">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-primary-400 flex items-center gap-1.5">
                  <Sparkles size={14} className="text-primary-400" />
                  Enhanced Multi-Page React Specification
                </span>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={handleCopy}
                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl shadow-xs transition-all"
                  >
                    {copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
                    <span>{copied ? 'Copied!' : 'Copy'}</span>
                  </button>
                  {onUsePrompt && (
                    <button
                      type="button"
                      onClick={handleUsePrompt}
                      className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-bold bg-primary-600 hover:bg-primary-500 text-white rounded-xl shadow-md shadow-primary-500/30 transition-all"
                    >
                      <span>Insert In Studio</span>
                      <ArrowRight size={14} />
                    </button>
                  )}
                </div>
              </div>

              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-sans font-medium whitespace-pre-wrap">
                {enhancedPrompt}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PromptEnhancer;
