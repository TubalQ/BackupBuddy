#!/usr/bin/env python3
"""
Directory navigation utilities for BackupBuddy.
Matrix UI implementation.
"""

from pathlib import Path
from typing import Optional, List, Tuple
from utils.commands import run_command
from utils.matrix_ui import MatrixUI, MatrixColors


def navigate_remote_directories(remote_name: str) -> Optional[str]:
    """
    Navigate remote directories with Matrix UI.
    
    Args:
        remote_name: Name of remote to navigate
    
    Returns:
        Selected path or None if user cancels
    """
    current_path = remote_name
    
    while True:
        MatrixUI.clear_screen()
        
        # List directories
        try:
            result = run_command(f"rclone lsd {current_path}", capture_output=True)
            remote_directories = [
                line.split()[-1] for line in result.stdout.strip().splitlines()
                if line.strip()
            ]
        except Exception as e:
            MatrixUI.print_error("LIST FAILED", f"Error listing directories: {e}")
            remote_directories = []

        # Show current location with Matrix UI
        breadcrumb = current_path.replace(":", " → ")
        print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 71}╗{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}  📍 REMOTE LOCATION: {current_path}{' ' * (70 - len(current_path) - 21)}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╠{'═' * 71}╣{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║  Breadcrumb: {breadcrumb}{' ' * (68 - len(breadcrumb))}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 71}╝{MatrixColors.RESET}\n")

        # Show directories
        if not remote_directories:
            print(f"    {MatrixColors.WARNING_AMBER}⚠{MatrixColors.RESET} {MatrixColors.DIM}No directories found in this location{MatrixColors.RESET}\n")
        else:
            print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * 65}┐{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ REMOTE DIRECTORIES {'▓' * 41}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * 65}┤{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
            
            for idx, directory in enumerate(remote_directories[:15], start=1):
                dir_display = f"  ┃ {idx:2d} ┃ 📁 {directory[:50]}"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}{dir_display}{' ' * (65 - len(dir_display))}│{MatrixColors.RESET}")
            
            if len(remote_directories) > 15:
                more = f"  ... and {len(remote_directories) - 15} more directories"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.DIM}{more}{' ' * (65 - len(more))}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * 65}┘{MatrixColors.RESET}\n")

        # Show options
        print(f"    {MatrixColors.MATRIX_GREEN}┏{'━' * 65}┓{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┃{MatrixColors.CYBER_BLUE}  [0] Select current  [..] Up  [m] Create dir  [q] Cancel{' ' * 6}┃{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┗{'━' * 65}┛{MatrixColors.RESET}")

        choice = input(f"\n{MatrixColors.CYBER_BLUE}    ▸ COMMAND: {MatrixColors.RESET}").strip()

        if choice.lower() == "q":
            return None
        elif choice == "0":
            return current_path
        elif choice == "..":
            if ":" in current_path and current_path.count("/") > 0:
                current_path = "/".join(current_path.rsplit("/", 1)[:-1]) or remote_name
        elif choice.lower() == "m":
            new_dir = input(f"{MatrixColors.MATRIX_GREEN}Enter new directory name: {MatrixColors.RESET}").strip()
            if new_dir:
                try:
                    run_command(f'rclone mkdir "{current_path}/{new_dir}"')
                    print(f"{MatrixColors.MATRIX_GREEN}✓{MatrixColors.RESET} Directory created\n")
                    input("Press Enter to continue...")
                except Exception as e:
                    MatrixUI.print_error("CREATE FAILED", f"Failed to create directory: {e}")
                    input("\nPress Enter to continue...")
        else:
            try:
                idx = int(choice)
                if 1 <= idx <= len(remote_directories):
                    current_path = f"{current_path}/{remote_directories[idx - 1]}"
                else:
                    MatrixUI.print_error("INVALID CHOICE", "Directory number out of range")
                    input("\nPress Enter to continue...")
            except ValueError:
                MatrixUI.print_error("INVALID INPUT", "Please enter a valid number")
                input("\nPress Enter to continue...")


