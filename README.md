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

### Visual Enhancements

   Color Coding:
      Directories and files are highlighted with distinct colors for improved readability.
      The current directory is clearly displayed at the bottom of the menu.
   File Limitation: Displays up to three files per directory and indicates with [...] if more files are present.

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

### Usage

   Run BackupBuddy(BackupBuddy needs sudo or root):

    sudo ./backupbuddy

   Follow the interactive menu options to:
        Create a new backup.
        Restore an existing backup.
        Manage remotes and local shortcuts.

## Miscs
Some cloud providers (like Google Drive and Proton Drive are very sensetive about API requests.
Consider using these flags in your cron job to lower them, these settings have worked very well for me.
    
    
    
    rclone sync source:path your-source:your-destination:path --tpslimit 2 --tpslimit-burst 1 --transfers 2 --checkers 1 --low-level-retries 3 --retries 5 --log-file=rclone.log --log-level INFO 
   
   or
   
    rclone sync source:path your-source:your-destination:path \
    --tpslimit 2 \         # Limit to 1 API request per second
    --tpslimit-burst 1 \   # Disallow bursts; keep it steady at 1 request
    --transfers 2 \        # Perform only one file transfer at a time
    --checkers 1 \         # Limit concurrent check processes to 1
    --low-level-retries 3 \ # Retry low-level errors a maximum of 3 times
    --retries 5 \          # Limit total retries to 5
    --log-file=rclone.log \ # Log all operations to a file
    --log-level INFO       # Use medium verbosity level for monitoring

#### You need to answer "yes" or "no", and not "y" or "n".

### Local Directories

#### Current local directory: /home/user

Directories:
1. Documents
2. Downloads
3. Pictures

0. Select this location
b. Go back
c. Enter a custom local directory path
d. Create a new directory

#### Remote Directories

Current remote directory: ProtonDrive:/backups

#### Remote Directories:
1. directory1
2. directory2

0. Select this location
b. Go back
c. Enter a custom remote directory path
d. Create a new directory



#### Contributing

   Fork this repository.
   Create a branch for your changes:

    git checkout -b feature/my-feature

#### Make your changes and commit:

    git commit -m "Description of your changes"

    Submit a pull request for review.

## License

BackupBuddy is licensed under the MIT License. See LICENSE for more details.

Feel free to copy and paste this updated README into your project. If you need assistance with pushing it to GitHub or have any other questions, don't hesitate to ask! 😊
