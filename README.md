# BackupBuddy

A powerful Python-based backup and transfer tool with support for rclone, compression, encryption, and automated scheduling.

## Features

- **Backup Jobs**: Create automated backups with compression and splitting support
- **Transfer Jobs**: Transfer files between local and remote locations
- **Restore Jobs**: Restore backups to original or new locations  
- **Cron Scheduling**: Automate backups with cron jobs
- **Remote Management**: Easy rclone remote configuration and management
- **Progress Tracking**: Real-time progress indicators
- **Error Handling**: Robust error handling and logging

## Installation

```bash
cd /root/BackupBuddy
chmod +x install.sh
./install.sh
```

## Usage

```bash
python3 backupbuddy.py
```

## Project Structure

```
BackupBuddy/
├── config/         # Configuration management
├── core/           # Core functionality (dependencies, remotes, navigation)
├── jobs/           # Job types (backup, transfer, restore)
├── scripts/        # Script generation
├── cron/           # Cron job scheduling
├── utils/          # Utilities (display, commands, validation)
└── backupbuddy.py  # Main entry point
```

## Requirements

- Python 3.6+
- rclone
- pigz
- tar
- pv
- cron

## License

MIT License

## Author

T-Q - https://itdetective.eu
