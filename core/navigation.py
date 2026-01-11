#!/usr/bin/env python3
"""
Directory navigation utilities for BackupBuddy.
"""

from pathlib import Path
from typing import Optional
from utils.commands import run_command
from utils.display import Colors


def navigate_remote_directories(remote_name: str) -> Optional[str]:
    """
    Navigate remote directories with improved error handling.
    
    Args:
        remote_name: Name of remote to navigate
    
    Returns:
        Selected path or None if user cancels
    """
    current_path = remote_name
    
    while True:
        print(f"\n{Colors.YELLOW}Current remote directory: {current_path}{Colors.RESET}")

        # List directories
        try:
            result = run_command(f"rclone lsd {current_path}", capture_output=True)
            remote_directories = [
                line.split()[-1] for line in result.stdout.strip().splitlines()
                if line.strip()
            ]
        except Exception as e:
            print(f"{Colors.RED}Error listing directories: {e}{Colors.RESET}")
            remote_directories = []

        # Show current location
        print(f"\n{Colors.YELLOW}You are currently in:{Colors.RESET} {current_path}")

        # Show directories
        if not remote_directories:
            print(f"{Colors.RED}No directories found in this location.{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}Remote Directories:{Colors.RESET}")
            for idx, directory in enumerate(remote_directories, start=1):
                print(f"{Colors.RED}{idx}. {directory}{Colors.RESET}")

        # Show options
        _print_navigation_options()

        choice = input("\nEnter your choice: ").strip()

        # Handle user choice
        result = _handle_remote_choice(choice, current_path, remote_name, remote_directories)
        
        if result == "RETURN":
            return current_path
        elif result == "CANCEL":
            return None
        elif result is not None:
            current_path = result


def _print_navigation_options() -> None:
    """Print navigation options."""
    print(f"\n{Colors.YELLOW}0.{Colors.RESET} Select this location")
    print(f"{Colors.YELLOW}b.{Colors.RESET} Go back")
    print(f"{Colors.YELLOW}c.{Colors.RESET} Enter a custom remote directory path")
    print(f"{Colors.YELLOW}d.{Colors.RESET} Create a new directory")
    print(f"{Colors.YELLOW}e.{Colors.RESET} Copy files to this location")


def _handle_remote_choice(
    choice: str,
    current_path: str,
    remote_name: str,
    directories: list
) -> Optional[str]:
    """
    Handle user choice for remote navigation.
    
    Returns:
        "RETURN" to return current_path
        "CANCEL" to abort
        new path to continue navigating
        None for invalid input
    """
    if choice == "0":
        print(f"{Colors.YELLOW}You have selected: {current_path}{Colors.RESET}")
        return "RETURN"
    
    elif choice.lower() == "b":
        if "/" in current_path:
            return "/".join(current_path.rstrip("/").split("/")[:-1])
        else:
            print("You are already at the root remote directory.")
            return current_path
    
    elif choice.lower() == "c":
        custom_path = input("Enter the custom remote directory path: ").strip()
        if custom_path.startswith(remote_name):
            return custom_path
        else:
            return f"{remote_name}/{custom_path}".rstrip("/")
    
    elif choice.lower() == "d":
        return _create_remote_directory(current_path)
    
    elif choice.lower() == "e":
        _copy_to_remote(current_path)
        return current_path
    
    else:
        return _navigate_to_directory(choice, current_path, directories)


def _create_remote_directory(current_path: str) -> str:
    """Create new directory on remote."""
    new_dir = input("Enter the name for the new directory: ").strip()
    if new_dir:
        try:
            new_dir_path = f"{current_path.rstrip('/')}/{new_dir}".lstrip("/")
            run_command(f"rclone mkdir {new_dir_path}")
            print(f"{Colors.GREEN}Directory '{new_dir}' created at {new_dir_path}.{Colors.RESET}")
            return new_dir_path
        except Exception as e:
            print(f"{Colors.RED}Error creating directory: {e}{Colors.RESET}")
    else:
        print(f"{Colors.RED}Directory name cannot be empty.{Colors.RESET}")
    
    return current_path


def _copy_to_remote(current_path: str) -> None:
    """Copy files to remote directory."""
    source_path = input("Enter the local path of the files to copy: ").strip()
    if source_path:
        try:
            print(f"{Colors.YELLOW}Copying files from {source_path} to {current_path}{Colors.RESET}")
            run_command(f"rclone copy {source_path} {current_path}")
            print(f"{Colors.GREEN}Files successfully copied to {current_path}.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error copying files: {e}{Colors.RESET}")
    else:
        print(f"{Colors.RED}Source path cannot be empty.{Colors.RESET}")


def _navigate_to_directory(choice: str, current_path: str, directories: list) -> Optional[str]:
    """Navigate to selected directory."""
    try:
        choice_int = int(choice)
        if 1 <= choice_int <= len(directories):
            selected_directory = directories[choice_int - 1]
            return f"{current_path.rstrip('/')}/{selected_directory}".rstrip("/")
        else:
            print(f"{Colors.RED}Invalid choice. Try again.{Colors.RESET}")
    except ValueError:
        print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.RESET}")
    
    return current_path


