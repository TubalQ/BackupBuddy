# BackupBuddy

BackupBuddy is a Python-based backup and restore tool using rclone and pigz, designed for simplicity and flexibility. It supports compression, file splitting, and integration with popular cloud storage providers via rclone.

rclone for cloud storage
pigz for enabling more cores during compression for better performance

BackupBuddy is tested in Proxmox VE, Proxmox BS, Ubuntu and Parrot OS so far.

# Features

Backup and Restore: Easily back up and restore your files and directories.
Compression: Reduce backup size with customizable compression levels.
File Splitting: Split large backups into smaller parts for easier upload.
Cloud Integration: Seamlessly integrate with cloud storage providers like Google Drive, S3, ProtonDrive, and more via rclone.
User-Friendly: Interactive CLI interface with options to configure backups step-by-step.
Custom Scripts: Generates reusable backup and restore scripts.

# Installation
Prerequisites

Ensure the following are installed on your system:
(BackupBuddy should install it if you dont have theese)

Python 3.x
rclone for cloud storage integration

pigz for fast compression (optional)

You may need to manually install "sudo" on Proxmox

If you're installing on an unprivileged LXC and you're getting: Failed to retrieve remotes: Command 'rclone listremotes' returned non-zero exit status 127.
   Run: 
    
    apt install rclone

# Steps

Clone the repository:

    git clone https://github.com/TubalQ/BackupBuddy.git
    cd ~/BackupBuddy

Make the program executable:

    chmod +x BackupBuddy

Run the program:

    sudo ./BackupBuddy

# Usage
Main Menu

When you run the program, you'll see with the following options:

Create a New Backup Job: Configure and start a new backup job.

Restore from an Existing Backup Job: Restore files from a previously configured job.
Clear Configurations: Remove existing backup jobs or remotes.

Exit: Exit the program.

# Yes & No questions needs to be answered with "yes" or "no", not "y" or "n"

# Creating a Backup Job

Provide a unique ID for the job.
Enter the source directory to back up.
Select a remote destination from existing remotes or configure a new one.
Choose whether to compress files and set the compression level.
Decide if files should be split and specify the maximum part size.

# Restoring a Backup

Select the backup job you want to restore.
Files will be restored to the same directory from which they were backed up.

Clearing Configurations (this will only clear the info in the cli, it will not remove the generated files in /root/backup_scripts)

You can remove:

All remotes configured with rclone.
All existing backup jobs.

# Commands (BackupBuddy needs sudo))

    sudo ./BackupBuddy

# Example Backup

Backing up /home/user/documents to "your-name-for-your-cloud":/backups/documents.
Compressing files with level up to 9.
Splitting files into 5GB parts. (you can choose freely from 1MB to 99TB)

# Example Restore
BackupBuddy will restore files to the same location you backed them up from.

# Cronjonbs
Im working on integrating cron jobs from the menu.
If you want to add the generated scripts to a backjob, you should find the scripts in /root/backup_scripts/backup_examplename


# Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

# License

This project is licensed under the MIT License. See the LICENSE file for details.
