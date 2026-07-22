# Import Pipeline

The import pipeline ingests files from a directory tree into the metadata engine.

## Capabilities

- Recursive scanning of directories
- Hidden and system-file filtering
- Supported extension detection
- MIME type detection
- Queue management
- Progress tracking
- Duplicate detection through the metadata engine
- Batch processing and import reporting
- Resume-aware execution

## Usage

```python
from app.importer import Importer

importer = Importer(root_dir="./data")
result = importer.run()
print(result.statistics.imported_files)
```
