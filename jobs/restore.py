#!/usr/bin/env python3
"""
Restore job management for BackupBuddy.
Matrix UI implementation.
"""

from scripts.generator import generate_restore_script
from utils.commands import run_script
from utils.matrix_ui import MatrixUI, MatrixColors


def restore_backup_job(config: dict) -> None:
    """
    Guide user through restoring a backup job with Matrix UI.
    """
    if not config:
        MatrixUI.print_warning("NO JOBS FOUND", "No backup jobs configured. Create a backup job first.")
        input("\nPress Enter to continue...")
        return

    while True:
        MatrixUI.clear_screen()
        MatrixUI.print_header("RESTORE FROM BACKUP", "Select a job to restore")
        
        job_list = list(config.keys())
        
        print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'AVAILABLE BACKUP JOBS'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
        
        for i, job_id in enumerate(job_list, start=1):
            job_data = config[job_id]
            source = job_data.get('source_dir', 'N/A')
            dest = job_data.get('destination', 'N/A')
            
            print(f"{MatrixColors.MATRIX_GREEN}{i}.{MatrixColors.RESET} {MatrixColors.BOLD}{job_id}{MatrixColors.RESET}")
            print(f"   {MatrixColors.DIM}Source: {source}{MatrixColors.RESET}")
            print(f"   {MatrixColors.DIM}Backup location: {dest}{MatrixColors.RESET}\n")
        
        print(f"{MatrixColors.YELLOW}Enter 'b' to go back{MatrixColors.RESET}\n")
        
        selected_job = input(f"{MatrixColors.CYBER_BLUE}Select a job to restore from: {MatrixColors.RESET}").strip()
        
        if selected_job.lower() == "b":
            return

        try:
            selected_index = int(selected_job) - 1
            if selected_index < 0 or selected_index >= len(job_list):
                MatrixUI.print_error("INVALID CHOICE", "Job number out of range")
                input("\nPress Enter to continue...")
                continue
            
            job_id = job_list[selected_index]
            job_data = config[job_id]
            
            # Display job information
            MatrixUI.clear_screen()
            _display_job_info(job_id, job_data)
            
            confirm = input(f"\n{MatrixColors.CYBER_BLUE}Proceed with restore? (yes/no): {MatrixColors.RESET}").strip().lower()
            
            if confirm != "yes":
                MatrixUI.print_warning("CANCELLED", "Restore operation cancelled")
                input("\nPress Enter to continue...")
                continue
            
            # Generate and run restore script
            MatrixUI.clear_screen()
            print(f"\n{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Generating restore script...\n")
            
            script_path = generate_restore_script(config, job_id)
            
            print(f"{MatrixColors.MATRIX_GREEN}✓{MatrixColors.RESET} Restore script generated: {script_path}\n")
            print(f"{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Running restore job '{job_id}'...\n")
            
            if run_script(str(script_path)):
                MatrixUI.print_success(
                    "RESTORE COMPLETED",
                    f"Job '{job_id}' restored successfully",
                    stats={
                        "Job ID": job_id,
                        "Source": job_data.get('source_dir', 'N/A'),
                        "Backup location": job_data.get('destination', 'N/A')
                    }
                )
            else:
                MatrixUI.print_error(
                    "RESTORE FAILED",
                    f"Job '{job_id}' encountered an error during restore",
                    actions=[
                        "Check if backup exists at destination",
                        "Verify remote connection",
                        "Check log file for details"
                    ]
                )
            
            input("\nPress Enter to continue...")
            return
        
        except ValueError:
            MatrixUI.print_error("INVALID INPUT", "Please enter a valid job number")
            input("\nPress Enter to continue...")


def _display_job_info(job_id: str, job_data: dict) -> None:
    """Display information about a job with Matrix UI."""
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 66}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'RESTORE JOB DETAILS'.center(66)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 66}╝{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.BOLD}Job ID:{MatrixColors.RESET} {job_id}")
    print(f"{MatrixColors.BOLD}Source directory:{MatrixColors.RESET} {job_data.get('source_dir', 'N/A')}")
    print(f"{MatrixColors.BOLD}Backup location:{MatrixColors.RESET} {job_data.get('destination', 'N/A')}")
    print(f"{MatrixColors.BOLD}Encrypted:{MatrixColors.RESET} {job_data.get('encrypt', False)}")
    print(f"{MatrixColors.BOLD}Compressed:{MatrixColors.RESET} {job_data.get('compress', False)}")
    print(f"{MatrixColors.BOLD}Split files:{MatrixColors.RESET} {job_data.get('split_files', False)}")
    
    if job_data.get("encrypt"):
        print(f"\n{MatrixColors.WARNING_AMBER}⚠ Note:{MatrixColors.RESET} This job is encrypted.")
        print(f"{MatrixColors.DIM}You will need to provide the decryption password during restore.{MatrixColors.RESET}")
