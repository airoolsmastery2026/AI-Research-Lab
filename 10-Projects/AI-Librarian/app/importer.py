from pathlib import Path
from datetime import datetime

from metadata import DocumentMetadata
from config import (
    DATA_DIR,
    SUPPORTED_EXTENSIONS,
)


def scan_documents() -> list[DocumentMetadata]:
    """
    Quét toàn bộ thư mục DATA_DIR và tạo danh sách DocumentMetadata.
    """

    documents = []

    # Nếu thư mục data chưa tồn tại
    if not DATA_DIR.exists():
        return documents

    for file in DATA_DIR.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        stat = file.stat()

        document = DocumentMetadata(
            file_name=file.name,
            file_path=file.resolve(),
            extension=file.suffix.lower(),
            size=stat.st_size,
            created_time=datetime.fromtimestamp(stat.st_ctime),
            modified_time=datetime.fromtimestamp(stat.st_mtime),
        )

        documents.append(document)

    return documents


if __name__ == "__main__":

    docs = scan_documents()

    print(f"\nĐã tìm thấy {len(docs)} tài liệu.\n")

    for doc in docs:
        print(doc.to_dict())