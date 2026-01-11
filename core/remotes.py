#!/usr/bin/env python3
"""
Rclone remote management for BackupBuddy.
Matrix UI implementation.
"""

from typing import List, Optional
from utils.commands import run_command
from utils.matrix_ui import MatrixUI, MatrixColors
from utils.validation import confirm_action


def list_remotes() -> List[str]:
    """List configured rclone remotes."""
    try:
        result = run_command("rclone listremotes", capture_output=True)
        remotes = result.stdout.strip().splitlines()
        return [r for r in remotes if r]
    except Exception:
        return []


def select_remote() -> Optional[str]:
    """Select a remote from list or configure a new one with Matrix UI."""
    while True:
        remotes = list_remotes()
        
        if not remotes:
            MatrixUI.print_warning(
                "NO REMOTES FOUND",
                "You need to configure a remote before continuing",
                actions=["Create a new remote via rclone config"]
            )
            if confirm_action("Would you like to create a new remote now?"):
                print(f"\n{MatrixColors.CYBER_BLUE}Starting rclone configuration...{MatrixColors.RESET}\n")
                run_command("rclone config", check=False)
                continue
            return None

        print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 50}╗{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'AVAILABLE REMOTES'.center(50)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 50}╝{MatrixColors.RESET}\n")
        
        for i, remote in enumerate(remotes, start=1):
            print(f"{MatrixColors.MATRIX_GREEN}{i}.{MatrixColors.RESET} {MatrixColors.CYBER_BLUE}{remote}{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}0.{MatrixColors.RESET} Create a new remote\n")

        choice = input(f"{MatrixColors.CYBER_BLUE}Enter the number of the remote to use (or 'b' to go back): {MatrixColors.RESET}").strip()

        if choice.lower() == "b":
            return None
        elif choice == "0":
            print(f"\n{MatrixColors.CYBER_BLUE}Starting rclone configuration to create a new remote...{MatrixColors.RESET}\n")
            run_command("rclone config", check=False)
            continue
        
        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(remotes):
                return remotes[choice_int - 1]
            MatrixUI.print_error("INVALID CHOICE", "Remote number out of range")
        except ValueError:
            MatrixUI.print_error("INVALID INPUT", "Please enter a valid number")


def manage_remotes() -> None:
    """Manage remotes and local shortcuts with Matrix UI."""
    MatrixUI.clear_screen()
    MatrixUI.print_header("MANAGE REMOTES", "Configure rclone cloud storage connections")
    
    print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 50}╗{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'REMOTE MANAGEMENT OPTIONS'.center(50)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
    print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 50}╝{MatrixColors.RESET}\n")
    
    print(f"{MatrixColors.MATRIX_GREEN}1.{MatrixColors.RESET} Add a new remote")
    print(f"{MatrixColors.MATRIX_GREEN}2.{MatrixColors.RESET} View existing remotes")
    print(f"{MatrixColors.MATRIX_GREEN}3.{MatrixColors.RESET} Back to main menu\n")

    choice = input(f"{MatrixColors.CYBER_BLUE}Enter your choice (1-3): {MatrixColors.RESET}").strip()

    if choice == "1":
        MatrixUI.clear_screen()
        print(f"\n{MatrixColors.CYBER_BLUE}Adding a new remote...{MatrixColors.RESET}\n")
        try:
            run_command("rclone config", check=False)
            MatrixUI.print_success("REMOTE CONFIGURED", "Remote configuration completed")
        except Exception as e:
            MatrixUI.print_error("CONFIG FAILED", f"Error adding remote: {e}")
    
    elif choice == "2":
        MatrixUI.clear_screen()
        MatrixUI.print_header("CONFIGURED REMOTES", "Available cloud storage connections")
        
        remotes = list_remotes()
        if remotes:
            print(f"{MatrixColors.MATRIX_GREEN}╔{'═' * 50}╗{MatrixColors.RESET}")
            print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{'REMOTE LIST'.center(50)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
            print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 50}╝{MatrixColors.RESET}\n")
            
            for i, remote in enumerate(remotes, start=1):
                print(f"{MatrixColors.MATRIX_GREEN}{i}.{MatrixColors.RESET} {MatrixColors.CYBER_BLUE}{remote}{MatrixColors.RESET}")
            print()
        else:
            MatrixUI.print_warning("NO REMOTES", "No remotes configured yet")
    
    elif choice == "3":
        return
    
    else:
        MatrixUI.print_error("INVALID CHOICE", "Please enter a number between 1-3")
