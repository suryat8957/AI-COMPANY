import React, { useState, useEffect } from 'react';
import { 
  Download, CheckCircle, XCircle, Clock, ChevronLeft, 
  Layers, Zap, Activity, Terminal, Trash2, Code2, Eye, 
  FileCode, Sparkles, Compass, Check, Copy, ExternalLink,
  ShieldCheck, RefreshCw, FolderTree, ArrowRight
} from 'lucide-react';
import EmployeeCard from './EmployeeCard';
import WorkflowVisualization from './WorkflowVisualization';
import TaskList from './TaskList';
import LogViewer from './LogViewer';
import { projectAPI, employeeAPI } from '../services/api';

const Dashboard = ({ projectId, onBack }) => {
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [employees, setEmployees] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');
  const [fileLoading, setFileLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadEmployees();
    loadProject(true);
    let interval;
    
    const poll = async () => {
      try {
        const data = await projectAPI.getProject(projectId);
        setProject(data);
        if (data.status !== 'pending' && data.status !== 'in_progress') {
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    };
    
    interval = setInterval(poll, 2500);
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [projectId]);

  const loadEmployees = async () => {
    try {
      const data = await employeeAPI.listEmployees();
      if (data && data.employees) {
        setEmployees(data.employees);
      }
    } catch (e) {
      console.error('Error fetching employees:', e);
    }
  };

  const loadProject = async (showLoading = true) => {
    if (showLoading) setLoading(true);
    try {
      const data = await projectAPI.getProject(projectId);
      setProject(data);
    } catch (error) {
      console.error('Error loading project:', error);
    } finally {
      if (showLoading) setLoading(false);
    }
  };

  const handleOpenFile = async (filename) => {
    setSelectedFile(filename);
    setFileLoading(true);
    try {
      const res = await projectAPI.getFileContent(projectId, filename);
      setFileContent(res.content || '');
    } catch (err) {
      setFileContent(`// Error loading ${filename}\n${err.message}`);
    } finally {
      setFileLoading(false);
    }
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(fileContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this project? This cannot be undone.')) {
      try {
        await projectAPI.deleteProject(projectId);
        onBack();
      } catch (error) {
        console.error('Error deleting project:', error);
        alert('Failed to delete project');
      }
    }
  };

  const handleDownload = async () => {
    try {
      const blob = await projectAPI.downloadProject(projectId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${project.name || 'ReactProject'}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading project:', error);
      alert('Failed to download project');
    }
  };

  const getStatusBadge = () => {
    if (!project) return null;
    
    switch (project.status) {
      case 'completed':
        return (
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/40 shadow-sm shadow-emerald-500/10">
            <CheckCircle size={15} className="text-emerald-400" />
            <span className="text-xs font-bold uppercase tracking-wider">Production Ready</span>
          </div>
        );
      case 'failed':
      case 'rejected':
        return (
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-rose-500/15 text-rose-300 border border-rose-500/40">
            <XCircle size={15} className="text-rose-400" />
            <span className="text-xs font-bold uppercase tracking-wider">Failed</span>
          </div>
        );
      default:
        return (
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-500/15 text-primary-300 border border-primary-500/40 shadow-sm shadow-primary-500/10">
            <Zap size={15} className="text-primary-400 animate-pulse" />
            <span className="text-xs font-bold uppercase tracking-wider">Agents Collaborating...</span>
          </div>
        );
    }
  };

  const getCurrentStep = () => {
    if (!project) return 1;
    if (project.status === 'completed') return 10;
    if (project.status === 'in_progress') {
      const fileCount = (project.files || []).length;
      if (fileCount >= 12) return 7;
      if (fileCount >= 4) return 5;
      if (project.tasks && project.tasks.length > 0) return 3;
      return 2;
    }
    return 1;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950 text-slate-100">
        <div className="text-center animate-fade-in">
          <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-primary-600 via-indigo-600 to-purple-600 flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-primary-500/30 animate-pulse">
            <Layers className="text-white" size={32} />
          </div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Initializing Agent Studio...</h2>
          <p className="mt-2 text-xs text-slate-400">Connecting to real-time engineering stream</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 pb-20 font-sans bg-grid-pattern">
      {/* Top Header */}
      <nav className="bg-slate-950/80 backdrop-blur-xl border-b border-white/10 sticky top-0 z-40 shadow-2xl">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-slate-400 hover:text-primary-400 transition-colors font-semibold text-xs uppercase tracking-wider"
          >
            <ChevronLeft size={16} />
            Back to Studio Hub
          </button>
          
          <div className="flex items-center gap-3">
            {getStatusBadge()}
            {project?.status === 'completed' && (
              <button
                onClick={handleDownload}
                className="bg-gradient-to-r from-primary-600 via-indigo-600 to-purple-600 hover:from-primary-500 hover:to-purple-500 text-white font-bold py-2 px-5 rounded-xl flex items-center gap-2 transition-all shadow-lg shadow-primary-500/25 text-xs"
              >
                <Download size={15} />
                Download React Project (ZIP)
              </button>
            )}
            <button
              onClick={handleDelete}
              className="bg-slate-900 border border-rose-500/30 text-rose-400 hover:bg-rose-500/20 py-2 px-3 rounded-xl flex items-center gap-1.5 transition-all text-xs"
              title="Delete Project"
            >
              <Trash2 size={15} />
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 mt-8 animate-fade-in">
        
        {/* Project Header Banner */}
        <div className="glass-card-glow rounded-3xl p-8 border border-primary-500/30 mb-8 shadow-2xl">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div>
              <div className="flex items-center gap-2.5 mb-2.5">
                <span className="text-[10px] font-extrabold uppercase tracking-wider px-3 py-1 bg-primary-500/20 text-primary-300 rounded-full border border-primary-500/30">
                  React 18 + Vite Production Platform
                </span>
                {project?.autonomous_mode && (
                  <span className="text-[10px] font-bold px-2.5 py-0.5 bg-emerald-500/15 text-emerald-300 rounded-full border border-emerald-500/30">
                    Autonomous Mode
                  </span>
                )}
              </div>
              <h1 className="text-3xl md:text-4xl font-extrabold text-slate-100 tracking-tight">
                {project?.name || 'React Web Application'}
              </h1>
              <p className="text-sm text-slate-300 max-w-3xl mt-2 leading-relaxed font-normal">
                {project?.description || project?.client_request}
              </p>
            </div>
            
            {/* Quick Metrics Bar */}
            <div className="flex items-center gap-3 flex-shrink-0 bg-slate-950/80 p-4 rounded-2xl border border-white/10 shadow-inner">
              <div className="text-center px-4 border-r border-slate-800">
                <div className="text-2xl font-black text-primary-400">{project?.files?.length || 0}</div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">React Files</div>
              </div>
              <div className="text-center px-4 border-r border-slate-800">
                <div className="text-2xl font-black text-indigo-400">{project?.pages?.length || 5}</div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Pages</div>
              </div>
              <div className="text-center px-4">
                <div className="text-2xl font-black text-emerald-400">{project?.quality_score || 9}/10</div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">QA Score</div>
              </div>
            </div>
          </div>

          {/* Generated Pages Badges */}
          {project?.pages && project.pages.length > 0 && (
            <div className="mt-6 pt-5 border-t border-slate-800/80 flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-2 flex items-center gap-1">
                <Compass size={13} className="text-primary-400" /> Multi-Page Sitemap:
              </span>
              {project.pages.map((page, idx) => (
                <span 
                  key={idx} 
                  className="text-xs font-mono font-medium px-3 py-1 rounded-xl bg-slate-950/80 text-primary-300 border border-primary-500/20"
                >
                  /{page.toLowerCase().replace(/\s+/g, '-')}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* AI Engineering Team Grid */}
        <div className="mb-10">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-slate-100 tracking-tight flex items-center gap-2">
              <Sparkles size={18} className="text-primary-400" />
              Specialized React AI Engineering Team
            </h2>
            <span className="text-xs font-semibold text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-white/10">
              {employees.length || 8} Active Agents
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 gap-3.5">
            {employees.map((employee) => (
              <EmployeeCard
                key={employee.id}
                employee={employee}
                active={project?.status === 'in_progress'}
              />
            ))}
          </div>
        </div>

        {/* Main Grid: Pipeline, Logs & React Code Explorer */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-8">
          
          {/* Left Column (8 cols): Pipeline & Agent Logs */}
          <div className="lg:col-span-8 space-y-8">
            <WorkflowVisualization 
              currentStep={getCurrentStep()} 
              currentAgent={project?.current_agent}
            />
            
            <div className="glass-card rounded-3xl p-6 border border-white/10 shadow-2xl">
              <h3 className="text-base font-bold text-slate-100 mb-4 flex items-center gap-2">
                <Terminal size={17} className="text-primary-400" />
                Live Agent Collaboration Stream
              </h3>
              <LogViewer messages={project?.messages || []} />
            </div>
          </div>
          
          {/* Right Column (4 cols): Task Breakdown & Generated React Code Explorer */}
          <div className="lg:col-span-4 space-y-6">
            
            {/* Generated React Code Explorer */}
            {project?.files && project.files.length > 0 && (
              <div className="glass-card rounded-3xl p-6 border border-white/10 shadow-2xl">
                <div className="flex items-center justify-between mb-4 pb-2.5 border-b border-slate-800">
                  <h3 className="text-xs font-bold text-slate-100 flex items-center gap-2 uppercase tracking-wider">
                    <FileCode size={15} className="text-primary-400" />
                    React Code Explorer
                  </h3>
                  <span className="text-[10px] font-bold text-primary-300 bg-primary-500/20 border border-primary-500/30 px-2 py-0.5 rounded-full">
                    {project.files.length} files
                  </span>
                </div>
                <div className="space-y-1.5 max-h-[300px] overflow-y-auto pr-1">
                  {project.files.map((file, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleOpenFile(file)}
                      className="w-full text-left px-3 py-2 rounded-xl text-xs font-mono font-medium hover:bg-primary-900/40 hover:text-primary-200 hover:border-primary-500/40 transition-all flex items-center justify-between group bg-slate-950/70 border border-white/5"
                    >
                      <span className="truncate text-slate-300 group-hover:text-primary-200">{file}</span>
                      <Eye size={13} className="text-slate-500 group-hover:text-primary-400 flex-shrink-0" />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Task Breakdown */}
            <div className="glass-card rounded-3xl p-6 border border-white/10 shadow-2xl">
              <h3 className="text-xs font-bold text-slate-100 mb-4 flex items-center gap-2 uppercase tracking-wider">
                <Layers size={15} className="text-primary-400" />
                Engineering Roadmap
              </h3>
              <TaskList tasks={project?.tasks || []} />
            </div>
          </div>
        </div>

      </div>

      {/* Code Viewer Modal */}
      {selectedFile && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 md:p-8 animate-fade-in">
          <div className="bg-slate-900 text-slate-100 rounded-3xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl border border-primary-500/30 overflow-hidden">
            {/* Modal Header */}
            <div className="px-6 py-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-primary-500/20 text-primary-400 flex items-center justify-center border border-primary-500/30">
                  <Code2 size={16} />
                </div>
                <div>
                  <h3 className="text-xs font-bold font-mono text-slate-100">{selectedFile}</h3>
                  <p className="text-[10px] text-slate-400">Generated by Senior React Developer</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopyCode}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all text-slate-200"
                >
                  {copied ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
                  <span>{copied ? 'Copied!' : 'Copy Code'}</span>
                </button>
                <button
                  onClick={() => setSelectedFile(null)}
                  className="p-1.5 hover:bg-slate-800 rounded-xl text-slate-400 hover:text-white transition-colors"
                >
                  <XCircle size={18} />
                </button>
              </div>
            </div>

            {/* Modal Code Body */}
            <div className="p-6 overflow-auto font-mono text-xs leading-relaxed flex-1 bg-slate-950/90">
              {fileLoading ? (
                <div className="py-16 text-center text-slate-400">
                  <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full mx-auto mb-3" />
                  Loading file content...
                </div>
              ) : (
                <pre className="text-emerald-300/90 whitespace-pre-wrap select-text">{fileContent}</pre>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;