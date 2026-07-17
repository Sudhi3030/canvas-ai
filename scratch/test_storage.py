import os
import sys
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.project_manager.storage import FileProjectStorage, StorageException

def test_storage():
    print("=== Running ProjectStorage Unit Tests ===")
    storage = FileProjectStorage()
    
    business = "Tester Cafe"
    platform = "Pinterest"
    dummy_layout = {"canvas": {"width": 800, "height": 800}}

    # 1. Test Project Creation
    print("\n[Test 1] Testing project structure creation...")
    project = storage.create_project(business, platform, dummy_layout)
    project_id = project["project_id"]
    assert "project_id" in project
    assert project["business_name"] == business
    assert project["platform"] == platform
    print("✓ Project created with ID:", project_id)

    # 2. Test JSON Save & Load
    print("\n[Test 2] Testing saving and loading layout JSON...")
    json_path = storage.save_layout_json(project_id, project)
    assert json_path.exists()
    
    loaded = storage.load_project(project_id)
    assert loaded["project_id"] == project_id
    assert loaded["business_name"] == business
    print("✓ JSON save and parse check OK.")

    # 3. Test Image Save
    print("\n[Test 3] Testing image save persistence...")
    img = Image.new("RGBA", (10, 10), (0, 255, 0, 255))
    image_path = storage.save_rendered_image(project_id, img)
    assert image_path.exists()
    print("✓ Image save check OK.")

    # 4. Test Overwrite Protection
    print("\n[Test 4] Testing overwrite lock safety...")
    try:
        storage.save_layout_json(project_id, project, overwrite=False)
        print("✗ Fail: Overwrite protection did not raise warning.")
        sys.exit(1)
    except StorageException:
        print("✓ Success: Overwrite protection triggered on JSON file.")

    try:
        storage.save_rendered_image(project_id, img, overwrite=False)
        print("✗ Fail: Overwrite protection did not raise warning.")
        sys.exit(1)
    except StorageException:
        print("✓ Success: Overwrite protection triggered on PNG file.")

    # 5. Test Listings
    print("\n[Test 5] Testing project directory listing...")
    project_list = storage.list_projects()
    print("Listing output list:", project_list)
    assert len(project_list) >= 1
    assert any(p["project_id"] == project_id for p in project_list)
    print("✓ Project listing contains test project ID.")

    # 6. Test Deletions
    print("\n[Test 6] Testing clean project deletion...")
    storage.delete_project(project_id)
    assert not json_path.exists()
    assert not image_path.exists()
    print("✓ Layout and image files deleted cleanly.")

    print("\n=== All Storage Tests Passed ===")

if __name__ == "__main__":
    test_storage()
