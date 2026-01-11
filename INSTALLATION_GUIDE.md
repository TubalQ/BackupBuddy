# BackupBuddy - Installation Guide

## 📦 What's Inside

This archive contains a fully modular Python-based backup tool with:

- **24 Python files** organized in 6 modules
- **Automated installation script**
- **Complete documentation**
- **MIT License**

## 🏗️ Project Structure

```
BackupBuddy/
├── backupbuddy.py          # Main entry point
├── install.sh              # Installation script
├── README.md               # Documentation
├── LICENSE                 # MIT License
├── STATUS.md               # Project status
├── config/                 # Configuration management
│   ├── __init__.py
│   ├── constants.py
│   └── manager.py
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── dependencies.py
│   ├── navigation.py
│   └── remotes.py
├── jobs/                   # Job types
│   ├── __init__.py
│   ├── backup.py
│   ├── transfer.py
│   └── restore.py
├── scripts/                # Script generation
│   ├── __init__.py
│   └── generator.py
├── cron/                   # Cron scheduling
│   ├── __init__.py
│   └── scheduler.py
└── utils/                  # Utilities
    ├── __init__.py
    ├── commands.py
    ├── display.py
    └── validation.py
```

## 🚀 Quick Start

### 1. Extract the Archive

```bash
unzip BackupBuddy.zip
cd BackupBuddy
```

### 2. Install

**Option A: System-wide Installation (Recommended)**
```bash
chmod +x install.sh
sudo ./install.sh
```

This installs BackupBuddy to `/opt/backupbuddy` and creates a symlink at `/usr/local/bin/backupbuddy`.

**Option B: Run Directly**
```bash
chmod +x backupbuddy.py
python3 backupbuddy.py
```

### 3. Run BackupBuddy

After system-wide installation:
```bash
backupbuddy
```

Or run directly:
```bash
python3 /path/to/BackupBuddy/backupbuddy.py
```

## 📋 Features

1. **Backup Jobs**: Create automated backups with compression and splitting
2. **Transfer Jobs**: Transfer files between local and remote locations
3. **Restore Jobs**: Restore backups to original or new locations
4. **Cron Scheduling**: Automate backups with cron jobs
5. **Remote Management**: Easy rclone remote configuration
6. **Progress Tracking**: Real-time progress indicators
7. **Error Handling**: Robust error handling and logging

## 🔧 Requirements

BackupBuddy will automatically install these dependencies:

- Python 3.6+
- rclone
- pigz
- tar
- pv
- cron

## 💡 Usage Examples

### Create a Backup Job
1. Run `backupbuddy`
2. Select option `1` - Create a new backup job
3. Follow the prompts to configure your backup

### Restore from Backup
1. Run `backupbuddy`
2. Select option `3` - Restore from an existing backup job
3. Choose the job to restore

### Schedule Automated Backups
1. Create a backup job (option 1)
2. When prompted, choose to schedule a cron job
3. Set your desired schedule

## 🆘 Getting Help

- Run `backupbuddy` and select option `9` for help
- Check README.md for detailed documentation
- Visit: https://github.com/TubalQ/BackupBuddy

## 📝 Notes

- All text and comments are in English
- The code is fully modular and easy to extend
- Default rclone flags are optimized for Proton and Google providers
- Sensitive data is never logged

## 🔐 Security

- No passwords or API keys are stored in plain text
- All backup scripts are generated with proper permissions (755)
- Temporary files are automatically cleaned up

## 📧 Support

For issues or questions:
- GitHub: https://github.com/TubalQ/BackupBuddy
- Website: https://t-vault.se

## 📄 License

MIT License - See LICENSE file for details

---

**Created by T-Q** | https://t-vault.se
