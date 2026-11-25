import React from 'react';
import { CheckCircle2, Circle, Loader2, Sparkles, ShieldCheck, ChevronRight, Activity } from 'lucide-react';

const WorkflowVisualization = ({ currentStep, steps, currentAgent }) => {
  const defaultSteps = [
    { id: 1, name: 'Product & Sitemap Blueprint', agent: 'Alex Thompson (CEO & Product Lead)', icon: '👔' },
    { id: 2, name: 'Sprint & Task Decomposition', agent: 'Sarah Martinez (Project Manager)', icon: '📊' },
    { id: 3, name: 'UI Design System & Tokens', agent: 'Maya Patel (Lead UI/UX Designer)', icon: '🎨' },
    { id: 4, name: 'React Architecture & Routing', agent: 'David Vance (Principal React Architect)', icon: '🏗️' },
    { id: 5, name: 'Multi-Page React Generation', agent: 'Jordan Lee (Senior React Developer)', icon: '💻' },
    { id: 6, name: 'File & Import Integrity Audit', agent: 'Marcus Brody (File Integrity Specialist)', icon: '🛡️' },
    { id: 7, name: 'Visual & UX Polish Review', agent: 'Sophia Rossi (Visual & UX Reviewer)', icon: '✨' },
    { id: 8, name: 'QA & Accessibility Audit', agent: 'Chris Anderson (Lead React QA Auditor)', icon: '🔍' },
    { id: 9, name: 'Production Documentation', agent: 'Emily Zhang (Technical Documentation Lead)', icon: '📝' },
    { id: 10, name: 'Executive Approval & Delivery', agent: 'CEO & System Engine', icon: '🚀' },
  ];

  const workflowSteps = steps || defaultSteps;

  const getStepStatus = (stepId) => {
    if (stepId < currentStep) return 'completed';
    if (stepId === currentStep) return 'active';
    return 'pending';
  };

  return (
    <div className="glass-card rounded-3xl p-6 border border-white/10 shadow-2xl">
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Activity size={18} className="text-primary-400" />
            <span>Autonomous Engineering Pipeline</span>
            <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-primary-500/20 text-primary-300 border border-primary-500/30">
              React 18 + Vite
            </span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">Multi-agent coordinated lifecycle</p>
        </div>
        {currentAgent && (
          <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-500/15 border border-amber-500/30 rounded-full text-xs font-semibold text-amber-300 animate-pulse">
            <Sparkles size={13} className="text-amber-400" />
            <span>Active: {currentAgent}</span>
          </div>
        )}
      </div>

      <div className="space-y-2.5">
        {workflowSteps.map((step) => {
          const status = getStepStatus(step.id);

          return (
            <div 
              key={step.id} 
              className={`flex items-center gap-3.5 p-3 rounded-2xl transition-all ${
                status === 'active' 
                  ? 'bg-primary-900/40 border border-primary-500/40 shadow-lg shadow-primary-500/10' 
                  : status === 'completed'
                  ? 'bg-slate-950/40 border border-white/5'
                  : 'opacity-40 bg-slate-950/20 border border-transparent'
              }`}
            >
              <div className="flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-xl bg-slate-900 border border-white/10 shadow-inner">
                {status === 'completed' ? (
                  <CheckCircle2 className="text-emerald-400" size={18} />
                ) : status === 'active' ? (
                  <Loader2 className="text-primary-400 animate-spin" size={17} />
                ) : (
                  <span className="text-sm">{step.icon || '⭕'}</span>
                )}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3
                    className={`text-xs sm:text-sm font-bold truncate ${
                      status === 'active'
                        ? 'text-primary-200'
                        : status === 'completed'
                        ? 'text-slate-200'
                        : 'text-slate-500'
                    }`}
                  >
                    {step.name}
                  </h3>
                </div>
                <p className="text-[11px] text-slate-400 truncate">{step.agent}</p>
              </div>

              <div className="flex-shrink-0">
                {status === 'active' && (
                  <span className="text-[10px] bg-gradient-to-r from-primary-600 to-indigo-600 text-white font-bold px-3 py-1 rounded-full shadow-md shadow-primary-500/30 animate-pulse">
                    Executing
                  </span>
                )}
                {status === 'completed' && (
                  <span className="text-[10px] bg-emerald-500/15 text-emerald-300 font-semibold px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                    Passed
                  </span>
                )}
                {status === 'pending' && (
                  <span className="text-[10px] text-slate-500 font-medium px-2">
                    Queued
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default WorkflowVisualization;