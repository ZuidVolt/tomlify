#!/usr/bin/env python3
import os
import shutil
import logging
from pathlib import Path
import sys
import argparse

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get the directory of the script
SCRIPT_DIR = Path(__file__).parent

# Find the template folder in the project directory
DEFAULT_TEMPLATE_PATH = SCRIPT_DIR / "template" / "pyproject.toml"

# Configure terminal output
terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(logging.Formatter("%(message)s"))
terminal_handler.setLevel(logging.INFO)
logger.addHandler(terminal_handler)


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


def copy_pyproject_toml(custom_template: Path | None = None, output_dir: Path | None = None) -> None:
    """Copy pyproject.toml template to current directory with error handling"""
    try:
        template_path = custom_template or DEFAULT_TEMPLATE_PATH
        dest_path = (output_dir or Path.cwd()) / "pyproject.toml"

        if not template_path.exists():
            raise TomlifyError(f"Template not found at {template_path}")

        if not verify_file_health(template_path):
            raise TomlifyError("Template file is corrupted or empty")

        if not verify_permissions(template_path) or not verify_permissions(dest_path):
            raise TomlifyError("Insufficient permissions")

        if dest_path.exists():
            response = input("pyproject.toml already exists. Overwrite? (y/n): ").lower()
            if response != "y":
                return

            backup_path = dest_path.with_suffix(".toml.backup")
            shutil.copy2(dest_path, backup_path)
            logger.info(f"Created backup at {backup_path}")

        shutil.copy2(template_path, dest_path)

        if not verify_file_health(dest_path):
            raise TomlifyError("Failed to create a valid destination file")

        logger.info(f"pyproject.toml copied successfully to {dest_path}")

    except (TomlifyError, FileNotFoundError, PermissionError, OSError) as e:
        logger.error(str(e) if isinstance(e, TomlifyError) else f"{type(e).__name__}: {e}")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy pyproject.toml template to a directory")
    parser.add_argument("-t", "--template", type=Path, help="Path to custom template file")
    parser.add_argument("-o", "--output", type=Path, help="Directory to output pyproject.toml")
    args = parser.parse_args()

    try:
        copy_pyproject_toml(args.template, args.output)
    except (TomlifyError, KeyboardInterrupt) as e:
        if isinstance(e, KeyboardInterrupt):
            logger.error("Operation cancelled by user")
        else:
            logger.error("Failed to copy pyproject.toml")
        sys.exit(1)


if __name__ == "__main__":
    main()
