import React from 'react';
import { Sparkles, Shield, Cpu, Code2, CheckCircle2 } from 'lucide-react';

const EmployeeCard = ({ employee, active }) => {
  const { name, role, avatar, bio } = employee;

  return (
    <div
      className={`glass-card rounded-2xl p-4 transition-all duration-300 border ${
        active 
          ? 'border-primary-500/80 bg-primary-950/30 shadow-lg shadow-primary-500/20 ring-1 ring-primary-500/50' 
          : 'border-white/10 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900/80'
      }`}
    >
      <div className="flex items-start gap-3.5">
        <div className="text-3xl flex-shrink-0 bg-slate-950 p-2 rounded-2xl border border-white/10 shadow-inner">
          {avatar}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-slate-100 text-xs truncate">{name}</h3>
            <div
              className={`w-2 h-2 rounded-full flex-shrink-0 ${
                active ? 'bg-emerald-400 animate-ping' : 'bg-slate-700'
              }`}
            />
          </div>
          <p className="text-[11px] font-semibold text-primary-400 truncate mt-0.5">{role}</p>
          {bio && (
            <p className="text-[11px] text-slate-400 line-clamp-2 mt-1.5 leading-relaxed">{bio}</p>
          )}
        </div>
      </div>
      {active && (
        <div className="mt-3 text-[10px] text-emerald-300 bg-emerald-500/15 border border-emerald-500/30 px-2.5 py-1 rounded-xl font-bold inline-flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          Active Sprint
        </div>
      )}
    </div>
  );
};

export default EmployeeCard;