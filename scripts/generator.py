#!/usr/bin/env python3
"""
Script generation for BackupBuddy.
"""

from pathlib import Path
from typing import Dict
from config.constants import SCRIPT_DIR, TEMP_DIR


def generate_backup_script(config: Dict, job_id: str) -> Path:
    """
    Generate a backup script for specified job.
    
    Args:
        config: Configuration dictionary
        job_id: Job ID
    
    Returns:
        Path to generated script
    """
    job = config[job_id]
    script_path = SCRIPT_DIR / f"backup_{job_id}.sh"
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    rclone_flags = _build_rclone_flags(job.get("rclone_flags", {}))
    use_progress = "--progress" in rclone_flags
    log_file = job.get("rclone_flags", {}).get("--log-file")

    script_lines = _build_backup_script_lines(job, rclone_flags, use_progress, log_file)
    
    # Write script to file
    script_path.write_text("\n".join(script_lines))
    script_path.chmod(0o755)
    
    return script_path


def _build_rclone_flags(flags: Dict) -> str:
    """Build rclone flags from dictionary."""
    return " ".join(f"{flag} {value}" for flag, value in flags.items())


def _build_backup_script_lines(job: Dict, rclone_flags: str, use_progress: bool, log_file: str) -> list:
    """Build script lines for backup script."""
    lines = [
        "#!/bin/bash",
        "set -e",
        "echo 'Starting backup process...'",
        "",
        "# Ensure temp directory exists",
        f"if [ ! -d \"{TEMP_DIR}\" ]; then",
        f"    echo 'Creating temporary directory: {TEMP_DIR}'",
        f"    mkdir -p {TEMP_DIR}",
        "fi",
        f"chmod 777 {TEMP_DIR}",
        ""
    ]

    if job["compress"]:
        lines.extend(_build_compression_lines(job, use_progress))
    else:
        lines.extend(_build_copy_lines(job, rclone_flags))

    lines.append("echo 'Backup completed.'")
    
    if log_file:
        lines.extend(_build_log_cleanup_lines(log_file))
    
    lines.extend(_build_temp_cleanup_lines())
    
    return lines


def _build_compression_lines(job: Dict, use_progress: bool) -> list:
    """Build script lines for compression."""
    compression_level = job.get("compression_level", 6)
    cores = job.get("cores", 4)
    
    lines = [
        f"echo 'Compressing files with pigz -{compression_level}, using {cores} cores...'"
    ]
    
    if use_progress:
        lines.append(
            f"tar -cf - -C {job['source_dir']} . | "
            f"pv -cN 'Compressing' | "
            f"pigz -{compression_level} -p {cores} > {TEMP_DIR}/backup.tar.gz"
        )
    else:
        lines.append(
            f"tar -cf - -C {job['source_dir']} . | "
            f"pigz -{compression_level} -p {cores} > {TEMP_DIR}/backup.tar.gz"
        )
    
    if job.get('split_files'):
        split_size = job.get("split_size", "100M")
        lines.append("echo 'Splitting compressed file...'")
        
        if use_progress:
            lines.append(
                f"pv -cN 'Splitting' {TEMP_DIR}/backup.tar.gz | "
                f"split -b {split_size} - {TEMP_DIR}/backup-part-"
            )
        else:
            lines.append(f"split -b {split_size} {TEMP_DIR}/backup.tar.gz {TEMP_DIR}/backup-part-")
        
        lines.append(f"rm {TEMP_DIR}/backup.tar.gz")
    
    rclone_flags = _build_rclone_flags(job.get("rclone_flags", {}))
    lines.append(f"rclone copy {TEMP_DIR}/ {job['destination']} {rclone_flags}")
    
    return lines


def _build_copy_lines(job: Dict, rclone_flags: str) -> list:
    """Build script lines for direct copy."""
    return [
        "echo 'Copying files without compression or splitting...'",
        f"rclone copy {job['source_dir']} {job['destination']} {rclone_flags}"
    ]


def _build_log_cleanup_lines(log_file: str) -> list:
    """Build script lines for log cleanup."""
    return [
        f"if ! grep -qE 'ERROR|FATAL' {log_file}; then",
        f"    echo 'No errors found in log. Deleting {log_file}...'",
        f"    rm -f {log_file}",
        "else",
        "    echo 'Errors detected in log. Keeping it for review.'",
        "fi"
    ]


