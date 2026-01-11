#!/usr/bin/env python3
"""
BackupBuddy - Main entry point
A powerful backup and transfer tool with rclone integration
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.manager import load_config, save_config, list_jobs, delete_job
from config.constants import CONFIG_FILE, SCRIPT_DIR
from core.dependencies import check_and_install_dependencies, remove_dependencies
from core.remotes import manage_remotes
from cron.scheduler import edit_cron_jobs, remove_cron_jobs
from jobs.backup import create_backup_job
from jobs.transfer import create_transfer
from jobs.restore import restore_backup_job
from utils.display import display_logo, show_help, Colors
from utils.commands import run_script
from utils.validation import confirm_action


def rerun_job(config: dict) -> None:
    """Rerun an existing backup or transfer job."""
    if not config:
        print("No jobs found to rerun.")
        return

    print("\nExisting jobs:")
    job_list = list(config.keys())
    for i, job_id in enumerate(job_list, start=1):
        job = config[job_id]
        job_type = "Transfer" if job.get("type") == "transfer" else "Backup"
        source = job.get('source_dir', job.get('source', 'N/A'))
        print(f"{i}. [{job_type}] {job_id} - Source: {source}, Destination: {job['destination']}")

    try:
        choice = int(input("\nEnter the number of the job to rerun: ").strip()) - 1
        if choice < 0 or choice >= len(job_list):
            print("Invalid choice. Returning to main menu.")
            return

        job_id = job_list[choice]
        job_type = "transfer" if config[job_id].get("type") == "transfer" else "backup"
        script_path = SCRIPT_DIR / f"{job_type}_{job_id}.sh"
        
        if not script_path.exists():
            print(f"{Colors.RED}Error: Script for job {job_id} does not exist. Please recreate the job.{Colors.RESET}")
            return

        print(f"Running the job {job_id}...")
        if run_script(str(script_path)):
            print(f"{Colors.GREEN}Job completed successfully.{Colors.RESET}")
        else:
            print(f"{Colors.RED}Job failed.{Colors.RESET}")
    except ValueError:
        print("Invalid input. Returning to main menu.")


def clear_configurations() -> None:
    """Clear configurations: Backup jobs, remotes, or all data."""
    print("\nWhat do you want to clear?")
    print("1. Clear all remotes (rclone config)")
    print("2. Clear a specific job")
    print("3. Clear all jobs")
    print("4. Clear temporary files")
    print("5. Cancel")
    choice = input("Enter your choice (1/2/3/4/5): ").strip()

    if choice == "1":
        print("\nClearing all remotes using rclone config...")
        from utils.commands import run_command
        run_command("rclone config", check=False)
        print("Remotes cleared. You can now configure new remotes.")
    
    elif choice == "2":
        config = load_config()
        if not config:
            print("No jobs found to clear.")
            return
        
        print("\nConfigured jobs:")
        job_list = list(config.keys())
        for i, job_id in enumerate(job_list, start=1):
            print(f"{i}. {job_id}")
        
        try:
            job_choice = int(input("\nEnter the number of the job to delete: ").strip()) - 1
            if job_choice < 0 or job_choice >= len(job_list):
                print("Invalid choice. Returning to main menu.")
                return
            
            job_id = job_list[job_choice]
            print(f"\nDeleting job: {job_id}")
            if delete_job(config, job_id):
                print(f"{Colors.GREEN}Job '{job_id}' deleted successfully.{Colors.RESET}")
            else:
                print(f"{Colors.RED}Failed to delete job.{Colors.RESET}")
        except (ValueError, IndexError):
            print("Invalid input. Returning to main menu.")
    
    elif choice == "3":
        if confirm_action("Are you sure you want to clear all jobs?"):
            if CONFIG_FILE.exists():
                CONFIG_FILE.unlink()
                print(f"{Colors.GREEN}All jobs cleared.{Colors.RESET}")
            else:
                print("Configuration file not found. No jobs to clear.")
        else:
            print("Operation canceled.")
    
    elif choice == "4":
        if confirm_action("Are you sure you want to clear all temporary files?"):
            from config.constants import TEMP_DIR
            from utils.commands import run_command
            run_command(f"rm -rf {TEMP_DIR}/*", check=False)
            print(f"{Colors.GREEN}Temporary files cleared.{Colors.RESET}")
        else:
            print("Operation canceled.")
    
    elif choice == "5":
        print("Returning to main menu.")
    else:
        print("Invalid choice. Returning to main menu.")


def uninstall_backupbuddy() -> None:
    """Uninstall BackupBuddy and all related components."""
    print("\nUninstall BackupBuddy")
    print("1. Remove tools and dependencies only")
    print("2. Remove everything (tools, dependencies, temp, configs, jobs, cronjobs)")
    print("3. Cancel")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        remove_dependencies()
    elif choice == "2":
        if confirm_action("Are you sure you want to completely uninstall BackupBuddy?"):
            remove_cron_jobs()
            
            # Remove temp files
            from config.constants import TEMP_DIR
            from utils.commands import run_command
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
            
            print(f"\n{Colors.GREEN}BackupBuddy and all related components have been fully removed.{Colors.RESET}")
            print("Exiting BackupBuddy. Goodbye!")
            sys.exit(0)
        else:
            print("Uninstallation canceled.")
    elif choice == "3":
        print("Uninstallation canceled.")
    else:
        print("Invalid choice. Returning to main menu.")


def main():
    """Main program to handle backup and restore operations."""
    check_and_install_dependencies()

    # Display logo and welcome message
    display_logo()

    while True:
        config = load_config()
        list_jobs(config)

        print("\nWhat would you like to do:")
        print(f"{Colors.YELLOW}1.{Colors.RESET} Create a new backup job")
        print(f"{Colors.YELLOW}2.{Colors.RESET} Create a new transfer job")
        print(f"{Colors.YELLOW}3.{Colors.RESET} Restore from an existing backup job")
        print(f"{Colors.YELLOW}4.{Colors.RESET} Rerun an existing job")
        print(f"{Colors.YELLOW}5.{Colors.RESET} Manage cron jobs")
        print(f"{Colors.YELLOW}6.{Colors.RESET} Clear configurations and data")
        print(f"{Colors.YELLOW}7.{Colors.RESET} Add a new remote or local path")
        print(f"{Colors.YELLOW}8.{Colors.RESET} Uninstall BackupBuddy")
        print(f"{Colors.YELLOW}9.{Colors.RESET} Help")
        print(f"{Colors.YELLOW}10.{Colors.RESET} Exit")
        
        choice = input("Enter your choice (1-10): ").strip()

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
        elif choice == "6":
            clear_configurations()
        elif choice == "7":
            manage_remotes()
        elif choice == "8":
            uninstall_backupbuddy()
        elif choice == "9":
            show_help()
        elif choice == "10":
            print("Goodbye! Thanks for using BackupBuddy.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
