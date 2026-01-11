# Changelog

All notable changes to BackupBuddy will be documented in this file.

## [1.0.0] - 2026-01-11

### UI Overhaul - "Neo Matrix" Theme

#### Added
- **Matrix-inspired UI system** 
  - Neon green color scheme 
  - Unicode box drawing characters for all UI elements
  - Animated ASCII logo on startup
  - Typer effect for important messages
  - Styled message boxes (success/warning/error)
  - Progress bars with Unicode block characters
  - Real-time spinner animations

- **Enhanced Main Menu**
  - Organized sections: Job Management, System Configuration, Utilities
  - Status bar showing active jobs count
  - Color-coded menu items with icons
  - Improved visual hierarchy

- **Improved Job Display**
  - Separate sections for Backup and Transfer jobs
  - Visual indicators for compression and split settings
  - Better formatting with box characters
  - Size indicators with progress bars

- **Better Error Messages**
  - Styled error boxes with color coding
  - Error codes and timestamps
  - Suggested actions and quick fixes
  - Contextual help

- **File Navigation Enhancement**
  - Breadcrumb navigation
  - Visual file/directory distinction
  - Size bars for directories
  - Improved keyboard shortcuts display

### Changed
- **Rclone Installation**
  - Now always uses official install script: `sudo -v ; curl https://rclone.org/install.sh | sudo bash`
  - Falls back to apt only if curl method fails
  - Better error handling and status messages

- **Display System**
  - All displays now use Matrix UI components
  - Consistent color scheme throughout
  - Better spacing and alignment
  - Improved readability

- **User Experience**
  - Smoother transitions between screens
  - Better feedback for user actions
  - Clear visual separation of sections
  - More intuitive navigation

### Technical Improvements
- Modular UI system (MatrixUI and MatrixColors classes)
- Centralized color management
- Reusable UI components
- Better code organization
- Improved type hints

## [1.0.0] - 2026-01-11

### Added
- Initial modular rewrite from monolithic script
- Complete backup functionality
- Transfer job support  
- Restore capabilities
- Cron job scheduling
- rclone remote management
- Local and remote directory navigation
- Dependency management
- Configuration system
- Installation script
- Comprehensive documentation

### Project Structure
- Created 6 main packages: config, core, jobs, scripts, cron, utils
- 20 Python modules
- English codebase
- MIT License
- Git repository initialization

---

## Version Naming

- **2.0.0**: Matrix UI era
- **0.1.0**: Initial modular version
- **0.0.1**: Legacy monolithic script (deprecated)
