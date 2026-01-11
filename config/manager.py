#!/usr/bin/env python3
"""
Configuration management for BackupBuddy.
"""

import json
from pathlib import Path
from typing import Dict
from config.constants import CONFIG_FILE, JOB_DEFAULTS
from utils.display import Colors


def load_config() -> Dict:
    """Load configuration from JSON file with validation."""
    if not CONFIG_FILE.exists():
        return {}
    
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
        
        # Add default values for missing keys
        for job in config.values():
            for key, default_value in JOB_DEFAULTS.items():
                job.setdefault(key, default_value)
        
        return config
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}Error reading config file: {e}{Colors.RESET}")
        return {}
    except Exception as e:
        print(f"{Colors.RED}Unexpected error loading config: {e}{Colors.RESET}")
        return {}


def save_config(config: Dict) -> bool:
    """Save configuration to JSON file."""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        return True
    except Exception as e:
        print(f"{Colors.RED}Error saving config: {e}{Colors.RESET}")
        return False


def list_jobs(config: Dict) -> None:
    """List all backup and transfer jobs."""
    if not config:
        print("No jobs found.")
        return
    
    print("\nConfigured jobs:")
    for i, (job_id, job_data) in enumerate(config.items(), start=1):
        job_type = job_data.get("type", "backup")
        if job_type == "transfer":
            print(f"{i}. [Transfer] {job_id}")
            print(f"   Source: {job_data.get('source', 'N/A')}")
            print(f"   Destination: {job_data.get('destination', 'N/A')}")
        else:
            print(f"{i}. [Backup] {job_id}")
            print(f"   Source: {job_data.get('source_dir', 'N/A')}")
            print(f"   Destination: {job_data.get('destination', 'N/A')}")
            print(f"   Compressed: {job_data.get('compress', False)}, "
                  f"Split: {job_data.get('split_files', False)}")


def delete_job(config: Dict, job_id: str) -> bool:
    """Remove a job from configuration."""
    if job_id in config:
        del config[job_id]
        return save_config(config)
    return False


def get_job(config: Dict, job_id: str) -> Dict:
    """Get a specific job from configuration."""
    return config.get(job_id, {})
