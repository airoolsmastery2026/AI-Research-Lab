from pathlib import Path

# ======================================================
# AI LIBRARIAN CONFIG
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_DIR = PROJECT_ROOT / "output"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".md",
    ".txt",
]

AUTO_CREATE_FOLDERS = True