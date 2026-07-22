# Core Module

This package contains the foundational building blocks for the AI Librarian project.

## Files

- app/core/__init__.py: package exports
- app/core/config.py: configuration loading and validation
- app/core/constants.py: shared defaults and environment variable names
- app/core/exceptions.py: custom exception types
- app/core/logger.py: logging helpers
- app/core/paths.py: project directory and path management

## Quick start

```python
from app.core.config import load_config
from app.core.logger import setup_logging

config = load_config(project_root=".")
logger = setup_logging(level=config.log_level)
logger.info("Core module initialized")
```

## Notes

The implementation is production-oriented, validates inputs, creates required directories, and is compatible with the test suite included in the repository.
