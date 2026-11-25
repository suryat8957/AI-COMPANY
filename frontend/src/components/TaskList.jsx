import React from 'react';
import { CheckCircle2, Circle, Clock, Layers, Sparkles } from 'lucide-react';

const TaskList = ({ tasks }) => {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-8 text-slate-500">
        <Layers size={28} className="mx-auto mb-2 opacity-30" />
        <p className="text-xs font-medium">No engineering tasks active</p>
      </div>
    );
  }

  return (
    <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-1">
      {tasks.map((task, index) => (
        <div
          key={index}
          className="bg-slate-950/60 border border-white/5 hover:border-primary-500/30 rounded-2xl p-3.5 transition-all"
        >
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 mt-0.5">
              {task.status === 'completed' ? (
                <CheckCircle2 className="text-emerald-400" size={17} />
              ) : task.status === 'in_progress' ? (
                <Clock className="text-primary-400 animate-spin" size={17} />
              ) : (
                <Circle className="text-slate-600" size={17} />
              )}
            </div>

            <div className="flex-1 min-w-0">
              <h4 className="text-xs font-bold text-slate-200 truncate">{task.title}</h4>
              <p className="text-[11px] text-slate-400 line-clamp-2 mt-0.5 leading-relaxed">
                {task.description}
              </p>
              <div className="flex items-center justify-between mt-2 pt-1.5 border-t border-slate-800/60 text-[10px]">
                <span className="text-primary-400 font-semibold truncate max-w-[160px]">
                  {task.assigned_to}
                </span>
                {task.estimated_duration && (
                  <span className="text-slate-500 font-mono">
                    {task.estimated_duration}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;