import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from design_engine.config import CONFIG
from design_engine.project_manager.storage import BaseProjectStorage, StorageException

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger("ProjectManager")

class ProjectManagerException(Exception):
    """Base exception for Project Manager operations."""
    pass

class ProjectNotFoundException(ProjectManagerException):
    """Raised when the project file is not found."""
    pass

class ProjectCorruptedException(ProjectManagerException):
    """Raised when the project layout file contains malformed or un-parsable JSON."""
    pass

class InvalidMetadataException(ProjectManagerException):
    """Raised when project metadata attributes violate schema boundaries."""
    pass

class ProjectAlreadyExistsException(ProjectManagerException):
    """Raised when trying to create a project with an ID that already exists."""
    pass

class ProjectManager:
    def __init__(self, storage: BaseProjectStorage):
        """
        Dependency Injection: ProjectManager depends only on the BaseProjectStorage abstraction.
        """
        self.storage = storage
        self.image_dir = CONFIG.IMAGE_OUTPUT_DIR

    def create_project(self, business_name: str, platform: str, layout: Dict[str, Any]) -> str:
        """
        Creates a new design project and persists its layout JSON.
        Returns the generated project_id.
        """
        if not business_name or not platform:
            raise InvalidMetadataException("Business name and platform are required to create a project.")
            
        logger.info(f"Creating project for '{business_name}' on '{platform}'")
        try:
            # Generate the envelope using the storage client
            project_data = self.storage.create_project(business_name, platform, layout)
            project_id = project_data["project_id"]
            
            # Save the JSON envelope to disk
            self.storage.save_layout_json(project_id, project_data, overwrite=False)
            logger.info(f"Successfully created and stored project: {project_id}")
            return project_id
        except StorageException as e:
            if "already exists" in str(e).lower():
                raise ProjectAlreadyExistsException(f"Project ID collision detected: {e}")
            raise ProjectManagerException(f"Failed to create project: {e}")

    def load_project(self, project_id: str) -> Dict[str, Any]:
        """
        Loads project layout and appends preview paths.
        Raises ProjectNotFoundException or ProjectCorruptedException.
        """
        logger.info(f"Loading project details for ID: {project_id}")
        try:
            project_data = self.storage.load_project(project_id)
        except StorageException as e:
            if "not found" in str(e).lower():
                logger.warning(f"Project not found: {project_id}")
                raise ProjectNotFoundException(f"Project with ID '{project_id}' does not exist.")
            if "expecting" in str(e).lower() or "json" in str(e).lower() or "decode" in str(e).lower():
                logger.error(f"Corrupted layout JSON for project '{project_id}': {e}")
                raise ProjectCorruptedException(f"Project '{project_id}' contains malformed JSON. Details: {e}")
            raise ProjectManagerException(str(e))
        except Exception as e:
            logger.error(f"Unexpected error loading project '{project_id}': {e}")
            raise ProjectManagerException(f"Error loading project: {e}")

        # Construct image preview path
        image_path = self.image_dir / f"{project_id}.png"
        
        return {
            "metadata": {
                "project_id": project_data.get("project_id"),
                "created_at": project_data.get("created_at"),
                "business_name": project_data.get("business_name"),
                "platform": project_data.get("platform"),
                "industry": project_data.get("industry"),
                "offer": project_data.get("offer"),
                "tags": project_data.get("tags", [])
            },
            "layout": project_data.get("layout"),
            "image_path": str(image_path) if image_path.exists() else None
        }

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        Returns all projects sorted by newest first.
        Includes paths to rendering outputs.
        """
        logger.info("Listing projects list index...")
        try:
            summaries = self.storage.list_projects()
            formatted_list = []
            
            for proj in summaries:
                project_id = proj.get("project_id")
                if not project_id:
                    continue
                
                image_path = self.image_dir / f"{project_id}.png"
                formatted_list.append({
                    "project_id": project_id,
                    "business_name": proj.get("business_name"),
                    "platform": proj.get("platform"),
                    "created_at": proj.get("created_at"),
                    "image_path": str(image_path) if image_path.exists() else None
                })
            return formatted_list
        except Exception as e:
            logger.error(f"Failed to index projects directory: {e}")
            raise ProjectManagerException(f"Failed to list projects: {e}")

    def delete_project(self, project_id: str) -> bool:
        """
        Deletes project layout and rendering artifacts.
        """
        logger.info(f"Deleting project and attachments: {project_id}")
        try:
            # Check existence first
            self.storage.load_project(project_id)
        except StorageException:
            raise ProjectNotFoundException(f"Cannot delete: Project '{project_id}' does not exist.")
            
        try:
            status = self.storage.delete_project(project_id)
            logger.info(f"Project '{project_id}' deleted successfully: {status}")
            return status
        except Exception as e:
            logger.error(f"Error during project deletion '{project_id}': {e}")
            raise ProjectManagerException(f"Failed to delete project: {e}")

    def rename_project(self, project_id: str, new_name: str) -> None:
        """
        Renames the business name inside layout metadata envelopes.
        """
        if not new_name:
            raise InvalidMetadataException("New name cannot be empty.")
            
        logger.info(f"Renaming project '{project_id}' business name to '{new_name}'")
        try:
            # Load current state
            project_data = self.storage.load_project(project_id)
            project_data["business_name"] = new_name
            
            # Save updated layout
            self.storage.save_layout_json(project_id, project_data, overwrite=True)
            logger.info(f"Successfully renamed project: {project_id}")
        except StorageException as e:
            if "not found" in str(e).lower():
                raise ProjectNotFoundException(f"Cannot rename: Project '{project_id}' does not exist.")
            raise ProjectManagerException(str(e))

    def update_metadata(self, project_id: str, metadata: Dict[str, Any]) -> None:
        """
        Allows updating business_name, platform, industry, offer, and tags.
        Does not affect the inner canvas layout properties.
        """
        logger.info(f"Updating metadata for project ID: {project_id}")
        
        # Guard against key violations
        allowed_keys = {"business_name", "platform", "industry", "offer", "tags"}
        for k in metadata.keys():
            if k not in allowed_keys:
                raise InvalidMetadataException(f"Field '{k}' is not allowed in metadata updates.")

        try:
            # Load project envelope
            project_data = self.storage.load_project(project_id)
            
            # Apply changes
            for k, v in metadata.items():
                project_data[k] = v
                
            # Persist changes
            self.storage.save_layout_json(project_id, project_data, overwrite=True)
            logger.info(f"Successfully updated metadata parameters on project: {project_id}")
        except StorageException as e:
            if "not found" in str(e).lower():
                raise ProjectNotFoundException(f"Cannot update: Project '{project_id}' does not exist.")
            raise ProjectManagerException(str(e))
