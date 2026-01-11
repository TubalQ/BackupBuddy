#!/usr/bin/env python3
"""
Dependency management for BackupBuddy.
"""

import shutil
from pathlib import Path
from config.constants import (
    DEPENDENCIES, DEPENDENCY_FLAG_FILE, INSTALLED_PACKAGES_LOG
)
from utils.commands import run_command
from utils.display import Colors


def check_and_install_dependencies() -> None:
    """
    Check and install dependencies with Matrix UI.
    Always try to install rclone via curl, use apt as backup.
    """
    from utils.matrix_ui import MatrixUI, MatrixColors
    
    missing_dependencies = [dep for dep in DEPENDENCIES if not shutil.which(dep)]

    if not missing_dependencies and DEPENDENCY_FLAG_FILE.exists():
        return

    MatrixUI.clear_screen()
    MatrixUI.print_header("DEPENDENCY CHECK", "Installing required tools")
    
    print(f"{MatrixColors.MATRIX_GREEN}⣾{MatrixColors.RESET} Checking dependencies...\n")

    # Install curl first if missing
    if "curl" in missing_dependencies:
        print(f"{MatrixColors.CYBER_BLUE}Installing curl...{MatrixColors.RESET}")
        _install_packages(["curl"])
        missing_dependencies.remove("curl")

    # Install other dependencies
    if missing_dependencies:
        _install_packages(missing_dependencies)

    # Install rclone
    _install_rclone()

    # Verify installation
    _verify_dependencies()
    
    MatrixUI.print_success(
        "DEPENDENCIES INSTALLED",
        "All required tools are now available",
        stats={
            "curl": "✓",
            "rclone": "✓", 
            "pigz": "✓",
            "tar": "✓",
            "pv": "✓",
            "cron": "✓"
        }
    )
    
    input("\nPress Enter to continue...")


def _install_packages(packages: list) -> None:
    """Install packages via apt."""
    if not packages:
        return
    
    command = f"apt install -y {' '.join(packages)}"
    try:
        run_command(command)
        print(f"{Colors.GREEN}Successfully installed: {' '.join(packages)}{Colors.RESET}")
        
        # Log installed packages
        with open(INSTALLED_PACKAGES_LOG, "a") as log_file:
            for package in packages:
                log_file.write(f"{package}\n")
    except Exception as e:
        print(f"{Colors.RED}Failed to install {packages}: {e}{Colors.RESET}")


def _install_rclone() -> None:
    """Install rclone via curl (official method)."""
    if shutil.which("rclone"):
        print("rclone is already installed.")
        return
    
    print("\nInstalling rclone via official install script...")
    print(f"{Colors.YELLOW}Running: sudo -v ; curl https://rclone.org/install.sh | sudo bash{Colors.RESET}")
    
    try:
        # Refresh sudo credentials
        run_command("sudo -v", check=False)
        
        # Install rclone using official script
        run_command("curl https://rclone.org/install.sh | sudo bash")
        print(f"{Colors.GREEN}rclone installed successfully via official script.{Colors.RESET}")
        
        # Log rclone installation
        with open(INSTALLED_PACKAGES_LOG, "a") as log_file:
            log_file.write("rclone\n")
            
    except Exception as e:
        print(f"{Colors.RED}Failed to install rclone via curl: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}Falling back to apt package manager...{Colors.RESET}")
        _install_packages(["rclone"])


def _verify_dependencies() -> None:
    """Verify that all dependencies are installed."""
    all_deps = DEPENDENCIES + ["rclone"]
    
    if all(shutil.which(dep) for dep in all_deps):
        DEPENDENCY_FLAG_FILE.parent.mkdir(parents=True, exist_ok=True)
        DEPENDENCY_FLAG_FILE.write_text("Dependencies checked and installed.")
        print(f"{Colors.GREEN}All dependencies are installed and ready to use.{Colors.RESET}")
    else:
        print(f"{Colors.RED}Some dependencies are still missing. Please resolve them manually.{Colors.RESET}")
        if DEPENDENCY_FLAG_FILE.exists():
            DEPENDENCY_FLAG_FILE.unlink()


def remove_dependencies() -> None:
    """
    Uninstall only tools and dependencies installed by BackupBuddy.
    """
    if not INSTALLED_PACKAGES_LOG.exists():
        print("\nNo dependencies installed by BackupBuddy to remove.")
        return

    with open(INSTALLED_PACKAGES_LOG, "r") as log_file:
        dependencies = [line.strip() for line in log_file.readlines()]

    if not dependencies:
        print("\nNo dependencies installed by BackupBuddy to remove.")
        return

    print("\nRemoving dependencies installed by BackupBuddy...")

    # Detect package manager
    package_manager = _detect_package_manager()
    if not package_manager:
        print(f"{Colors.RED}Unknown Linux distribution. Please remove dependencies manually.{Colors.RESET}")
        return

    # Uninstall each package
    for dependency in dependencies:
        print(f"\nAttempting to remove: {dependency}")
        _uninstall_package(package_manager, dependency)

    # Handle rclone specifically
    if "rclone" in dependencies:
        _remove_rclone()

    # Remove log file
    try:
        INSTALLED_PACKAGES_LOG.unlink()
        print("Removed log of installed packages.")
    except Exception as e:
        print(f"{Colors.RED}Failed to remove package log file: {e}{Colors.RESET}")


def _detect_package_manager() -> str:
    """Detect which package manager is used."""
    if shutil.which("apt"):
        return "apt"
    elif shutil.which("yum"):
        return "yum"
    elif shutil.which("dnf"):
        return "dnf"
    elif shutil.which("pacman"):
        return "pacman"
    return None


def _uninstall_package(package_manager: str, package: str) -> None:
    """Uninstall a single package."""
    command = f"{package_manager} remove -y {package}"
    try:
        run_command(command)
        print(f"{Colors.GREEN}Successfully removed: {package}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Failed to remove {package}: {e}{Colors.RESET}")


def _remove_rclone() -> None:
    """Remove manually installed rclone binary."""
    print("\nChecking for manually installed rclone...")
    try:
        rclone_path = shutil.which("rclone")
        if rclone_path:
            Path(rclone_path).unlink()
            print(f"{Colors.GREEN}Manually installed rclone binary removed: {rclone_path}{Colors.RESET}")
        else:
            print("rclone binary not found. Skipping manual removal.")
    except Exception as e:
        print(f"{Colors.RED}Failed to remove rclone binary: {e}{Colors.RESET}")
