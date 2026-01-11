#!/usr/bin/env python3
"""
Backup job creation and management for BackupBuddy.
Matrix UI implementation.
"""

from config.manager import save_config
from config.constants import DEFAULT_BACKUP_FLAGS, DEFAULT_COMPRESSION_LEVEL, DEFAULT_CORES, DEFAULT_SPLIT_SIZE
from core.navigation import navigate_local_directories, navigate_remote_directories
from core.remotes import select_remote
from scripts.generator import generate_backup_script
from cron.scheduler import schedule_cron
from utils.commands import run_script
from utils.matrix_ui import MatrixUI, MatrixColors
from utils.validation import get_yes_no, get_int_input


def create_backup_job(config: dict) -> None:
    """
    Guide user through creating a new backup job with Matrix UI.
    """
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE BACKUP JOB", "Configure a new backup workflow")
    
    # Step 1: Job ID
    print(f"{MatrixColors.CYBER_BLUE}Step 1/5: Job Configuration{MatrixColors.RESET}\n")
    job_id = input(f"{MatrixColors.MATRIX_GREEN}Enter a unique ID for the backup job: {MatrixColors.RESET}").strip()
    
    if not job_id:
        MatrixUI.print_error("INVALID INPUT", "Job ID cannot be empty")
        input("\nPress Enter to continue...")
        return
    
    if job_id in config:
        MatrixUI.print_error("DUPLICATE ID", f"Job ID '{job_id}' already exists", 
                           actions=["Choose a different ID", "Delete the existing job first"])
        input("\nPress Enter to continue...")
        return

    # Step 2: Select source directory
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE BACKUP JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 2/5: Source Selection{MatrixColors.RESET}\n")
    print(f"{MatrixColors.MATRIX_GREEN}Navigate to select the source directory (local).{MatrixColors.RESET}\n")
    
    source_dir = navigate_local_directories()
    if not source_dir:
        MatrixUI.print_warning("CANCELLED", "Backup job creation cancelled")
        input("\nPress Enter to continue...")
        return

    # Step 3: Select destination (remote)
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE BACKUP JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 3/5: Destination Selection{MatrixColors.RESET}\n")
    print(f"{MatrixColors.MATRIX_GREEN}Navigate to select the destination directory (remote).{MatrixColors.RESET}\n")
    
    remote_name = select_remote()
    if not remote_name:
        MatrixUI.print_warning("CANCELLED", "Backup job creation cancelled")
        input("\nPress Enter to continue...")
        return
    
    destination_path = navigate_remote_directories(remote_name)
    if not destination_path:
        MatrixUI.print_warning("CANCELLED", "Backup job creation cancelled")
        input("\nPress Enter to continue...")
        return

    # Step 4: Configure compression
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE BACKUP JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 4/5: Compression Settings{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'COMPRESSION OPTIONS'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
    
    compress = get_yes_no("Do you want to compress files?")
    compression_level = None
    cores = None
    split_files = False
    split_size = None

    if compress:
        print()
        compression_level = get_int_input(
            f"{MatrixColors.MATRIX_GREEN}Compression level (1=low, 9=high, default: {DEFAULT_COMPRESSION_LEVEL}){MatrixColors.RESET}",
            default=DEFAULT_COMPRESSION_LEVEL,
            min_val=1,
            max_val=9
        )
        cores = get_int_input(
            f"{MatrixColors.MATRIX_GREEN}Number of CPU cores (default: {DEFAULT_CORES}){MatrixColors.RESET}",
            default=DEFAULT_CORES,
            min_val=1
        )

        print()
        split_files = get_yes_no("Do you want to split the compressed archive?")
        if split_files:
            split_size = input(
                f"{MatrixColors.MATRIX_GREEN}Maximum size per part (e.g., 10M, 1G, default: {DEFAULT_SPLIT_SIZE}): {MatrixColors.RESET}"
            ).strip() or DEFAULT_SPLIT_SIZE

    # Step 5: Configure rclone flags
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE BACKUP JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 5/5: rclone Configuration{MatrixColors.RESET}\n")
    
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
        MatrixUI.print_error("SAVE FAILED", "Failed to save configuration")
        input("\nPress Enter to continue...")
        return

    # Generate and run backup script
    MatrixUI.clear_screen()
    print(f"\n{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Generating backup script...\n")
    
    script_path = generate_backup_script(config, job_id)
    
    MatrixUI.print_success(
        "SCRIPT GENERATED",
        f"Backup script created: {script_path}"
    )

    if get_yes_no("Do you want to run the backup job now?", default=True):
        MatrixUI.clear_screen()
        print(f"\n{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Running backup job '{job_id}'...\n")
        
        if run_script(str(script_path)):
            MatrixUI.print_success(
                "BACKUP COMPLETED",
                f"Job '{job_id}' executed successfully",
                stats={
                    "Job ID": job_id,
                    "Source": source_dir,
                    "Destination": destination_path,
                    "Compressed": "Yes" if compress else "No"
                }
            )
        else:
            MatrixUI.print_error(
                "BACKUP FAILED",
                f"Job '{job_id}' encountered an error",
                actions=["Check the log file", "Verify remote connection", "Try running again"]
            )
        input("\nPress Enter to continue...")
        return

    # Ask about cron scheduling
    if get_yes_no("Do you want to schedule this job with a cron job?"):
        schedule_cron(config[job_id], job_id)
    
    input("\nPress Enter to continue...")


def _configure_rclone_flags(job_id: str, default_flags: dict) -> dict:
    """
    Configure rclone flags for the job with Matrix UI.
    """
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'RCLONE FLAGS CONFIGURATION'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.DIM}Press Enter to use default values{MatrixColors.RESET}\n")
    
    flags = default_flags.copy()
    flags["--log-file"] = f"{job_id}_rclone.log"
    
    for flag, value in flags.items():
        if flag == "--log-file":
            continue
        
        new_value = input(f"{MatrixColors.MATRIX_GREEN}{flag}{MatrixColors.RESET} (default: {MatrixColors.CYBER_BLUE}{value}{MatrixColors.RESET}): ").strip()
        if new_value:
            flags[flag] = new_value

    print()
    if get_yes_no("Enable progress output (--progress)?"):
        flags["--progress"] = ""

    return flags
