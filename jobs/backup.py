#!/usr/bin/env python3
"""
Backup job creation and management for BackupBuddy.
"""

from config.manager import save_config
from config.constants import DEFAULT_BACKUP_FLAGS, DEFAULT_COMPRESSION_LEVEL, DEFAULT_CORES, DEFAULT_SPLIT_SIZE
from core.navigation import navigate_local_directories, navigate_remote_directories
from core.remotes import select_remote
from scripts.generator import generate_backup_script
from cron.scheduler import schedule_cron
from utils.commands import run_script
from utils.display import Colors
from utils.validation import get_yes_no, get_int_input


def create_backup_job(config: dict) -> None:
    """
    Guide user through creating a new backup job.
    """
    print("\nCreating a new backup job.")
    job_id = input("Enter a unique ID for the backup job: ").strip()
    
    if not job_id:
        print(f"{Colors.RED}Job ID cannot be empty.{Colors.RESET}")
        return
    
    if job_id in config:
        print(f"{Colors.RED}Job ID already exists. Please choose a different ID.{Colors.RESET}")
        return

    # Select source directory
    print("\nNavigate to select the source directory (local).")
    source_dir = navigate_local_directories()
    if not source_dir:
        print("Operation canceled.")
        return

    # Select destination (remote)
    print("\nNavigate to select the destination directory (remote).")
    remote_name = select_remote()
    if not remote_name:
        print("Operation canceled.")
        return
    
    destination_path = navigate_remote_directories(remote_name)
    if not destination_path:
        print("Operation canceled.")
        return

    # Configure compression
    compress = get_yes_no("Do you want to compress files?")
    compression_level = None
    cores = None
    split_files = False
    split_size = None

    if compress:
        compression_level = get_int_input(
            f"Enter compression level (1=low, 9=high, default: {DEFAULT_COMPRESSION_LEVEL})",
            default=DEFAULT_COMPRESSION_LEVEL,
            min_val=1,
            max_val=9
        )
        cores = get_int_input(
            f"Enter the number of CPU cores to use (default: {DEFAULT_CORES})",
            default=DEFAULT_CORES,
            min_val=1
        )

        # Ask about split files (only if compression is enabled)
        split_files = get_yes_no("Do you want to split the compressed archive?")
        if split_files:
            split_size = input(
                f"Enter maximum size per part (e.g., 10M, 1G, default: {DEFAULT_SPLIT_SIZE}): "
            ).strip() or DEFAULT_SPLIT_SIZE

    # Configure rclone flags
    rclone_flags = _configure_rclone_flags(job_id, DEFAULT_BACKUP_FLAGS)

    # Save configuration
    config[job_id] = {
        "source_dir": source_dir,
        "destination": destination_path,
        "compress": compress,
        "compression_level": compression_level,
        "split_files": split_files,
        "split_size": split_size,
        "cores": cores,
        "rclone_flags": rclone_flags,
    }
    
    if not save_config(config):
        print(f"{Colors.RED}Failed to save configuration.{Colors.RESET}")
        return

    # Generate and run backup script
    script_path = generate_backup_script(config, job_id)
    print(f"{Colors.GREEN}Backup script generated: {script_path}{Colors.RESET}")

    if get_yes_no("Do you want to run the backup job now?", default=True):
        print(f"Running the backup job {job_id}...")
        if run_script(str(script_path)):
            print(f"{Colors.GREEN}Backup job completed successfully.{Colors.RESET}")
        else:
            print(f"{Colors.RED}Backup job failed.{Colors.RESET}")
            return

    # Ask about cron scheduling
    if get_yes_no("Do you want to schedule this job with a cron job?"):
        schedule_cron(config[job_id], job_id)
    else:
        print("Skipping cron job setup.")


def _configure_rclone_flags(job_id: str, default_flags: dict) -> dict:
    """
    Configure rclone flags for the job.
    
    Args:
        job_id: Job ID
        default_flags: Dictionary with default flags
    
    Returns:
        Dictionary with configured flags
    """
    print("\nConfigure rclone flags for this job (Press Enter to use default values):")
    
    flags = default_flags.copy()
    flags["--log-file"] = f"{job_id}_rclone.log"
    
    for flag, value in flags.items():
        if flag == "--log-file":
            continue  # Skip log-file, we set it automatically
        
        new_value = input(f"{flag} (default: {value}): ").strip()
        if new_value:
            flags[flag] = new_value

    # Ask about --progress
    if get_yes_no("Do you want to enable progress output (--progress)?"):
        flags["--progress"] = ""

    return flags
