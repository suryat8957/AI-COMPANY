from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger
import json

logger = setup_logger(__name__)

class ProjectManagerAgent(BaseAgent):
    """Project Manager Agent - Orchestrates task planning, milestones, and team assignments for React projects"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.PROJECT_MANAGER,
            name="Sarah Martinez",
            temperature=0.4
        )
    
    def _get_system_prompt(self) -> str:
        return """You are Sarah Martinez, elite Project Manager at a world-class AI Frontend Engineering Studio.

Your responsibilities:
1. Break down complex web applications into clear, coordinated engineering milestones.
2. Coordinate tasks across all specialized team members:
   - CEO / Product Lead (Alex Thompson)
   - UI/UX Designer (Maya Patel)
   - React Architect (David Vance)
   - Senior React Developer (Jordan Lee)
   - File Integrity Specialist (Marcus Brody)
   - Visual & UX Reviewer (Sophia Rossi)
   - QA & Accessibility Auditor (Chris Anderson)
   - Technical Documentation Lead (Emily Zhang)
3. Ensure crisp dependencies and end-to-end quality."""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute project management tasks"""
        task_type = task.get("type", "create_plan")
        
        if task_type == "create_plan":
            return await self._create_project_plan(task, context)
        elif task_type == "monitor_progress":
            return await self._monitor_progress(task, context)
        else:
            return {"status": "error", "message": "Unknown task type"}
    
    async def _create_project_plan(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed React project plan with tasks"""
        logger.info("Project Manager creating React project plan")
        
        client_request = context.get("client_request", "")
        product_spec = context.get("product_spec", {})
        
        prompt = f"""Create a detailed React Engineering Project Plan:

Client Request: {client_request}
Product Specification:
{json.dumps(product_spec, indent=2) if product_spec else 'Standard multi-page React application'}

Generate a structured JSON array of 8-10 sequential tasks.
Each task must have:
- `task_id` (string e.g. 'task_1', 'task_2')
- `title` (string)
- `description` (string)
- `assigned_to` (one of: 'UI Designer', 'React Architect', 'Frontend Developer', 'File Integrity Specialist', 'Visual & UX Reviewer', 'QA Tester', 'Documentation Writer')
- `dependencies` (array of preceding task_ids)
- `estimated_duration` (string)

Return ONLY a valid JSON array of tasks."""

        try:
            response = await self._generate_response(prompt, context)
            tasks = self._parse_tasks(response)
            
            self.add_to_memory(f"Created React project plan with {len(tasks)} tasks")
            return {
                "status": "completed",
                "tasks": tasks,
                "plan_summary": f"Created {len(tasks)} engineering tasks"
            }
        except Exception as e:
            logger.error(f"Project planning failed: {e}")
            return {
                "status": "completed",
                "tasks": self._get_default_tasks(),
                "plan_summary": "Using default React task structure"
            }
    
    def _parse_tasks(self, response: str) -> List[Dict]:
        """Parse tasks from LLM response"""
        parsed = self._extract_json(response)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
        return self._get_default_tasks()
    
    def _get_default_tasks(self) -> List[Dict]:
        """Get default task structure for multi-page React engineering"""
        return [
            {
                "task_id": "task_1",
                "title": "Design System & UI Tokens",
                "description": "Create bespoke design system, archetype tokens, color palette, and typography pairing",
                "assigned_to": "UI Designer",
                "dependencies": [],
                "estimated_duration": "1 hour"
            },
            {
                "task_id": "task_2",
                "title": "React Architecture & Routing Blueprint",
                "description": "Design component hierarchy, React Router v6 tree, and package manifest",
                "assigned_to": "React Architect",
                "dependencies": ["task_1"],
                "estimated_duration": "1 hour"
            },
            {
                "task_id": "task_3",
                "title": "Project Scaffolding & Design Tokens",
                "description": "Generate package.json, vite.config.js, index.html, index.css, mockData.js, and AppContext.jsx",
                "assigned_to": "Frontend Developer",
                "dependencies": ["task_2"],
                "estimated_duration": "2 hours"
            },
            {
                "task_id": "task_4",
                "title": "UI Components & Layout Development",
                "description": "Build Button, Card, Badge, Modal, SectionTitle, Navbar, Footer, and MainLayout",
                "assigned_to": "Frontend Developer",
                "dependencies": ["task_3"],
                "estimated_duration": "3 hours"
            },
            {
                "task_id": "task_5",
                "title": "Multi-Page & Routing Implementation",
                "description": "Develop all pages (HomePage, AboutPage, ServicesPage, PricingPage, ContactPage, NotFoundPage) and App.jsx",
                "assigned_to": "Frontend Developer",
                "dependencies": ["task_4"],
                "estimated_duration": "4 hours"
            },
            {
                "task_id": "task_6",
                "title": "File & Dependency Integrity Verification",
                "description": "Verify 100% of required files exist and check all local and external import paths",
                "assigned_to": "File Integrity Specialist",
                "dependencies": ["task_5"],
                "estimated_duration": "1 hour"
            },
            {
                "task_id": "task_7",
                "title": "Visual & UX Review",
                "description": "Audit visual hierarchy, design authenticity, and responsive mobile feel",
                "assigned_to": "Visual & UX Reviewer",
                "dependencies": ["task_6"],
                "estimated_duration": "1 hour"
            },
            {
                "task_id": "task_8",
                "title": "QA & Accessibility Audit",
                "description": "Audit React hooks, interactive forms, accessibility (ARIA), and JSX syntax",
                "assigned_to": "QA Tester",
                "dependencies": ["task_7"],
                "estimated_duration": "2 hours"
            },
            {
                "task_id": "task_9",
                "title": "Project Documentation & README",
                "description": "Create production README with setup, run, build, and architecture guides",
                "assigned_to": "Documentation Writer",
                "dependencies": ["task_8"],
                "estimated_duration": "1 hour"
            }
        ]
    
    async def _monitor_progress(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor project progress"""
        completed_tasks = context.get("completed_tasks", [])
        total_tasks = context.get("total_tasks", 0)
        progress = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        return {
            "status": "completed",
            "progress": progress,
            "completed_tasks": len(completed_tasks),
            "total_tasks": total_tasks
        }