from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import json
from datetime import datetime
from database import mongodb, ProjectRequest
from workflow import WorkflowEngine
from utils import setup_logger
from config.settings import settings
from agents.llm_manager import llm_manager
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import zipfile
import io
import shutil
import asyncio
import uuid

logger = setup_logger(__name__)
router = APIRouter()

# Initialize workflow engine
workflow_engine = WorkflowEngine()

class EnhancePromptRequest(BaseModel):
    prompt: str

class UserFeedbackRequest(BaseModel):
    feedback: str
    approved: bool = True

@router.post("/api/enhance-prompt")
async def enhance_prompt(request: EnhancePromptRequest):
    """Enhance user's website idea into a detailed multi-page React application prompt"""
    try:
        user_input = request.prompt.strip()
        if not user_input:
            raise HTTPException(status_code=400, detail="Prompt input cannot be empty")

        system_prompt = """You are an elite Product Architect & React UX Consultant.
Transform the user's brief idea into a comprehensive, multi-page React web application specification.

Structure your response with:
1. "Create a modern, high-conversion multi-page React web application for [Concept]..."
2. Bespoke Visual Identity & Aesthetic (Design Archetype, Color Palette, Typography Pairing).
3. 4-6 Dedicated Pages with Key Features (e.g. Home, About, Services/Products, Pricing/Booking, Contact, Interactive Tools).
4. Rich Interactivity (Tabs, Modals, Dynamic Filters, State-driven Forms, Animated Micro-interactions).
5. Tech Stack: React 18, Vite, React Router v6, Lucide Icons, CSS Variables Design System.

Keep the prompt concise, inspiring, around 120-180 words, with no markdown code blocks or preambles."""

        # Use 3-Model LLM Mesh (Gemini primary for planning/reasoning, Qwen fallback)
        content = await llm_manager.execute_with_fallback(
            role="ceo",
            prompt=f"Enhance this user product request into a rich specification: {user_input}",
            system_prompt=system_prompt,
            agent_name="Prompt Enhancer",
            temperature=0.7
        )

        if not content:
            raise HTTPException(status_code=500, detail="No LLM provider available to enhance prompt.")

        if isinstance(content, list):
            text_blocks = []
            for item in content:
                if isinstance(item, str):
                    text_blocks.append(item)
                elif isinstance(item, dict) and "text" in item:
                    text_blocks.append(item["text"])
            content = " ".join(text_blocks)

        return {
            "status": "success",
            "enhanced_prompt": str(content).strip()
        }
    except Exception as e:
        logger.error(f"Error enhancing prompt: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket connections for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@router.post("/api/projects/create")
async def create_project(request: ProjectRequest):
    """Create a new React frontend project and trigger multi-agent pipeline"""
    try:
        logger.info(f"Received React project request: {request.description}")
        
        project_id = str(uuid.uuid4())
        project_name = request.name if request.name else f"ReactProject_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        autonomous_mode = getattr(request, "autonomous_mode", True)
        
        # Create initial DB record so dashboard can load it
        db = mongodb.get_database()
        db.projects.insert_one({
            "id": project_id,
            "name": project_name,
            "description": request.description,
            "client_request": request.description,
            "autonomous_mode": autonomous_mode,
            "status": "pending",
            "created_at": datetime.utcnow()
        })
        
        # Background workflow task
        async def run_workflow():
            try:
                result = await workflow_engine.execute_workflow(
                    request.description, 
                    project_id=project_id,
                    project_name=project_name,
                    autonomous_mode=autonomous_mode
                )
                
                # Broadcast real-time completion
                await manager.broadcast({
                    "type": "project_completed",
                    "data": result
                })
            except Exception as e:
                logger.error(f"Background workflow failed: {e}")
                
        # Launch in background
        asyncio.create_task(run_workflow())
        
        return {"success": True, "project_id": project_id, "project_name": project_name}
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/projects")
async def list_projects():
    """List all projects sorted newest first"""
    try:
        db = mongodb.get_database()
        projects = list(db.projects.find({}, {"_id": 0}).sort("created_at", -1).limit(50))
        for p in projects:
            if "created_at" in p and isinstance(p["created_at"], datetime):
                p["created_at"] = p["created_at"].isoformat()
            if "completed_at" in p and isinstance(p["completed_at"], datetime):
                p["completed_at"] = p["completed_at"].isoformat()
        return {"projects": projects}
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get complete project details, tasks, messages, and files"""
    try:
        db = mongodb.get_database()
        project = db.projects.find_one({"id": project_id}, {"_id": 0})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if "created_at" in project and isinstance(project["created_at"], datetime):
            project["created_at"] = project["created_at"].isoformat()
        if "completed_at" in project and isinstance(project["completed_at"], datetime):
            project["completed_at"] = project["completed_at"].isoformat()
        
        # Get tasks
        tasks = list(db.tasks.find({"project_id": project_id}, {"_id": 0}).sort("created_at", 1))
        for t in tasks:
            if "created_at" in t and isinstance(t["created_at"], datetime):
                t["created_at"] = t["created_at"].isoformat()
        project["tasks"] = tasks
        
        # Get messages
        messages = list(db.messages.find({"project_id": project_id}, {"_id": 0}).sort("timestamp", 1))
        for m in messages:
            if "timestamp" in m and isinstance(m["timestamp"], datetime):
                m["timestamp"] = m["timestamp"].isoformat()
        project["messages"] = messages
        
        # If project has a workspace path, list existing files
        if project.get("workspace_path"):
            wpath = Path(project["workspace_path"])
            if wpath.exists():
                file_list = []
                for p in wpath.rglob('*'):
                    if p.is_file():
                        file_list.append(str(p.relative_to(wpath)).replace('\\', '/'))
                project["files"] = sorted(file_list)
        
        return project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/projects/{project_id}/file-content")
async def get_project_file_content(project_id: str, file_path: str = Query(..., description="Relative file path like src/App.jsx")):
    """Get the source code content of a specific file in the project"""
    try:
        db = mongodb.get_database()
        project = db.projects.find_one({"id": project_id})
        
        if not project or not project.get("workspace_path"):
            raise HTTPException(status_code=404, detail="Project not found")
            
        wpath = Path(project["workspace_path"])
        target_file = (wpath / file_path).resolve()
        
        # Prevent directory traversal attacks
        if not str(target_file).startswith(str(wpath.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")
            
        if not target_file.exists() or not target_file.is_file():
            raise HTTPException(status_code=404, detail=f"File '{file_path}' not found")
            
        with open(target_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            
        return {
            "project_id": project_id,
            "file_path": file_path,
            "content": content
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/projects/{project_id}/download")
async def download_project(project_id: str):
    """Download the full React project as a clean ZIP archive"""
    try:
        db = mongodb.get_database()
        project = db.projects.find_one({"id": project_id})
        
        if not project or not project.get("workspace_path"):
            raise HTTPException(status_code=404, detail="Project not found")
        
        workspace_path = Path(project["workspace_path"])
        
        if not workspace_path.exists():
            raise HTTPException(status_code=404, detail="Project files not found")
        
        # Create ZIP file in memory preserving relative tree
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in workspace_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(workspace_path)
                    zip_file.write(file_path, arcname)
        
        zip_buffer.seek(0)
        
        import tempfile
        temp_dir = Path(tempfile.gettempdir())
        temp_zip = temp_dir / f"{project_id}.zip"
        
        with open(temp_zip, 'wb') as f:
            f.write(zip_buffer.getvalue())
        
        safe_name = project.get("name", "ReactProject").replace(" ", "_")
        return FileResponse(
            temp_zip,
            media_type='application/zip',
            filename=f"{safe_name}.zip"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project and its workspace files"""
    try:
        db = mongodb.get_database()
        project = db.projects.find_one({"id": project_id})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        if project.get("workspace_path"):
            workspace_path = Path(project["workspace_path"])
            if workspace_path.exists():
                shutil.rmtree(workspace_path, ignore_errors=True)
                
        db.projects.delete_one({"id": project_id})
        db.tasks.delete_many({"project_id": project_id})
        db.messages.delete_many({"project_id": project_id})
        
        return {"success": True, "message": "Project deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/employees")
async def list_employees():
    """List all 8 specialized AI React engineering employees"""
    employees = [
        {
            "id": "ceo",
            "name": "Alex Thompson",
            "role": "CEO & Product Lead",
            "status": "active",
            "avatar": "👔",
            "bio": "Defines multi-page sitemaps, business domain logic, and executive approvals."
        },
        {
            "id": "pm",
            "name": "Sarah Martinez",
            "role": "Project Manager",
            "status": "active",
            "avatar": "📊",
            "bio": "Orchestrates engineering sprints, task breakdown, and dependency tracking."
        },
        {
            "id": "designer",
            "name": "Maya Patel",
            "role": "Lead UI/UX Designer",
            "status": "active",
            "avatar": "🎨",
            "bio": "Creates bespoke design archetypes, Google Font pairings, and CSS token systems."
        },
        {
            "id": "architect",
            "name": "David Vance",
            "role": "Principal React Architect",
            "status": "active",
            "avatar": "🏗️",
            "bio": "Designs React Router v6 hierarchy, file manifests, and state models."
        },
        {
            "id": "developer",
            "name": "Jordan Lee",
            "role": "Senior React Developer",
            "status": "active",
            "avatar": "💻",
            "bio": "Builds production-grade React 18 JSX components, layouts, pages, and interactive hooks."
        },
        {
            "id": "file_integrity",
            "name": "Marcus Brody",
            "role": "File Integrity Specialist",
            "status": "active",
            "avatar": "🛡️",
            "bio": "Verifies 100% manifest completeness, inspects local imports, and validates route consistency."
        },
        {
            "id": "visual_reviewer",
            "name": "Sophia Rossi",
            "role": "Visual & UX Reviewer",
            "status": "active",
            "avatar": "✨",
            "bio": "Audits visual hierarchy, bespoke authenticity, color contrast, and responsive layout polish."
        },
        {
            "id": "qa",
            "name": "Chris Anderson",
            "role": "Lead React QA Auditor",
            "status": "active",
            "avatar": "🔍",
            "bio": "Performs deep functional testing, interactive state validation, ARIA accessibility, and JSX integrity checks."
        },
        {
            "id": "docs",
            "name": "Emily Zhang",
            "role": "Technical Documentation Lead",
            "status": "active",
            "avatar": "📝",
            "bio": "Creates developer-ready README.md files with local setup, run, build, and architecture guides."
        }
    ]
    return {"employees": employees}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"ACK: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "engine": "React-First Multi-Agent Platform",
        "timestamp": datetime.utcnow().isoformat()
    }