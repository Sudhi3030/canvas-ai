import os
from pathlib import Path
from typing import Dict, Tuple
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Attempt to load keys from secret_key module fallback
openai_fallback_key = None
gemini_fallback_key = None
try:
    from secret_key import openai_key, gemini_key
    openai_fallback_key = openai_key
    gemini_fallback_key = gemini_key
except ImportError:
    pass
except AttributeError:
    try:
        from secret_key import openai_key
        openai_fallback_key = openai_key
    except ImportError:
        pass

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", openai_fallback_key or "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    
    # Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", gemini_fallback_key or "")
    DEFAULT_GEMINI_MODEL: str = os.getenv("DEFAULT_GEMINI_MODEL", "gemini-3.5-flash")
    
    # Path configurations (goes up 3 levels from design_engine/config/__init__.py to root)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    OUTPUTS_DIR: Path = BASE_DIR / "outputs"
    JSON_OUTPUT_DIR: Path = OUTPUTS_DIR / "json"
    IMAGE_OUTPUT_DIR: Path = OUTPUTS_DIR / "images"
    
    # Default Canvas sizes for platforms
    PLATFORM_SIZES: Dict[str, Tuple[int, int]] = {
        "Instagram": (1080, 1080),
        "Facebook": (1200, 630),
        "Pinterest": (1000, 1500),
        "Twitter": (1024, 512),
        "Default": (800, 800)
    }

CONFIG = Config()
