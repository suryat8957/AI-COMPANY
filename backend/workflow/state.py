from typing import TypedDict, List, Dict, Any, Optional
from database.models import ProjectStatus, TaskStatus

class WorkflowState(TypedDict):
    """State object passed between workflow nodes in the Multi-Model Mesh Engineering Studio"""
    # Project Information
    project_id: str
    project_name: str
    client_request: str
    status: ProjectStatus
    autonomous_mode: bool
    human_review_required: bool
    waiting_for_user: bool
    user_feedback: Optional[str]
    
    # Task Router Phase (Inception Mercury Decide / Deterministic)
    router_decision: Optional[Dict[str, Any]]
    
    # Requirements & Product Phase (CEO / Product Lead - Gemini)
    ceo_approved: bool
    ceo_analysis: Optional[str]
    complexity: Optional[str]
    product_spec: Optional[Dict[str, Any]]
    pages: Optional[List[str]]
    
    # Project Management Phase (Project Manager - Gemini)
    tasks: List[Dict[str, Any]]
    current_task_index: int
    completed_tasks: List[str]
    
    # Design Phase (UI/UX Designer - Qwen)
    design_spec: Optional[Dict[str, Any]]
    design_specifications: Optional[str]
    
    # Architecture Phase (React Architect - Qwen)
    architecture_spec: Optional[Dict[str, Any]]
    file_manifest: List[str]
    routing: List[Dict[str, Any]]
    
    # Development Phase (Senior React Developer - Qwen)
    files: Dict[str, str]
    
    # File Integrity Phase (File Integrity Specialist - Qwen)
    integrity_passed: bool
    missing_files: List[str]
    broken_imports: List[str]
    route_issues: List[str]
    integrity_report: Optional[str]
    
    # Visual Review Phase (Visual & UX Reviewer - Gemini)
    visual_review: Optional[Dict[str, Any]]
    visual_score: Optional[int]
    visual_approved: bool
    
    # QA & Audit Phase (QA Tester - Gemini + Mercury Decide Gate)
    qa_report: Optional[str]
    quality_score: Optional[int]
    test_status: Optional[str]
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    qa_iterations: int
    remediation_needed: Optional[bool]
    remediation_decision: Optional[Dict[str, Any]]
    
    # Documentation Phase (Documentation Writer - Qwen)
    readme_content: Optional[str]
    
    # Delivery Phase (CEO Final Review - Gemini)
    final_approved: bool
    workspace_path: Optional[str]
    
    # Real-time Communication & Logs
    messages: List[Dict[str, Any]]
    errors: List[str]
    current_agent: Optional[str]