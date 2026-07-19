from design_engine.scene_graph.node import Node
from typing import List, Tuple

class CollisionDetector:
    @staticmethod
    def detect_collisions(layout) -> List[Tuple[Node, Node]]:
        """
        Pass 8: Passive collision validator checking overlap conflicts.
        """
        conflicts = []
        nodes = []
        
        def traverse(node):
            if node.visible and node.width > 0 and node.height > 0:
                nodes.append(node)
            if hasattr(node, "children"):
                for child in node.children:
                    traverse(child)

        for root in layout.scene_tree:
            traverse(root)
            
        # Passive overlap checks pairwise
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1 = nodes[i]
                n2 = nodes[j]
                
                if (n1.x < n2.x + n2.width and
                    n1.x + n1.width > n2.x and
                    n1.y < n2.y + n2.height and
                    n1.y + n1.height > n2.y):
                    if not (hasattr(n1, "children") and n2 in n1.children) and \
                       not (hasattr(n2, "children") and n1 in n2.children):
                        conflicts.append((n1, n2))
                        
        return conflicts
