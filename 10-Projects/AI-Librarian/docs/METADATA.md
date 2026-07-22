# Metadata Engine

The metadata engine extracts structured information from document files and produces reusable metadata objects.

## Capabilities

- Computes SHA256 hashes
- Records file size in bytes
- Detects MIME type by extension
- Stores absolute and relative paths
- Captures creation, modification, and access timestamps
- Records file owner when available
- Provides a language detection interface
- Generates document IDs
- Detects duplicate files by content hash
- Serializes metadata to JSON-compatible dictionaries
- Validates document paths and readability

## Usage

```python
from app.metadata import extract_metadata, find_duplicates, serialize_metadata

metadata = extract_metadata("sample.txt")
payload = serialize_metadata(metadata)
```

## Design Notes

The implementation is built around small, reusable modules and dataclasses for clarity and maintainability.
