import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from design_engine.validator import validate_layout
from design_engine.renderer.canvas_renderer import CanvasRenderer

TEST_PERF_LAYOUT = {
  "canvas": {
    "width": 1000,
    "height": 1000,
    "background_color": "#0F172A",
    "unit": "px"
  },
  "scene_tree": [
    # Repeating gradient shapes
    {
      "id": f"card_{i}",
      "name": f"Gradient Card {i}",
      "type": "shape",
      "x": float(50 * i), "y": float(50 * i), "width": 300.0, "height": 300.0,
      "z_index": i,
      "properties": {
        "border_radius": 16,
        "fill_gradient": {
          "colors": ["#10B981", "#3B82F6"],
          "angle": 45.0
        }
      }
    } for i in range(5)
  ] + [
    # Repeating remote image node
    {
      "id": "remote_image",
      "name": "Cached Remote Image",
      "type": "image",
      "x": 400.0, "y": 400.0, "width": 200.0, "height": 200.0,
      "z_index": 10,
      "properties": {
        "url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&q=80",
        "fit_mode": "cover"
      }
    }
  ],
  "metadata": {
    "created_by": "Performance Phase 8",
    "template": "Performance Test",
    "version": "1.0"
  }
}

def main():
    print("=== Testing Render Performance & Caching ===")
    layout = validate_layout(TEST_PERF_LAYOUT)
    renderer = CanvasRenderer()
    
    # Pass 1: Cold Run
    print("Running pass 1 (Cold Run - download + compute)...")
    start_cold = time.time()
    p1_path = renderer.render(layout, filename="test_perf_cold.png")
    cold_time = time.time() - start_cold
    print(f"Cold run completed in: {cold_time:.4f}s")
    
    # Pass 2: Hot Run (Cache active)
    print("Running pass 2 (Hot Run - cache hits)...")
    start_hot = time.time()
    p2_path = renderer.render(layout, filename="test_perf_hot.png")
    hot_time = time.time() - start_hot
    print(f"Hot run completed in: {hot_time:.4f}s")
    
    print(f"Speedup factor: {cold_time / hot_time:.1f}x faster!")
    assert hot_time < cold_time, "Error: Caching did not improve rendering speeds!"
    print("=== Performance Test Passed ===")

if __name__ == "__main__":
    main()
