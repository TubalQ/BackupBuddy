#!/usr/bin/env python3
"""
Restore job management for BackupBuddy.
"""

from scripts.generator import generate_restore_script
from utils.commands import run_script
from utils.display import Colors


def restore_backup_job(config: dict) -> None:
    """
    Guide user through restoring a backup job.
    """
    if not config:
        print("No backup jobs are configured. Create a backup job first.")
        return

    while True:
        print("\nAvailable backup jobs: (Enter 'b' to go back)")
        job_list = list(config.keys())
        
        for i, job_id in enumerate(job_list, start=1):
            print(f"{i}. {job_id}")
        
        selected_job = input("Select a job to restore from: ").strip()
        
        if selected_job.lower() == "b":
            return

        try:
            selected_index = int(selected_job) - 1
            if selected_index < 0 or selected_index >= len(job_list):
                print(f"{Colors.RED}Invalid choice. Try again.{Colors.RESET}")
                continue
            
            job_id = job_list[selected_index]
            job_data = config[job_id]
            
            # Display job information
            _display_job_info(job_id, job_data)
            
            # Generate and run restore script
            script_path = generate_restore_script(config, job_id)
            print(f"{Colors.GREEN}Restore script generated: {script_path}{Colors.RESET}")
            
            if run_script(str(script_path)):
                print(f"{Colors.GREEN}Restore completed successfully.{Colors.RESET}")
            else:
                print(f"{Colors.RED}Restore failed.{Colors.RESET}")
            
            return
        
        except ValueError:
            print(f"{Colors.RED}Invalid input. Enter a number.{Colors.RESET}")


def _display_job_info(job_id: str, job_data: dict) -> None:
    """Display information about a job."""
    print(f"\nRestoring job '{job_id}':")
    print(f"- Source directory: {job_data.get('source_dir', 'N/A')}")
    print(f"- Destination: {job_data.get('destination', 'N/A')}")
    print(f"- Encrypted: {job_data.get('encrypt', False)}")
    print(f"- Compressed: {job_data.get('compress', False)}")
    print(f"- Split files: {job_data.get('split_files', False)}")
    
    if job_data.get("encrypt"):
        print("\nNote: This job is encrypted. You will need to provide the decryption password during restore.")
