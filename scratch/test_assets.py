import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.assets.manager import AssetManager
from design_engine.assets.exceptions import AssetNotFoundException
from design_engine.renderer.canvas_renderer import CanvasRenderer
from design_engine.scene_graph.document import Layout, Canvas, Metadata
from design_engine.scene_graph.node import ImageNode

class TestAssetManager(unittest.TestCase):
    def test_local_remote_loading(self):
        manager = AssetManager()
        # Remote Image
        url = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"
        img = manager.load_image(url)
        self.assertIsNotNone(img)
        
        # Cache hit
        meta = manager.get_metadata(url)
        self.assertEqual(meta.version, 1)
        
    def test_duplicate_detection(self):
        manager = AssetManager()
        url = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"
        img1 = manager.load_image(url)
        
        # Force load same url under an alias name to check deduplication hashes
        img2 = manager.load_image(url)
        meta1 = manager.get_metadata(url)
        self.assertIsNotNone(meta1.hash)
        
    def test_cache_invalidation_and_versioning(self):
        manager = AssetManager()
        url = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80"
        manager.load_image(url)
        
        manager.invalidate(url)
        meta = manager.get_metadata(url)
        self.assertEqual(meta.version, 2)
        
    def test_exceptions_handling(self):
        manager = AssetManager()
        with self.assertRaises(AssetNotFoundException):
            manager.load_image("nonexistent_file.png")
            
    def test_renderer_integration(self):
        manager = AssetManager()
        renderer = CanvasRenderer(asset_manager=manager)
        layout = Layout(
            canvas=Canvas(width=400, height=400),
            scene_tree=[
                ImageNode(
                    id="img", name="Injected Asset",
                    x=50, y=50, width=300, height=300,
                    properties={"url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80", "fit_mode": "cover"}
                )
            ],
            metadata=Metadata()
        )
        out = renderer.render(layout, filename="test_assets_integration.png")
        self.assertTrue(os.path.exists(out))

if __name__ == "__main__":
    unittest.main()
