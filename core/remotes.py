#!/usr/bin/env python3
"""
Rclone remote management for BackupBuddy.
"""

from typing import List, Optional
from utils.commands import run_command
from utils.display import Colors
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
    """Select a remote from list or configure a new one."""
    while True:
        remotes = list_remotes()
        
        if not remotes:
            print(f"{Colors.YELLOW}No remotes found. You need to configure one.{Colors.RESET}")
            if confirm_action("Would you like to create a new remote?"):
                print("\nStarting rclone configuration...")
                run_command("rclone config", check=False)
                continue
            return None

        print(f"\n{Colors.GREEN}Available remotes:{Colors.RESET}")
        for i, remote in enumerate(remotes, start=1):
            print(f"{i}. {remote}")
        print("0. Create a new remote")

        choice = input("Enter the number of the remote to use (or 'b' to go back): ").strip()

        if choice.lower() == "b":
            return None
        elif choice == "0":
            print("\nStarting rclone configuration to create a new remote...")
            run_command("rclone config", check=False)
            continue
        
        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(remotes):
                return remotes[choice_int - 1]
            print(f"{Colors.RED}Invalid choice. Try again.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.RESET}")


def manage_remotes() -> None:
    """Manage remotes and local shortcuts."""
    print("\nManage Remotes and Local Paths")
    print("1. Add a new remote")
    print("2. View existing remotes")
    print("3. Back to main menu")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        print("\nAdding a new remote...")
        try:
            run_command("rclone config", check=False)
            print(f"{Colors.GREEN}Remote configuration completed.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error adding remote: {e}{Colors.RESET}")
    
    elif choice == "2":
        print("\nExisting remotes:")
        remotes = list_remotes()
        if remotes:
            for remote in remotes:
                print(f"- {remote}")
        else:
            print("No remotes configured yet.")
    
    elif choice == "3":
        print("Returning to main menu.")
    
    else:
        print("Invalid choice. Returning to main menu.")
