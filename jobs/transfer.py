#!/usr/bin/env python3
"""
Transfer job creation and management for BackupBuddy.
Matrix UI implementation.
"""

from config.manager import save_config
from config.constants import DEFAULT_TRANSFER_FLAGS, DEFAULT_COMPRESSION_LEVEL, DEFAULT_CORES, DEFAULT_SPLIT_SIZE
from core.navigation import navigate_local_directories, navigate_remote_directories
from core.remotes import select_remote
from scripts.generator import generate_transfer_script
from cron.scheduler import schedule_cron
from utils.commands import run_script
from utils.matrix_ui import MatrixUI, MatrixColors
from utils.validation import get_yes_no, get_int_input, get_user_choice


def create_transfer(config: dict) -> None:
    """
    Guide user through creating a new transfer job with Matrix UI.
    """
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE TRANSFER JOB", "Configure a new transfer workflow")
    
    # Step 1: Job ID
    print(f"{MatrixColors.CYBER_BLUE}Step 1/5: Job Configuration{MatrixColors.RESET}\n")
    job_id = input(f"{MatrixColors.MATRIX_GREEN}Enter a unique ID for the transfer job: {MatrixColors.RESET}").strip()
    
    if not job_id:
        MatrixUI.print_error("INVALID INPUT", "Job ID cannot be empty")
        input("\nPress Enter to continue...")
        return
    
    if job_id in config:
        MatrixUI.print_error("DUPLICATE ID", f"Job ID '{job_id}' already exists",
                           actions=["Choose a different ID", "Delete the existing job first"])
        input("\nPress Enter to continue...")
        return

    # Step 2: Select source
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE TRANSFER JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 2/5: Source Selection{MatrixColors.RESET}\n")
    
    source = _select_source()
    if not source:
        MatrixUI.print_warning("CANCELLED", "Transfer job creation cancelled")
        input("\nPress Enter to continue...")
        return

    # Step 3: Select destination
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE TRANSFER JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 3/5: Destination Selection{MatrixColors.RESET}\n")
    
    destination = _select_destination()
    if not destination:
        MatrixUI.print_warning("CANCELLED", "Transfer job creation cancelled")
        input("\nPress Enter to continue...")
        return

    # Step 4: Configure compression
    MatrixUI.clear_screen()
    MatrixUI.print_header("CREATE TRANSFER JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 4/5: Compression Settings{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'COMPRESSION OPTIONS'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
    
    compress = get_yes_no("Do you want to compress files before transfer?")
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
    MatrixUI.print_header("CREATE TRANSFER JOB", f"Job: {job_id}")
    print(f"{MatrixColors.CYBER_BLUE}Step 5/5: rclone Configuration{MatrixColors.RESET}\n")
    
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
        MatrixUI.print_error("SAVE FAILED", "Failed to save configuration")
        input("\nPress Enter to continue...")
        return

    # Generate and run transfer script
    MatrixUI.clear_screen()
    print(f"\n{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Generating transfer script...\n")
    
    script_path = generate_transfer_script(config, job_id)
    
    MatrixUI.print_success(
        "SCRIPT GENERATED",
        f"Transfer script created: {script_path}"
    )

    if get_yes_no("Do you want to run the transfer job now?", default=True):
        MatrixUI.clear_screen()
        print(f"\n{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Running transfer job '{job_id}'...\n")
        
        if run_script(str(script_path)):
            MatrixUI.print_success(
                "TRANSFER COMPLETED",
                f"Job '{job_id}' executed successfully",
                stats={
                    "Job ID": job_id,
                    "Source": source,
                    "Destination": destination,
                    "Type": "Transfer"
                }
            )
        else:
            MatrixUI.print_error(
                "TRANSFER FAILED",
                f"Job '{job_id}' encountered an error",
                actions=["Check the log file", "Verify source/destination", "Try running again"]
            )
        input("\nPress Enter to continue...")
        return

    # Ask about cron scheduling
    if get_yes_no("Do you want to schedule this job with a cron job?"):
        schedule_cron(config[job_id], job_id)
    
    input("\nPress Enter to continue...")


def _select_source() -> str:
    """Select source for transfer with Matrix UI."""
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 50}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'SELECT SOURCE'.center(50)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 50}╝{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.MATRIX_GREEN}1.{MatrixColors.RESET} Local directory")
    print(f"{MatrixColors.MATRIX_GREEN}2.{MatrixColors.RESET} Remote\n")
    
    source_type = get_user_choice("Enter your choice", ["1", "2"], allow_back=False)
    
    if source_type == "1":
        print(f"\n{MatrixColors.CYBER_BLUE}Navigate to select the source directory (local).{MatrixColors.RESET}\n")
        return navigate_local_directories()
    elif source_type == "2":
        print(f"\n{MatrixColors.CYBER_BLUE}Select the source remote:{MatrixColors.RESET}\n")
        source_remote = select_remote()
        if source_remote:
            return navigate_remote_directories(source_remote)
    
    return None


def _select_destination() -> str:
    """Select destination for transfer with Matrix UI."""
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 50}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'SELECT DESTINATION'.center(50)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 50}╝{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.MATRIX_GREEN}1.{MatrixColors.RESET} Local directory")
    print(f"{MatrixColors.MATRIX_GREEN}2.{MatrixColors.RESET} Remote\n")
    
    dest_type = get_user_choice("Enter your choice", ["1", "2"], allow_back=False)
    
    if dest_type == "1":
        print(f"\n{MatrixColors.CYBER_BLUE}Navigate to select the destination directory (local).{MatrixColors.RESET}\n")
        return navigate_local_directories()
    elif dest_type == "2":
        print(f"\n{MatrixColors.CYBER_BLUE}Select the destination remote:{MatrixColors.RESET}\n")
        dest_remote = select_remote()
        if dest_remote:
            return navigate_remote_directories(dest_remote)
    
    return None


def _configure_rclone_flags(job_id: str, default_flags: dict) -> dict:
    """Configure rclone flags for transfer job with Matrix UI."""
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
