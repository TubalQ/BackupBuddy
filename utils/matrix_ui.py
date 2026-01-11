#!/usr/bin/env python3
"""
Matrix-inspired UI components for BackupBuddy.
"""

import time
import sys
from typing import List, Optional


class MatrixColors:
    """Matrix-inspired color scheme."""
    # Primary colors
    MATRIX_GREEN = '\033[38;2;0;255;65m'      # Bright neon green
    DEEP_GREEN = '\033[38;2;0;59;0m'          # Dark background green
    TERMINAL_BLACK = '\033[38;2;13;2;8m'      # Almost pure black
    GHOST_WHITE = '\033[38;2;0;255;65m'       # For highlights (50% opacity simulation)
    
    # Accent colors
    CYBER_BLUE = '\033[38;2;0;217;255m'       # Info/neutral
    WARNING_AMBER = '\033[38;2;255;176;0m'    # Warnings
    ALERT_RED = '\033[38;2;255;0;81m'         # Errors
    PURPLE_HAZE = '\033[38;2;176;38;255m'     # Special features
    
    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    CLEAR_LINE = '\033[K'
    
    # Background
    BG_BLACK = '\033[48;2;13;2;8m'


class MatrixUI:
    """Matrix-style UI components."""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        print('\033[2J\033[H', end='')
    
    @staticmethod
    def type_text(text: str, delay: float = 0.03):
        """Type text character by character (typer effect)."""
        for char in text:
            sys.stdout.write(MatrixColors.MATRIX_GREEN + char + MatrixColors.RESET)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def print_logo():
        """Print the BackupBuddy ASCII logo."""
        logo = f"""{MatrixColors.MATRIX_GREEN}{MatrixColors.BOLD}
     ██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗ 
     ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗
     ██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝
     ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝ 
     ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║     
     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                        
     ██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗       
     ██╔══██╗██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝       
     ██████╔╝██║   ██║██║  ██║██║  ██║ ╚████╔╝        
     ██╔══██╗██║   ██║██║  ██║██║  ██║  ╚██╔╝         
     ██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║          
     ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝          
{MatrixColors.RESET}
{MatrixColors.CYBER_BLUE}     [ SYSTEM INITIALIZED ] [ v2.0.0 ] [ READY ]{MatrixColors.RESET}
"""
        print(logo)
    
    @staticmethod
    def print_header(title: str, subtitle: str = ""):
        """Print a section header."""
        width = 70
        print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * width}╗{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}{title.center(width)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
        if subtitle:
            print(f"{MatrixColors.MATRIX_GREEN}╠{'═' * width}╣{MatrixColors.RESET}")
            print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.CYBER_BLUE}{subtitle.center(width)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * width}╝{MatrixColors.RESET}\n")
    
    @staticmethod
    def print_menu_section(title: str, items: List[tuple], width: int = 65):
        """
        Print a menu section.
        items: List of tuples (number, icon, text, description)
        """
        print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * width}┐{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ {title.upper()} {'▓' * (width - len(title) - 6)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * width}┤{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * width}│{MatrixColors.RESET}")
        
        for num, icon, text, desc in items:
            entry = f"  ┃ {num} ┃ {icon} {text}"
            spacing = width - len(entry) - len(desc) - 5
            print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}{entry}{MatrixColors.RESET}{' ' * spacing}{MatrixColors.DIM}▸ {desc}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
        
        print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * width}│{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * width}┘{MatrixColors.RESET}\n")
    
    @staticmethod
    def print_status_bar(message: str):
        """Print a status bar at the bottom."""
        width = 70
        print(f"    {MatrixColors.MATRIX_GREEN}┏{'━' * width}┓{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┃{MatrixColors.CYBER_BLUE}  ▸ {message}{' ' * (width - len(message) - 4)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}┃{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┗{'━' * width}┛{MatrixColors.RESET}")
    
    @staticmethod
    def print_success(title: str, message: str, stats: Optional[dict] = None):
        """Print a success message box."""
        width = 66
        print(f"\n{MatrixColors.MATRIX_GREEN}┏{'━' * width}┓{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}┃{MatrixColors.BOLD}  ✓ {title.upper()}{' ' * (width - len(title) - 4)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}┣{'━' * width}┫{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}┃{' ' * width}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}┃  {message}{' ' * (width - len(message) - 2)}┃{MatrixColors.RESET}")
        
        if stats:
            print(f"{MatrixColors.MATRIX_GREEN}┃{' ' * width}┃{MatrixColors.RESET}")
            print(f"{MatrixColors.MATRIX_GREEN}┃  {MatrixColors.BOLD}Stats:{MatrixColors.RESET}{' ' * (width - 8)}┃{MatrixColors.RESET}")
            for key, value in stats.items():
                line = f"  ├─ {key}: {value}"
                print(f"{MatrixColors.MATRIX_GREEN}┃  {line}{' ' * (width - len(line) - 2)}┃{MatrixColors.RESET}")
        
        print(f"{MatrixColors.MATRIX_GREEN}┃{' ' * width}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}┗{'━' * width}┛{MatrixColors.RESET}\n")
    
    @staticmethod
    def print_warning(title: str, message: str, actions: Optional[List[str]] = None):
        """Print a warning message box."""
        width = 66
        print(f"\n{MatrixColors.WARNING_AMBER}┏{'━' * width}┓{MatrixColors.RESET}")
        print(f"{MatrixColors.WARNING_AMBER}┃{MatrixColors.BOLD}  ⚠ {title.upper()}{' ' * (width - len(title) - 4)}{MatrixColors.RESET}{MatrixColors.WARNING_AMBER}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.WARNING_AMBER}┣{'━' * width}┫{MatrixColors.RESET}")
        print(f"{MatrixColors.WARNING_AMBER}┃{' ' * width}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.WARNING_AMBER}┃  {message}{' ' * (width - len(message) - 2)}┃{MatrixColors.RESET}")
        
        if actions:
            print(f"{MatrixColors.WARNING_AMBER}┃{' ' * width}┃{MatrixColors.RESET}")
            print(f"{MatrixColors.WARNING_AMBER}┃  {MatrixColors.BOLD}Recommended actions:{MatrixColors.RESET}{' ' * (width - 22)}┃{MatrixColors.RESET}")
            for action in actions:
                line = f"  ├─ {action}"
                print(f"{MatrixColors.WARNING_AMBER}┃  {line}{' ' * (width - len(line) - 2)}┃{MatrixColors.RESET}")
        
        print(f"{MatrixColors.WARNING_AMBER}┃{' ' * width}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.WARNING_AMBER}┗{'━' * width}┛{MatrixColors.RESET}\n")
    
    @staticmethod
    def print_error(title: str, message: str, error_code: str = "", actions: Optional[List[str]] = None, quick_fix: str = ""):
        """Print an error message box."""
        width = 66
        print(f"\n{MatrixColors.ALERT_RED}┏{'━' * width}┓{MatrixColors.RESET}")
        print(f"{MatrixColors.ALERT_RED}┃{MatrixColors.BOLD}  ✗ {title.upper()}{' ' * (width - len(title) - 4)}{MatrixColors.RESET}{MatrixColors.ALERT_RED}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.ALERT_RED}┣{'━' * width}┫{MatrixColors.RESET}")
        print(f"{MatrixColors.ALERT_RED}┃{' ' * width}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.ALERT_RED}┃  {message}{' ' * (width - len(message) - 2)}┃{MatrixColors.RESET}")
        
        if error_code:
            print(f"{MatrixColors.ALERT_RED}┃{' ' * width}┃{MatrixColors.RESET}")
            print(f"{MatrixColors.ALERT_RED}┃  Error Code: {error_code}{' ' * (width - len(error_code) - 14)}┃{MatrixColors.RESET}")
        
        if actions:
            print(f"{MatrixColors.ALERT_RED}┃{' ' * width}┃{MatrixColors.RESET}")
            print(f"{MatrixColors.ALERT_RED}┃  {MatrixColors.BOLD}Possible causes:{MatrixColors.RESET}{' ' * (width - 18)}┃{MatrixColors.RESET}")
            for action in actions:
                line = f"  ├─ {action}"
                print(f"{MatrixColors.ALERT_RED}┃  {line}{' ' * (width - len(line) - 2)}┃{MatrixColors.RESET}")
        
        if quick_fix:
            print(f"{MatrixColors.ALERT_RED}┃{' ' * width}┃{MatrixColors.RESET}")
            print(f"{MatrixColors.ALERT_RED}┃  {MatrixColors.BOLD}Quick fix:{MatrixColors.RESET}{' ' * (width - 13)}┃{MatrixColors.RESET}")
            print(f"{MatrixColors.ALERT_RED}┃  $ {quick_fix}{' ' * (width - len(quick_fix) - 4)}┃{MatrixColors.RESET}")
        
        print(f"{MatrixColors.ALERT_RED}┃{' ' * width}┃{MatrixColors.RESET}")
        print(f"{MatrixColors.ALERT_RED}┗{'━' * width}┛{MatrixColors.RESET}\n")
    
    @staticmethod
    def print_progress_bar(progress: int, total: int, label: str = "", width: int = 50):
        """Print a progress bar."""
        percentage = int((progress / total) * 100) if total > 0 else 0
        filled = int((progress / total) * width) if total > 0 else 0
        bar = '▓' * filled + '░' * (width - filled)
        
        print(f"\r{MatrixColors.MATRIX_GREEN}    [{bar}] {percentage}%{MatrixColors.RESET} {MatrixColors.CYBER_BLUE}| {label}{MatrixColors.RESET}", end='', flush=True)
    
    @staticmethod
    def spinner(message: str = "Processing"):
        """Return a spinner animation."""
        frames = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        for frame in frames:
            print(f"\r{MatrixColors.MATRIX_GREEN}{frame}{MatrixColors.RESET} {message}...", end='', flush=True)
            time.sleep(0.1)
    
    @staticmethod
    def print_file_tree(current_path: str, directories: List[tuple], files: List[tuple]):
        """
        Print file navigation tree.
        directories: List of tuples (name, item_count, size)
        files: List of tuples (name, type, size, date)
        """
        width = 65
        
        # Header
        print(f"\n{MatrixColors.MATRIX_GREEN}╔{'═' * 71}╗{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}║{MatrixColors.BOLD}  📍 LOCATION: {current_path}{' ' * (69 - len(current_path))}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╠{'═' * 71}╣{MatrixColors.RESET}")
        
        # Breadcrumb
        breadcrumb = " → ".join(current_path.split('/'))
        print(f"{MatrixColors.MATRIX_GREEN}║  Breadcrumb: {breadcrumb}{' ' * (68 - len(breadcrumb))}║{MatrixColors.RESET}")
        print(f"{MatrixColors.MATRIX_GREEN}╚{'═' * 71}╝{MatrixColors.RESET}\n")
        
        # Directories section
        if directories:
            print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * width}┐{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ DIRECTORIES {'▓' * (width - 17)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * width}┤{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * width}│{MatrixColors.RESET}")
            
            for idx, (name, items, size) in enumerate(directories[:10], 1):
                # Simple size bar (6 chars)
                size_mb = float(size.replace('GB', '000').replace('MB', '').replace('KB', '0.001'))
                bar_len = min(6, int(size_mb / 1000))
                size_bar = '▓' * bar_len + '░' * (6 - bar_len)
                
                line = f"  ┃ {idx} ┃ 📁 {name[:20]:<20} │ {items:>8} │ {size_bar} {size:>8}"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}{line}{' ' * (width - len(line))}│{MatrixColors.RESET}")
            
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * width}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * width}┘{MatrixColors.RESET}\n")
        
        # Files section
        if files:
            print(f"    {MatrixColors.MATRIX_GREEN}┌{'─' * width}┐{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.BOLD} ▓▓▓ FILES {'▓' * (width - 11)}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}├{'─' * width}┤{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * width}│{MatrixColors.RESET}")
            
            for name, ftype, size, date in files[:3]:
                line = f"  📄 {name[:25]:<25} │ {ftype:>4} │ {size:>7} │ {date}"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}{line}{' ' * (width - len(line))}│{MatrixColors.RESET}")
            
            if len(files) > 3:
                more = f"  ... and {len(files) - 3} more files"
                print(f"    {MatrixColors.MATRIX_GREEN}│{MatrixColors.DIM}{more}{' ' * (width - len(more))}{MatrixColors.RESET}{MatrixColors.MATRIX_GREEN}│{MatrixColors.RESET}")
            
            print(f"    {MatrixColors.MATRIX_GREEN}│{' ' * width}│{MatrixColors.RESET}")
            print(f"    {MatrixColors.MATRIX_GREEN}└{'─' * width}┘{MatrixColors.RESET}\n")
        
        # Command bar
        print(f"    {MatrixColors.MATRIX_GREEN}┏{'━' * width}┓{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┃{MatrixColors.CYBER_BLUE}  [0] Select  [..] Up  [c] Custom  [/] Search  [q] Cancel{' ' * 3}┃{MatrixColors.RESET}")
        print(f"    {MatrixColors.MATRIX_GREEN}┗{'━' * width}┛{MatrixColors.RESET}")
