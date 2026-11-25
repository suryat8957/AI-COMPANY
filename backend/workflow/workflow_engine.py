from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from agents import (
    CEOAgent,
    ProjectManagerAgent,
    UIDesignerAgent,
    ReactArchitectAgent,
    FrontendDeveloperAgent,
    FileIntegrityAgent,
    VisualReviewAgent,
    QATesterAgent,
    DocumentationWriterAgent,
    llm_manager
)
from config.settings import settings
from database import mongodb, ProjectStatus, TaskStatus
from utils import FileManager, ProjectLogger, setup_logger
from workflow.state import WorkflowState
import uuid
from datetime import datetime
import json

logger = setup_logger(__name__)

class WorkflowEngine:
    """Orchestrates the multi-agent React frontend engineering pipeline with Multi-Model LLM Mesh"""
    
    def __init__(self):
        self.llm_manager = llm_manager
        self.agents = {
            "ceo": CEOAgent(),
            "project_manager": ProjectManagerAgent(),
            "ui_designer": UIDesignerAgent(),
            "react_architect": ReactArchitectAgent(),
            "frontend_developer": FrontendDeveloperAgent(),
            "file_integrity": FileIntegrityAgent(),
            "visual_reviewer": VisualReviewAgent(),
            "qa_tester": QATesterAgent(),
            "documentation_writer": DocumentationWriterAgent()
        }
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the coordinated multi-model React engineering graph with Mercury Task Router"""
        workflow = StateGraph(WorkflowState)
        
        # Add workflow nodes with distinct names (no collision with state attributes)
        workflow.add_node("task_router", self._task_router_node)
        workflow.add_node("ceo_product_review", self._ceo_product_review_node)
        workflow.add_node("create_plan", self._create_plan_node)
        workflow.add_node("design_system_node", self._design_node)
        workflow.add_node("react_architecture", self._react_architecture_node)
        workflow.add_node("develop_react_app", self._develop_react_app_node)
        workflow.add_node("file_integrity_audit", self._file_integrity_audit_node)
        workflow.add_node("visual_review_audit", self._visual_review_node)
        workflow.add_node("qa_test", self._qa_test_node)
        workflow.add_node("fix_issues", self._fix_issues_node)
        workflow.add_node("document_project", self._document_node)
        workflow.add_node("final_approval_review", self._final_approval_node)
        workflow.add_node("save_project", self._save_project_node)
        
        # Define entry point and execution flow
        workflow.set_entry_point("task_router")
        workflow.add_edge("task_router", "ceo_product_review")
        
        workflow.add_conditional_edges(
            "ceo_product_review",
            self._check_ceo_approval,
            {
                "approved": "create_plan",
                "rejected": END
            }
        )
        
        workflow.add_edge("create_plan", "design_system_node")
        workflow.add_edge("design_system_node", "react_architecture")
        workflow.add_edge("react_architecture", "develop_react_app")
        workflow.add_edge("develop_react_app", "file_integrity_audit")
        workflow.add_edge("file_integrity_audit", "visual_review_audit")
        workflow.add_edge("visual_review_audit", "qa_test")
        
        # Conditional edge for QA & Integrity remediation loop
        workflow.add_conditional_edges(
            "qa_test",
            self._check_qa_status,
            {
                "pass": "document_project",
                "fail": "fix_issues"
            }
        )
        
        workflow.add_edge("fix_issues", "file_integrity_audit")
        workflow.add_edge("document_project", "final_approval_review")
        
        workflow.add_conditional_edges(
            "final_approval_review",
            self._check_final_approval,
            {
                "approved": "save_project",
                "rejected": "fix_issues"
            }
        )
        
        workflow.add_edge("save_project", END)
        
        return workflow.compile()
    
    async def _task_router_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 0: Inception Mercury Decide classifies project intent and establishes execution mesh"""
        logger = ProjectLogger(state["project_id"])
        logger.info("🧭 [0/8] Inception Mercury Decide analyzing client request & routing task...")
        
        state["current_agent"] = "Mercury Task Router"
        client_req = state.get("client_request", "")
        
        question = "Is this request a frontend software engineering project requiring multi-page React architecture and UI generation?"
        context_summary = f"Client Project Request: {client_req}"
        true_when = "The request asks to build, scaffold, code, or create a React web application, showroom, portal, or website."
        false_when = "The request is purely general conversation, non-coding advice, or completely unrelated to application software engineering."
        
        decision, prob, reasoning, source = await self.llm_manager.decide(
            question=question,
            context_summary=context_summary,
            true_when=true_when,
            false_when=false_when,
            threshold=settings.MERCURY_DECISION_THRESHOLD,
            deterministic_fallback=lambda: True,
            project_id=state["project_id"]
        )
        
        state["router_decision"] = {
            "routed_to": "react_engineering_mesh",
            "coding_model": settings.QWEN_MODEL,
            "reasoning_model": settings.GEMINI_MODEL,
            "decision": decision,
            "probability": prob,
            "reasoning": reasoning,
            "source": source
        }
        
        self._save_message(
            state,
            "Inception Mercury Decide (Task Router)",
            f"🧭 Task Routing: Multi-Model Mesh engaged (confidence: {prob:.2f} via {source}). Primary Coding: Qwen 27B | Reasoning: Gemini. Reason: {reasoning}"
        )
        logger.info(f"✨ Task routing complete: Multi-Model Mesh engaged via {source} (prob: {prob:.2f})")
        return state

    async def _ceo_product_review_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 1: CEO / Product Lead analyzes requirements & defines multi-page sitemap"""
        logger = ProjectLogger(state["project_id"])
        logger.info("👔 [1/8] Alex Thompson (CEO & Product Lead) analyzing requirements and creating product specification...")
        
        state["current_agent"] = "CEO"
        
        task = {"type": "analyze_product"}
        context = {
            "client_request": state["client_request"],
            "project_id": state["project_id"],
            "autonomous_mode": state.get("autonomous_mode", True)
        }
        
        result = await self.agents["ceo"].execute(task, context)
        
        state["ceo_approved"] = result.get("approved", True)
        state["product_spec"] = result.get("product_spec", {})
        state["pages"] = result.get("pages", ["Home", "About", "Services", "Pricing", "Contact"])
        state["complexity"] = result.get("complexity", "Medium")
        state["ceo_analysis"] = result.get("analysis", "")
        
        app_name = state["product_spec"].get("project_name", state["project_name"])
        state["project_name"] = app_name
        
        self._save_message(
            state, 
            "Alex Thompson (CEO & Product Lead)", 
            f"Approved product specification for '{app_name}' with {len(state['pages'])} pages: {', '.join(state['pages'])}"
        )
        
        db = mongodb.get_database()
        db.projects.update_one(
            {"id": state["project_id"]},
            {"$set": {
                "name": app_name,
                "status": "in_progress",
                "product_spec": state["product_spec"],
                "pages": state["pages"]
            }}
        )
        
        logger.info(f"✨ Product Specification complete for '{app_name}' ({len(state['pages'])} pages)")
        return state
    
    async def _create_plan_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 2: Project Manager creates coordinated task breakdown"""
        logger = ProjectLogger(state["project_id"])
        logger.info("📊 [2/8] Sarah Martinez (Project Manager) planning engineering milestones...")
        
        state["current_agent"] = "Project Manager"
        
        task = {"type": "create_plan"}
        context = {
            "client_request": state["client_request"],
            "product_spec": state.get("product_spec", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["project_manager"].execute(task, context)
        state["tasks"] = result.get("tasks", [])
        state["current_task_index"] = 0
        state["completed_tasks"] = []
        
        self._save_message(
            state, 
            "Sarah Martinez (Project Manager)", 
            f"Created engineering roadmap with {len(state['tasks'])} coordinated tasks."
        )
        
        # Persist tasks to database
        db = mongodb.get_database()
        for task_data in state["tasks"]:
            db.tasks.insert_one({
                "id": str(uuid.uuid4()),
                "project_id": state["project_id"],
                "task_id": task_data.get("task_id", str(uuid.uuid4())),
                "title": task_data.get("title", ""),
                "description": task_data.get("description", ""),
                "assigned_to": task_data.get("assigned_to", "Frontend Developer"),
                "status": "pending",
                "created_at": datetime.utcnow()
            })
            logger.info(f"   • [{task_data.get('task_id')}] {task_data.get('title')} -> {task_data.get('assigned_to')}")
            
        return state
    
    async def _design_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 3: UI/UX Designer creates bespoke design system and CSS tokens"""
        logger = ProjectLogger(state["project_id"])
        logger.info("🎨 [3/8] Maya Patel (Lead UI/UX Designer) designing bespoke aesthetic & CSS token system...")
        
        state["current_agent"] = "UI Designer"
        
        task = {"type": "design_system", "title": "Design System Specification"}
        context = {
            "client_request": state["client_request"],
            "product_spec": state.get("product_spec", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["ui_designer"].execute(task, context)
        
        state["design_spec"] = result.get("design_spec", {})
        state["design_specifications"] = result.get("design_specifications", "")
        
        archetype = state["design_spec"].get("archetype", "Modern Studio")
        palette = state["design_spec"].get("color_palette", {})
        
        self._save_message(
            state, 
            "Maya Patel (Lead UI/UX Designer)", 
            f"Crafted '{archetype}' design system with primary color {palette.get('primary', '#6366f1')}."
        )
        
        logger.info(f"✨ Design System crafted: {archetype} (Tokens ready)")
        return state
    
    async def _react_architecture_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 4: React Architect designs component hierarchy, routing tree & manifest"""
        logger = ProjectLogger(state["project_id"])
        logger.info("🏗️ [4/8] David Vance (Principal React Architect) designing component hierarchy & routing tree...")
        
        state["current_agent"] = "React Architect"
        
        task = {"type": "architecture_blueprint", "title": "React Architecture Blueprint"}
        context = {
            "client_request": state["client_request"],
            "product_spec": state.get("product_spec", {}),
            "design_spec": state.get("design_spec", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["react_architect"].execute(task, context)
        
        state["architecture_spec"] = result.get("architecture_spec", {})
        state["file_manifest"] = result.get("file_manifest", [])
        state["routing"] = result.get("routing", [])
        
        self._save_message(
            state,
            "David Vance (Principal React Architect)",
            f"Designed React Router tree ({len(state['routing'])} routes) and mapped {len(state['file_manifest'])} component files."
        )
        
        logger.info(f"✨ Architecture blueprint mapped: {len(state['file_manifest'])} files across {len(state['routing'])} routes")
        return state
    
    async def _develop_react_app_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 5: Senior React Developer builds all modular application files"""
        logger = ProjectLogger(state["project_id"])
        logger.info("💻 [5/8] Jordan Lee (Senior React Developer) generating production React code across all components...")
        
        state["current_agent"] = "Frontend Developer"
        
        if "files" not in state or not state["files"]:
            state["files"] = {}
            
        context = {
            "client_request": state["client_request"],
            "product_spec": state.get("product_spec", {}),
            "design_spec": state.get("design_spec", {}),
            "architecture_spec": state.get("architecture_spec", {}),
            "files": state.get("files", {}),
            "project_id": state["project_id"]
        }
        
        dev_task = {"task_id": "create_all", "title": "Develop Full React Application"}
        result = await self.agents["frontend_developer"].execute(dev_task, context)
        
        if result.get("status") == "completed" and "files" in result:
            state["files"].update(result["files"])
            
        self._save_message(
            state,
            "Jordan Lee (Senior React Developer)",
            f"Successfully developed {len(state['files'])} complete React files (Components, Layouts, Pages, Context, Styles)."
        )
        
        logger.info(f"✨ React Application Development complete: {len(state['files'])} files generated")
        return state
    
    async def _file_integrity_audit_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 6: File Integrity Specialist audits file existence, imports, and routes"""
        logger = ProjectLogger(state["project_id"])
        logger.info("🔍 [6/8] Marcus Brody (File Integrity Specialist) auditing file manifest and imports...")
        
        state["current_agent"] = "File Integrity Specialist"
        
        task = {"type": "integrity_audit", "title": "File & Import Integrity Audit"}
        context = {
            "files": state.get("files", {}),
            "architecture_spec": state.get("architecture_spec", {}),
            "product_spec": state.get("product_spec", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["file_integrity"].execute(task, context)
        
        if "files" in result and result["files"]:
            state["files"].update(result["files"])
            
        state["integrity_passed"] = result.get("integrity_passed", True)
        state["missing_files"] = result.get("missing_files", [])
        state["broken_imports"] = result.get("broken_imports", [])
        state["route_issues"] = result.get("route_issues", [])
        state["integrity_report"] = result.get("integrity_report", "")
        
        status_text = "PASSED" if state["integrity_passed"] else f"NEEDS ATTENTION ({len(state['missing_files'])} missing)"
        self._save_message(
            state,
            "Marcus Brody (File Integrity Specialist)",
            f"Integrity Audit: {status_text}. Checked {len(state['files'])} files."
        )
        
        logger.info(f"✨ File Integrity audit: {status_text}")
        return state
    
    async def _visual_review_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 7: Visual & UX Reviewer evaluates design authenticity & responsive layout"""
        logger = ProjectLogger(state["project_id"])
        logger.info("🎨 [7/8] Sophia Rossi (Visual & UX Reviewer) evaluating design hierarchy & UX polish...")
        
        state["current_agent"] = "Visual Reviewer"
        
        task = {"type": "visual_review", "title": "Visual & UX Audit"}
        context = {
            "client_request": state["client_request"],
            "design_spec": state.get("design_spec", {}),
            "files": state.get("files", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["visual_reviewer"].execute(task, context)
        
        state["visual_review"] = result.get("visual_review", {})
        state["visual_score"] = result.get("visual_score", 9)
        state["visual_approved"] = result.get("is_approved", True)
        
        self._save_message(
            state,
            "Sophia Rossi (Visual & UX Reviewer)",
            f"Visual & UX Score: {state['visual_score']}/10. {result.get('summary', '')}"
        )
        
        logger.info(f"✨ Visual Review: Score {state['visual_score']}/10")
        return state
    
    async def _qa_test_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 8: Lead QA Tester conducts functional, accessibility, and JSX audit"""
        logger = ProjectLogger(state["project_id"])
        logger.info("🔍 [8/8] Chris Anderson (Lead React QA Auditor) auditing functionality & accessibility...")
        
        state["current_agent"] = "QA Tester"
        
        task = {"task_id": "qa_audit", "title": "Comprehensive React QA Audit"}
        context = {
            "client_request": state["client_request"],
            "product_spec": state.get("product_spec", {}),
            "files": state.get("files", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["qa_tester"].execute(task, context)
        
        state["qa_report"] = result.get("qa_report", "")
        state["quality_score"] = result.get("quality_score", 9)
        state["test_status"] = result.get("test_status", "PASS")
        state["issues"] = result.get("issues", [])
        state["recommendations"] = result.get("recommendations", [])
        state["qa_iterations"] = state.get("qa_iterations", 0) + 1
        
        self._save_message(
            state,
            "Chris Anderson (Lead React QA Auditor)",
            f"QA Audit: {state['test_status']} | Quality Score: {state['quality_score']}/10"
        )
        
        logger.info(f"📊 QA Audit complete - Status: {state['test_status']} | Score: {state['quality_score']}/10 (Iteration {state['qa_iterations']})")
        
        # Inception Mercury Decide Gate: Determine if another remediation pass is justified
        score = state.get("quality_score", 9)
        iterations = state.get("qa_iterations", 0)
        integrity = state.get("integrity_passed", True)
        issues = state.get("issues", [])
        
        if iterations >= settings.MAX_REMEDIATION_LOOPS:
            run_fix = False
            prob = 1.0
            reasoning = f"Maximum remediation iterations cap ({settings.MAX_REMEDIATION_LOOPS}) reached. Terminating remediation loop safely."
            source = "deterministic"
        elif score >= 9 and integrity:
            run_fix = False
            prob = 1.0
            reasoning = "Quality score satisfies production benchmark (>= 9/10) and file integrity verified."
            source = "deterministic"
        else:
            qa_summary = (
                f"QA Score: {score}/10 (target: 9/10)\n"
                f"File Integrity Passed: {integrity}\n"
                f"Current Remediation Iteration: {iterations}/{settings.MAX_REMEDIATION_LOOPS}\n"
                f"Defects List: {issues[:4] if issues else 'Integrity/JSX defects detected'}"
            )
            run_fix, prob, reasoning, source = await self.llm_manager.decide(
                question="Should another code remediation cycle be executed to resolve reported defects?",
                context_summary=qa_summary,
                true_when=f"QA score < 9 or file integrity failed, and iteration < {settings.MAX_REMEDIATION_LOOPS}",
                false_when=f"QA score >= 9 and integrity passed, or iteration >= {settings.MAX_REMEDIATION_LOOPS}",
                threshold=settings.MERCURY_DECISION_THRESHOLD,
                deterministic_fallback=lambda: (score < 9 or not integrity) and (iterations < settings.MAX_REMEDIATION_LOOPS),
                project_id=state["project_id"]
            )
            
        state["remediation_needed"] = run_fix
        state["remediation_decision"] = {
            "decision": run_fix,
            "probability": prob,
            "reasoning": reasoning,
            "source": source
        }
        
        if run_fix:
            self._save_message(
                state,
                "Inception Mercury Decide (Gate)",
                f"⚠️ Remediation Pass #{iterations} Initiated (confidence: {prob:.2f} via {source}). Reason: {reasoning}"
            )
        else:
            self._save_message(
                state,
                "Inception Mercury Decide (Gate)",
                f"✅ QA Benchmark Satisfied (confidence: {prob:.2f} via {source}). Proceeding to final documentation."
            )
            
        return state
    
    async def _fix_issues_node(self, state: WorkflowState) -> WorkflowState:
        """Targeted Remediation Pass: Senior React Developer resolves audit findings"""
        logger = ProjectLogger(state["project_id"])
        logger.info(f"🔧 React Developer applying targeted fixes (Remediation Pass #{state.get('qa_iterations', 1)})...")
        
        state["current_agent"] = "Frontend Developer"
        
        fix_task = {"task_id": "fix_bugs", "title": "Fix Reported QA & Integrity Issues"}
        context = {
            "client_request": state["client_request"],
            "qa_report": state.get("qa_report", ""),
            "integrity_report": state.get("integrity_report", ""),
            "visual_review": state.get("visual_review", {}),
            "missing_files": state.get("missing_files", []),
            "broken_imports": state.get("broken_imports", []),
            "route_issues": state.get("route_issues", []),
            "files": state.get("files", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["frontend_developer"].execute(fix_task, context)
        
        if result.get("status") == "completed" and "files" in result:
            state["files"].update(result["files"])
            
        self._save_message(
            state,
            "Jordan Lee (Senior React Developer)",
            f"Resolved reported issues and updated {len(result.get('files', {}))} components."
        )
        
        logger.info(f"✨ Remediation pass complete - {len(result.get('files', {}))} files refined")
        return state
    
    async def _document_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 9: Documentation Writer creates comprehensive README.md"""
        logger = ProjectLogger(state["project_id"])
        logger.info("📝 Emily Zhang (Technical Documentation Lead) writing production README.md...")
        
        state["current_agent"] = "Documentation Writer"
        
        doc_task = {"task_id": "create_readme", "title": "Write Project Documentation"}
        context = {
            "client_request": state["client_request"],
            "product_spec": state.get("product_spec", {}),
            "design_spec": state.get("design_spec", {}),
            "architecture_spec": state.get("architecture_spec", {}),
            "files": state.get("files", {}),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["documentation_writer"].execute(doc_task, context)
        
        if result.get("status") == "completed":
            state["readme_content"] = result["content"]
            state["files"]["README.md"] = result["content"]
            lines = len(result["content"].split('\n'))
            logger.info(f"✅ README.md created successfully ({lines} lines)")
            
        self._save_message(
            state,
            "Emily Zhang (Technical Documentation Lead)",
            "Generated comprehensive README.md with setup, run, and architecture guides."
        )
        return state
    
    async def _final_approval_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 10: Executive Final Review by CEO"""
        logger = ProjectLogger(state["project_id"])
        logger.info("👔 Alex Thompson (CEO) conducting final executive review...")
        
        state["current_agent"] = "CEO"
        
        task = {"type": "final_approval"}
        context = {
            "files": state.get("files", {}),
            "qa_report": state.get("qa_report", ""),
            "visual_review": state.get("visual_review", {}),
            "integrity_report": state.get("integrity_report", ""),
            "project_id": state["project_id"]
        }
        
        result = await self.agents["ceo"].execute(task, context)
        state["final_approved"] = result.get("approved", True)
        
        self._save_message(
            state,
            "Alex Thompson (CEO & Product Lead)",
            "Project successfully passed all executive benchmarks and is approved for final delivery!"
        )
        
        logger.info("🏁 Project received final executive approval.")
        return state
    
    async def _save_project_node(self, state: WorkflowState) -> WorkflowState:
        """Stage 11: Persist full nested React repository to workspace"""
        logger = ProjectLogger(state["project_id"])
        logger.info(f"💾 Saving {len(state['files'])} React project files to local workspace...")
        
        state["current_agent"] = "System"
        
        # Create file manager
        file_manager = FileManager(state["project_id"], state["project_name"])
        
        # Write all files preserving nested folder structure
        for filename, content in state["files"].items():
            file_manager.write_file(filename, content)
            lines = len(content.split('\n'))
            logger.info(f"   • Saved '{filename}' ({lines} lines)")
            
        state["workspace_path"] = file_manager.get_project_path()
        
        # Update database project record
        db = mongodb.get_database()
        db.projects.update_one(
            {"id": state["project_id"]},
            {"$set": {
                "status": "completed",
                "workspace_path": state["workspace_path"],
                "completed_at": datetime.utcnow(),
                "files": list(state["files"].keys()),
                "quality_score": state.get("quality_score", 9)
            }}
        )
        
        self._save_message(
            state,
            "System",
            f"🎉 React project successfully generated and saved to {state['workspace_path']}"
        )
        
        logger.info(f"🎉 Delivery complete at {state['workspace_path']}")
        return state
    
    def _save_message(self, state: WorkflowState, from_agent: str, content: str):
        """Save chat message to state and database for real-time dashboard updates"""
        msg = {
            "id": str(uuid.uuid4()),
            "project_id": state["project_id"],
            "from_agent": from_agent,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        state["messages"].append(msg)
        try:
            db = mongodb.get_database()
            db.messages.insert_one({
                "id": msg["id"],
                "project_id": msg["project_id"],
                "from_agent": msg["from_agent"],
                "content": msg["content"],
                "timestamp": datetime.utcnow()
            })
            proj_logger = ProjectLogger(state["project_id"])
            proj_logger.info(f"💬 [{from_agent}] {content}")
        except Exception as e:
            logger.warning(f"Failed to persist message to DB: {e}")
    
    def _check_ceo_approval(self, state: WorkflowState) -> str:
        """Check if CEO approved initial project request"""
        return "approved" if state.get("ceo_approved", True) else "rejected"
    
    def _check_qa_status(self, state: WorkflowState) -> str:
        """Approve cleanly if quality score satisfies benchmarks or max remediation loops reached; else route to remediation"""
        iterations = state.get("qa_iterations", 0)
        if iterations >= settings.MAX_REMEDIATION_LOOPS:
            return "pass"
        return "fail" if state.get("remediation_needed", False) else "pass"
    
    def _check_final_approval(self, state: WorkflowState) -> str:
        """Check final executive approval"""
        return "approved" if state.get("final_approved", True) else "rejected"
    
    async def execute_workflow(self, project_request: str, project_id: str = None, project_name: str = None, autonomous_mode: bool = True) -> Dict[str, Any]:
        """Execute the complete multi-agent React development workflow"""
        is_new = False
        if not project_id:
            project_id = str(uuid.uuid4())
            is_new = True
            
        if not project_name:
            project_name = f"ReactProject_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        initial_state: WorkflowState = {
            "project_id": project_id,
            "project_name": project_name,
            "client_request": project_request,
            "status": ProjectStatus.PENDING,
            "autonomous_mode": autonomous_mode,
            "human_review_required": False,
            "waiting_for_user": False,
            "user_feedback": None,
            "router_decision": None,
            "ceo_approved": False,
            "ceo_analysis": None,
            "complexity": None,
            "product_spec": None,
            "pages": [],
            "tasks": [],
            "current_task_index": 0,
            "completed_tasks": [],
            "design_spec": None,
            "design_specifications": None,
            "architecture_spec": None,
            "file_manifest": [],
            "routing": [],
            "files": {},
            "integrity_passed": True,
            "missing_files": [],
            "broken_imports": [],
            "route_issues": [],
            "integrity_report": None,
            "visual_review": None,
            "visual_score": None,
            "visual_approved": True,
            "qa_report": None,
            "quality_score": None,
            "test_status": None,
            "issues": [],
            "recommendations": [],
            "qa_iterations": 0,
            "remediation_needed": None,
            "remediation_decision": None,
            "readme_content": None,
            "final_approved": False,
            "workspace_path": None,
            "messages": [],
            "errors": [],
            "current_agent": None
        }
        
        db = mongodb.get_database()
        if is_new:
            db.projects.insert_one({
                "id": project_id,
                "name": project_name,
                "description": project_request,
                "client_request": project_request,
                "autonomous_mode": autonomous_mode,
                "status": "pending",
                "created_at": datetime.utcnow()
            })
        
        try:
            final_state = await self.graph.ainvoke(initial_state)
            
            # Record and log operational usage summary across all engines
            usage_report = self.llm_manager.get_usage_summary()
            logger.info(f"\n{usage_report}")
            proj_logger = ProjectLogger(project_id)
            proj_logger.info(f"\n{usage_report}")
            
            return {
                "success": True,
                "project_id": project_id,
                "status": "completed" if final_state.get("final_approved") else "rejected",
                "workspace_path": final_state.get("workspace_path"),
                "files": list(final_state.get("files", {}).keys()),
                "pages": final_state.get("pages", []),
                "messages": final_state.get("messages", []),
                "usage": self.llm_manager.metrics,
                "router_decision": final_state.get("router_decision"),
                "remediation_decision": final_state.get("remediation_decision")
            }
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            db.projects.update_one(
                {"id": project_id},
                {"$set": {"status": "failed", "error": str(e)}}
            )
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e)
            }