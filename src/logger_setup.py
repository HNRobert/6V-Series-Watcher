import logging
import logging.handlers
import os


def setup_logging():
    """Configure and set up the logging system for 6V-Series-Watcher"""
    logger = logging.getLogger('6v_watcher')
    logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler - primary logging method
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler for persistent logs
    try:
        log_file = os.environ.get('LOG_FILE', '/var/log/6v_watcher/app.log')
        log_dir = os.path.dirname(log_file)

        # Ensure log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=10485760,  # 10MB
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # Just log to console if file logging fails
        print(
            f"Warning: Could not set up file logging: {e}. Using console logging only.")

    return logger


# Initialize the global logger once
logger = setup_logging()
