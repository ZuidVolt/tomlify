#!/usr/bin/env python3
import os
import shutil
import logging
from pathlib import Path
import sys

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_TEMPLATE_PATH = Path("/Users/cooper/Dev/vscode/tomlify/template/pyproject.toml")

# Create a separate handler for the terminal output
terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(logging.Formatter("%(message)s"))
terminal_handler.setLevel(logging.INFO)

# Create a separate handler for the log file
file_handler = logging.FileHandler(Path.home() / ".logs" / "tomlify.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Add handlers to the logger
logger.addHandler(terminal_handler)
logger.addHandler(file_handler)


class TomlifyError(Exception):
    """Custom exception for Tomlify-specific errors"""


def verify_permissions(path: Path) -> bool:
    """Verify read/write permissions for given path"""
    try:
        if path.exists():
            return os.access(path, os.R_OK | os.W_OK)
        return os.access(path.parent, os.W_OK)
    except OSError as e:
        logger.error(f"Permission check failed: {e}")
        return False


def verify_file_health(path: Path) -> bool:
    """Verify file isn't corrupted or empty"""
    try:
        return bool(path.read_text(encoding="utf-8").strip())
    except (UnicodeDecodeError, OSError) as e:
        logger.error(f"File health check failed: {e}")
        return False


def copy_pyproject_toml(custom_template: Path | None = None) -> None:
    """Copy pyproject.toml template to current directory with error handling"""
    try:
        # Set default template path
        default_template_path = DEFAULT_TEMPLATE_PATH
        template_path = custom_template or default_template_path
        dest_path = Path.cwd() / "pyproject.toml"
        log_dir = Path.home() / ".logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        if not template_path.exists():
            raise TomlifyError(f"Template not found at {template_path}")

        if not verify_file_health(template_path):
            raise TomlifyError("Template file is corrupted or empty")

        if not verify_permissions(template_path) or not verify_permissions(dest_path):
            raise TomlifyError("Insufficient permissions")

        # Handle existing destination file
        if dest_path.exists():
            response = input("pyproject.toml already exists. Overwrite? (y/n): ").lower()
            if response != "y":
                return

            # Create backup of existing destination file
            backup_path = dest_path.with_suffix(".toml.backup")
            shutil.copy2(dest_path, backup_path)
            logger.info(f"Created backup at {backup_path}")

        # Copy template to destination
        shutil.copy2(template_path, dest_path)

        # Verify destination file health
        if not verify_file_health(dest_path):
            raise TomlifyError("Failed to create a valid destination file")

        logger.info("pyproject.toml copied successfully")

    except (TomlifyError, FileNotFoundError, PermissionError, OSError) as e:
        logger.error(str(e) if isinstance(e, TomlifyError) else f"{type(e).__name__}: {e}")
        raise


def main() -> None:
    try:
        copy_pyproject_toml()
    except (TomlifyError, KeyboardInterrupt) as e:
        if isinstance(e, KeyboardInterrupt):
            logger.error("Operation cancelled by user")
        else:
            logger.error("Failed to copy pyproject.toml")
        sys.exit(1)


if __name__ == "__main__":
    main()
