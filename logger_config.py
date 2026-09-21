"""
Logging Configuration for Cybersecurity News Dashboard
Provides structured logging with rotation and multiple log files.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Base directory for logs
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths
APP_LOG = os.path.join(LOG_DIR, 'app.log')
ERROR_LOG = os.path.join(LOG_DIR, 'error.log')
ACCESS_LOG = os.path.join(LOG_DIR, 'access.log')
UPDATE_LOG = os.path.join(LOG_DIR, 'update.log')
FEED_LOG = os.path.join(LOG_DIR, 'feed.log')

# Log format
DETAILED_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

SIMPLE_FORMAT = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def setup_logger(name, log_file, level=logging.INFO, format_type='detailed'):
    """
    Set up a logger with rotation.

    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level
        format_type: 'detailed' or 'simple'

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers = []

    # File handler with rotation (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )

    # Set format
    if format_type == 'simple':
        file_handler.setFormatter(SIMPLE_FORMAT)
    else:
        file_handler.setFormatter(DETAILED_FORMAT)

    logger.addHandler(file_handler)

    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(DETAILED_FORMAT)
    logger.addHandler(console_handler)

    return logger


# Set up default loggers
app_logger = setup_logger('app', APP_LOG, logging.INFO, 'detailed')
error_logger = setup_logger('error', ERROR_LOG, logging.ERROR, 'detailed')
access_logger = setup_logger('access', ACCESS_LOG, logging.INFO, 'simple')
update_logger = setup_logger('update', UPDATE_LOG, logging.INFO, 'simple')
feed_logger = setup_logger('feed', FEED_LOG, logging.INFO, 'simple')


def log_app(message, level='info'):
    """Log application message."""
    getattr(app_logger, level.lower())(message)


def log_error(message, exc_info=None):
    """Log error message."""
    error_logger.error(message, exc_info=exc_info)


def log_access(request_info):
    """Log HTTP access."""
    access_logger.info(request_info)


def log_update(message):
    """Log update activity."""
    update_logger.info(message)


def log_feed(source, message, level='info'):
    """Log feed fetch activity."""
    getattr(feed_logger, level.lower())(f"[{source}] {message}")


def get_log_files():
    """Get list of all log files with metadata."""
    log_files = []

    for log_name, log_path in [
        ('Application Log', APP_LOG),
        ('Error Log', ERROR_LOG),
        ('Access Log', ACCESS_LOG),
        ('Update Log', UPDATE_LOG),
        ('Feed Log', FEED_LOG),
    ]:
        if os.path.exists(log_path):
            stat = os.stat(log_path)
            log_files.append({
                'name': log_name,
                'path': log_path,
                'filename': os.path.basename(log_path),
                'size': stat.st_size,
                'size_human': _human_readable_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })

    return log_files


def _human_readable_size(size_bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_log_tail(log_file, lines=100):
    """Get last N lines from log file."""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            return ''.join(f.readlines()[-lines:])
    except Exception as e:
        return f"Error reading log: {str(e)}"


def clear_log(log_file):
    """Clear a log file."""
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"# Log cleared at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        return True
    except Exception:
        return False
