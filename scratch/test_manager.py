import os
import sys
import json
from pathlib import Path
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.project_manager.storage import FileProjectStorage
from design_engine.project_manager.manager import (
    ProjectManager, 
    ProjectNotFoundException, 
    ProjectCorruptedException, 
    InvalidMetadataException
)
from design_engine.config import CONFIG

def test_manager():
    print("=== Running ProjectManager Service Unit Tests ===")
    storage = FileProjectStorage()
    manager = ProjectManager(storage)

    # Clean legacy directories first
    for f in CONFIG.JSON_OUTPUT_DIR.glob("test_proj_*.json"):
        f.unlink()

    # 1. Create Project
    print("\n[Test 1] Testing project creation...")
    layout_data = {"canvas": {"width": 1000, "height": 1000}, "elements": []}
    project_id = manager.create_project("Organic Bread", "Facebook", layout_data)
    print("✓ Project created successfully. Generated ID:", project_id)

    # Write a test image preview to check loads
    img = Image.new("RGB", (100, 100), (255, 255, 255))
    storage.save_rendered_image(project_id, img)

    # 2. Load Project
    print("\n[Test 2] Testing loading project envelopes...")
    loaded = manager.load_project(project_id)
    assert loaded["metadata"]["project_id"] == project_id
    assert loaded["metadata"]["business_name"] == "Organic Bread"
    assert loaded["metadata"]["platform"] == "Facebook"
    assert loaded["layout"] == layout_data
    assert loaded["image_path"] is not None
    assert Path(loaded["image_path"]).exists()
    print("✓ Loaded project envelope structure verified successfully.")

    # 3. List Projects
    print("\n[Test 3] Testing project indexing listing...")
    project_list = manager.list_projects()
    assert len(project_list) >= 1
    assert any(p["project_id"] == project_id for p in project_list)
    print("✓ Listing summary found correct design ID details.")

    # 4. Rename Project
    print("\n[Test 4] Testing project renaming envelope update...")
    manager.rename_project(project_id, "Gluten-Free Organic Bread")
    updated = manager.load_project(project_id)
    assert updated["metadata"]["business_name"] == "Gluten-Free Organic Bread"
    print("✓ Business name updated successfully inside metadata block.")

    # 5. Update Metadata fields
    print("\n[Test 5] Testing custom metadata fields updates...")
    meta_updates = {
        "platform": "Pinterest",
        "industry": "Bakery",
        "offer": "10% discount",
        "tags": ["healthy", "bakery", "bread"]
    }
    manager.update_metadata(project_id, meta_updates)
    updated_meta = manager.load_project(project_id)["metadata"]
    assert updated_meta["platform"] == "Pinterest"
    assert updated_meta["industry"] == "Bakery"
    assert updated_meta["offer"] == "10% discount"
    assert updated_meta["tags"] == ["healthy", "bakery", "bread"]
    print("✓ Metadata fields updated and saved successfully.")

    # 6. Test Metadata Key Guards
    print("\n[Test 6] Testing invalid metadata key guards...")
    try:
        manager.update_metadata(project_id, {"invalid_key": "some_value"})
        print("✗ Fail: Expect validation warning on unauthorized keys.")
        sys.exit(1)
    except InvalidMetadataException as e:
        print(f"✓ Success: Guard caught invalid key with details: {e}")

    # 7. Test Missing Project Load Exception
    print("\n[Test 7] Testing missing project loading errors...")
    try:
        manager.load_project("non_existent_id")
        print("✗ Fail: Expected ProjectNotFoundException.")
        sys.exit(1)
    except ProjectNotFoundException as e:
        print(f"✓ Success: Guard raised ProjectNotFoundException: {e}")

    # 8. Test Corrupted JSON File Exception
    print("\n[Test 8] Testing corrupted file parser validation errors...")
    corrupt_id = "test_corrupted_id"
    corrupt_path = CONFIG.JSON_OUTPUT_DIR / f"{corrupt_id}.json"
    
    with open(corrupt_path, "w") as f:
        f.write("{ malformed json string }") # Invalid JSON format

    try:
        manager.load_project(corrupt_id)
        print("✗ Fail: Expected ProjectCorruptedException.")
        sys.exit(1)
    except ProjectCorruptedException as e:
        print(f"✓ Success: Guard raised ProjectCorruptedException: {e}")
    finally:
        if corrupt_path.exists():
            corrupt_path.unlink()

    # 9. Test Delete Project
    print("\n[Test 9] Testing project file deletions...")
    status = manager.delete_project(project_id)
    assert status is True
    # Verify missing check raises error post deletion
    try:
        manager.load_project(project_id)
        print("✗ Fail: Loaded project layout post deletion.")
        sys.exit(1)
    except ProjectNotFoundException:
        print("✓ Success: Project files cleared and verified missing.")

    print("\n=== All ProjectManager Service Tests Passed ===")

if __name__ == "__main__":
    test_manager()
