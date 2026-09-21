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

# Try to use the new logging system, fall back to standard logging
try:
    from logger_config import update_logger, log_update
    logger = update_logger
    use_structured_logging = True
except ImportError:
    logger = logging.getLogger(__name__)
    use_structured_logging = False
    def log_update(msg):
        logger.info(msg)

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
        log_update("Checking for updates...")
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

            log_update(f"Updates available: {commits_behind} new commit(s)")
            return {
                'available': True,
                'commits_behind': commits_behind,
                'current_commit': self.get_current_commit(),
                'branch': branch,
                'new_commits': commits_output.strip() if success else '',
                'message': f'{commits_behind} new commit(s) available'
            }
        else:
            log_update("Already up to date")
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
        log_update(f"Pulling latest changes from branch: {branch}")
        logger.info("Pulling latest changes from remote...")
        success, output, error = self._run_git_command(['git', 'pull', 'origin', branch])

        if not success:
            log_update(f"Git pull failed: {error}")
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
            log_update(message)
        else:
            message = f"Updated from {old_commit[:7]} to {new_commit[:7]}"
            log_update(f"Git pull successful: {message}")

            # Make scripts executable after update
            self._make_scripts_executable()

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

        result = {
            'success': True,
            'message': message,
            'old_commit': old_commit,
            'new_commit': new_commit,
            'output': output
        }

        # Check if restart is requested and something was updated
        if old_commit != new_commit:
            from database import get_setting
            restart_after_update = get_setting('restart_after_update', 'false').lower() == 'true'

            if restart_after_update:
                restart_result = self.restart_service()
                result['restart'] = restart_result
                if restart_result['success']:
                    result['message'] += ' - Service restarted'
                else:
                    result['message'] += ' - Manual restart required'

        return result

    def _make_scripts_executable(self):
        """Make shell scripts executable after update."""
        try:
            import stat
            script_files = ['setup.sh', 'service.sh']
            for script in script_files:
                script_path = os.path.join(self.repo_path, script)
                if os.path.exists(script_path):
                    os.chmod(script_path, os.stat(script_path).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
                    logger.info(f"Made {script} executable")
        except Exception as e:
            logger.warning(f"Failed to make scripts executable: {e}")

    def _detect_service_mode(self):
        """
        Detect if application is running as a systemd service.

        Returns:
            Tuple of (is_service, service_type) where service_type is 'user' or 'system' or None
        """
        try:
            # Check if running under systemd
            if not os.path.exists('/run/systemd/system'):
                return False, None

            # Try to detect service type
            # Check for user service
            result = subprocess.run(
                ['systemctl', '--user', 'is-active', 'cybersec-news'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, 'user'

            # Check for system service
            result = subprocess.run(
                ['systemctl', 'is-active', 'cybersec-news'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, 'system'

            return False, None
        except Exception as e:
            logger.warning(f"Failed to detect service mode: {e}")
            return False, None

    def restart_service(self):
        """
        Restart the application service if running as systemd service.

        Returns:
            dict with success status and message
        """
        is_service, service_type = self._detect_service_mode()

        if not is_service:
            log_update("Not running as systemd service - manual restart required")
            return {
                'success': False,
                'error': 'Not running as a systemd service',
                'message': 'Service restart not applicable - please restart manually'
            }

        try:
            log_update(f"Restarting {service_type} service...")
            logger.info(f"Restarting {service_type} service...")

            if service_type == 'user':
                cmd = ['systemctl', '--user', 'restart', 'cybersec-news']
            else:
                cmd = ['sudo', 'systemctl', 'restart', 'cybersec-news']

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                log_update(f"Service restarted successfully ({service_type} mode)")
                logger.info(f"Service restarted successfully ({service_type} mode)")
                return {
                    'success': True,
                    'message': f'Service restarted successfully ({service_type} mode)',
                    'service_type': service_type
                }
            else:
                log_update(f"Service restart failed: {result.stderr}")
                logger.error(f"Service restart failed: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'message': f'Service restart failed: {result.stderr}'
                }
        except Exception as e:
            log_update(f"Exception during service restart: {str(e)}")
            logger.error(f"Exception during service restart: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Service restart failed: {str(e)}'
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
