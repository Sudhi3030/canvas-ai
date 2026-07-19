from typing import Optional
from design_engine.scene_graph.document import Layout

class HistoryManager:
    def __init__(self, max_depth: int = 10):
        self.max_depth = max_depth
        self.undo_stack: list[str] = []
        self.redo_stack: list[str] = []

    def commit(self, layout: Layout) -> None:
        """
        Saves a Pydantic serialization snapshot of the layout state.
        """
        dump = layout.model_dump_json()
        if len(self.undo_stack) >= self.max_depth:
            self.undo_stack.pop(0)
        self.undo_stack.append(dump)
        self.redo_stack.clear()

    def undo(self, current_layout: Layout) -> Optional[Layout]:
        """
        Reverts to the previous layout state snapshot.
        """
        if not self.undo_stack:
            return None
        self.redo_stack.append(current_layout.model_dump_json())
        prev_json = self.undo_stack.pop()
        return Layout.model_validate_json(prev_json)

    def redo(self, current_layout: Layout) -> Optional[Layout]:
        """
        Restores a previously undone layout state snapshot.
        """
        if not self.redo_stack:
            return None
        self.undo_stack.append(current_layout.model_dump_json())
        next_json = self.redo_stack.pop()
        return Layout.model_validate_json(next_json)
