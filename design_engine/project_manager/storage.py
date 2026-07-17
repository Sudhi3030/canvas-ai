import json
import logging
import uuid
import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from PIL import Image
from design_engine.config import CONFIG

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("ProjectStorage")

class StorageException(Exception):
    """Custom exception for storage persistence failures."""
    pass

class BaseProjectStorage(ABC):
    @abstractmethod
    def create_project(self, business_name: str, platform: str, layout: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a project metadata envelope structure."""
        pass

    @abstractmethod
    def save_layout_json(self, project_id: str, project_data: Dict[str, Any], overwrite: bool = False) -> Path:
        """Saves the project metadata envelope JSON file."""
        pass

    @abstractmethod
    def save_rendered_image(self, project_id: str, image: Image.Image, overwrite: bool = False) -> Path:
        """Saves the rendered PNG preview file."""
        pass

    @abstractmethod
    def load_project(self, project_id: str) -> Dict[str, Any]:
        """Loads a project metadata envelope JSON from storage."""
        pass

    @abstractmethod
    def list_projects(self) -> List[Dict[str, Any]]:
        """Lists metadata summaries for all stored projects."""
        pass

    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """Removes the project layout JSON and preview image."""
        pass

class FileProjectStorage(BaseProjectStorage):
    def __init__(self):
        self.json_dir: Path = CONFIG.JSON_OUTPUT_DIR
        self.image_dir: Path = CONFIG.IMAGE_OUTPUT_DIR
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        try:
            self.json_dir.mkdir(parents=True, exist_ok=True)
            self.image_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Storage directories ensured.")
        except Exception as e:
            raise StorageException(f"Failed to create output directories: {e}")

    def create_project(self, business_name: str, platform: str, layout: Dict[str, Any]) -> Dict[str, Any]:
        project_id = f"project_{uuid.uuid4().hex[:8]}"
        created_at = datetime.datetime.utcnow().isoformat() + "Z"
        
        project_envelope = {
            "project_id": project_id,
            "created_at": created_at,
            "business_name": business_name,
            "platform": platform,
            "layout": layout
        }
        logger.info(f"Initialized new project metadata envelope for project: {project_id}")
        return project_envelope

    def save_layout_json(self, project_id: str, project_data: Dict[str, Any], overwrite: bool = False) -> Path:
        filepath = self.json_dir / f"{project_id}.json"
        if filepath.exists() and not overwrite:
            raise StorageException(f"File overwrite protection: {filepath} already exists.")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=2)
            logger.info(f"Saved layout JSON state to {filepath}")
            return filepath
        except Exception as e:
            raise StorageException(f"Failed to save JSON file for project {project_id}: {e}")

    def save_rendered_image(self, project_id: str, image: Image.Image, overwrite: bool = False) -> Path:
        filepath = self.image_dir / f"{project_id}.png"
        if filepath.exists() and not overwrite:
            raise StorageException(f"File overwrite protection: {filepath} already exists.")
            
        try:
            image.save(filepath, "PNG")
            logger.info(f"Saved rendered preview PNG image to {filepath}")
            return filepath
        except Exception as e:
            raise StorageException(f"Failed to save rendered PNG file for project {project_id}: {e}")

    def load_project(self, project_id: str) -> Dict[str, Any]:
        filepath = self.json_dir / f"{project_id}.json"
        if not filepath.exists():
            raise StorageException(f"Project JSON file not found: {filepath}")
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise StorageException(f"Failed to read project JSON file: {e}")

    def list_projects(self) -> List[Dict[str, Any]]:
        projects = []
        try:
            for file_path in self.json_dir.glob("*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        projects.append({
                            "project_id": data.get("project_id"),
                            "created_at": data.get("created_at"),
                            "business_name": data.get("business_name"),
                            "platform": data.get("platform"),
                        })
                except Exception:
                    continue
            return sorted(projects, key=lambda p: p.get("created_at") or "", reverse=True)
        except Exception as e:
            raise StorageException(f"Failed to list stored projects: {e}")

    def delete_project(self, project_id: str) -> bool:
        json_file = self.json_dir / f"{project_id}.json"
        image_file = self.image_dir / f"{project_id}.png"
        deleted = False
        
        try:
            if json_file.exists():
                json_file.unlink()
                logger.info(f"Deleted project layout file: {json_file}")
                deleted = True
            if image_file.exists():
                image_file.unlink()
                logger.info(f"Deleted project image file: {image_file}")
                deleted = True
            return deleted
        except Exception as e:
            raise StorageException(f"Failed to delete files for project {project_id}: {e}")
