#!/usr/bin/env python3
"""
BackupBuddy - Main entry point
A powerful backup and transfer tool with rclone integration
Matrix-inspired UI for a cyberpunk experience
"""

import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.manager import load_config, save_config, list_jobs, delete_job
from config.constants import CONFIG_FILE, SCRIPT_DIR, TEMP_DIR
from core.dependencies import check_and_install_dependencies, remove_dependencies
from core.remotes import manage_remotes
from cron.scheduler import edit_cron_jobs, remove_cron_jobs
from jobs.backup import create_backup_job
from jobs.transfer import create_transfer
from jobs.restore import restore_backup_job
from utils.display import show_help, Colors
from utils.matrix_ui import MatrixUI, MatrixColors
from utils.commands import run_script, run_command
from utils.validation import confirm_action


def display_main_menu():
    """Display the main menu with Matrix styling."""
    MatrixUI.clear_screen()
    MatrixUI.print_logo()
    
    # System status bar
    config = load_config()
    active_jobs = len(config)
    status_text = f"[SYSTEM STATUS] Active Jobs: {active_jobs} | Status: OPERATIONAL"
    
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 71}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║  {status_text}{' ' * (69 - len(status_text))}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 71}╝{MatrixColors.RESET}\n")
    
    # Job Management Section
    MatrixUI.print_menu_section(
        "JOB MANAGEMENT",
        [
            ("1", "💾", "CREATE BACKUP JOB     ", "New backup workflow"),
            ("2", "📦", "CREATE TRANSFER JOB   ", "Move data between locations"),
            ("3", "🔄", "RESTORE FROM BACKUP   ", "Recover lost data"),
            ("4", "▶️ ", "RERUN EXISTING JOB    ", "Execute saved job"),
        ]
    )
    
    # System Configuration Section
    MatrixUI.print_menu_section(
        "SYSTEM CONFIGURATION",
        [
            ("5", "⏰", "MANAGE CRON JOBS      ", "Schedule automation"),
            ("6", "🗑️ ", "CLEAR CONFIGURATIONS  ", "Reset settings"),
            ("7", "☁️ ", "MANAGE REMOTES        ", "Cloud connections"),
        ]
    )
    
    # Utilities Section
    MatrixUI.print_menu_section(
        "UTILITIES",
        [
            ("8", "🗑️ ", "UNINSTALL SYSTEM      ", "Remove BackupBuddy"),
            ("9", "❓", "HELP & DOCS           ", "Documentation"),
            ("0", "🚪", "EXIT SYSTEM           ", "Shutdown safely"),
        ]
    )
    
    MatrixUI.print_status_bar("COMMAND: _")


def display_job_list_matrix(config: dict):
    """Display configured jobs with Matrix styling."""
    if not config:
        return
    
    backup_jobs = []
    transfer_jobs = []
    
    for job_id, job_data in config.items():
        if job_data.get("type") == "transfer":
            source = job_data.get("source", "N/A")
            dest = job_data.get("destination", "N/A")
            transfer_jobs.append((job_id, source, dest))
        else:
            source = job_data.get("source_dir", "N/A")
            dest = job_data.get("destination", "N/A")
            compressed = "Yes" if job_data.get("compress") else "No"
            split = "Yes" if job_data.get("split_files") else "No"
            backup_jobs.append((job_id, source, dest, compressed, split))
    
    print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 68}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'CONFIGURED JOBS'.center(68)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 68}╝{MatrixColors.RESET}\n")
    
    if backup_jobs:
        print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * 65}┐{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ BACKUP JOBS {'▓' * 48}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * 65}┤{MatrixColors.RESET}")
        
        for idx, (job_id, source, dest, compressed, split) in enumerate(backup_jobs, 1):
            print(f"    {MatrixColors.MATRIX_GREEN}│ {MatrixColors.BOLD}{idx}. 💾 {job_id[:30]:<30}{MatrixColors.RESET}{' ' * 30}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│    {MatrixColors.DIM}📂 {source[:40]} → {dest[:15]}{MatrixColors.RESET}{' ' * 4}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│    {MatrixColors.DIM}🗜️  Compressed: {compressed} | Split: {split}{MatrixColors.RESET}{' ' * 22}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            if idx < len(backup_jobs):
                print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
        
        print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * 65}┘{MatrixColors.RESET}\n")
    
    if transfer_jobs:
        print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * 65}┐{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ TRANSFER JOBS {'▓' * 47}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * 65}┤{MatrixColors.RESET}")
        
        for idx, (job_id, source, dest) in enumerate(transfer_jobs, 1):
            print(f"    {MatrixColors.MATRIX_GREEN}│ {MatrixColors.BOLD}{idx}. 📦 {job_id[:30]:<30}{MatrixColors.RESET}{' ' * 30}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│    {MatrixColors.DIM}📂 {source[:40]} → {dest[:15]}{MatrixColors.RESET}{' ' * 4}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            if idx < len(transfer_jobs):
                print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
        
        print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * 65}┘{MatrixColors.RESET}\n")