def _build_temp_cleanup_lines() -> list:
    """Build script lines for temp cleanup."""
    return [
        "echo 'Cleaning up temporary files...'",
        f"rm -rf {TEMP_DIR}/*"
    ]


def generate_transfer_script(config: Dict, job_id: str) -> Path:
    """
    Generate a transfer script for specified job.
    
    Args:
        config: Configuration dictionary
        job_id: Job ID
    
    Returns:
        Path to generated script
    """
    job = config[job_id]
    script_path = SCRIPT_DIR / f"transfer_{job_id}.sh"
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    rclone_flags = _build_rclone_flags(job.get("rclone_flags", {}))
    log_file = job.get("rclone_flags", {}).get("--log-file")

    script_lines = [
        "#!/bin/bash",
        "set -e",
        f"echo 'Starting transfer process for job {job_id}...'",
        "",
        f"rclone copy {job['source']} {job['destination']} {rclone_flags}",
        "",
        "echo 'Transfer completed.'"
    ]

    if log_file:
        script_lines.extend(_build_log_cleanup_lines(log_file))
    
    script_lines.extend(_build_temp_cleanup_lines())

    script_path.write_text("\n".join(script_lines))
    script_path.chmod(0o755)
    
    return script_path


def generate_restore_script(config: Dict, job_id: str) -> Path:
    """
    Generate a restore script for specified job.
    
    Args:
        config: Configuration dictionary
        job_id: Job ID
    
    Returns:
        Path to generated script
    """
    job = config[job_id]
    target_dir = job["source_dir"]
    script_path = SCRIPT_DIR / f"restore_{job_id}.sh"
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    rclone_flags = _build_rclone_flags(job.get("rclone_flags", {}))
    use_progress = "--progress" in rclone_flags

    script_lines = _build_restore_script_lines(job, target_dir, rclone_flags, use_progress)
    
    script_path.write_text("\n".join(script_lines))
    script_path.chmod(0o755)
    
    return script_path


def _build_restore_script_lines(job: Dict, target_dir: str, rclone_flags: str, use_progress: bool) -> list:
    """Build script lines for restore script."""
    lines = [
        "#!/bin/bash",
        "set -e",
        "echo 'Starting restore process...'",
        "",
        "echo 'Downloading files from remote...'",
        f"rclone copy {job['destination']} {TEMP_DIR} {rclone_flags}",
        ""
    ]

    if job.get("split_files"):
        lines.extend(_build_reassemble_lines(use_progress))
    
    if job.get("compress"):
        lines.extend(_build_extract_lines(target_dir, use_progress))
    else:
        lines.extend([
            "echo 'Restoring files without compression...'",
            f"rclone copy {TEMP_DIR} {target_dir} {rclone_flags}"
        ])
    
    lines.extend([
        "",
        "echo 'Cleaning up temporary files...'",
        f"rm -rf {TEMP_DIR}/*",
        "echo 'Restore completed.'"
    ])
    
    return lines


def _build_reassemble_lines(use_progress: bool) -> list:
    """Build script lines for reassembling split files."""
    lines = [
        "echo 'Checking for split files...'",
        f"if ls {TEMP_DIR}/backup-part-* 1> /dev/null 2>&1; then",
        "    echo 'Split files found. Reassembling...'"
    ]
    
    if use_progress:
        lines.append(
            f"    cat {TEMP_DIR}/backup-part-* | "
            f"pv -cN Reassembling > {TEMP_DIR}/backup.tar.gz"
        )
    else:
        lines.append(f"    cat {TEMP_DIR}/backup-part-* > {TEMP_DIR}/backup.tar.gz")
    
    lines.extend([
        f"    rm {TEMP_DIR}/backup-part-* || true",
        "else",
        "    echo 'Error: No split files found!'",
        "    exit 1",
        "fi",
        ""
    ])
    
    return lines


def _build_extract_lines(target_dir: str, use_progress: bool) -> list:
    """Build script lines for extracting compressed files."""
    lines = [
        "echo 'Extracting compressed files...'",
        f"mkdir -p {target_dir}"
    ]
    
    if use_progress:
        lines.append(
            f"pv -cN Extracting {TEMP_DIR}/backup.tar.gz | tar -xz -C {target_dir}"
        )
    else:
        lines.append(f"tar -xzf {TEMP_DIR}/backup.tar.gz -C {target_dir}")
    
    lines.append(f"rm {TEMP_DIR}/backup.tar.gz")
    
    return lines
