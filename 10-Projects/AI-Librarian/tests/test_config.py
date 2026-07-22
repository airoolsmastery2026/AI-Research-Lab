import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import AppConfig, load_config
from app.core.exceptions import ConfigurationError
from app.core.paths import AppPaths


def test_default_config_is_valid(tmp_path):
    config = AppConfig(project_root=tmp_path)
    config.validate()

    assert config.app_name == "AI-Librarian"
    assert config.environment == "development"
    assert config.supported_extensions == (".pdf", ".docx", ".md", ".txt")


def test_load_config_from_env(tmp_path):
    env = {
        "APP_NAME": "Test App",
        "APP_ENVIRONMENT": "testing",
        "APP_DEBUG": "true",
        "APP_LOG_LEVEL": "DEBUG",
        "APP_MAX_FILE_SIZE_MB": "10",
        "APP_REQUEST_TIMEOUT_SECONDS": "20",
        "APP_SUPPORTED_EXTENSIONS": ".md,.txt",
    }
    config = load_config(env, project_root=tmp_path)

    assert config.app_name == "Test App"
    assert config.environment == "testing"
    assert config.debug is True
    assert config.log_level == "DEBUG"
    assert config.max_file_size_mb == 10
    assert config.request_timeout_seconds == 20
    assert config.supported_extensions == (".md", ".txt")


def test_paths_are_created(tmp_path):
    paths = AppPaths.from_project_root(tmp_path, create=True)

    assert paths.project_root == tmp_path.resolve()
    assert paths.data_dir.exists()
    assert paths.docs_dir.exists()
    assert paths.output_dir.exists()
    assert paths.prompts_dir.exists()
    assert paths.templates_dir.exists()
    assert paths.logs_dir.exists()


def test_invalid_config_raises_error(tmp_path):
    config = AppConfig(project_root=tmp_path, app_name="", max_file_size_mb=0)

    try:
        config.validate()
    except ConfigurationError as exc:
        assert "app_name" in str(exc) or "max_file_size_mb" in str(exc)
    else:
        raise AssertionError("Expected ConfigurationError")
