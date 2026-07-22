# Core Foundation Module

The core foundation module provides the shared infrastructure for the AI Librarian application.

## What is included

- Configuration loading from environment variables
- Centralized constants and defaults
- Custom exception types for predictable failures
- Structured logging helpers
- Managed project path resolution and directory creation

## Main components

### Configuration

Use AppConfig to keep application settings in one place and validate them before runtime.

```python
from app.core.config import load_config

config = load_config(project_root=".")
```

### Logging

Use the logger helpers when you need consistent, formatted logs.

```python
from app.core.logger import setup_logging

logger = setup_logging(level="INFO")
logger.info("Application started")
```

### Paths

Use AppPaths to ensure the standard project directories exist.

```python
from app.core.paths import AppPaths

paths = AppPaths.from_project_root(".")
print(paths.data_dir)
```

## Validation

The module is designed to be used by other application components and is covered by tests in the tests directory.
