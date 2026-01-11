#!/usr/bin/env python3
"""
Subprocess command utilities for BackupBuddy.
"""

import os
import subprocess
from typing import Optional
from utils.display import Colors


def run_command(
    command: str,
    check: bool = True,
    capture_output: bool = False,
    shell: bool = True
) -> subprocess.CompletedProcess:
    """
    Run a command with or without sudo depending on if script runs as root.
    
    Args:
        command: Command to run
        check: If True, raise exception on error
        capture_output: If True, capture stdout/stderr
        shell: If True, run command in shell
    
    Returns:
        subprocess.CompletedProcess object
    """
    if os.geteuid() != 0 and not command.startswith("sudo"):
        command = f"sudo {command}"
    
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print(f"{Colors.RED}Error executing command: {command}{Colors.RESET}")
            if e.stderr:
                print(f"{Colors.RED}{e.stderr}{Colors.RESET}")
            raise
        return e


def run_script(script_path: str) -> bool:
    """
    Run a bash script and return True if successful.
    
    Args:
        script_path: Path to the script
    
    Returns:
        True if script executed without error, otherwise False
    """
    try:
        run_command(f"bash {script_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Script execution failed: {e}{Colors.RESET}")
        return False
