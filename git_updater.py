"""
Git Updater Module for Cybersecurity News Dashboard
Handles automatic updates from GitHub repository with safety checks.
"""

import os
import logging
import subprocess
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Get the base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class GitUpdater:
    """Handle Git repository updates with safety checks."""

    def __init__(self):
        self.repo_path = BASE_DIR
        self.update_log_file = os.path.join(BASE_DIR, 'update_history.json')
        self.backup_db_on_update = True

    def _run_git_command(self, command, capture_output=True):
        """
        Run a git command and return the result.

        Args:
            command: List of command arguments
            capture_output: Whether to capture output

        Returns:
            Tuple of (success, output, error)
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error("Git command timed out")
            return False, "", "Command timed out"
        except Exception as e:
            logger.error(f"Error running git command: {e}")
            return False, "", str(e)

    def check_git_available(self):
        """Check if git is installed and repository is valid."""
        success, output, error = self._run_git_command(['git', '--version'])
        if not success:
            logger.error("Git is not available")
            return False

        # Check if current directory is a git repository
        success, output, error = self._run_git_command(['git', 'rev-parse', '--git-dir'])
        if not success:
            logger.error("Not a git repository")
            return False

        return True

    def get_current_branch(self):
        """Get the current git branch name."""
        success, output, error = self._run_git_command(['git', 'branch', '--show-current'])
        if success:
            return output.strip()
        return None

    def get_current_commit(self):
        """Get the current commit hash."""
        success, output, error = self._run_git_command(['git', 'rev-parse', 'HEAD'])
        if success:
            return output.strip()
        return None

    def get_remote_url(self):
        """Get the remote repository URL."""
        success, output, error = self._run_git_command(['git', 'remote', 'get-url', 'origin'])
        if success:
            return output.strip()
        return None

    def check_for_updates(self):
        """
        Check if updates are available from remote repository.

        Returns:
            dict with status, commits_behind, and message
        """
        if not self.check_git_available():
            return {
                'available': False,
                'error': 'Git is not available or not a git repository',
                'commits_behind': 0
            }

        # Fetch latest from remote
        logger.info("Fetching latest changes from remote...")
        success, output, error = self._run_git_command(['git', 'fetch', 'origin'])
        if not success:
            logger.error(f"Failed to fetch from remote: {error}")
            return {
                'available': False,
                'error': f'Failed to fetch from remote: {error}',
                'commits_behind': 0
            }

        # Check how many commits behind we are
        branch = self.get_current_branch()
        if not branch:
            return {
                'available': False,
                'error': 'Could not determine current branch',
                'commits_behind': 0
            }

        success, output, error = self._run_git_command([
            'git', 'rev-list', '--count', f'HEAD..origin/{branch}'
        ])

        if not success:
            return {
                'available': False,
                'error': f'Could not check for updates: {error}',
                'commits_behind': 0
            }

        commits_behind = int(output.strip())

        if commits_behind > 0:
            # Get commit messages
            success, commits_output, error = self._run_git_command([
                'git', 'log', '--oneline', f'HEAD..origin/{branch}'
            ])

            return {
                'available': True,
                'commits_behind': commits_behind,
                'current_commit': self.get_current_commit(),
                'branch': branch,
                'new_commits': commits_output.strip() if success else '',
                'message': f'{commits_behind} new commit(s) available'
            }
        else:
            return {
                'available': False,
                'commits_behind': 0,
                'current_commit': self.get_current_commit(),
                'branch': branch,
                'message': 'Already up to date'
            }

    def has_local_changes(self):
        """Check if there are uncommitted local changes."""
        success, output, error = self._run_git_command(['git', 'status', '--porcelain'])
        if success:
            # Output will be empty if no changes
            return bool(output.strip())
        return False

    def backup_database(self):
        """Create a backup of the database before updating."""
        try:
            from config import DATABASE_PATH
            if os.path.exists(DATABASE_PATH):
                backup_path = f"{DATABASE_PATH}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                import shutil
                shutil.copy2(DATABASE_PATH, backup_path)
                logger.info(f"Database backed up to: {backup_path}")
                return True, backup_path
        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            return False, str(e)
        return True, None

    def perform_update(self):
        """
        Perform git pull to update the application.

        Returns:
            dict with success status and message
        """
        if not self.check_git_available():
            return {
                'success': False,
                'error': 'Git is not available',
                'message': 'Git is not installed or repository is invalid'
            }

        # Check for local changes
        if self.has_local_changes():
            logger.warning("Local changes detected, stashing them")
            success, output, error = self._run_git_command(['git', 'stash'])
            if not success:
                return {
                    'success': False,
                    'error': 'Failed to stash local changes',
                    'message': f'Cannot update with local changes: {error}'
                }

        # Backup database if enabled
        if self.backup_db_on_update:
            db_backed_up, backup_info = self.backup_database()
            if not db_backed_up:
                logger.warning(f"Database backup failed: {backup_info}")

        # Get current commit before update
        old_commit = self.get_current_commit()
        branch = self.get_current_branch()

        # Perform git pull
        logger.info("Pulling latest changes from remote...")
        success, output, error = self._run_git_command(['git', 'pull', 'origin', branch])

        if not success:
            logger.error(f"Git pull failed: {error}")
            return {
                'success': False,
                'error': error,
                'message': f'Update failed: {error}'
            }

        # Get new commit after update
        new_commit = self.get_current_commit()

        # Check if anything was updated
        if old_commit == new_commit:
            message = "Already up to date"
        else:
            message = f"Updated from {old_commit[:7]} to {new_commit[:7]}"

        # Log the update
        self._log_update({
            'timestamp': datetime.utcnow().isoformat(),
            'old_commit': old_commit,
            'new_commit': new_commit,
            'branch': branch,
            'success': True,
            'message': message
        })

        logger.info(message)
        return {
            'success': True,
            'message': message,
            'old_commit': old_commit,
            'new_commit': new_commit,
            'output': output
        }

    def _log_update(self, update_info):
        """Log update information to file."""
        try:
            history = []
            if os.path.exists(self.update_log_file):
                with open(self.update_log_file, 'r') as f:
                    history = json.load(f)

            history.append(update_info)

            # Keep only last 50 updates
            history = history[-50:]

            with open(self.update_log_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to log update: {e}")

    def get_update_history(self, limit=10):
        """Get update history from log file."""
        try:
            if os.path.exists(self.update_log_file):
                with open(self.update_log_file, 'r') as f:
                    history = json.load(f)
                return history[-limit:]
        except Exception as e:
            logger.error(f"Failed to read update history: {e}")
        return []

    def get_git_info(self):
        """Get comprehensive git repository information."""
        return {
            'is_git_repo': self.check_git_available(),
            'current_branch': self.get_current_branch(),
            'current_commit': self.get_current_commit(),
            'remote_url': self.get_remote_url(),
            'has_local_changes': self.has_local_changes(),
        }


def check_and_update_if_needed():
    """
    Check for updates and perform update if auto-update is enabled.
    This function is called by the scheduler.
    """
    from database import get_setting

    # Check if auto-update is enabled
    auto_update_enabled = get_setting('auto_update_enabled', 'false').lower() == 'true'

    if not auto_update_enabled:
        logger.info("Auto-update is disabled")
        return

    updater = GitUpdater()

    # Check for updates
    update_check = updater.check_for_updates()

    if update_check.get('available'):
        logger.info(f"Updates available: {update_check['message']}")

        # Perform update
        result = updater.perform_update()

        if result['success']:
            logger.info(f"Auto-update successful: {result['message']}")

            # Check if restart is required
            restart_after_update = get_setting('restart_after_update', 'false').lower() == 'true'
            if restart_after_update:
                logger.warning("Restart required after update - please restart the application manually")
        else:
            logger.error(f"Auto-update failed: {result.get('error')}")
    else:
        logger.info("No updates available")
