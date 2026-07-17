from collections import OrderedDict
from typing import Any, Optional

class MemoryCache:
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self.cache = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        # Move key to end to track recent usage (LRU logic)
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def set(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.maxsize:
            # Evict the oldest item (first item in OrderedDict)
            self.cache.popitem(last=False)
        self.cache[key] = value

    def remove(self, key: str) -> None:
        if key in self.cache:
            self.cache.pop(key)

    def clear(self) -> None:
        self.cache.clear()
