#!/usr/bin/env python3
"""
Display utilities and color handling for BackupBuddy.
"""


class Colors:
    """ANSI color codes for terminal output."""
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    RESET = '\033[0m'


def display_logo() -> None:
    """Display ASCII logo and welcome message."""
    ascii_logo = rf"""
     {Colors.RED} _________________
    | | ____My_____ |o|
    | | ____Old____ | |
    | | _Pictures__ | |
    | | _____&_____ | |
    | |____Taxes____| |
    |     _______     |
    |    |       |   ||
    | DD |       |   V|
    |____|_______|____|{Colors.RESET}
    """
    
    print(f"{Colors.GREEN}{'.' * 57}{Colors.RESET}")
    print(f"{Colors.YELLOW}psst, look here:{Colors.RESET}")
    print(f"Have you considered trying out Parrot OS Sec/Home or HTB edition?")
    print(f"Find them here: {Colors.RED}https://www.parrotsec.org{Colors.RESET}\n")
    print(f"\n{Colors.GREEN}{'=' * 47}\n{Colors.RESET}")
    print(f"{Colors.GREEN}Welcome to BackupBuddy!                      ||{Colors.RESET}")
    print(f"{Colors.GREEN}Let's back up your files and keep them safe. ||{Colors.RESET}")
    print(f"{Colors.GREEN}{'=' * 47}\n{Colors.RESET}")
    print(ascii_logo)
    print(f"For help: {Colors.GREEN}https://github.com/TubalQ/BackupBuddy{Colors.RESET}")
    print(f"Good Luck & check option 9 for help // Best regards T-Q {Colors.GREEN}https://t-vault.se{Colors.RESET}")


def show_help() -> None:
    """Display help information."""
    print("\n" + "=" * 40)
    print("Welcome to the BackupBuddy Help Section!")
    print("=" * 40 + "\n")
    
    print("BackupBuddy is a powerful tool for backing up, restoring, and transferring files")
    print("between local and cloud-based systems.")
    print("It supports task scheduling using cron jobs and provides flexible settings")
    print("to minimize API requests to cloud providers.\n")
    print("BackupBuddy's default flags are set to minimize problems with providers such as Proton and Google\n")
    
    print("Key Features:")
    print("1. Create Backups: Back up local files or folders to cloud storage")
    print("2. Restore Backups: Restore files from a backup to your desired destination")
    print("3. Schedule Tasks: Set up cron jobs to automate backups and transfers")
    print("4. Configure rclone Remotes: Manage cloud storage accounts and connections")
    print("5. Optimize API Requests: Customize rclone flags to avoid exceeding API limits\n")
    
    print("Example Customizable rclone Flags:")
    print("  --tpslimit <number>: Limits API requests per second (default: 2)")
    print("  --tpslimit-burst <number>: Short burst above limit (default: 1)")
    print("  --transfers <number>: Concurrent file transfers (default: 2)")
    print("  --checkers <number>: File integrity checkers (default: 1)")
    print("  --low-level-retries <number>: Low-level error retries (default: 3)")
    print("  --retries <number>: Operation retries (default: 5)")
    print("  --log-level <level>: Logging verbosity (default: INFO)\n")
    
    print("Tips:")
    print("1. Use reasonable flag values to avoid hitting API limits")
    print("2. Review log files to troubleshoot issues or monitor operations")
    print("3. Use 'Manage Configurations' to update or clean up tasks\n")
    
    print("For more information, visit the rclone documentation!")


def print_section_header(title: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.GREEN}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.GREEN}{title.center(50)}{Colors.RESET}")
    print(f"{Colors.GREEN}{'=' * 50}{Colors.RESET}\n")
