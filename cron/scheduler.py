#!/usr/bin/env python3
"""
Cron job scheduling for BackupBuddy.
"""

import os
from utils.commands import run_command
from utils.display import Colors
from utils.validation import get_int_input, confirm_action


def schedule_cron(job: dict, job_id: str) -> None:
    """
    Add a cron job to schedule a task.
    
    Args:
        job: Job configuration
        job_id: Job ID
    """
    print("\nSetting up a cron job for your task...")

    # Build rclone command with flags from job configuration
    rclone_flags = " ".join(f"{flag} {value}" for flag, value in job.get("rclone_flags", {}).items())
    source = job.get("source") or job.get("source_dir")
    destination = job["destination"]
    cron_command = f"rclone copy {source} {destination} {rclone_flags}"

    # Collect cron schedule
    print("\nSet up your cron schedule:")
    minute = get_int_input("Minute (0-59, default: 0)", default=0, min_val=0, max_val=59)
    hour = get_int_input("Hour (0-23, default: 0)", default=0, min_val=0, max_val=23)
    
    month = input("Month (1-12, default: * for every month): ").strip() or "*"
    day_of_week = input("Day of the week (0=Sunday, 6=Saturday, * for every day, default: *): ").strip() or "*"

    # Build cron schedule
    schedule = f"{minute} {hour} * {month} {day_of_week}"
    full_cron = f"{schedule} {cron_command} # backupbuddy"

    # Add cron job
    print(f"\nAdding the following cron job:\n{full_cron}")
    try:
        add_command = f'(crontab -l 2>/dev/null; echo "{full_cron}") | crontab -'
        run_command(add_command)
        print(f"{Colors.GREEN}Cron job added successfully.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Failed to add cron job: {e}{Colors.RESET}")


def edit_cron_jobs() -> None:
    """List, edit or remove existing cron jobs."""
    print("\nManaging cron jobs...\n")

    try:
        result = run_command("crontab -l", capture_output=True, check=False)
        if result.returncode != 0 or not result.stdout.strip():
            print("No cron jobs found.")
            return
        
        cron_jobs = result.stdout.strip().split("\n")
    except Exception:
        print("No cron jobs found.")
        return

    if not cron_jobs:
        print("No cron jobs found.")
        return

    print("Existing cron jobs:")
    for i, job in enumerate(cron_jobs, start=1):
        print(f"{Colors.YELLOW}{i}.{Colors.RESET} {Colors.GREEN}{job}{Colors.RESET}")

    print("\nWhat would you like to do:")
    print(f"{Colors.YELLOW}1.{Colors.RESET} {Colors.GREEN}Delete a cron job{Colors.RESET}")
    print(f"{Colors.YELLOW}2.{Colors.RESET} {Colors.GREEN}Cancel{Colors.RESET}")

    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        _delete_cron_job(cron_jobs)
    elif choice == "2":
        print("Returning to main menu.")
    else:
        print("Invalid choice. Returning to main menu.")


def _delete_cron_job(cron_jobs: list) -> None:
    """Delete a specific cron job."""
    try:
        job_index = int(input("\nEnter the number of the cron job to delete: ").strip()) - 1
        
        if job_index < 0 or job_index >= len(cron_jobs):
            print(f"{Colors.RED}Invalid choice.{Colors.RESET}")
            return
        
        if confirm_action(f"Are you sure you want to delete this cron job?\n{cron_jobs[job_index]}"):
            # Remove job from list
            cron_jobs.pop(job_index)
            
            # Update crontab
            new_crontab = "\n".join(cron_jobs) + "\n" if cron_jobs else ""
            run_command(f'echo "{new_crontab}" | crontab -')
            print(f"{Colors.GREEN}Cron job deleted successfully.{Colors.RESET}")
        else:
            print("Deletion canceled.")
    
    except ValueError:
        print(f"{Colors.RED}Invalid input.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Failed to delete cron job: {e}{Colors.RESET}")


def remove_cron_jobs() -> None:
    """
    Remove only cron jobs created by BackupBuddy.
    Identified by the comment "# backupbuddy".
    """
    print("\nRemoving BackupBuddy cron jobs...")

    try:
        command = "crontab -l" if os.geteuid() == 0 else "sudo crontab -l"
        result = run_command(command, capture_output=True, check=False)

        if result.returncode != 0 or not result.stdout.strip():
            print("No cron jobs found.")
            return

        # Filter out BackupBuddy jobs
        current_cron_jobs = result.stdout.strip().split("\n")
        updated_cron_jobs = [job for job in current_cron_jobs if "# backupbuddy" not in job.lower()]

        if len(updated_cron_jobs) == len(current_cron_jobs):
            print("No BackupBuddy cron jobs found to remove.")
            return

        # Update crontab
        command = "crontab -" if os.geteuid() == 0 else "sudo crontab -"
        cron_data = "\n".join(updated_cron_jobs) + "\n"
        run_command(f"echo '{cron_data}' | {command}")

        print(f"{Colors.GREEN}BackupBuddy cron jobs removed successfully.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Failed to remove cron jobs: {e}{Colors.RESET}")