def navigate_local_directories() -> Optional[str]:
    """
    Navigate local directories with Matrix UI.
    
    Returns:
        Selected path or None if user cancels
    """
    current_path = Path.home()
    
    while True:
        MatrixUI.clear_screen()
        
        # Get directories and files
        try:
            directories = sorted([d for d in current_path.iterdir() if d.is_dir()])
            files = sorted([f for f in current_path.iterdir() if f.is_file()])
        except PermissionError:
            MatrixUI.print_error("PERMISSION DENIED", f"Cannot access {current_path}")
            directories, files = [], []
            input("\nPress Enter to continue...")
            current_path = current_path.parent
            continue

        # Show current location with Matrix UI
        breadcrumb = " → ".join(current_path.parts[-4:]) if len(current_path.parts) > 4 else str(current_path)
        
        print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 71}╗{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}  📍 LOCAL LOCATION: {str(current_path)[:48]}{' ' * (70 - min(len(str(current_path)), 48) - 20)}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╠{'═' * 71}╣{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║  Breadcrumb: ...{breadcrumb[-55:]}{' ' * (68 - min(len(breadcrumb), 55) - 3)}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 71}╝{MatrixColors.RESET}\n")

        # Show directories
        if directories:
            print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * 65}┐{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ DIRECTORIES {'▓' * 47}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * 65}┤{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
            
            for idx, directory in enumerate(directories[:15], start=1):
                try:
                    size = sum(f.stat().st_size for f in directory.rglob('*') if f.is_file())
                    size_str = _format_size(size)
                    item_count = len(list(directory.iterdir()))
                except:
                    size_str = "?"
                    item_count = "?"
                
                dir_display = f"  ┃ {idx:2d} ┃ 📁 {directory.name[:30]:<30} │ {str(item_count):>4} items"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}{dir_display}{' ' * (65 - len(dir_display))}│{MatrixColors.RESET}")
            
            if len(directories) > 15:
                more = f"  ... and {len(directories) - 15} more directories"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.DIM}{more}{' ' * (65 - len(more))}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * 65}┘{MatrixColors.RESET}\n")

        # Show files (limited)
        if files:
            print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * 65}┐{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ FILES {'▓' * 54}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * 65}┤{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
            
            for f in files[:3]:
                size_str = _format_size(f.stat().st_size)
                file_display = f"  📄 {f.name[:35]:<35} │ {size_str:>8}"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.DIM}{file_display}{' ' * (65 - len(file_display))}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            
            if len(files) > 3:
                more = f"  ... and {len(files) - 3} more files"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.DIM}{more}{' ' * (65 - len(more))}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * 65}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * 65}┘{MatrixColors.RESET}\n")

        # Show options
        print(f"    {MatrixColors.MATRIX_GREEN}┏{'━' * 65}┓{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┃{MatrixColors.CYBER_BLUE}  [0] Select current  [..] Up  [c] Custom  [q] Cancel{' ' * 9}┃{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┗{'━' * 65}┛{MatrixColors.RESET}")

        choice = input(f"\n{MatrixColors.CYBER_BLUE}    ▸ COMMAND: {MatrixColors.RESET}").strip()

        if choice.lower() == "q":
            return None
        elif choice == "0":
            return str(current_path)
        elif choice == "..":
            if current_path.parent != current_path:
                current_path = current_path.parent
        elif choice.lower() == "c":
            custom_path = input(f"{MatrixColors.MATRIX_GREEN}Enter custom path: {MatrixColors.RESET}").strip()
            if custom_path:
                try:
                    new_path = Path(custom_path).expanduser().resolve()
                    if new_path.exists() and new_path.is_dir():
                        current_path = new_path
                    else:
                        MatrixUI.print_error("INVALID PATH", "Path does not exist or is not a directory")
                        input("\nPress Enter to continue...")
                except Exception as e:
                    MatrixUI.print_error("PATH ERROR", f"Invalid path: {e}")
                    input("\nPress Enter to continue...")
        else:
            try:
                idx = int(choice)
                if 1 <= idx <= len(directories):
                    current_path = directories[idx - 1]
                else:
                    MatrixUI.print_error("INVALID CHOICE", "Directory number out of range")
                    input("\nPress Enter to continue...")
            except ValueError:
                MatrixUI.print_error("INVALID INPUT", "Please enter a valid number")
                input("\nPress Enter to continue...")


def _format_size(size: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"
