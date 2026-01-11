#!/usr/bin/env python3
"""
Transfer job creation and management for BackupBuddy.
"""

from config.manager import save_config
from config.constants import DEFAULT_TRANSFER_FLAGS, DEFAULT_COMPRESSION_LEVEL, DEFAULT_CORES, DEFAULT_SPLIT_SIZE
from core.navigation import navigate_local_directories, navigate_remote_directories
from core.remotes import select_remote
from scripts.generator import generate_transfer_script
from cron.scheduler import schedule_cron
from utils.commands import run_script
from utils.display import Colors
from utils.validation import get_yes_no, get_int_input, get_user_choice


def create_transfer(config: dict) -> None:
    """
    Guide user through creating a new transfer job.
    """
    print("\nCreating a new transfer job.")
    job_id = input("Enter a unique ID for the transfer job: ").strip()
    
    if not job_id:
        print(f"{Colors.RED}Job ID cannot be empty.{Colors.RESET}")
        return
    
    if job_id in config:
        print(f"{Colors.RED}Job ID already exists. Please choose a different ID.{Colors.RESET}")
        return

    # Select source
    source = _select_source()
    if not source:
        print("Operation canceled.")
        return

    # Select destination
    destination = _select_destination()
    if not destination:
        print("Operation canceled.")
        return

    # Configure compression
    compress = get_yes_no("Do you want to compress files before transfer?")
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

        split_files = get_yes_no("Do you want to split the compressed archive?")
        if split_files:
            split_size = input(
                f"Enter maximum size per part (e.g., 10M, 1G, default: {DEFAULT_SPLIT_SIZE}): "
            ).strip() or DEFAULT_SPLIT_SIZE

    # Configure rclone flags
    rclone_flags = _configure_rclone_flags(job_id, DEFAULT_TRANSFER_FLAGS)

    # Save configuration
    config[job_id] = {
        "source": source,
        "destination": destination,
        "type": "transfer",
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

    # Generate and run transfer script
    script_path = generate_transfer_script(config, job_id)
    print(f"{Colors.GREEN}Transfer script generated: {script_path}{Colors.RESET}")

    if get_yes_no("Do you want to run the transfer job now?", default=True):
        print(f"Running the transfer job {job_id}...")
        if run_script(str(script_path)):
            print(f"{Colors.GREEN}Transfer job completed successfully.{Colors.RESET}")
        else:
            print(f"{Colors.RED}Transfer job failed.{Colors.RESET}")
            return

    # Ask about cron scheduling
    if get_yes_no("Do you want to schedule this job with a cron job?"):
        schedule_cron(config[job_id], job_id)
    else:
        print("Skipping cron job setup.")


def _select_source() -> str:
    """Select source for transfer."""
    print("\nSelect the source:")
    print("1. Local directory")
    print("2. Remote")
    
    source_type = get_user_choice("Enter your choice", ["1", "2"], allow_back=False)
    
    if source_type == "1":
        print("\nNavigate to select the source directory (local).")
        return navigate_local_directories()
    elif source_type == "2":
        print("\nSelect the source remote:")
        source_remote = select_remote()
        if source_remote:
            return navigate_remote_directories(source_remote)
    
    return None


def _select_destination() -> str:
    """Select destination for transfer."""
    print("\nSelect the destination:")
    print("1. Local directory")
    print("2. Remote")
    
    dest_type = get_user_choice("Enter your choice", ["1", "2"], allow_back=False)
    
    if dest_type == "1":
        print("\nNavigate to select the destination directory (local).")
        return navigate_local_directories()
    elif dest_type == "2":
        print("\nSelect the destination remote:")
        dest_remote = select_remote()
        if dest_remote:
            return navigate_remote_directories(dest_remote)
    
    return None


def _configure_rclone_flags(job_id: str, default_flags: dict) -> dict:
    """Configure rclone flags for transfer job."""
    print("\nConfigure rclone flags for this job (Press Enter to use default values):")
    
    flags = default_flags.copy()
    flags["--log-file"] = f"{job_id}_rclone.log"
    
    for flag, value in flags.items():
        if flag == "--log-file":
            continue
        
        new_value = input(f"{flag} (default: {value}): ").strip()
        if new_value:
            flags[flag] = new_value

    if get_yes_no("Do you want to enable progress output (--progress)?"):
        flags["--progress"] = ""

    return flags
