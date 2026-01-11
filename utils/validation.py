#!/usr/bin/env python3
"""
Input validation utilities for BackupBuddy.
"""

from typing import List, Optional
from utils.display import Colors


def get_user_choice(
    prompt: str,
    valid_choices: List[str],
    allow_back: bool = True
) -> Optional[str]:
    """
    Get user input with validation.
    
    Args:
        prompt: Message to display to user
        valid_choices: List of valid choices
        allow_back: If True, allow 'b' to go back
    
    Returns:
        User's choice or None if user chose to go back
    """
    valid = [str(c).lower() for c in valid_choices]
    if allow_back:
        valid.append('b')
        prompt += " (or 'b' to go back)"
    
    while True:
        choice = input(f"{prompt}: ").strip().lower()
        if choice in valid:
            return None if choice == 'b' else choice
        print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")


def get_int_input(
    prompt: str,
    default: Optional[int] = None,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None
) -> int:
    """
    Get integer input from user with validation.
    
    Args:
        prompt: Message to display
        default: Default value if user presses Enter
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        Validated integer
    """
    while True:
        user_input = input(f"{prompt}: ").strip()
        
        if not user_input and default is not None:
            return default
        
        try:
            value = int(user_input)
            
            if min_val is not None and value < min_val:
                print(f"{Colors.RED}Value must be at least {min_val}.{Colors.RESET}")
                continue
            
            if max_val is not None and value > max_val:
                print(f"{Colors.RED}Value must be at most {max_val}.{Colors.RESET}")
                continue
            
            return value
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.RESET}")


def get_yes_no(prompt: str, default: bool = False) -> bool:
    """
    Get yes/no answer from user.
    
    Args:
        prompt: Question to ask
        default: Default answer if user presses Enter
    
    Returns:
        True for yes, False for no
    """
    default_str = "yes" if default else "no"
    response = input(f"{prompt} (yes/no, default: {default_str}): ").strip().lower()
    
    if not response:
        return default
    
    return response in ['yes', 'y']


def confirm_action(message: str) -> bool:
    """
    Request confirmation from user.
    
    Args:
        message: Confirmation message
    
    Returns:
        True if user confirms, otherwise False
    """
    return get_yes_no(message, default=False)


def validate_flag_value(flag: str, value: str) -> Optional[int]:
    """
    Validate values for rclone flags.
    
    Args:
        flag: Flag name
        value: Value to validate
    
    Returns:
        Validated value or None on error
    """
    numeric_flags = [
        "--tpslimit", "--tpslimit-burst", "--transfers",
        "--checkers", "--low-level-retries", "--retries"
    ]
    
    if flag in numeric_flags:
        try:
            int_value = int(value)
            if int_value < 1:
                raise ValueError(f"{flag} must be greater than 0.")
            return int_value
        except ValueError as e:
            print(f"{Colors.RED}Invalid value for {flag}: {e}{Colors.RESET}")
            return None
    
    return value
