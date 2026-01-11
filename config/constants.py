#!/usr/bin/env python3
"""
Constants and global configurations for BackupBuddy.
"""

from pathlib import Path

# Paths
CONFIG_FILE = Path.home() / ".backup_tool_jobs.json"
SCRIPT_DIR = Path.home() / "backup_scripts"
TEMP_DIR = Path("/var/tmp/backupbuddy_temp")
DEPENDENCY_FLAG_FILE = Path.home() / ".backupbuddy_dependencies_checked"
INSTALLED_PACKAGES_LOG = Path.home() / ".backupbuddy_installed_packages.log"

# Dependencies
DEPENDENCIES = ["curl", "pigz", "tar", "pv", "cron"]

# Default rclone flags for backup
DEFAULT_BACKUP_FLAGS = {
    "--tpslimit": "2",
    "--tpslimit-burst": "1",
    "--transfers": "2",
    "--checkers": "1",
    "--low-level-retries": "3",
    "--retries": "5",
    "--log-level": "INFO",
}

# Default rclone flags for transfer
DEFAULT_TRANSFER_FLAGS = {
    "--transfers": "4",
    "--checkers": "2",
    "--retries": "5",
    "--log-level": "INFO",
}

# Job defaults
JOB_DEFAULTS = {
    "encrypt": False,
    "compress": False,
    "compression_level": None,
    "split_files": False,
    "split_size": None,
    "cores": 4
}

# Compression defaults
DEFAULT_COMPRESSION_LEVEL = 6
DEFAULT_CORES = 4
DEFAULT_SPLIT_SIZE = "100M"
