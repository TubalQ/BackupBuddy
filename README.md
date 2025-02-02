# BackupBuddy

BackupBuddy is a flexible and interactive tool designed to simplify your backup needs, both locally and remotely via rclone. It’s built to make backup and restoration processes intuitive and user-friendly.
Features
Interactive Directory Navigation

   Local Directories: Navigate, select, or create directories directly from the menu.
   
   Remote Directories (via rclone): Browse, select, or create directories on remote locations without manual commands.

   Set cron jobs easily and chose between "copy" or "sync"

   Set local shortcuts

   Remote to Remote
   Local to Remote
   Remote to Local


### Improved Directory Management

   Automatic Directory Creation: Create new directories locally or remotely directly from the menu.
   Immediate Usage: Newly created directories are instantly ready for uploads or backups.
   Fail-Safe Handling: Prevents errors when directories are empty or paths are invalid.

### Remote Server Management

   Manage Remotes: Add, view, and manage your rclone remotes directly from BackupBuddy.
   Multi-Remote Support: Seamlessly works with multiple cloud providers via rclone.

### Customizable Backups

   Compression and Splitting:
      Compress files with adjustable compression levels.
      Split large files into smaller chunks for easier handling.
   CPU Optimization: Configure the number of CPU cores used for compression tasks.

### Restoration and Scheduling#

   Restoration Mode: Restore backups as easily as creating them.
   Cron Integration: Schedule automatic backups directly from BackupBuddy.

### Installation
Requirements
BackupBuddy should install these for you.

 Python 3.7 or later.
 Install using:

    git clone https://github.com/TubalQ/BackupBuddy.git
    cd ~/BackupBuddy
    chmod +x BackupBuddy
    
In unprivileged LXC's you may need to manually install rclone
     
     apt install rclone

### Usage

   Run BackupBuddy(BackupBuddy needs sudo or root):

    sudo ./backupbuddy

   Follow the interactive menu options to:
        Create a new backup.
        Restore an existing backup.
        Manage remotes and local shortcuts.

## Miscs
Some cloud providers (like Google Drive and Proton Drive) are very sensetive about API requests.
Consider using these flags in your cron job to lower them, and help yourself and others by not making them angry.
BackupBuddy will give suggestions during the configuration.


#### You need to answer "yes" or "no", and not "y" or "n" on the questions!!!