def rerun_job(config: dict) -> None:
    """Rerun an existing backup or transfer job."""
    if not config:
        MatrixUI.print_warning("NO JOBS FOUND", "No jobs configured to rerun.")
        input("\nPress Enter to continue...")
        return

    print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 68}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'RERUN EXISTING JOB'.center(68)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 68}╝{MatrixColors.RESET}\n")

    job_list = list(config.keys())
    for i, job_id in enumerate(job_list, start=1):
        job = config[job_id]
        job_type = "Transfer" if job.get("type") == "transfer" else "Backup"
        source = job.get('source_dir', job.get('source', 'N/A'))
        print(f"{MatrixColors.MATRIX_GREEN}{i}. [{job_type}] {job_id}{MatrixColors.RESET}")
        print(f"   {MatrixColors.DIM}Source: {source}{MatrixColors.RESET}")
        print(f"   {MatrixColors.DIM}Destination: {job['destination']}{MatrixColors.RESET}\n")

    try:
        choice = int(input(f"{MatrixColors.CYBER_BLUE}Enter job number to rerun: {MatrixColors.RESET}").strip()) - 1
        if choice < 0 or choice >= len(job_list):
            MatrixUI.print_error("INVALID CHOICE", "Job number out of range")
            input("\nPress Enter to continue...")
            return

        job_id = job_list[choice]
        job_type = "transfer" if config[job_id].get("type") == "transfer" else "backup"
        script_path = SCRIPT_DIR / f"{job_type}_{job_id}.sh"
        
        if not script_path.exists():
            MatrixUI.print_error(
                "SCRIPT NOT FOUND",
                f"Script for job '{job_id}' does not exist",
                actions=["Recreate the job", "Check script directory"]
            )
            input("\nPress Enter to continue...")
            return

        print(f"\n{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Running job {job_id}...")
        
        if run_script(str(script_path)):
            MatrixUI.print_success(
                "JOB COMPLETED",
                f"Job '{job_id}' executed successfully"
            )
        else:
            MatrixUI.print_error(
                "JOB FAILED",
                f"Job '{job_id}' encountered an error"
            )
        
        input("\nPress Enter to continue...")
    except ValueError:
        MatrixUI.print_error("INVALID INPUT", "Please enter a valid number")
        input("\nPress Enter to continue...")


def clear_configurations() -> None:
    """Clear configurations with Matrix styling."""
    print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 68}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'CLEAR CONFIGURATIONS'.center(68)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 68}╝{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.MATRIX_GREEN}1.{MatrixColors.RESET} Clear all remotes (rclone config)")
    print(f"{MatrixColors.MATRIX_GREEN}2.{MatrixColors.RESET} Clear a specific job")
    print(f"{MatrixColors.MATRIX_GREEN}3.{MatrixColors.RESET} Clear all jobs")
    print(f"{MatrixColors.MATRIX_GREEN}4.{MatrixColors.RESET} Clear temporary files")
    print(f"{MatrixColors.MATRIX_GREEN}5.{MatrixColors.RESET} Cancel\n")
    
    choice = input(f"{MatrixColors.CYBER_BLUE}Enter your choice (1-5): {MatrixColors.RESET}").strip()

    if choice == "1":
        print(f"\n{MatrixColors.YELLOW}Opening rclone configuration...{MatrixColors.RESET}")
        run_command("rclone config", check=False)
        
    elif choice == "2":
        config = load_config()
        if not config:
            MatrixUI.print_warning("NO JOBS", "No jobs found to clear")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{MatrixColors.BOLD}Configured jobs:{MatrixColors.RESET}")
        job_list = list(config.keys())
        for i, job_id in enumerate(job_list, start=1):
            print(f"{MatrixColors.MATRIX_GREEN}{i}.{MatrixColors.RESET} {job_id}")
        
        try:
            job_choice = int(input(f"\n{MatrixColors.CYBER_BLUE}Enter job number to delete: {MatrixColors.RESET}").strip()) - 1
            if 0 <= job_choice < len(job_list):
                job_id = job_list[job_choice]
                if confirm_action(f"Delete job '{job_id}'?"):
                    if delete_job(config, job_id):
                        MatrixUI.print_success("JOB DELETED", f"Job '{job_id}' removed successfully")
                    else:
                        MatrixUI.print_error("DELETE FAILED", "Could not delete job")
                input("\nPress Enter to continue...")
        except (ValueError, IndexError):
            MatrixUI.print_error("INVALID INPUT", "Please enter a valid job number")
            input("\nPress Enter to continue...")
    
    elif choice == "3":
        if confirm_action("Are you sure you want to clear ALL jobs?"):
            if CONFIG_FILE.exists():
                CONFIG_FILE.unlink()
                MatrixUI.print_success("ALL JOBS CLEARED", "All job configurations removed")
            input("\nPress Enter to continue...")
    
    elif choice == "4":
        if confirm_action("Clear all temporary files?"):
            run_command(f"rm -rf {TEMP_DIR}/*", check=False)
            MatrixUI.print_success("TEMP CLEARED", "Temporary files removed")
        input("\nPress Enter to continue...")


