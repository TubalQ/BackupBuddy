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
    Add a cron job to schedule a task with Matrix UI.
    
    Args:
        job: Job configuration
        job_id: Job ID
    """
    from utils.matrix_ui import MatrixUI, MatrixColors
    
    MatrixUI.clear_screen()
    MatrixUI.print_header("SCHEDULE CRON JOB", f"Job: {job_id}")
    
    print(f"{MatrixColors.CYBER_BLUE}Configure automatic scheduling for this job{MatrixColors.RESET}\n")

    # Build rclone command with flags from job configuration
    rclone_flags = " ".join(f"{flag} {value}" for flag, value in job.get("rclone_flags", {}).items())
    source = job.get("source") or job.get("source_dir")
    destination = job["destination"]
    cron_command = f"rclone copy {source} {destination} {rclone_flags}"

    # Collect cron schedule
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'CRON SCHEDULE CONFIGURATION'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
    
    minute = get_int_input(f"{MatrixColors.MATRIX_GREEN}Minute (0-59, default: 0){MatrixColors.RESET}", default=0, min_val=0, max_val=59)
    hour = get_int_input(f"{MatrixColors.MATRIX_GREEN}Hour (0-23, default: 0){MatrixColors.RESET}", default=0, min_val=0, max_val=23)
    
    month = input(f"{MatrixColors.MATRIX_GREEN}Month (1-12, default: * for every month): {MatrixColors.RESET}").strip() or "*"
    day_of_week = input(f"{MatrixColors.MATRIX_GREEN}Day of the week (0=Sunday, 6=Saturday, * for every day, default: *): {MatrixColors.RESET}").strip() or "*"

    # Build cron schedule
    schedule = f"{minute} {hour} * {month} {day_of_week}"
    full_cron = f"{schedule} {cron_command} # backupbuddy"

    # Display preview
    print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'CRON JOB PREVIEW'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
    print(f"{MatrixColors.DIM}{full_cron}{MatrixColors.RESET}\n")

    # Add cron job
    try:
        add_command = f'(crontab -l 2>/dev/null; echo "{full_cron}") | crontab -'
        run_command(add_command)
        MatrixUI.print_success("CRON JOB ADDED", f"Job '{job_id}' scheduled successfully")
    except Exception as e:
        MatrixUI.print_error("CRON FAILED", f"Failed to add cron job: {e}")
    
    input("\nPress Enter to continue...")


def edit_cron_jobs() -> None:
    """List, edit or remove existing cron jobs with Matrix UI."""
    from utils.matrix_ui import MatrixUI, MatrixColors
    
    MatrixUI.clear_screen()
    MatrixUI.print_header("MANAGE CRON JOBS", "View and modify scheduled tasks")

    try:
        result = run_command("crontab -l", capture_output=True, check=False)
        if result.returncode != 0 or not result.stdout.strip():
            MatrixUI.print_warning("NO CRON JOBS", "No cron jobs found")
            return
        
        cron_jobs = result.stdout.strip().split("\n")
    except Exception:
        MatrixUI.print_warning("NO CRON JOBS", "No cron jobs found")
        return

    if not cron_jobs:
        MatrixUI.print_warning("NO CRON JOBS", "No cron jobs found")
        return

    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'EXISTING CRON JOBS'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
    
    for i, job in enumerate(cron_jobs, start=1):
        print(f"{MatrixColors.MATRIX_GREEN}{i}.{MatrixColors.RESET} {MatrixColors.CYBER_BLUE}{job}{MatrixColors.RESET}")

    print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 50}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'ACTIONS'.center(50)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 50}╝{MatrixColors.RESET}\n")
    print(f"{MatrixColors.MATRIX_GREEN}1.{MatrixColors.RESET} Delete a cron job")
    print(f"{MatrixColors.MATRIX_GREEN}2.{MatrixColors.RESET} Cancel\n")

    choice = input(f"{MatrixColors.CYBER_BLUE}Enter your choice (1/2): {MatrixColors.RESET}").strip()

    if choice == "1":
        _delete_cron_job(cron_jobs)
    elif choice == "2":
        return
    else:
        MatrixUI.print_error("INVALID CHOICE", "Please enter 1 or 2")


def _delete_cron_job(cron_jobs: list) -> None:
    """Delete a specific cron job with Matrix UI."""
    from utils.matrix_ui import MatrixUI, MatrixColors
    
    try:
        job_index = int(input(f"\n{MatrixColors.CYBER_BLUE}Enter the number of the cron job to delete: {MatrixColors.RESET}").strip()) - 1
        
        if job_index < 0 or job_index >= len(cron_jobs):
            MatrixUI.print_error("INVALID CHOICE", "Job number out of range")
            return
        
        if confirm_action(f"Delete this cron job?\n{cron_jobs[job_index]}"):
            # Remove job from list
            cron_jobs.pop(job_index)
            
            # Update crontab
            new_crontab = "\n".join(cron_jobs) + "\n" if cron_jobs else ""
            run_command(f'echo "{new_crontab}" | crontab -')
            MatrixUI.print_success("CRON JOB DELETED", "Cron job removed successfully")
        else:
            MatrixUI.print_warning("CANCELLED", "Deletion cancelled")
    
    except ValueError:
        MatrixUI.print_error("INVALID INPUT", "Please enter a valid number")
    except Exception as e:
        MatrixUI.print_error("DELETE FAILED", f"Failed to delete cron job: {e}")


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
