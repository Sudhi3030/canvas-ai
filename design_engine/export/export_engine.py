import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Literal
from PIL import Image
from design_engine.scene_graph.document import Layout
from design_engine.scene_graph.node import Node, TextNode, ImageNode, ShapeNode, GroupNode
from design_engine.layout_engine.layout import LayoutSolver

logger = logging.getLogger("ExportEngine")

class BaseExporter(ABC):
    @abstractmethod
    def export(self, layout: Layout, rendered_image: Image.Image, output_path: str, **kwargs) -> str:
        """
        Base export interface representing all file formats compilation pipelines.
        """
        pass

class RasterExporter(BaseExporter):
    def export(self, layout: Layout, rendered_image: Image.Image, output_path: str, format_type: str = "PNG", **kwargs) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if format_type == "JPEG" and rendered_image.mode == "RGBA":
            rgb_img = Image.new("RGB", rendered_image.size, (255, 255, 255))
            rgb_img.paste(rendered_image, mask=rendered_image.split()[3])
            rgb_img.save(output_path, "JPEG", quality=95)
        else:
            save_kwargs = {}
            if format_type == "WEBP":
                save_kwargs["quality"] = 90
            rendered_image.save(output_path, format_type, **save_kwargs)
        return output_path

class PDFExporter(BaseExporter):
    def export(self, layout: Layout, rendered_image: Image.Image, output_path: str, **kwargs) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if rendered_image.mode == "RGBA":
            pdf_img = Image.new("RGB", rendered_image.size, (255, 255, 255))
            pdf_img.paste(rendered_image, mask=rendered_image.split()[3])
            pdf_img.save(output_path, "PDF")
        else:
            rendered_image.save(output_path, "PDF")
        return output_path

class LayeredJSONExporter(BaseExporter):
    def export(self, layout: Layout, rendered_image: Image.Image, output_path: str, **kwargs) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        solver = LayoutSolver()
        solver.solve(layout)
        
        layers = []
        for node in layout.scene_tree:
            ExportEngine._flatten_node_recursive(node, 0.0, 0.0, 1.0, 0.0, layers)

        layered_document = {
            "canvas": {
                "width": layout.canvas.width,
                "height": layout.canvas.height,
                "background": layout.canvas.background_color
            },
            "layers": layers,
            "metadata": {
                "format": "LayeredJSON-v1.0",
                "created_by": layout.metadata.created_by,
                "version": layout.metadata.version
            }
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(layered_document, f, indent=2)
            
        return output_path

# Future-ready placeholder exporters following BaseExporter
class SVGExporter(BaseExporter):
    def export(self, layout: Layout, rendered_image: Image.Image, output_path: str, **kwargs) -> str:
        # Future SVG vector compilation path
        logger.info(f"Preparing SVG export pipeline for {output_path}...")
        raise NotImplementedError("SVG export pipeline is in progress.")

class VideoExporter(BaseExporter):
    def export(self, layout: Layout, rendered_image: Image.Image, output_path: str, format_type: str = "MP4", **kwargs) -> str:
        # Future animation sequences compilation path
        logger.info(f"Preparing animated {format_type} sequence export for {output_path}...")
        raise NotImplementedError("Animation sequence compilation path is in progress.")

class ExportEngine:
    @staticmethod
    def export_raster(image: Image.Image, output_path: str, format_type: Literal["PNG", "JPEG", "WEBP"] = "PNG") -> str:
        """
        Exports Pillow Image into standard web raster formats (PNG, JPEG, WebP).
        Delegates to RasterExporter.
        """
        exporter = RasterExporter()
        return exporter.export(None, image, output_path, format_type=format_type)

    @staticmethod
    def export_pdf(image: Image.Image, output_path: str) -> str:
        """
        Exports layout preview to high-fidelity PDF formats.
        Delegates to PDFExporter.
        """
        exporter = PDFExporter()
        return exporter.export(None, image, output_path)

    @staticmethod
    def export_layered_json(layout: Layout, output_path: str) -> str:
        """
        Exports the layout design with fully solved absolute positions and dimensions.
        Delegates to LayeredJSONExporter.
        """
        exporter = LayeredJSONExporter()
        return exporter.export(layout, None, output_path)

    @staticmethod
    def _flatten_node_recursive(node: Node, parent_x: float, parent_y: float, parent_opacity: float, parent_rotation: float, layers: List[Dict[str, Any]]) -> None:
        if not node.visible:
            return

        # Solve absolute geometries
        world_x = parent_x + node.x
        world_y = parent_y + node.y
        world_opacity = parent_opacity * node.opacity
        world_rotation = parent_rotation + node.rotation

        # GroupNode is a boundary container: we do not write it as a visual shape,
        # but recurse into its kids to resolve their layers.
        if isinstance(node, GroupNode):
            for child in node.children:
                ExportEngine._flatten_node_recursive(
                    child, world_x, world_y, world_opacity, world_rotation, layers
                )
        else:
            # Concrete visual leaf layers
            layer = {
                "id": node.id,
                "name": node.name,
                "type": node.type,
                "left": world_x,
                "top": world_y,
                "width": node.width,
                "height": node.height,
                "opacity": world_opacity,
                "angle": world_rotation,
                "zIndex": node.z_index,
                "animation": node.animation.model_dump() if node.animation else None
            }

            # Append properties depending on node subclass
            if isinstance(node, TextNode):
                layer.update({
                    "text": node.properties.content,
                    "fontFamily": node.properties.font_family,
                    "fontSize": node.properties.font_size,
                    "fontStyle": node.properties.font_weight,
                    "fill": node.properties.color,
                    "lineHeight": node.properties.line_height,
                    "charSpacing": node.properties.letter_spacing
                })
            elif isinstance(node, ImageNode):
                layer.update({
                    "src": node.properties.url,
                    "fitMode": node.properties.fit_mode,
                    "borderRadius": node.properties.border_radius,
                    "clipCircle": node.properties.clip_circle
                })
            elif isinstance(node, ShapeNode):
                layer.update({
                    "fill": node.properties.fill_color,
                    "stroke": node.properties.stroke_color,
                    "strokeWidth": node.properties.stroke_width,
                    "rx": node.properties.border_radius,
                    "ry": node.properties.border_radius
                })

            layers.append(layer)
