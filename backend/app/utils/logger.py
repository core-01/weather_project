import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def configure_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("weather_app")
    if logger.handlers:
        return  # already configured

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    try:
        fh = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3)
        fh.setLevel(logging.INFO)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except Exception:
        logger.warning("Could not initialize file rotating handler. Continuing with console logging only.")

# expose module-level logger object after configuration
configure_logging()
logger = logging.getLogger("weather_app")
