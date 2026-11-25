import React, { useState, useEffect } from 'react';
import { 
  Briefcase, Sparkles, Layers, Cpu, Download, ArrowRight, Activity, 
  Terminal, Trash2, CheckCircle2, ShieldCheck, Code2, Globe, 
  Zap, Check, HelpCircle, ChevronDown, ChevronUp, Star,
  Compass, Eye, Play, Flame, Laptop, FolderGit2
} from 'lucide-react';
import ProjectForm from './components/ProjectForm';
import PromptEnhancer from './components/PromptEnhancer';
import Dashboard from './components/Dashboard';
import { projectAPI } from './services/api';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [currentProject, setCurrentProject] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [enhancedPrompt, setEnhancedPrompt] = useState('');
  const [activeTab, setActiveTab] = useState('all');
  const [expandedFaq, setExpandedFaq] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await projectAPI.listProjects();
      setProjects(data.projects || []);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const handleCreateProject = async (description, name, autonomousMode = true) => {
    setLoading(true);
    try {
      const result = await projectAPI.createProject(description, name, autonomousMode);
      
      if (result.success) {
        setCurrentProject(result.project_id);
        setCurrentView('dashboard');
        loadProjects();
      } else {
        alert('Project creation failed: ' + (result.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error creating project:', error);
      alert('Failed to create project. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProject = async (e, projectId) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await projectAPI.deleteProject(projectId);
        loadProjects();
      } catch (error) {
        alert('Failed to delete project');
      }
    }
  };

  const handleViewProject = (projectId) => {
    setCurrentProject(projectId);
    setCurrentView('dashboard');
  };

  const handleBackToHome = () => {
    setCurrentView('home');
    setCurrentProject(null);
    loadProjects();
  };

  const agents = [
    {
      category: 'product',
      avatar: '👔',
      name: 'Alex Thompson',
      role: 'CEO & Product Lead',
      badge: 'Product Vision',
      skills: ['Sitemap Mapping (4-6 Pages)', 'Business Logic Matrix', 'Executive Sign-Off'],
      description: 'Deconstructs raw user ideas into a comprehensive product blueprint with multi-page routes, feature matrices, and target audience alignment.'
    },
    {
      category: 'product',
      avatar: '📊',
      name: 'Sarah Martinez',
      role: 'Project Manager',
      badge: 'Sprint Planning',
      skills: ['Milestone Breakdown', 'Dependency Graphing', 'Agent Orchestration'],
      description: 'Coordinates the 8 specialized agents into sequential sprints with clear inputs, outputs, and time estimates.'
    },
    {
      category: 'design',
      avatar: '🎨',
      name: 'Maya Patel',
      role: 'Lead UI/UX Designer',
      badge: 'Design Systems',
      skills: ['CSS :root Token Engine', 'Google Font Pairings', 'Design Archetypes'],
      description: 'Creates bespoke visual design systems—from Cyberpunk Terminal to Editorial Luxury—with harmonic color palettes and animation keyframes.'
    },
    {
      category: 'design',
      avatar: '🏗️',
      name: 'David Vance',
      role: 'Principal React Architect',
      badge: 'React Architecture',
      skills: ['React Router v6 Hierarchy', 'AppContext State Model', 'Package Manifests'],
      description: 'Architects component trees, global context providers, mock data schemas, and modern package.json dependency blueprints.'
    },
    {
      category: 'code',
      avatar: '💻',
      name: 'Jordan Lee',
      role: 'Senior React Developer',
      badge: 'React 18 Lead',
      skills: ['Modular JSX Components', 'Interactive Event Handlers', 'Vite Scaffolding'],
      description: 'Engineers production-grade React 18 functional components, UI primitives (Button, Modal, Card, Badge), and responsive views.'
    },
    {
      category: 'qa',
      avatar: '🛡️',
      name: 'Marcus Brody',
      role: 'File Integrity Specialist',
      badge: 'File & Import Audit',
      skills: ['100% Manifest Audit', 'Broken Import Detection', 'Route Link Validation'],
      description: 'Ensures every single imported component exists on disk with correct relative paths and zero missing dependencies.'
    },
    {
      category: 'qa',
      avatar: '✨',
      name: 'Sophia Rossi',
      role: 'Visual & UX Reviewer',
      badge: 'Aesthetic Review',
      skills: ['Visual Hierarchy Scoring', 'Contrast & Typography', 'Responsive Layout Feel'],
      description: 'Critically inspects layout balance, brand authenticity, and interactive polish on a strict 1-10 scoring benchmark.'
    },
    {
      category: 'qa',
      avatar: '🔍',
      name: 'Chris Anderson',
      role: 'Lead React QA Auditor',
      badge: 'Code Quality & A11y',
      skills: ['React Hooks Inspection', 'Form State Handling', 'ARIA Accessibility'],
      description: 'Conducts automated code audits to eliminate broken onClick handlers, missing props, and JSX syntax defects.'
    },
    {
      category: 'code',
      avatar: '📝',
      name: 'Emily Zhang',
      role: 'Technical Documentation Lead',
      badge: 'Developer Docs',
      skills: ['README.md Generation', 'Local Run Instructions', 'Theme Customization'],
      description: 'Writes complete developer documentation with npm install, npm run dev, routing guides, and component customization notes.'
    }
  ];

  const filteredAgents = activeTab === 'all' 
    ? agents 
    : agents.filter(a => a.category === activeTab);

  const faqs = [
    {
      q: 'What technology stack do the generated applications use?',
      a: 'Every generated project uses React 18 functional components with Vite 5.x for ultra-fast compilation, React Router DOM v6 for real multi-page routing, Lucide React for modern iconography, and a tailored CSS Variables (:root) design system.'
    },
    {
      q: 'How do I run the generated React application on my computer?',
      a: 'Download the project ZIP from the dashboard, extract it, and run "npm install" followed by "npm run dev". Vite will start a local development server at http://localhost:5173 with hot-module reloading.'
    },
    {
      q: 'How does the Autonomous Remediation Loop work?',
      a: 'After the developer generates the code, the File Integrity Specialist, Visual Reviewer, and QA Auditor evaluate the codebase. If any missing import, broken route, or score below 9/10 is detected, the Senior Developer automatically performs a remediation pass before executive approval.'
    },
    {
      q: 'Can I customize the color palette and typography?',
      a: 'Yes! All colors, fonts, shadows, and border radii are defined in src/index.css under CSS custom properties (:root). You can simply tweak values to instantly re-theme the entire application.'
    }
  ];

  if (currentView === 'dashboard' && currentProject) {
    return <Dashboard projectId={currentProject} onBack={handleBackToHome} />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 relative overflow-hidden font-sans bg-grid-pattern">
      {/* Glow Effects */}
      <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-primary-600/15 rounded-full filter blur-[120px] pointer-events-none animate-pulse-glow" />
      <div className="absolute top-40 right-1/4 w-[500px] h-[500px] bg-purple-600/15 rounded-full filter blur-[120px] pointer-events-none" />

      <div className="relative z-10">
        
        {/* Navigation Bar */}
        <nav className="bg-slate-950/80 backdrop-blur-xl border-b border-white/10 sticky top-0 z-50 shadow-2xl">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-primary-600 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-primary-500/30">
                <Code2 size={22} />
              </div>
              <div>
                <h1 className="text-base font-black tracking-tight leading-none text-slate-100 flex items-center gap-2">
                  Antigravity Studio
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-primary-500/20 text-primary-300 border border-primary-500/30">
                    React 18
                  </span>
                </h1>
                <p className="text-[10px] font-semibold text-primary-400 uppercase tracking-widest mt-0.5">
                  Autonomous AI Frontend Platform
                </p>
              </div>
            </div>

            <div className="hidden lg:flex items-center gap-7 text-xs font-semibold text-slate-400">
              <a href="#studio-creator" className="hover:text-primary-400 transition-colors">Studio Creator</a>
              <a href="#agent-fleet" className="hover:text-primary-400 transition-colors">AI Team ({agents.length})</a>
              <a href="#why-antigravity" className="hover:text-primary-400 transition-colors">Why Antigravity</a>
              <a href="#projects" className="hover:text-primary-400 transition-colors">Recent Projects</a>
              <a href="#faq" className="hover:text-primary-400 transition-colors">FAQ</a>
            </div>

            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 rounded-full text-xs font-semibold">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                <span>8 AI Agents Online</span>
              </div>
              <a
                href="#studio-creator"
                className="bg-gradient-to-r from-primary-600 via-indigo-600 to-purple-600 hover:from-primary-500 hover:to-purple-500 text-white font-bold text-xs py-2 px-4 rounded-xl transition-all shadow-md shadow-primary-500/25"
              >
                Launch App
              </a>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <main className="max-w-7xl mx-auto px-6 pt-16 pb-24">
          
          <div className="text-center max-w-4xl mx-auto mb-14 animate-slide-up">
            <div className="inline-flex items-center gap-2 bg-slate-900/80 backdrop-blur-xl border border-primary-500/30 text-primary-300 px-4 py-1.5 rounded-full mb-6 shadow-lg shadow-primary-500/5">
              <Sparkles size={14} className="text-primary-400 animate-spin" />
              <span className="text-xs font-bold tracking-wide uppercase">Next-Gen React 18 + Vite Engineering Engine</span>
            </div>

            <h2 className="text-4xl sm:text-6xl md:text-7xl font-black text-slate-100 mb-6 leading-tight tracking-tight">
              Describe Any Web App. <br />
              <span className="text-gradient">We Architect, Code & Deliver.</span>
            </h2>

            <p className="text-sm sm:text-base md:text-lg text-slate-300 mb-8 max-w-2xl mx-auto leading-relaxed font-normal">
              Our 8-agent AI team collaborates to create production-quality, multi-page React 18 applications with custom design systems, React Router v6, Lucide icons, and automated QA audits.
            </p>

            {/* Feature Pills */}
            <div className="flex flex-wrap items-center justify-center gap-2 max-w-3xl mx-auto text-xs font-semibold text-slate-300 mb-10">
              <span className="px-3 py-1 bg-slate-900/70 border border-white/10 rounded-full flex items-center gap-1.5">
                <Check size={13} className="text-emerald-400" /> Multi-Page React Router v6
              </span>
              <span className="px-3 py-1 bg-slate-900/70 border border-white/10 rounded-full flex items-center gap-1.5">
                <Check size={13} className="text-emerald-400" /> Bespoke CSS Design Tokens
              </span>
              <span className="px-3 py-1 bg-slate-900/70 border border-white/10 rounded-full flex items-center gap-1.5">
                <Check size={13} className="text-emerald-400" /> 100% Manifest Integrity
              </span>
              <span className="px-3 py-1 bg-slate-900/70 border border-white/10 rounded-full flex items-center gap-1.5">
                <Check size={13} className="text-emerald-400" /> Automated QA Remediation
              </span>
            </div>
          </div>

          {/* Interactive Studio Creator Section */}
          <div id="studio-creator" className="max-w-4xl mx-auto mb-24 relative animate-slide-up animate-delay-150">
            <PromptEnhancer onUsePrompt={(promptText) => setEnhancedPrompt(promptText)} />
            <ProjectForm onSubmit={handleCreateProject} loading={loading} initialDescription={enhancedPrompt} />
          </div>

          {/* 8-Agent Fleet Interactive Showcase */}
          <div id="agent-fleet" className="mb-24 pt-8">
            <div className="text-center max-w-3xl mx-auto mb-10">
              <span className="text-[10px] font-extrabold uppercase tracking-widest px-3 py-1 bg-primary-500/15 text-primary-300 rounded-full border border-primary-500/30">
                Specialized AI Fleet
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-100 mt-3 tracking-tight">
                Meet Your 8-Specialist AI Engineering Team
              </h2>
              <p className="text-sm text-slate-400 mt-2">
                Every agent operates with specialized domain knowledge, dedicated tools, and automated validation checkpoints.
              </p>

              {/* Category Filter Tabs */}
              <div className="flex flex-wrap items-center justify-center gap-2 mt-6">
                {[
                  { id: 'all', label: 'All Specialists (9)' },
                  { id: 'product', label: 'Product & Planning' },
                  { id: 'design', label: 'Design & Architecture' },
                  { id: 'code', label: 'Engineering & Docs' },
                  { id: 'qa', label: 'Quality & Integrity' },
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`text-xs px-4 py-2 rounded-xl font-bold transition-all ${
                      activeTab === tab.id
                        ? 'bg-gradient-to-r from-primary-600 to-indigo-600 text-white shadow-lg shadow-primary-500/20'
                        : 'bg-slate-900/60 text-slate-400 hover:text-slate-200 border border-white/5'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Agent Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {filteredAgents.map((agent, idx) => (
                <div 
                  key={idx} 
                  className="glass-card rounded-3xl p-6 border border-white/10 hover:border-primary-500/40 transition-all duration-300 flex flex-col justify-between group"
                >
                  <div>
                    <div className="flex items-start justify-between mb-4">
                      <div className="text-3xl p-3 bg-slate-950 rounded-2xl border border-white/10 shadow-inner group-hover:scale-105 transition-transform">
                        {agent.avatar}
                      </div>
                      <span className="text-[10px] font-bold px-3 py-1 rounded-full bg-primary-500/15 text-primary-300 border border-primary-500/30">
                        {agent.badge}
                      </span>
                    </div>
                    
                    <h3 className="text-base font-bold text-slate-100">{agent.name}</h3>
                    <p className="text-xs font-semibold text-primary-400 mb-3">{agent.role}</p>
                    <p className="text-xs text-slate-400 leading-relaxed mb-4">{agent.description}</p>
                  </div>

                  <div className="pt-3 border-t border-slate-800/80">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-2">Key Output Deliverables:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {agent.skills.map((skill, sIdx) => (
                        <span key={sIdx} className="text-[10px] font-medium px-2.5 py-0.5 rounded-lg bg-slate-950 text-slate-300 border border-white/5">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Why Antigravity Studio Comparison Matrix */}
          <div id="why-antigravity" className="mb-24 pt-8">
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-[10px] font-extrabold uppercase tracking-widest px-3 py-1 bg-primary-500/15 text-primary-300 rounded-full border border-primary-500/30">
                Industry Comparison
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-100 mt-3 tracking-tight">
                Why Antigravity Sets the New Benchmark
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Legacy AI */}
              <div className="bg-slate-950/60 rounded-3xl p-8 border border-rose-500/20 shadow-xl space-y-4">
                <div className="flex items-center gap-3 text-rose-400 font-bold text-base pb-3 border-b border-slate-800">
                  <span className="w-3 h-3 rounded-full bg-rose-500"></span>
                  Traditional / Legacy AI Generators
                </div>
                <ul className="space-y-3 text-xs text-slate-400 leading-relaxed">
                  <li className="flex items-start gap-2.5">
                    <span className="text-rose-400 font-bold">✕</span>
                    <span>Generates a single monolithic HTML file with inline styles.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <span className="text-rose-400 font-bold">✕</span>
                    <span>No real routing—dummy "#" links with fake page transitions.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <span className="text-rose-400 font-bold">✕</span>
                    <span>Broken JavaScript event listeners and unhandled edge cases.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <span className="text-rose-400 font-bold">✕</span>
                    <span>Generic styling lacking brand identity or cohesive font pairings.</span>
                  </li>
                </ul>
              </div>

              {/* Antigravity Studio */}
              <div className="glass-card-glow rounded-3xl p-8 border border-primary-500/40 shadow-2xl space-y-4">
                <div className="flex items-center gap-3 text-primary-300 font-bold text-base pb-3 border-b border-slate-800">
                  <span className="w-3 h-3 rounded-full bg-emerald-400 animate-ping"></span>
                  Antigravity Autonomous React Studio
                </div>
                <ul className="space-y-3 text-xs text-slate-200 leading-relaxed">
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 size={16} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span><strong>Real React 18 + Vite Architecture</strong>: Clean repository structure with modular components.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 size={16} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span><strong>React Router v6 Navigation</strong>: 4–6 real functional pages (Home, About, Services, Pricing, Contact).</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 size={16} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span><strong>Self-Healing QA Remediation</strong>: Automated file integrity and visual reviews before delivery.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 size={16} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span><strong>Bespoke Design Token System</strong>: Comprehensive CSS `:root` variables, keyframes, and Lucide icons.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Recent Projects Section */}
          {projects.length > 0 && (
            <div id="projects" className="mb-24 pt-8">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">Recent React Projects</h2>
                  <p className="text-xs text-slate-400 mt-1">Generated and verified by your AI team</p>
                </div>
                <span className="text-xs font-bold text-primary-300 bg-primary-500/20 border border-primary-500/30 px-3 py-1 rounded-full">
                  {projects.length} Total Projects
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.slice(0, 6).map((project) => (
                  <div
                    key={project.id}
                    className="glass-card rounded-3xl p-6 cursor-pointer group hover:border-primary-500/50 transition-all border border-white/10 shadow-xl"
                    onClick={() => handleViewProject(project.id)}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div className="w-10 h-10 rounded-2xl bg-primary-500/20 text-primary-400 flex items-center justify-center group-hover:scale-105 transition-all border border-primary-500/30">
                        <Code2 size={20} />
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider ${
                          project.status === 'completed'
                            ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                            : project.status === 'in_progress'
                            ? 'bg-primary-500/20 text-primary-300 border border-primary-500/30 animate-pulse'
                            : 'bg-slate-800 text-slate-400'
                        }`}>
                          {project.status.replace('_', ' ')}
                        </span>
                        <button 
                          onClick={(e) => handleDeleteProject(e, project.id)}
                          className="text-slate-500 hover:text-rose-400 transition-colors p-1"
                          title="Delete Project"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </div>
                    
                    <h3 className="font-bold text-base text-slate-100 mb-1 group-hover:text-primary-300 transition-colors line-clamp-1">
                      {project.name}
                    </h3>
                    
                    <p className="text-xs text-slate-400 mb-5 line-clamp-2 leading-relaxed font-normal">
                      {project.description || project.client_request}
                    </p>

                    {project.pages && project.pages.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-4">
                        {project.pages.slice(0, 3).map((p, idx) => (
                          <span key={idx} className="text-[10px] font-mono px-2 py-0.5 bg-slate-950 text-slate-400 rounded-md border border-white/5">
                            /{p.toLowerCase().replace(/\s+/g, '')}
                          </span>
                        ))}
                        {project.pages.length > 3 && (
                          <span className="text-[10px] font-mono px-2 py-0.5 bg-slate-950 text-primary-400 rounded-md">
                            +{project.pages.length - 3} more
                          </span>
                        )}
                      </div>
                    )}

                    <div className="flex items-center justify-between text-xs text-slate-400 font-medium pt-3 border-t border-slate-800">
                      <span className="text-[11px] font-mono">{new Date(project.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric'})}</span>
                      <span className="flex items-center gap-1 group-hover:text-primary-400 transition-colors font-bold text-xs">
                        Open Studio <ArrowRight size={13} />
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Developer FAQ Accordion */}
          <div id="faq" className="max-w-3xl mx-auto pt-8">
            <div className="text-center mb-10">
              <span className="text-[10px] font-extrabold uppercase tracking-widest px-3 py-1 bg-primary-500/15 text-primary-300 rounded-full border border-primary-500/30">
                Knowledge Base
              </span>
              <h2 className="text-3xl font-extrabold text-slate-100 mt-3 tracking-tight">
                Frequently Asked Questions
              </h2>
            </div>

            <div className="space-y-3">
              {faqs.map((faq, index) => {
                const isOpen = expandedFaq === index;
                return (
                  <div 
                    key={index}
                    className="glass-card rounded-2xl border border-white/10 overflow-hidden transition-all"
                  >
                    <button
                      type="button"
                      onClick={() => setExpandedFaq(isOpen ? null : index)}
                      className="w-full p-5 text-left flex items-center justify-between gap-4 font-bold text-xs sm:text-sm text-slate-200 hover:text-primary-300"
                    >
                      <span className="flex items-center gap-2.5">
                        <HelpCircle size={16} className="text-primary-400 flex-shrink-0" />
                        {faq.q}
                      </span>
                      {isOpen ? <ChevronUp size={16} className="text-slate-400" /> : <ChevronDown size={16} className="text-slate-400" />}
                    </button>
                    {isOpen && (
                      <div className="px-5 pb-5 text-xs text-slate-400 leading-relaxed border-t border-slate-800/60 pt-3">
                        {faq.a}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

        </main>

        {/* Footer */}
        <footer className="border-t border-white/10 bg-slate-950/80 backdrop-blur-xl py-12">
          <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-xl bg-primary-600/30 border border-primary-500/40 flex items-center justify-center text-primary-300">
                <Code2 size={18} />
              </div>
              <span className="font-bold text-sm text-slate-200">Antigravity React AI Engineering Platform</span>
            </div>
            <p className="text-slate-500 text-xs text-center md:text-right">
              Orchestrated with Multi-Agent LangGraph • FastAPI • Vite 5.x • React 18
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;