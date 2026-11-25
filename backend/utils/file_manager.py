from pathlib import Path
from typing import Dict, List
import json
import shutil
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class FileManager:
    """Manages project file creation and organization"""
    
    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = self._sanitize_name(project_name)
        self.project_path = settings.WORKSPACE_DIR / self.project_name
        self._create_project_structure()
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize project name for file system"""
        return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    
    def _create_project_structure(self):
        """Create project directory structure"""
        try:
            self.project_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created project directory: {self.project_path}")
        except Exception as e:
            logger.error(f"Failed to create project directory: {e}")
            raise
    
    def write_file(self, filename: str, content: str) -> bool:
        """Write content to a file"""
        try:
            file_path = self.project_path / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Written file: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to write file {filename}: {e}")
            return False
    
    def write_json(self, filename: str, data: Dict) -> bool:
        """Write JSON data to a file"""
        try:
            content = json.dumps(data, indent=2)
            return self.write_file(filename, content)
        except Exception as e:
            logger.error(f"Failed to write JSON file {filename}: {e}")
            return False
    
    def read_file(self, filename: str) -> str:
        """Read content from a file"""
        try:
            file_path = self.project_path / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {filename}: {e}")
            return ""
    
    def list_files(self) -> List[str]:
        """List all files in the project"""
        try:
            files = []
            for file_path in self.project_path.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.project_path)
                    files.append(str(relative_path))
            return files
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []
    
    def get_project_path(self) -> str:
        """Get absolute project path"""
        return str(self.project_path.absolute())
    
    def delete_project(self) -> bool:
        """Delete entire project directory"""
        try:
            if self.project_path.exists():
                shutil.rmtree(self.project_path)
                logger.info(f"Deleted project directory: {self.project_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete project: {e}")
            return False