def uninstall_backupbuddy() -> None:
    """Uninstall BackupBuddy with Matrix styling."""
    print(f"\n{MatrixColors.ALERT_RED}╔{'═' * 68}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.ALERT_RED}║{MatrixColors.BOLD}{'UNINSTALL BACKUPBUDDY'.center(68)}{MatrixColors.RESET}{MatrixColors.ALERT_RED}║{MatrixColors.RESET}")
    print(f"{MatrixColors.ALERT_RED}╚{'═' * 68}╝{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.MATRIX_GREEN}1.{MatrixColors.RESET} Remove tools and dependencies only")
    print(f"{MatrixColors.MATRIX_GREEN}2.{MatrixColors.RESET} Remove everything (complete uninstall)")
    print(f"{MatrixColors.MATRIX_GREEN}3.{MatrixColors.RESET} Cancel\n")

    choice = input(f"{MatrixColors.CYBER_BLUE}Enter your choice (1-3): {MatrixColors.RESET}").strip()

    if choice == "1":
        remove_dependencies()
        input("\nPress Enter to continue...")
        
    elif choice == "2":
        if confirm_action("⚠️  This will COMPLETELY remove BackupBuddy. Continue?"):
            print(f"\n{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Uninstalling...")
            
            remove_cron_jobs()
            
            # Remove temp files
            if TEMP_DIR.exists():
                run_command(f"rm -rf {TEMP_DIR}", check=False)
            
            # Remove configurations
            if CONFIG_FILE.exists():
                CONFIG_FILE.unlink()
            
            # Remove script directory
            if SCRIPT_DIR.exists():
                import shutil
                shutil.rmtree(SCRIPT_DIR)
            
            remove_dependencies()
            
            MatrixUI.print_success(
                "UNINSTALL COMPLETE",
                "BackupBuddy has been completely removed from your system"
            )
            
            print(f"\n{MatrixColors.MATRIX_GREEN}Goodbye! Thanks for using BackupBuddy.{MatrixColors.RESET}\n")
            time.sleep(2)
            sys.exit(0)


def main():
    """Main program loop with Matrix UI."""
    # Install dependencies first
    check_and_install_dependencies()
    
    # Initial welcome screen
    MatrixUI.clear_screen()
    MatrixUI.print_logo()
    time.sleep(1)
    
    MatrixUI.type_text("Initializing BackupBuddy systems...", delay=0.02)
    time.sleep(0.5)
    
    while True:
        config = load_config()
        display_main_menu()
        display_job_list_matrix(config)
        
        choice = input(f"\r{MatrixColors.CYBER_BLUE}    ▸ COMMAND: {MatrixColors.RESET}").strip()

        if choice == "1":
            create_backup_job(config)
        elif choice == "2":
            create_transfer(config)
        elif choice == "3":
            restore_backup_job(config)
        elif choice == "4":
            rerun_job(config)
        elif choice == "5":
            edit_cron_jobs()
            input("\nPress Enter to continue...")
        elif choice == "6":
            clear_configurations()
        elif choice == "7":
            manage_remotes()
            input("\nPress Enter to continue...")
        elif choice == "8":
            uninstall_backupbuddy()
        elif choice == "9":
            MatrixUI.clear_screen()
            show_help()
            input("\nPress Enter to continue...")
        elif choice == "0":
            MatrixUI.clear_screen()
            print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 68}╗{MatrixColors.RESET}")
            print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'SYSTEM SHUTDOWN'.center(68)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
            print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 68}╝{MatrixColors.RESET}\n")
            MatrixUI.type_text("Shutting down BackupBuddy...", delay=0.03)
            print(f"\n{MatrixColors.CYBER_BLUE}Goodbye! Thanks for using BackupBuddy.{MatrixColors.RESET}\n")
            time.sleep(1)
            break
        else:
            MatrixUI.print_error("INVALID COMMAND", f"'{choice}' is not a valid option")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{MatrixColors.WARNING_AMBER}⚠ Interrupted by user{MatrixColors.RESET}")
        print(f"{MatrixColors.CYBER_BLUE}Goodbye!{MatrixColors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        MatrixUI.print_error(
            "CRITICAL ERROR",
            str(e),
            error_code="UNHANDLED_EXCEPTION"
        )
        sys.exit(1)
