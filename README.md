# BackupBuddy

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
                                                        
     [ SYSTEM INITIALIZED ] [ v2.0.0 ] [ READY ]

A powerful Python-based backup and transfer tool with rclone integration, with a Matrix-inspired cyberpunk UI.

## Features

- **Matrix-Inspired UI**: Cyberpunk aesthetic with neon green color scheme
- **Backup Jobs**: Create automated backups with compression and splitting support
- **Transfer Jobs**: Transfer files between local and remote locations
- **Restore Jobs**: Restore backups to original or new locations  
- **Cron Scheduling**: Automate backups with cron jobs
- **Remote Management**: Easy rclone remote configuration and management
- **Progress Tracking**: Real-time progress indicators with Matrix-style animations
- **Error Handling**: Robust error handling with styled message boxes
- **Dashboard View**: System status at a glance

## Installation

```bash
cd /root/BackupBuddy
chmod +x install.sh
./install.sh
```

## Usage

```bash
# Using the symlink (after install.sh)
backupbuddy

# Or directly
python3 /root/BackupBuddy/backupbuddy.py
```

## Design Philosophy

BackupBuddy features a "Neo Matrix" design theme:
- **Primary**: Neon green (#00FF41) on deep black (#0D0208)
- **Accents**: Cyber blue, warning amber, alert red
- **Style**: Heavy use of Unicode box characters and ASCII art
- **Animations**: Subtle Matrix rain effects and progress indicators

## Project Structure

```
BackupBuddy/
├── config/         # Configuration management
├── core/           # Core functionality (dependencies, remotes, navigation)
├── jobs/           # Job types (backup, transfer, restore)
├── scripts/        # Script generation
├── cron/           # Cron job scheduling
├── utils/          # Utilities (display, commands, validation, matrix_ui)
└── backupbuddy.py  # Main entry point
```

## Requirements

- Python 3.6+
- rclone (installed automatically via official script)
- pigz
- tar
- pv
- cron

## Documentation

Run `backupbuddy` and select option **9** for help and documentation.

## UI Preview

The Matrix-inspired interface features:
- Animated ASCII logo on startup
- Color-coded status messages (success/warning/error)
- Progress bars with Unicode block characters
- Organized menu sections with box drawing
- File navigation with visual hierarchy
- Real-time spinner animations

## Security

- Secure credential handling
- Encrypted backup support (will be implemented)
- Safe configuration storage
- sudo privilege management

## License

MIT License - See LICENSE file for details

## Author

T-Q - https://itdetective.eu

## Acknowledgments

- rclone project for excellent cloud storage sync