def navigate_local_directories() -> Optional[str]:
    """
    Let user navigate local directories.
    
    Returns:
        Selected path or None if user cancels
    """
    current_path = Path("/")
    
    while True:
        print(f"\n{Colors.YELLOW}Current local directory: {current_path}{Colors.RESET}")

        try:
            # List directories and files
            directories, files = _list_local_contents(current_path)

            # Build directory list with navigation options
            nav_dirs = _build_navigation_list(current_path, directories)

            # Display directories
            _display_directories(nav_dirs)

            # Display files (max 3)
            _display_files(files)

            # Show options
            _print_local_navigation_options()
            print(f"\n{Colors.YELLOW}Current directory: {current_path}{Colors.RESET}")

            choice = input("\nEnter your choice: ").strip()

            # Handle user choice
            result = _handle_local_choice(choice, current_path, nav_dirs)
            
            if result == "RETURN":
                return str(current_path)
            elif result == "CANCEL":
                return None
            elif result is not None:
                current_path = result
        
        except PermissionError:
            print(f"{Colors.RED}Permission denied for this directory.{Colors.RESET}")
            return None
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            return None


def _list_local_contents(path: Path) -> tuple:
    """List directories and files in a local path."""
    directories = [d.name for d in path.iterdir() if d.is_dir()]
    files = [f.name for f in path.iterdir() if f.is_file()]
    return directories, files


def _build_navigation_list(current_path: Path, directories: list) -> list:
    """Build list with navigation options."""
    nav_dirs = []
    
    # Add special directories
    if current_path != Path("/root"):
        nav_dirs.append("root")
    if current_path != Path("/"):
        nav_dirs.append("/")
    nav_dirs.append("..")
    
    # Add current directories
    nav_dirs.extend(directories)
    
    return nav_dirs


def _display_directories(directories: list) -> None:
    """Display directory list."""
    print(f"\n{Colors.RED}Directories:{Colors.RESET}")
    for idx, directory in enumerate(directories, start=1):
        print(f"{Colors.RED}{idx}. {directory}{Colors.RESET}")


def _display_files(files: list) -> None:
    """Display file list (max 3 files)."""
    print(f"\n{Colors.GREEN}Files:{Colors.RESET}")
    if files:
        displayed_files = files[:3]
        for file in displayed_files:
            print(f"{Colors.GREEN}{file}{Colors.RESET}")
        if len(files) > 3:
            print(f"{Colors.GREEN}[ ... ]{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}No files to display.{Colors.RESET}")


def _print_local_navigation_options() -> None:
    """Print local navigation options."""
    print(f"\n{Colors.YELLOW}0.{Colors.RESET} Select this location")
    print(f"{Colors.YELLOW}b.{Colors.RESET} Go back")
    print(f"{Colors.YELLOW}c.{Colors.RESET} Enter a custom local directory path")
    print(f"{Colors.YELLOW}d.{Colors.RESET} Create a new directory")


def _handle_local_choice(choice: str, current_path: Path, directories: list) -> Optional[Path]:
    """
    Handle user choice for local navigation.
    
    Returns:
        "RETURN" to return current_path
        "CANCEL" to abort
        new Path to continue navigating
        None for invalid input
    """
    if choice == "0":
        print(f"{Colors.YELLOW}You have selected: {current_path}{Colors.RESET}")
        return "RETURN"
    
    elif choice.lower() == "b":
        return "CANCEL"
    
    elif choice.lower() == "c":
        return _handle_custom_path()
    
    elif choice.lower() == "d":
        return _create_local_directory(current_path)
    
    else:
        return _navigate_to_local_directory(choice, current_path, directories)


def _handle_custom_path() -> Optional[Path]:
    """Handle custom path."""
    custom_path = input("Enter the custom local directory path: ").strip()
    custom_path_obj = Path(custom_path)
    if custom_path_obj.exists() and custom_path_obj.is_dir():
        return custom_path_obj
    else:
        print(f"{Colors.RED}Invalid path or directory does not exist.{Colors.RESET}")
        return None


def _create_local_directory(current_path: Path) -> Path:
    """Create new local directory."""
    new_dir = input("Enter the name for the new directory: ").strip()
    if new_dir:
        try:
            new_dir_path = current_path / new_dir
            new_dir_path.mkdir(parents=True, exist_ok=True)
            print(f"{Colors.GREEN}Directory '{new_dir}' created at {new_dir_path}.{Colors.RESET}")
            return new_dir_path
        except Exception as e:
            print(f"{Colors.RED}Error creating directory: {e}{Colors.RESET}")
    else:
        print(f"{Colors.RED}Directory name cannot be empty.{Colors.RESET}")
    
    return current_path


def _navigate_to_local_directory(choice: str, current_path: Path, directories: list) -> Optional[Path]:
    """Navigate to selected local directory."""
    try:
        choice_int = int(choice)
        if 1 <= choice_int <= len(directories):
            selected_directory = directories[choice_int - 1]
            
            if selected_directory == "..":
                return current_path.parent if current_path != Path("/") else current_path
            elif selected_directory == "/":
                return Path("/")
            elif selected_directory == "root":
                return Path("/root")
            else:
                selected_path = current_path / selected_directory
                if selected_path.exists() and selected_path.is_dir():
                    return selected_path
                else:
                    print(f"{Colors.RED}Directory does not exist or is invalid.{Colors.RESET}")
        else:
            print(f"{Colors.RED}Invalid choice. Try again.{Colors.RESET}")
    except ValueError:
        print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.RESET}")
    
    return current_path
